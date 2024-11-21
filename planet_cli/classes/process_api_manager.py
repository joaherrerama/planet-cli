import datetime
import os
import requests

from planet_cli.classes.authorization_manager import AuthorizationManager
from planet_cli.classes.config_manager import ConfigManager
from sentinelhub import SHConfig
from sentinelhub import (
    geometry,
    DataCollection,
    MimeType,
    MosaickingOrder,
    SentinelHubRequest
)

from planet_cli.classes.evalscript_manager import EvalScriptManager
from planet_cli.classes.geometry_handler import GeometryHandler

class ProcessApiManager:

    def __init__(self): 
        self._collection = DataCollection.SENTINEL2_L2A


    def __get_sh_parameters(self, aoi: str):
        """
        Process the geometry utilizing the GeometryHandler
        returning the parameters wkt_geometry, sh_bbox, sh_dimensions
        required for SentinelHubRequest
        """
        geometry_instance = GeometryHandler(aoi)
        wkt_geometry = geometry_instance.get_geometry()
        sh_bbox = geometry_instance.get_sh_bbox()
        sh_dimensions = geometry_instance.get_sh_dimensions()
        return wkt_geometry, sh_bbox, sh_dimensions


    def process(
            self,
            aoi: str, 
            start_date: datetime.datetime,
            end_date: datetime.datetime,
            client_id: str = None,
            client_secret: str = None,
            output_type: str = None,
            output_format: str = None
        ) -> SentinelHubRequest:
        """
        The process method aims to collect all the parameters required
        to process a SentinelHubRequest

        params:
            - aoi: path to the area of interest
            - start_date: starting date in format datetime.datetime
            - end_date:  end date in format datetime.datetime
            - client_id: Client ID from SentinHub profile 
            - client_secret: Client Secret from SentinHub profile 
            - output_type: Type of product either visual or ndvi
            - output_format: Type of format either tiff or png
        """

        local_config = ConfigManager()

        if not client_id or not client_secret:
            client_id, client_secret = local_config.get_credentials()

        if not output_format:
            output_format = local_config.get_output_format()
        
        if not output_type:
            output_type = local_config.get_output_type()

        config = SHConfig(sh_client_id=client_id, sh_client_secret=client_secret)

        wkt_geometry, sh_bbox, sh_dimensions = self.__get_sh_parameters(aoi)

        evalscript_sh = EvalScriptManager().generate_script(output_type,output_format)
        output_format_sh = MimeType.TIFF if output_format == "tiff" else MimeType.PNG

        aoi_sh = geometry.Geometry(wkt_geometry, crs=4326)

        request = SentinelHubRequest(
            evalscript=evalscript_sh,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection= self._collection,
                    time_interval=(start_date, end_date),
                    mosaicking_order=MosaickingOrder.LEAST_CC,
                )
            ],
            responses=[SentinelHubRequest.output_response("default", output_format_sh)],
            geometry=aoi_sh,
            bbox=sh_bbox,
            size=sh_dimensions,
            config=config,
        )

        return request
    
    def download(self, request: SentinelHubRequest, destination_folder: str) -> None:
        """
        This method downloads the elements from the request done to 
        Sentinel Hob Process API
            - params:
                - request = a SentinelHubRequest instance
                - destination_folder: Path where the items want to be stored
        """

        destination_folder = os.path.abspath(destination_folder)
    
        os.makedirs(destination_folder, exist_ok=True)

        request.data_folder=destination_folder

        request.get_data(save_data=True)