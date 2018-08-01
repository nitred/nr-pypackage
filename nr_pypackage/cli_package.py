"""CLI entrypoint for creating entire python packages."""
from builtins import input

import click

from nr_pypackage import option_package

################################################################################
# Options
################################################################################


@click.command()
@click.option('--package_name', type=str, prompt='Name of the package (e.g. pypackage)', help='Name of the package.', )
@click.option('--author_name', type=str, prompt='Name of the author (e.g. Thor Thoronsson)', help='Name of the author.', )
@click.option('--author_email', type=str, prompt='Email of the author (e.g. thor@asgard.com)', help='Email of the author.', )
@click.option('--scm_url', type=str, prompt='URL of the SCM (e.g. github.com, gitlab.com)', help='URL of the SCM.', )
@click.option('--scm_username', type=str, prompt='Username for the SCM (e.g. thor_bigguns)', help='Username used for the SCM.', )
@click.option('--dry_run', type=bool, prompt='Do you want to do a dry run? (e.g. Yes/No)', help='Dry run.', )
def options(**kwargs):
    """Main CLI entrypoint for Python Package option."""
    click.echo("""
A python package with the following details will be created:
package_name: {package_name}
author_name : {author_name}
author_email: {author_email}
scm_url     : {scm_url}
scm_username: {scm_username}
dry_run     : {dry_run}
""".format(**kwargs))

    input("Please check the details above and hit enter to create package.")

    # Call the module that creates a package.
    option_package.create_package(**kwargs)


################################################################################
# Main Entry Point
################################################################################
main_doc = """
--------------------------------------------------------------------------------
                            Option: Python Package
--------------------------------------------------------------------------------
You have chosen the option to create an entire python package. The python
package will be created in the current working directory.

We require some details in order to create a project. Please type in the details
as prompted.

"""


@click.command()
def main():
    """Main CLI entrypoint."""
    click.echo(main_doc)
    options()


if __name__ == '__main__':
    main()
