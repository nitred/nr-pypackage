"""CLI entrypoint for creating entire python packages."""
from builtins import input
from pprint import pprint

import click
from nr_pypackage import package_creator

from . import cli_blueprints


@click.command()
@click.option('--package_name', type=str, prompt='Name of the package (e.g. pypackage)', help='Name of the package.', )
@click.option('--author_name', type=str, prompt='Name of the author (e.g. Thor Thoronsson)', help='Name of the author.', )
@click.option('--author_email', type=str, prompt='Email of the author (e.g. thor@asgard.com)', help='Email of the author.', )
@click.option('--scm_url', type=str, prompt='URL of the SCM (e.g. github.com, gitlab.com)', help='URL of the SCM.', )
@click.option('--scm_username', type=str, prompt='Username for the SCM (e.g. thor_bigguns)', help='Username used for the SCM.', )
@click.option('--dry_run', type=bool, prompt='Do you want to do a dry run? (e.g. Yes/No)', help='Dry run.', )
def package_simple(**kwargs):
    """Main CLI entrypoint for Python Package option."""
    kwargs['package_type'] = 'package_simple'
    click.echo("""
A python package with the following details will be created:
package_type: {package_type}
package_name: {package_name}
author_name : {author_name}
author_email: {author_email}
scm_url     : {scm_url}
scm_username: {scm_username}
dry_run     : {dry_run}
""".format(**kwargs))

    input("Please check the details above and hit enter to create package.")

    # Call the module that creates a package.
    package_creator.create_package(**kwargs)


@click.command()
@click.option('--package_name', type=str, prompt='Name of the package (e.g. pypackage)', help='Name of the package.', )
@click.option('--author_name', type=str, prompt='Name of the author (e.g. Thor Thoronsson)', help='Name of the author.', )
@click.option('--author_email', type=str, prompt='Email of the author (e.g. thor@asgard.com)', help='Email of the author.', )
@click.option('--scm_url', type=str, prompt='URL of the SCM (e.g. github.com, gitlab.com)', help='URL of the SCM.', )
@click.option('--scm_username', type=str, prompt='Username for the SCM (e.g. thor_bigguns)', help='Username used for the SCM.', )
@click.option('--dry_run', type=bool, prompt='Do you want to do a dry run? (e.g. Yes/No)', help='Dry run.', )
def package_flask(**kwargs):
    """Main CLI entrypoint for Python Package option."""
    kwargs['package_type'] = 'package_flask'
    click.echo("""
A python package with the following details will be created:
package_type: {package_type}
package_name: {package_name}
author_name : {author_name}
author_email: {author_email}
scm_url     : {scm_url}
scm_username: {scm_username}
dry_run     : {dry_run}
""".format(**kwargs))

    input("Please check the details above and hit enter to create package.")

    # Call the module that creates a package.
    package_creator.create_package(**kwargs)


@click.command()
@click.option('--package_name', type=str, prompt='Name of the package (e.g. pypackage)', help='Name of the package.', )
@click.option('--author_name', type=str, prompt='Name of the author (e.g. Thor Thoronsson)', help='Name of the author.', )
@click.option('--author_email', type=str, prompt='Email of the author (e.g. thor@asgard.com)', help='Email of the author.', )
@click.option('--scm_url', type=str, prompt='URL of the SCM (e.g. github.com, gitlab.com)', help='URL of the SCM.', )
@click.option('--scm_username', type=str, prompt='Username for the SCM (e.g. thor_bigguns)', help='Username used for the SCM.', )
@click.option('--dry_run', type=bool, prompt='Do you want to do a dry run? (e.g. y/n)', help='Dry run.', )
def package_flask_blueprints(**kwargs):
    """Main CLI endpoint to create a python flask package along with blueprints.

    How it works?
    * First we obtain all the package_flask options.
    * Then for each blueprint we obtain its options.
    * Then we render the package and the blueprints and write them to file.
    """
    kwargs['package_type'] = 'package_flask_blueprints'
    blueprint_options = {}
    for blueprint_name, blueprint_func in cli_blueprints.BLUEPRINTS.items():
        blueprint_include, blueprint_kwargs = blueprint_func()
        if blueprint_include is True:
            blueprint_options[blueprint_name] = blueprint_kwargs

    kwargs['blueprints'] = blueprint_options

    # Get confirmation from the user whether the details are correct.
    blueprints_list = [bp_name for bp_name, bp_kwargs in blueprint_options.items() if bp_kwargs['include'] is True]
    click.echo("""
    A python package with the following details will be created:
    package_type: {package_type}
    package_name: {package_name}
    author_name : {author_name}
    author_email: {author_email}
    scm_url     : {scm_url}
    scm_username: {scm_username}
    dry_run     : {dry_run}

    blueprints  : {blueprints_list}
    """.format(blueprints_list=blueprints_list, **kwargs))
    input("Please check the details above and hit enter to create package or Ctrl+C to cancel.")

    # Once we have confirmation from the user, create the package.
    package_creator.create_package(**kwargs)

    # Once the package has been created, printout the instructions for the blueprint.
    for blueprint_name, blueprint_kwargs in blueprint_options.items():
        if blueprint_kwargs.get('instructions', False):
            click.echo(blueprint_kwargs.get('instructions', ''))


def main(package_type):
    """Package CLI entrypoint.

    Args:
        package_type (str): `package_simple` or `package_flask`.
    """
    if package_type == 'package_simple':
        package_simple()
    elif package_type == 'package_flask':
        package_flask()
    elif package_type == 'package_flask_blueprints':
        package_flask_blueprints()
    else:
        raise NotImplementedError


if __name__ == '__main__':
    main()
