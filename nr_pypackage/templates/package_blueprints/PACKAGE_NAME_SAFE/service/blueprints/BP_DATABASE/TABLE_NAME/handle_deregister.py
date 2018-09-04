"""Utils for {{ current_table_name_lower }}s."""
import logging
from pprint import pformat, pprint

import pandas as pd
from flask import current_app, flash

from . import utils
from {{ package_name_safe }}.service.database import {{ current_table_name_lower }}_api
import traceback

logger = logging.getLogger(__name__)


def deregister_{{ current_table_name_lower }}_in_database({{ blueprints['database']['current_table'].column_names_as_args }}):
    try:
        return {{ current_table_name_lower }}_api.deregister_{{ current_table_name_lower }}(
            {% for column_name in blueprints['database']['current_table'].column_names %}
            {{ column_name }}={{ column_name }},
            {% endfor %}
        )
    except Exception as ex:
        flash(f"Error deregister_{{ current_table_name_lower }}_in_database()")
        flash(f"Exception: {str(ex)}")
        print(traceback.format_exc())
        return False


def deregister_{{ current_table_name_lower }}(session_form_data):
    """Register based on form data."""
    # Condition: User must be permitted.
    if not utils.is_user_permitted():
        flash("Did not deregister service. Your user is not permitted to deregister new services!")
        return None

    # Register.
    deregistered_{{ current_table_name_lower }} = deregister_{{ current_table_name_lower }}_in_database(
        {% for column_name in blueprints['database']['current_table'].column_names %}
        {{ column_name }}=session_form_data.{{ column_name }},
        {% endfor %}
    )

    if deregistered_{{ current_table_name_lower }}:
        msg = (f"Successfully deregistered {{ current_table_name }} with {{ current_table_name_lower }}.id: \"{deregistered_{{ current_table_name_lower }}.id}\"!")
        logger.info(msg)
        flash(msg)
    else:
        msg = (f"Did not deregister {{ current_table_name }}!. Please check error message or contact devs!")
        logger.error(msg)
        flash(msg)
