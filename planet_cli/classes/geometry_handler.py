"""
    This module will handle the Geometry Objects used un the CLI
"""
import geopandas as gpd
import shapely
from pyproj import Transformer
from shapely.ops import transform
from planet_cli.classes.error_manager import GeometryLimitError, GeometryTypeError
from sentinelhub import (
    BBox,
    bbox_to_dimensions,
    CRS
)

class GeometryHandler:
    """
    This class handles reading and converting geometry files in (SHP, KML, GeoJSON)
    It dissolves the geometries and return and general geometry
    """

    def __init__(self, file_path: str):
        self.geometry_file = file_path
        self._file_extension = self.__get_file_extension()
        self._max_limit_api = 2500 * 2500
        self._max_pixel_size = 1500
        self._resolution = 10

        self._extension_reader = {
            "shp": self._shp_reader,
            "kml": self._kml_reader,
            "geojson": self._geojson_reader
        }

    
    def __validate_geometry(self, geometry: shapely.geometry, is_projected: bool) -> bool:
        """
        Validates the provided geometry based on area constraints and API processing limits.

        Ensures that:
        - The geometry complies with the API's maximum resolution of 2500 x 2500 pixels.
        - The maximum spatial resolution of 1500 meters per pixel is not exceeded for site processing.
        """

        if not isinstance(geometry, (shapely.Polygon, shapely.MultiPolygon)):
            raise GeometryTypeError(f"Unexpected geometry type: {type(geometry)}. Expected Polygon or MultiPolygon.")

        bbox = geometry.bounds
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        area = width * height

        area = geometry.area
        if not is_projected:
            area = width * height * 111.139 * 1000 * self._resolution
            
        max_area_pixels = (self._max_limit_api ** 2) * (self._max_pixel_size ** 2)

        if area < max_area_pixels:
            return True
        else:
            raise GeometryLimitError("Provided is too large, please reduce the AOI, Max 625 Hectares (approx 1544 acres)")



    def __get_file_extension(self) -> str:
        """The method returns the file extension of the file"""
        return self.geometry_file.split(".")[-1].lower()
    
    def __read_geometry_file(self, driver: str) -> shapely.geometry:
        """ 
        This method handles all the readings in the different formats
        passing by a str and returning a wkt 
        """

        gdf = gpd.read_file(self.geometry_file, driver=driver)
        dissolved = gdf.union_all()

        is_projected = gdf.crs.is_projected
        
        self.__validate_geometry(dissolved, is_projected)

        if is_projected:
            transformer = Transformer.from_crs(gdf.crs.to_epsg(), 4326, always_xy=True)
            transformed_geometry = transform(transformer.transform, dissolved)
            return transformed_geometry
        return dissolved

    def _kml_reader(self) -> shapely.geometry:
        """Reads KML files and convert it into WKT"""
        return self.__read_geometry_file("KML")

    def _shp_reader(self) -> shapely.geometry:
        """Reads SHP files and convert it into WKT"""
        return self.__read_geometry_file("ESRI Shapefile")

    def _geojson_reader(self)-> shapely.geometry:
        """Reads Geojson files and convert it into WKT"""
        return self.__read_geometry_file("GeoJSON")

    def get_sh_bbox(self) -> BBox:
        """ 
        Method return the bbox format required for 
        SentinelHub Request based on the Geometry provided
        """
        geometry = self._extension_reader[self._file_extension]()
        return BBox(bbox=geometry.bounds, crs=CRS.WGS84)
    
    def get_sh_dimensions(self, resolution:int= 10) -> tuple:
        """
        Method return the dimensions required for 
        SentinelHub Request based on the Geometry provided
        """
        bbox = self.get_sh_bbox()
        return bbox_to_dimensions(bbox, resolution=resolution)

    def get_geometry(self) -> str:
        """Method returns the geometry in WKT format"""
        if self._file_extension in self._extension_reader:
            geometry = self._extension_reader[self._file_extension]()
            return geometry.wkt
        else:
            raise ValueError(f"Unsupported Format: {self._file_extension}. We support geojson, kml and shp.")
