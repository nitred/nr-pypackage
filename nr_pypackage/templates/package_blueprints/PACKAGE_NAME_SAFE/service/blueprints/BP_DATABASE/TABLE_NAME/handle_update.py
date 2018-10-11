"""Utils for pipelines."""
import logging
from pprint import pformat, pprint

import pandas as pd
from flask import current_app, flash
from flask_login import current_user

from . import utils
from pydagger.service.database import pipeline_api

logger = logging.getLogger(__name__)


def update_pipeline_in_database(id, name, tag):
    try:
        update_pipeline = pipeline_api.update_pipeline(id, name, tag)
        return update_pipeline
    except Exception as ex:
        flash(f"Error update_pipeline_in_database()")
        flash("Exception: {}".format(str(ex)))
        return False


def update_pipeline(session_form_data):
    """Update service based on form data."""
    # Condition: User must be permitted.
    if not utils.is_user_permitted():
        flash("Did not update service. Your user is not permitted to update new services!")
        return None

    # Condition: name should not be empty.
    if not session_form_data.name:
        flash(f"Did not update name. Pipeline Name is empty.")
        return None

    # Condition: pipeline name should not already exist in the services.
    pipelines_dict = utils.get_pipelines()  # guaranteed name uniqueness
    if session_form_data.id not in pipelines_dict.keys():
        flash(f"Did not update service. Pipeline ID: \"{session_form_data.id}\" does not exist in the pipelines.")
        return None

    # Update.
    updated_pipeline = update_pipeline_in_database(id=session_form_data.id,
                                                   name=session_form_data.name,
                                                   tag=session_form_data.tag)

    pipelines_dict = utils.get_pipelines()
    pipelines_names = [v['name'] for k, v in pipelines_dict.items()]
    if updated_pipeline and session_form_data.id in pipelines_dict.keys() and session_form_data.name in pipelines_names:
        msg = (f"Successfully updated pipeline with Pipeline ID: \"{session_form_data.id}\" and "
               f"Name: \"{session_form_data.name}\".")
        logger.info(msg)
        flash(msg)
    elif updated_pipeline:
        msg = (f"Updated the pipeline but data has been CORRUPTED! Please check data and contact devs!")
        logger.error(msg)
        flash(msg)
    else:
        msg = (f"Did not update pipeline with Pipeline ID: \"{session_form_data.id}\" and "
               f"Name: \"{session_form_data.name}\". We assume a failure of registration. Please contact devs!")
        logger.error(msg)
        flash(msg)
