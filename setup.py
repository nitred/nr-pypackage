import re
from codecs import open  # To use a consistent encoding
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# Get version without importing, which avoids dependency issues
def get_version():
    with open('nr_pypackage/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


install_requires = ['future']


test_requires = ['pytest', 'pytest-sugar', 'pytest-asyncio', 'pytest-cov', ]


setup(
    name='nr-pypackage',
    description="Some description about your project",
    long_description=long_description,
    version=get_version(),
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    entry_points={
        'console_scripts': [
            'pypackage-cli = nr_pypackage.cli_main:main',
        ],
    },
    tests_require=test_requires,
    packages=find_packages(),
    zip_safe=False,
    author="Nitish Reddy Koripalli",
    author_email="nitish.k.reddy@gmail.com",
    download_url="github.com/nitred/{}.tar.gz".format(get_version()),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6", ]
)
