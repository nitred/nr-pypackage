"""Utils for pipelines."""
import logging
from pprint import pformat, pprint

import pandas as pd
from flask import current_app, flash

from . import utils
from {{ package_name_safe }}.service.database import {{ current_table_name_lower }}_api
import traceback

logger = logging.getLogger(__name__)


def update_{{ current_table_name_lower }}_in_database({{ blueprints['database']['current_table'].column_names_as_args }}):
    try:
        return {{ current_table_name_lower }}_api.update_{{ current_table_name_lower }}(
            {% for column_name in blueprints['database']['current_table'].column_names %}
            {{ column_name }}={{ column_name }},
            {% endfor %}
        )
    except Exception as ex:
        flash(f"Error update_{{ current_table_name_lower }}_in_database()")
        flash("Exception: {}".format(str(ex)))
        print(traceback.format_exc())
        return False


def update_{{ current_table_name_lower }}(session_form_data):
    """Update based on form data."""
    # Condition: User must be permitted.
    if not utils.is_user_permitted():
        flash("Did not update service. Your user is not permitted to update new services!")
        return None

    # Register.
    updated_{{ current_table_name_lower }} = update_{{ current_table_name_lower }}_in_database(
        {% for column_name in blueprints['database']['current_table'].column_names %}
        {{ column_name }}=session_form_data.{{ column_name }},
        {% endfor %}
    )

    if updated_{{ current_table_name_lower }}:
        msg = (f"Successfully updated {{ current_table_name }} with {{ current_table_name_lower }}.id: \"{updated_{{ current_table_name_lower }}.id}\"!")
        logger.info(msg)
        flash(msg)
    else:
        msg = (f"Did not update {{ current_table_name }}!. Please check error message or contact devs!")
        logger.error(msg)
        flash(msg)
