"""CLI entrypoint for creating entire python packages."""
from builtins import input

import click
from nr_pypackage import package_creator


def auth(**kwargs):
    """Main CLI entrypoint for Python Package option."""
    include = click.prompt('Include "auth against LDAP" blueprint? (y/n)', type=bool)
    instructions = """--------------------------------------------------------------------------------
            SPECIAL INSTRUCTIONS FOR BLUEPRINT: "auth"
--------------------------------------------------------------------------------
1. Edit the docker/docker-compose.yml to have a custom network subnet.
2. Edit blueprints.auth.models to include an `is_ldap_authenticated_user` function.
"""

    return include, {'include': include, 'instructions': instructions}


# MODULES = ['auth[ldap]', 'auth[postgres]', 'job-queue[redis]', 'job-queue[redis,celery]']
BLUEPRINTS = {
    'auth': auth
}
