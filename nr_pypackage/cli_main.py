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
What do you want to create?
[1] simple python package
[2] flask  python package
[3] flask  python package with blueprints

Enter the option number"""


@click.command()
@click.option('--template_type', type=int, prompt='{}'.format(main_doc), help='Choice of template.', )
def main(template_type):
    """Main CLI entrypoint."""
    if template_type == 1:
        package_type = 'package_simple'
        cli_package.main(package_type)
    elif template_type == 2:
        package_type = 'package_flask'
        cli_package.main(package_type)
    elif template_type == 3:
        package_type = 'package_flask_blueprints'
        cli_package.main(package_type)
    else:
        print("Other options, coming soon!")


if __name__ == '__main__':
    main()
