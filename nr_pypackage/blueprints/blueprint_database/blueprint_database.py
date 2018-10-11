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
from pprint import pprint

from .ui_table import ui_table
from .ui_columns import ui_columns
from copy import deepcopy

from box import Box as DictBox


def abort():
    print("Aborted!")
    sys.exit(0)


database_instructions_doc = """--------------------------------------------------------------------------------
        SPECIAL INSTRUCTIONS FOR BLUEPRINT: "database"
--------------------------------------------------------------------------------
1. Enjoy yourself!
"""


database_header = """
--------------------------------------------------------------------------------
                                  DATABASE
--------------------------------------------------------------------------------
"""


def get_prepared_table_details(all_table_details):
    """Parse all table details and create readable/prepared table details dict."""
    table_details = {
        table_name: {
            'table_name': table_name,
            'table_name_lower': table_name.lower(),
            'column_names': table_dict['column_names'],
            'column_names_as_args': ", ".join([column_name for column_name in table_dict['column_names']]),
            'column_names_as_args_str': ", ".join([f"\'{column_name}\'" for column_name in table_dict['column_names']]),
            'column_details': table_dict['column_details'],
            'column_statements': [],
            'foreign_statements': set([]),
            'foreign_relationships': set([]),
        }
        for table_name, table_dict in all_table_details.items()
    }

    table_details = DictBox(table_details)

    # Iterating over a copy since we want to update the original as we iterate.
    for table_name, table_dict in deepcopy(table_details).items():
        for column_name, column_dict in table_dict.column_details.items():
            ####################################################################
            # FOREIGN KEY (on current table)
            ####################################################################
            if '.' in column_dict.type:
                # Column(Integer, ForeignKey('pipeline.id'), nullable=False)
                foreign_table = column_dict.type.split('.')[0]
                foreign_table_lower = foreign_table.lower()
                foreign_column = column_dict.type.split('.')[1]
                foreign_type = table_details[foreign_table]['column_details'][foreign_column]['type']

                foreign_statement = (f"{column_name} = "
                                     f"Column({foreign_type}, "
                                     f"ForeignKey('{foreign_table_lower}.{foreign_column}'), "
                                     f"primary_key={column_dict.primary_key}, "
                                     f"unique={column_dict.unique}, "
                                     f"nullable={column_dict.nullable})")

                table_details[table_name].foreign_statements.add(foreign_statement)

                ################################################################
                # FOREIGN RELATIONSHIP (on foreign table)
                ################################################################
                foreign_relationship = (f"{table_name.lower()}s = relationship('{table_name}')")
                table_details[foreign_table].foreign_relationships.add(foreign_relationship)

            ####################################################################
            # COLUMN
            ####################################################################
            else:
                column_statement = (f"{column_name} = "
                                    f"Column({column_dict.type}, "
                                    f"primary_key={column_dict.primary_key}, "
                                    f"unique={column_dict.unique}, "
                                    f"nullable={column_dict.nullable})")
                table_details[table_name].column_statements.append(column_statement)

    pprint("TABLE DETAILS")
    pprint(table_details, width=120, compact=True)
    return table_details


def handle_database(include):
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
                'table_name_lower': table_name.lower(),
                'column_names': [column_name.strip() for column_name in column_names.split(',')],
                'column_details': None,
            }

            # Pass along all possible table details to the ui_columns function along with current table.
            table_status, column_details = ui_columns(table_name=table_name, all_table_details=all_table_details)
            all_table_details[table_name]['column_details'] = column_details

            if table_status == "add_tables":
                pass
            elif table_status == "end_tables":
                break
            else:
                raise NotImplementedError(f"Unknown table_status: {table_status}")
        else:
            abort()

    table_details = get_prepared_table_details(all_table_details)

    return {'include': include, 'instructions': database_instructions_doc, 'tables': table_details}


if __name__ == "__main__":
    handle_database()
