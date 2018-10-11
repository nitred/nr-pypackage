"""Utils for consulate."""
import logging
from pprint import pformat, pprint

import pandas as pd
from flask import current_app, flash
from flask_login import current_user

from . import utils
from pydagger.service.database import pipeline_api

logger = logging.getLogger(__name__)


def deregister_pipeline_in_database(id):
    try:
        deregistered_pipeline = pipeline_api.deregister_pipeline(id=id)
        return deregistered_pipeline
    except Exception as ex:
        flash(f"Error deregister_pipeline_in_database()")
        flash("Exception: {}".format(str(ex)))
        return False


def deregister_pipeline(session_form_data):
    """Deregister service based on form data."""
    # Condition: User must be permitted.
    if not utils.is_user_permitted():
        flash("Did not update service. Your user is not permitted to update new services!")
        return None

    # Condition: id should exist in the services.
    pipelines_dict = utils.get_pipelines()
    if session_form_data.id not in pipelines_dict.keys():
        flash(f"Did not deregister pipeline. Pipeline ID: \"{session_form_data.id}\" does not exist in the pipelines.")
        return None

    # deregister.
    deregistered_pipeline = deregister_pipeline_in_database(id=session_form_data.id)

    pipelines_dict = utils.get_pipelines()
    if deregistered_pipeline and session_form_data.id not in pipelines_dict.keys():
        msg = (f"Successfully deregistered pipeline with Pipeline ID: \"{session_form_data.id}\"")
        logger.info(msg)
        flash(msg)
    elif deregistered_pipeline:
        msg = (f"Deregistered the pipeline but data has been CORRUPTED! Please check data and contact devs!")
        logger.error(msg)
        flash(msg)
    else:
        deregistered_pipeline
        msg = (f"Did not deregister pipeline with Pipeline ID: \"{session_form_data.id}\". "
               f"We assume a failure of registration. Please contact devs!")
        logger.error(msg)
        flash(msg)
