"""Utils for consulate."""
from pprint import pformat, pprint

import pandas as pd
from flask import current_app, flash
from flask_login import current_user

from . import utils


def get_list_of_{{ current_table_name_lower }}s_as_div():
    """Return dataframe as html."""
    try:
        column_order = [{{ blueprints['database']['current_table'].column_names_as_args_str }}]
        {{ current_table_name_lower }}s_dict = utils.get_dict_of_{{ current_table_name_lower }}s()
        if {{ current_table_name_lower }}s_dict:
            df = pd.DataFrame.from_dict({{ current_table_name_lower }}s_dict, orient='index')[column_order]
        else:
            df = pd.DataFrame(columns=column_order)
        return df.to_html(table_id='dataframe', index=False)
    except Exception as ex:
        flash(f"Error get_list_of_{{ current_table_name_lower }}s_as_div()")
        flash("Exception: {}".format(str(ex)))
        return pd.DataFrame().to_html(table_id='dataframe')
