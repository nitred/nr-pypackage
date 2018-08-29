# Changelog
All notable changes to this project will be documented in this file.

## 0.2.0 - 2018-08-29
### Added
- package-flask-blueprints template type
- added auth (for ldap authentication) blueprint
- added redis in docker-compose for auth blueprint (for flask-session)
- added nav-bar in navigation-template that supports logout and back buttons


## 0.1.2 - 2018-08-01
### Added
- Ignoring `__pycache__` dir in templates
- Ignoring `*.pyc` files in templates
- UTF-8 support

### Fixed
- Issue that was ignoring the Manifest files during packaging.


## 0.1.1 - 2018-08-01
### Added
- README.rst to gitignore

### Removed
- Removed Download URL from setup.py (in templates as well)

### Fixed
- Makefile upload_pypi script from testpypi to pypi


## 0.1.0 - 2018-08-01
### Added
- Added complete feature of create python package based on [ansrivas/protemplates](https://github.com/ansrivas/protemplates)
- Added entrypoint called `nr-pypackage-cli` which is subject to change in the future.
- Released via pip
