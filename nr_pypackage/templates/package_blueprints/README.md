# About
Long description of your project.


#### Current Stable Version
```
0.1.0
```


# Development: First Time Setup

* We require Anaconda3, which can be downloaded from their website.
* Once Anaconda3 has been downloaded and installed, make sure that the `conda` command is available in the `$PATH`.
* Create an Anaconda3 environment for this project - run the following command:
```
make recreate_pyenv
```
* Activate the environment that has just been created - run the following command:
```
source activate-env.sh
```


# Installation

#### Install via pip
```
pip install {{ package_name }}
```


# Test
To run the tests:
```
make test
```


# Examples
To run an example:
```
$ python examples/simple.py
```

## License
MIT
