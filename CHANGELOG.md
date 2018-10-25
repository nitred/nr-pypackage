# Changelog
All notable changes to this project will be documented in this file.

## 0.3.0.rc1 rc2 rc3 - 2018-10-07 to 2018-10-25
- package-flask-blueprints for database.
- cli for configuring tables and configuring columns of the table.
- added feature to accept name, type, uniqueness, composite uniqueness of columns.
- added feature to accept data for certain column as text or via file uploads.
- added feature to create foreign relationships with lazy or eager loading of foreign tables.
- added feature to create ui endpoints to manage (i.e. list, register, update, deregister) items in tables.
- added feature to create rest endpoints for each table.

## 0.2.0 - 2018-08-29
- package-flask-blueprints template type
- added auth (for ldap authentication) blueprint
- added redis in docker-compose for auth blueprint (for flask-session)
- added nav-bar in navigation-template that supports logout and back buttons

## 0.1.2 - 2018-08-01
- Ignoring `__pycache__` dir in templates
- Ignoring `*.pyc` files in templates
- added UTF-8 support
- fixed issue that was ignoring the Manifest files during packaging.

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
