<div id="top"> 
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/39/Planet_logo_New.png" alt="Planet CLI" style="height:40px" />
</div>

<h1 align="center">Planet CLI - Cloudless Sentinel 2 Imagery</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/joaherrerama/planet-cli?color=56BEB8">
  <img alt="Github language count" src="https://img.shields.io/github/languages/count/joaherrerama/planet-cli?color=56BEB8">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/joaherrerama/planet-cli?color=56BEB8">
  <img alt="License" src="https://img.shields.io/github/license/joaherrerama/planet-cli?color=56BEB8">
</p>

<p align="center">
  <a href="#about">About</a> &#xa0; | &#xa0; 
  <a href="#features">Features</a> &#xa0; | &#xa0;
  <a href="#technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#installation">Installation</a> &#xa0; | &#xa0;
  <a href="#notes">Notes</a> &#xa0; | &#xa0;
  <a href="#further-improvements">Further Improvments</a> &#xa0; | &#xa0;
  <a href="https://github.com/joaherrerama" target="_blank">Author</a>
</p>

<br>

## About ##

**Planet CLI** is a command-line interface tool designed to interact with the SentinelHub Catalog and Processing APIs. It facilitates configuring user credentials, specifying output preferences, and conducting efficient searches for satellite imagery based on user-defined parameters. The tool is ideal for researchers, developers, and organizations working with geospatial data who require streamlined access to satellite imagery.

## Commands ##

The following section shows the commans and it respective help information: 

- **Configuration Management:**
  ```bash
  planet-cli config                                                                          
  This CLI tool leverages the SentinelHub Catalog and Processing APIs
  Usage: planet-cli config [OPTIONS] COMMAND [ARGS]...

  This section allows you to set your credentials, output-format and output-
  type

  Options:
    --help  Show this message and exit.

  Commands:
    credentials    This command receives client id and client secret...
    output-format  output-format (default: tiff) - Set output format...
    output-type    output-type (default: visual) - Set output type...
  ```
  - **Credentials Setup:**  Store client ID and secret for authenticated access to SentinelHub APIs.
  ```bash
   planet-cli config credentials [OPTIONS] CLIENT_ID CLIENT_SECRET
  ```
  For more info use --help
  - **Output Format Selection:** Specify the desired output format for retrieved images (e.g., TIFF, PNG).
  ```bash
  planet-cli config output-format [OPTIONS] {tiff|png}
  ```
  For more info use --help
  - **Output Type Selection:**  Choose the type of data to process, such as visual images or NDVI (Normalized Difference Vegetation Index).
  ```bash
  planet-cli config output-type [OPTIONS] {visual|ndvi}
  ```
  For more info use --help

- **Search and Download:**
```bash
Usage: planet-cli search [OPTIONS]

  search and download the most cloudless image with the params given.

Options:
  --aoi PATH                   Area of interest in GeoJSON format  [required]
  --start-date TEXT            Start time of the range (e.g., '2019-01-20
                               08:00').  [required]
  --end-date TEXT              End time of the range (e.g., '2020-11-20
                               18:00').  [required]
  --destination-folder TEXT    The destination folder where the elements
                               should be saved
  --client-id TEXT             Client-id from SentinelHub. if not it will use
                               the one defined in config (planet-config
                               config)
  --client-secret TEXT         Client-secret from SentinelHub. if not it will
                               use the one defined in config (planet-config
                               config)
  --output-type [visual|ndvi]  Format of the file Visual or NDVI, if not
                               defined it uses Visual or the one defined in
                               config
  --output-format [tiff|png]   Format of the file Tiff or PNG, if not defined
                               it uses Tiff or the one defined in config
  --help                       Show this message and exit.
```

## Technologies ##

The following tools and libraries were used in this project:

- [Python 3.13](https://www.python.org/)
- [Click](https://click.palletsprojects.com/)
- [Pytest](https://pytest.org/)
- [SentinelHub Python Library](https://sentinelhub-py.readthedocs.io/)
- [GeoPandas](https://geopandas.org/)

## Requirements ##

## Requirements ##

Before starting, ensure you have the following installed:

- [Python 3.12 or higher](https://www.python.org/downloads/)
- [Git](https://git-scm.com)
- A Python package manager:  
  - Recommended: [Poetry](https://python-poetry.org/docs/#installation)  
  - Alternative: [Pip](https://pip.pypa.io/en/stable/installation/)  

## Installation ##

Follow the steps below to clone and set up the project:

```bash
### Clone this project
$ git clone https://github.com/joaherrerama/planet-cli

### Access the project directory
$ cd planet-cli

### Create a virtual environment (optional but recommended)
$ python -m venv venv
$ source venv/bin/activate

### Install dependencies
$ pip install -r requirements.txt

### Run the tool
$ python planet_cli --help

### Run tests
$ pytest
```

You can also built it using:
```bash
$ pip install --editable .
```

In the repository you can find also the [wheel file (.whl)](dist/planet_cli-0.0.1-py3-none-any.whl) or  [Tar package (.tar.gz)](dist/planet_cli-0.0.1.tar.gz)


## Notes ##

- Todos los archivos de aoi independientemente de su CRS, son transformados a CRS 4326
- Resolution is 10 meters in all cases thorugh the code.
- There are various validation points for geometry, credentials, dates and typos

## Further Improvements ##
The following items are suggestions for further implementation on the existing code:

  - **Functionality**: 
      - The current code manage the geometry and utilize one source of data S2A. An further step would be to implement a module to handles the different sources, this implies resolution and source as well as the complexity of the bands and evalscripts.
      - Evalscripts could be long and tedious to handle, a class was implemented to handles the different options, but a externat source or catalog would be convenient and feed it trough the registry command.
      - Enhance the managment of geometries, as currently any admited file is transform to CRS 4326
      - Future developments would be discriminate ErrorHandling and use of abstract classes
      - The cuerrent code uses a config.json to store credentials and format and times. Improve how to handle sensitive info like credentials would be something to dig into.

  - **Testing**:
    - The current test code does not cover all the functionalities. As a further step. Modular testing, functional testing and integration testing are highly important. 
    - Create more failing scenarios adding fail tests and improving Error Handling
    - Improve mocking implementation for Credentials validation


Made with :heart: by <a href="https://github.com/joaherrerama" target="_blank">Jorge Herrera</a>

 
<a href="#top">Back to top</a>