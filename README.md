# About
This project is about creating standardized python projects. We provide standard templates for multiple types of python projects. It is intended to be replicate most features from [ansrivas/protemplates](https://github.com/ansrivas/protemplates) and this project was created using that library.

The scope of this project is as follows:
  * It is only for Python projects and packages.
  * We provided options to create entire python packages including:
    * Source code templates
    * Test templates
    * Envrionment creation and management
  * We provide options to create modules and submodules based on popular libraries including:
    * Flask
    * Flask-blueprints
    * Flask-database integration


Current Features Include:
  * Easy pip installation with a cli
  * Creating a python package: Simple support
  * Creating a python package: Flask support
  * Creating a python package: Flask with Blueprints support

This repository is Python 3 compatible only.

## Current Stable Version
```
0.3.0
```

## Installation
### pip
```
pip install nr-pypackage==0.3.0 --user --upgrade
```

### Development Installation
* Clone the project.
* Install in Anaconda3 environment
* This command creates a python environment and then activates it.
```
$ make recreate_pyenv && chmod +x activate-env.sh && . activate-env.sh
```
* Now install the application in editable mode and you are ready to start development
```
$ pip install -e .
```

## Test
To run the tests:
```
make test
```

## Usage
After installing via Pip, run the following command and follow the instructions.
```
nr-pypackage-cli
```

## License
MIT
