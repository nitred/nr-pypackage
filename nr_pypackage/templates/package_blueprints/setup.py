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
    with open('{{ package_name_safe }}/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


install_requires = [
    "Flask>=1.1.1,<1.2",
    "Flask-restful==0.3.7",
    "gunicorn>=19.9.0,<19.10",
    "gevent==1.4.0",
    {% if blueprints['auth']['include'] %}
    "Flask-Login==0.4.1",
    "Flask-Session==0.3.1",
    "Flask-WTF==0.14.2",
    "redis>=3.3.7,<3.4",
    "ldap3>=2.6,<2.7",
    {% endif %}
    {% if blueprints['database']['include'] %}
    "Flask-SQLAlchemy>=2.4.0,<2.5",
    "psycopg2-binary>=2.8.2,<2.9",
    "pandas==0.23.4",
    {% endif %}
    "nr-common",
    "docker-compose",
]


test_requires = ['pytest', 'pytest-sugar', 'pytest-asyncio', 'pytest-cov', ]


setup(
    name='{{ package_name }}',
    description="Some description about your project",
    long_description=long_description,
    version=get_version(),
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    entry_points={},
    tests_require=test_requires,
    packages=find_packages(),
    zip_safe=False,
    author="{{ author_name }}",
    author_email="{{ author_email }}",
    # download_url="{{ scm_url }}/{{ scm_username }}/{{ package_name }}/archive/{}.tar.gz".format(get_version()),
    classifiers=[
        "Programming Language :: Python :: 3.6", ]
)
