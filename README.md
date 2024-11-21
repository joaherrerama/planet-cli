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

### Create config file
$ python post_installation/create_config.py

### Run the tool
$ python planet_cli --help

### Run tests
$ pytest
```
And easy way is using the install.sh, this wraps up the previous steps in one line:
```bash
$ bash installation.sh
```
You can also built it using:
```bash
$ pip install --editable .
```

In the repository you can find also the [wheel file (.whl)](dist/planet_cli-0.0.1-py3-none-any.whl) or  [Tar package (.tar.gz)](dist/planet_cli-0.0.1.tar.gz)


## Notes ##

- All AOI files, regardless of their original Coordinate Reference System (CRS), are converted to CRS 4326.
- A fixed resolution of 10 meters is used throughout the code.
- Various validation checks are in place for geometry, credentials, dates, and potential typos.

## Further Improvements ##
The following items are suggestions for further implementation on the existing code:

  - **Functionality**: 
      - Currently, the code processes geometry and utilizes S2A data. A next step would be to implement a module to handle various data sources, considering factors like resolution, source type, band complexity, and evaluation scripts.
      - Evaluation scripts can be lengthy and complex. While a class was implemented to handle different options, an external source or catalog could provide a more convenient solution, allowing scripts to be integrated via a registry command.
      - The current geometry management approach involves transforming all admitted files to CRS 4326. Future enhancements could include more flexible geometry handling, such as supporting multiple CRS or on-the-fly projections.
      - Future developments should focus on improving error handling and utilizing abstract classes to enhance code modularity and maintainability.
      The current code stores credentials, formats, and time information in a config.json file. It's essential to explore more secure methods for handling sensitive information like credentials.

  - **Testing**:
    - The current test code does not comprehensively cover all functionalities. To enhance test coverage, modular, functional, and integration testing should be implemented.
    - More failing test scenarios should be added to improve error handling and robustness.
    - The mocking implementation for credential validation should be refined to increase test reliability and efficiency.


Made with :heart: by <a href="https://github.com/joaherrerama" target="_blank">Jorge Herrera</a>

 
<a href="#top">Back to top</a>