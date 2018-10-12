"""Fill out the templates for package."""
import os
import sys

from pprint import pprint, pformat
import pkg_resources
from jinja2 import Template
from setuptools.package_index import safe_name
import traceback

RENDER_EXPEMPT_EXTENSIONS = []


def get_template_kwargs(package_name, author_name, author_email, scm_url, scm_username, blueprints):
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
        'blueprints': blueprints
    }


def is_ignore_file(file_path, blueprints_dict):
    """Should the file be ignored based on some conditions."""
    # Special rules.
    # NOTE 1: Ignore __pycache__ dir if you find it.
    if '__pycache__' in file_path:
        return True

    # NOTE 2: Ignore .pyc files if you find it.
    if file_path.endswith(".pyc"):
        return True

    # NOTE 3: Ignore blueprints that are not included.
    # We identify folders that belong entirely to a blueprint by the folder's name. The name of a folder that
    # belongs to a blueprint called `auth` is expected to "BP_AUTH" i.e. the format is
    # "BP_<blueprint_name.upper()>". We ignore these directories if the corresponding blueprint is not included.
    for blueprint_name, blueprint_kwargs in blueprints_dict.items():
        blueprint_placeholder = "/BP_{bp_name_upper}/".format(bp_name_upper=blueprint_name.upper())
        if blueprint_placeholder in file_path and blueprint_kwargs['include'] is not True:
            print("IGNORING BLUEPRINT FILE: {}: {}".format(blueprint_name, file_path))
            return True

    return False


def is_file_render_exempt(template_filename):
    """Return boolean to indicate if file should be rendered or not."""
    for render_expempt_extension in RENDER_EXPEMPT_EXTENSIONS:
        # If filename ends with render exempt extension.
        if template_filename.endswith(render_expempt_extension):
            return True

    return False


def render_template(template_filename, **template_kwargs):
    """Render template from filename based on keywords."""
    # print("render_template: {}".format(template_filename))
    with open(template_filename, 'rb') as f:
        file_contents = f.read().decode('utf-8')

    if is_file_render_exempt(template_filename):
        return file_contents
    else:
        return Template(file_contents,
                        trim_blocks=True,
                        lstrip_blocks=True,
                        keep_trailing_newline=True).render(**template_kwargs)


def get_file_path_package(package_dir, relative_path, replace_dict=None):
    """Get package file path, which is "package_dir/relative_path"."""
    replace_dict = replace_dict if replace_dict is not None else {}

    # NOTE: We place on the relative_path not the package_dir since package_dir comes from the user.
    for replace_key, replace_val in replace_dict.items():
        relative_path = relative_path.replace(replace_key, replace_val)

    file_path_package = os.path.abspath(os.path.join(package_dir, relative_path))

    return file_path_package


def get_rendered_file(file_path_template, template_kwargs):
    """Get rendered file from template file path."""
    assert os.path.isfile(file_path_template), ("Template file {file_path_template} must be a FILE but is not."
                                                .format(file_path_template=file_path_template))
    # Render file.
    rendered_file = render_template(file_path_template, **template_kwargs)
    return rendered_file


