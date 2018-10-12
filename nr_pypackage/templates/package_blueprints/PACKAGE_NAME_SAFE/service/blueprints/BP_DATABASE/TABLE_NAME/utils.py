"""Utils for {{ current_table_name_lower }}."""
from pprint import pformat, pprint


import pandas as pd
from flask import current_app, flash
{% if blueprints['auth']['include'] %}
from flask_login import current_user
{% endif %}
from {{ package_name_safe }}.service.database.{{ current_table_name_lower }} import {{ current_table_name_lower }}_api


################################################################################
# Common Utils
################################################################################
class SessionFormData(object):
    """A key value pair store for Form data.

    # NOTE: SessionFormData is supposed to be a store for key-value pairs with default values.
    # It is better if SessionFormData data to do no validation and let the endpoints and util functions
    # handle the use case specific validation.
    """

    KEYS = [{{ blueprints['database']['current_table'].column_names_as_args_str }}, 'submitted']

    def __init__(self, **kwargs):
        """Update the KEYS from kwargs."""
        self.kwargs = {}
        for key in self.KEYS:
            if key in kwargs.keys():
                # NOTE: Making sure that if a string is provided we strip away useless chars.
                if isinstance(kwargs[key], str):
                    kwargs[key] = kwargs[key].strip()
                self.kwargs[key] = kwargs[key]
            else:
                # Default value.
                self.kwargs[key] = ""

            # Special rules
            if key == 'id' and self.kwargs[key]:
                self.kwargs[key] = int(self.kwargs[key])

            setattr(self, key, self.kwargs[key])

    def _asdict(self):
        """Return the kwargs dict."""
        return self.kwargs


def generate_session_form_data_from_request(request):
    """Generate or populate a SessionFormData from request.form."""
    args = request.args.to_dict()
    print('generate_session_form_data_from_request: args              : \n{}'.format(pformat(args)))
    try:
        session_form_data = SessionFormData(**args)
        print('generate_session_form_data_from_request: session_form_data : \n{}'.format(pformat(session_form_data._asdict())))
        return session_form_data
    except Exception as ex:
        flash("Exception occured converting & validating form. Please check form details again.")
        return SessionFormData()


def get_{{ current_table_name_lower }}_config():
    """Get {{ current_table_name_lower }} config from the app config."""
    return current_app.config['app_config']['services']['{{ current_table_name_lower }}']


{% if blueprints['auth']['include'] %}
def is_user_permitted():
    """Is current user permitted."""
    {{ current_table_name_lower }}_config = get_{{ current_table_name_lower }}_config()
    permitted_users = {{ current_table_name_lower }}_config['permitted_users']
    if current_user.username in permitted_users:
        return True
    else:
        return False
{% else %}
def is_user_permitted():
    """No authentication."""
    return True
{% endif %}



def get_dict_of_{{ current_table_name_lower }}s():
    """Get {{ current_table_name_lower }} from database."""
    try:
        {{ current_table_name_lower }}_objs = {{ current_table_name_lower }}_api.get_{{ current_table_name_lower }}s()
        {{ current_table_name_lower }}_dict = {
            {{ current_table_name_lower }}.id: {
                {% for column_name in blueprints['database']['current_table'].column_names %}
                '{{ column_name }}': {{ current_table_name_lower }}.{{ column_name }},
                {% endfor %}
            }
            for {{ current_table_name_lower }} in {{ current_table_name_lower }}_objs
        }
        return {{ current_table_name_lower }}_dict
    except Exception:
        raise
