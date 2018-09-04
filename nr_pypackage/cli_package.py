"""CLI entrypoint for creating entire python packages."""
from builtins import input
from pprint import pprint, pformat

import click
from nr_pypackage import package_creator

from . import blueprints


def common_options(function):
    function = click.option(
        "--dry_run",
        type=bool,
        prompt="Do you want to do a dry run? (e.g. Yes/No)",
        help="Is this a dry run?",
    )(function)
    function = click.option(
        "--scm_username",
        type=str,
        prompt="Username for the SCM (e.g. thor_bigguns)",
        help="Username used for the SCM.",
    )(function)
    function = click.option(
        "--scm_url",
        type=str,
        prompt="URL of the SCM (e.g. github.com, gitlab.com)",
        help="URL of the SCM.",
    )(function)
    function = click.option(
        "--author_email",
        type=str,
        prompt="Email of the author (e.g. thor@asgard.com)",
        help="Email of the author.",
    )(function)
    function = click.option(
        "--author_name",
        type=str,
        prompt="Name of the author (e.g. Thor Thoronsson)",
        help="Name of the author.",
    )(function)
    function = click.option(
        "--package_name",
        type=str,
        prompt="Name of the package (e.g. pypackage)",
        help="Name of the package.",
    )(function)
    return function


def echo_summary(**kwargs):
    msg = (
        f"A python package with the following details will be created:\n\n"
        f"package_type: {kwargs['package_type']}\n"
        f"package_name: {kwargs['package_name']}\n"
        f"author_name: {kwargs['author_name']}\n"
        f"author_email: {kwargs['author_email']}\n"
        f"scm_url: {kwargs['scm_url']}\n"
        f"scm_username: {kwargs['scm_username']}\n"
        f"dry_run: {kwargs['dry_run']}\n"
    )

    if "blueprints_list" in kwargs:
        msg += f"\nblueprints  : {kwargs['blueprints_list']}\n"

    click.echo(msg)

    input("Please check the details above and hit enter to create package or Ctrl+C to cancel.")


@click.command()
@common_options
def package_simple(**kwargs):
    """Entrypoint for simple package."""
    kwargs["package_type"] = "package_simple"
    echo_summary(**kwargs)

    # Call the module that creates a package.
    package_creator.create_package(**kwargs)


@click.command()
@common_options
def package_flask(**kwargs):
    """Entrypoint for package with flask."""
    kwargs["package_type"] = "package_flask"
    echo_summary(**kwargs)

    # Call the module that creates a package.
    package_creator.create_package(**kwargs)


@click.command()
@common_options
def package_blueprints(**kwargs):
    """Entrypoint for package with flask & blueprints.

    How it works?
    * First we obtain all the package_flask options.
    * Then for each blueprint we obtain its options.
    * Then we render the package and the blueprints and write them to file.
    """
    kwargs["package_type"] = "package_blueprints"
    blueprint_options = blueprints.handle_blueprints()
    kwargs["blueprints"] = blueprint_options

    # Get confirmation from the user whether the details are correct.
    blueprints_list = [
        bp_name for bp_name, bp_kwargs in blueprint_options.items() if bp_kwargs["include"] is True
    ]
    echo_summary(blueprints_list=blueprints_list, **kwargs)

    # Once we have confirmation from the user, create the package.
    package_creator.create_package(**kwargs)

    # Once the package has been created, printout the instructions for the blueprint.
    for blueprint_name, blueprint_kwargs in blueprint_options.items():
        if blueprint_kwargs.get("instructions", False):
            click.echo(blueprint_kwargs.get("instructions", ""))


def main(package_type):
    """Package CLI entrypoint.

    Args:
        package_type (str): `package_simple` or `package_flask`.
    """
    if package_type == "package_simple":
        package_simple()
    elif package_type == "package_flask":
        package_flask()
    elif package_type == "package_blueprints":
        package_blueprints()
    else:
        raise NotImplementedError


if __name__ == "__main__":
    main()
