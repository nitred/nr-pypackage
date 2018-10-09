from prompt_toolkit.application import Application
from prompt_toolkit.layout.containers import VSplit, HSplit
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea, Label, Frame, Box, Checkbox, Dialog, Button, RadioList, MenuContainer, MenuItem, ProgressBar
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.application.current import get_app
import sys
from prompt_toolkit import prompt

from .ui_table import ui_table
from .ui_columns import ui_columns


def abort():
    print("Aborted!")
    sys.exit(0)


database_header = """
--------------------------------------------------------------------------------
                                  DATABASE
--------------------------------------------------------------------------------
"""


def handle_database():
    """Entrypoint for first interaction with user. Ask user to choose type of pypackage.

    NOTE: We're using python-prompt-toolkit which is both powerful and complicated, so we try to document its use asmuch as possible.
    """
    # print(database_header)

    ############################################################################
    # TABLES
    ############################################################################
    all_table_details = {}
    while True:
        (table_status, table_name, column_names) = ui_table()

        if table_status:
            # If table_status is not False, that means we have some valid table details.
            # Populate the table details into a dictionary.
            all_table_details[table_name] = {
                'table_name': table_name,
                'column_names': [column_name.strip() for column_name in column_names.split(',')],
                'column_details': None,
            }

            # Pass along all possible table details to the ui_columns function along with current table.
            columns_result = ui_columns(table_name=table_name, all_table_details=all_table_details)

            if table_status == "add_tables":
                pass
            elif table_status == "end_tables":
                break
        else:
            abort()

    print("end of the line")
    sys.exit(0)

    # ############################################################################
    # # Actually application container.
    # ############################################################################
    # print(blueprints_doc)
    # result = app.run()
    #
    # if result:
    #     blueprint_options = {}
    #     for blueprint_name, blueprint_checkbox in blueprints.items():
    #         if blueprint_checkbox.checked:
    #             blueprint_handler = blueprint_handlers[blueprint_name]
    #             blueprint_options[blueprint_name] = blueprint_handler(include=True)
    #     print(blueprint_options)
    #     return blueprint_options
    # else:
    #     print("Aborted!")
    #     sys.exit(0)


if __name__ == "__main__":
    handle_database()
