# About
[![Build Status](https://travis-ci.org/{{ scm_username }}/{{ package_name }}.svg?branch=master)](https://travis-ci.org/{{ scm_username }}/{{ package_name }})

Long description of your project.


## Current Stable Version
```
0.1.0
```

## Installation
### pip
```
pip install {{ package_name }}
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


## Examples
```
$ python examples/simple.py
```

## License
MIT
