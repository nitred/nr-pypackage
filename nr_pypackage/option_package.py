"""Fill out the templates for package."""
import os
import sys

import pkg_resources
from jinja2 import Template
from setuptools.package_index import safe_name


def get_template_kwargs(package_name, author_name, author_email, scm_url, scm_username):
    """Get template kwargs for python package options from the arguments."""
    package_name = safe_name(package_name)
    package_name_safe = package_name.replace("-", "_")
    return {
        'package_name': package_name,
        'package_name_safe': package_name_safe,
        'author_name': author_name,
        'author_name': author_name,
        'author_email': author_email,
        'scm_url': scm_url,
        'scm_username': scm_username,
    }


def render_template(template_filename, **template_kwargs):
    """Render template from filename based on keywords."""
    # print("render_template: {}".format(template_filename))
    with open(template_filename, 'rb') as f:
        template = Template(f.read().decode('utf-8'))

    return template.render(**template_kwargs)


def get_generator_of_template_filenames_and_renders(CWD, PACKAGE_DIR, template_kwargs):
    """Get generator of tuples consisting of rendered templates and filename to write to.

    How this works:
      - `os.walk` along the templates directory
      - Whenever you encounter a template `file`:
        - render it with the template_kwargs
        - get the template file's path w.r.t the cwd

    Args:
        CWD (str): Current working directory.
        PACKAGE_DIR (str): Package directory.
        template_kwargs (dict): Dictionary containing the template keyword arguments that are used to render the
            template.

    Returns:
        generator of tuples (str, str): Generator of tuple of two strings. First string is the rendered template and the
            second string is the path to which to write the rendered template.
    """
    TEMPLATES_DIR = pkg_resources.resource_filename('nr_pypackage', 'templates')

    for root, dirs, files in os.walk(TEMPLATES_DIR):
        for filename in files:
            file_path_template = os.path.join(root, filename)                                            # File path, within templates

            # Special rules.
            # NOTE 1: Ignore __pycache__ dir if you find it.
            if '__pycache__' in file_path_template:
                # print("IGNORING __pycache__: {}".format(file_path_template))
                continue

            # NOTE 2: Ignore __pycache__ dir if you find it.
            if file_path_template.endswith(".pyc"):
                # print("IGNORING __pycache__: {}".format(file_path_template))
                continue

            file_path_relative = os.path.relpath(file_path_template, TEMPLATES_DIR)                      # File path, relative within templates
            file_path_package = os.path.abspath(os.path.join(PACKAGE_DIR, file_path_relative))           # File path, within package
            rendered_file = render_template(file_path_template, **template_kwargs)

            assert os.path.isfile(file_path_template), ("Template file {file_path_template} must be a FILE but is not."
                                                        .format(file_path_template=file_path_template))

            # Special rules.
            # NOTE 3: Replace the folder name 'PACKAGE_NAME_SAFE' with the actual 'package_name_safe'
            file_path_package = file_path_package.replace("PACKAGE_NAME_SAFE", template_kwargs.get('package_name_safe',
                                                                                                   'PACKAGE_NAME_SAFE'))

            yield (file_path_package, rendered_file)


def create_package(package_name, author_name, author_email, scm_url, scm_username, dry_run):
    """Create the python package from the provided details.

    Here is the pipeline for creating the package:
      - Get current working directory (CWD)
      - Get package directory from CWD
      - Render all templates
      - Create package directory
      - Create all templates into package directory
    """
    # GET STUFF
    CWD = os.path.abspath("./")
    PACKAGE_DIR = os.path.join(CWD, package_name)

    if os.path.exists(PACKAGE_DIR):
        print("************************************************************************")
        print("ERROR: Package directory already exists! We will not overwrite anything!")
        print("ERROR: Package directory: {PACKAGE_DIR}".format(PACKAGE_DIR=PACKAGE_DIR))
        print("************************************************************************")
        sys.exit(0)

    # GET TEMPLATE KWARGS
    template_kwargs = get_template_kwargs(package_name, author_name, author_email, scm_url, scm_username)

    # RENDER TEMPLATES & WRITE THEM
    for package_filename, rendered_file in get_generator_of_template_filenames_and_renders(CWD, PACKAGE_DIR, template_kwargs):
        # Create file.
        if dry_run is False:
            # Create directories for the file.
            if not os.path.exists(os.path.dirname(package_filename)):
                os.makedirs(os.path.dirname(package_filename))

            print("Creating file: {package_filename}".format(package_filename=package_filename))
            with open(package_filename, 'wb') as f:
                f.write(rendered_file.encode('utf-8'))
        else:
            print("(DRY-RUN) Creating file: {package_filename}".format(package_filename=package_name))

    # STARTING GIT
    if dry_run is False:
        print("Initializing git in {PACKAGE_DIR}".format(PACKAGE_DIR=PACKAGE_DIR))
        os.chdir(PACKAGE_DIR)
        os.system("git init")
    else:
        print("(DRY-RUN) Initializing git in {PACKAGE_DIR}".format(PACKAGE_DIR=PACKAGE_DIR))