def get_generator_of_template_filenames_and_renders(CWD, PACKAGE_DIR, package_type, template_kwargs):
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
        generator of tuples (str, str): (template_filename, template_rendered)
            Generator of tuple of two strings. First string is the path to which to write the rendered template
            and second is the rendered template.
    """
    TEMPLATES_DIR = pkg_resources.resource_filename('nr_pypackage', 'templates/{}'.format(package_type))

    for root, dirs, files in os.walk(TEMPLATES_DIR):
        for filename in files:
            # File path, within templates
            file_path_template = os.path.join(root, filename)

            # NOTE: Ignore files based on file extensions and some conditions specific to blueprints.
            if is_ignore_file(file_path_template, blueprints_dict=template_kwargs.get('blueprints', {})):
                continue

            # NOTE: Special way to render files when database blueprint is enabled.
            # If filename consists of TABLE_NAME anywhere, then it must be looped for every table in
            # blueprints['database']['tables'].keys().
            # We also set blueprints['database']['current_table'] = blueprints['database']['tables'][current_table_name].
            # After it has been used, we will pop `current_table_name` from blueprints['database']['tables'].
            if "BP_DATABASE" in file_path_template and "TABLE_NAME" in file_path_template:
                blueprints = template_kwargs.get('blueprints', {})
                bp_database = blueprints.get('database', {})
                bp_tables = bp_database.get('tables', {})
                for table_name, table_details in bp_tables.items():
                    # Add a new entry in template_kwargs called current_table.
                    template_kwargs['blueprints']['database']['current_table'] = bp_tables[table_name]
                    template_kwargs['current_table_name'] = table_name
                    template_kwargs['current_table_name_lower'] = table_name.lower()
                    # print(f"rendering file: {file_path_template}")
                    rendered_file = get_rendered_file(file_path_template, template_kwargs)
                    # Remove current_table from template_kwargs once rendering is done.
                    template_kwargs['blueprints']['database'].pop('current_table', None)
                    template_kwargs.pop('current_table_name', None)
                    template_kwargs.pop('current_table_name_lower', None)

                    file_path_relative = os.path.relpath(file_path_template, TEMPLATES_DIR)
                    file_path_package = get_file_path_package(package_dir=PACKAGE_DIR,
                                                              relative_path=file_path_relative,
                                                              replace_dict={
                                                                  'PACKAGE_NAME_SAFE': template_kwargs['package_name_safe'],
                                                                  "BP_AUTH": "auth",
                                                                  "BP_DATABASE": "database",
                                                                  "TABLE_NAME": table_name.lower()
                                                              })
                    yield (file_path_package, rendered_file)
            else:
                # print(f"rendering file: {file_path_template}")
                rendered_file = get_rendered_file(file_path_template, template_kwargs)
                file_path_relative = os.path.relpath(file_path_template, TEMPLATES_DIR)
                file_path_package = get_file_path_package(package_dir=PACKAGE_DIR,
                                                          relative_path=file_path_relative,
                                                          replace_dict={
                                                              'PACKAGE_NAME_SAFE': template_kwargs['package_name_safe'],
                                                              "BP_AUTH": "auth",
                                                              "BP_DATABASE": "database",
                                                          })

                yield (file_path_package, rendered_file)


def create_package(package_type, package_name, author_name, author_email, scm_url, scm_username, dry_run, blueprints=None):
    """Create the python package from the provided details.

    Here is the pipeline for creating the package:
      - Get current working directory (CWD)
      - Get package directory from CWD
      - Render all templates
      - Create package directory
      - Create all templates into package directory

    Special:
      - If blueprints don't exist, then just give an empty dictionary.
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
    blueprints = {} if blueprints is None else blueprints

    template_kwargs = get_template_kwargs(package_name, author_name, author_email, scm_url, scm_username, blueprints)

    try:
        # # Create directory.
        # if dry_run is False:
        #     os.makedirs(PACKAGE_DIR)

        # RENDER TEMPLATES & WRITE THEM
        for package_filename, rendered_file in get_generator_of_template_filenames_and_renders(CWD,
                                                                                               PACKAGE_DIR,
                                                                                               package_type,
                                                                                               template_kwargs):

            # Create file.
            if dry_run is False:
                # Create directories for the file.
                if not os.path.exists(os.path.dirname(package_filename)):
                    os.makedirs(os.path.dirname(package_filename))

                print("Creating file: {package_filename}".format(package_filename=package_filename))
                with open(package_filename, 'wb') as f:
                    f.write(rendered_file.encode('utf-8'))
            else:
                print("(DRY-RUN) Creating file: {package_filename}".format(package_filename=package_filename))

        # STARTING GIT
        if dry_run is False:
            print("Initializing git in {PACKAGE_DIR}".format(PACKAGE_DIR=PACKAGE_DIR))
            os.chdir(PACKAGE_DIR)
            os.system("git init")
        else:
            print("(DRY-RUN) Initializing git in {PACKAGE_DIR}".format(PACKAGE_DIR=PACKAGE_DIR))
    except Exception as ex:
        print("************************************************************************")
        print("ERROR: Exception has occured! Removing all created folders if not dry run!")
        print("ERROR: Package directory: {PACKAGE_DIR}".format(PACKAGE_DIR=PACKAGE_DIR))
        if dry_run is False:
            if os.path.exists(PACKAGE_DIR):
                print("ERROR: Package directory exists, removing it!")
                # os.rmdir(PACKAGE_DIR)
        print("************************************************************************")
        raise
