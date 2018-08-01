"""Main entrypoint."""
import click

from . import cli_package

################################################################################
# Main Entry Point
################################################################################
main_doc = """
--------------------------------------------------------------------------------
                             NR-PYPACKAGE
--------------------------------------------------------------------------------
This project is about creating standardized python projects, packages
and modules.

We provide standardized template options for the following use cases:

[1] python package
    Choose this if you would like to create an entire python package.

[2] python modules
    Choose this if you would like to create specific python modules within your
    pre-existing python package. This creates a python submodule in the current
    directory.

Please choose the option you want from above. Use the option number (i.e. 1 or 2):
"""


@click.command()
@click.option('--template_type', type=int, prompt='{}'.format(main_doc), help='The person to greet.', )
def main(template_type):
    """Main CLI entrypoint."""
    if template_type == 1:
        cli_package.main()


if __name__ == '__main__':
    main()
