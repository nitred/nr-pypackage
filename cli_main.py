"""Main entrypoint."""
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


def abort():
    print("Aborted!")
    sys.exit(0)


database_header = """
--------------------------------------------------------------------------------
                                  DATABASE
--------------------------------------------------------------------------------
"""


table_header = """
--------------------------------------------------------------------------------
                               TABLE CREATION
--------------------------------------------------------------------------------
"""

column_header = """
--------------------------------------------------------------------------------
                    COLUMN CREATION FOR TABLE: {table_name}
--------------------------------------------------------------------------------
"""


def _ui_columns(table_name, all_table_details):
    ############################################################################
    # SETUP BINDINGS
    ############################################################################
    print(column_header)

    bindings = KeyBindings()
    bindings.add(Keys.Tab)(focus_next)
    bindings.add(Keys.Enter)(focus_next)
    bindings.add(Keys.BackTab)(focus_previous)

    # CTRL-C to quit the prompt-app.
    @bindings.add('c-c')
    def exit_c(event):
        """Ctrl-C to quit."""
        event.app.exit(result=False)

    @bindings.add('c-m')
    def exit_enter(event):
        """Enter."""
        import pprint
        pprint(dir(get_app().layout))

    def add_tables():
        get_app().exit(result="add_tables")

    def end_tables():
        get_app().exit(result="end_tables")

    ############################################################################
    # TABLE DETAILS
    ############################################################################
    table_name = TextArea(prompt='table_name (lower-case)       : ', multiline=False)
    column_names = TextArea(prompt='column_names (comma separated): ', multiline=False)

    column_data = {
        'col1': {
            'primary_key': False,
            'type': "Integer",
            'unique': False,
        },
        'col2': {
            'primary_key': False,
            'type': "Integer",
            'unique': False,
        },
    }

    def generate_column_text():
        from pprint import pformat
        return pformat(column_data, width=40)

    column_text_container = TextArea(
        text=generate_column_text(),
        read_only=True,
        focusable=False,
    )

    def update_column_text_container():
        column_text_container.text = generate_column_text()

    column_menu_container_body = TextArea(focusable=False, read_only=True)

    def c1_pk_true():
        get_app().layout.focus(column_menu_container)
        column_data['col1']['primary_key'] = True
        update_column_text_container()

    def c1_pk_false():
        get_app().layout.focus(column_menu_container)
        column_data['col1']['primary_key'] = False
        update_column_text_container()

    def c2_pk_true():
        get_app().layout.focus(column_menu_container)
        column_data['col2']['primary_key'] = True
        update_column_text_container()

    def c2_pk_false():
        get_app().layout.focus(column_menu_container)
        column_data['col2']['primary_key'] = False
        update_column_text_container()

    column_menu_container = MenuContainer(
        key_bindings=bindings,
        body=column_menu_container_body,
        menu_items=[
            MenuItem(
                text='EDIT COLUMN DETAILS',
                children=[
                    MenuItem(
                        text='col1',
                        handler=None,
                        children=[
                            MenuItem(
                                text='primary_key',
                                handler=None,
                                children=[
                                    MenuItem(
                                        text='True',
                                        handler=c1_pk_true,
                                    ),
                                    MenuItem(
                                        text='False',
                                        handler=c1_pk_false,
                                    )
                                ]
                            )
                        ],
                    ),
                    MenuItem(
                        text='col2',
                        handler=None,
                        children=[
                            MenuItem(
                                text='primary_key',
                                handler=None,
                                children=[
                                    MenuItem(
                                        text='True',
                                        handler=c2_pk_true,
                                    ),
                                    MenuItem(
                                        text='False',
                                        handler=c2_pk_false,
                                    )
                                ]
                            )
                        ],
                    ),
                ]
            ),
        ]
    )

    root_container = VSplit(
        width=80,
        children=[
            HSplit(
                padding=1,
                children=[
                    column_text_container,
                    VSplit(
                        height=10,
                        children=[
                            column_menu_container,
                        ]
                    ),
                    VSplit(
                        children=[
                            Button('Add More Tables', handler=add_tables, width=40),
                            Button('Done', handler=end_tables, width=40),
                        ],
                    ),
                ],
            ),
        ]
    )

    layout = Layout(root_container)

    app = Application(layout=layout,
                      key_bindings=bindings,
                      full_screen=False)

    app.layout.focus(column_menu_container)

    app_status = app.run()

    if not app_status:
        abort()

    return (app_status, table_name.text, column_names.text)


def _ui_table():
    ############################################################################
    # SETUP BINDINGS
    ############################################################################
    bindings = KeyBindings()
    bindings.add(Keys.Tab)(focus_next)
    bindings.add(Keys.Enter)(focus_next)
    bindings.add(Keys.BackTab)(focus_previous)

    # CTRL-C to quit the prompt-app.
    @bindings.add('c-c')
    def exit_c(event):
        """Ctrl-C to quit."""
        event.app.exit(result=False)

    def add_tables():
        get_app().exit(result="add_tables")

    def end_tables():
        get_app().exit(result="end_tables")

    ############################################################################
    # TABLE DETAILS
    ############################################################################
    table_name = TextArea(prompt='table_name (lower-case)       : ', multiline=False)
    column_names = TextArea(prompt='column_names (comma separated): ', multiline=False)

    root_container = VSplit(
        width=80,
        children=[
            HSplit(
                padding=1,
                children=[
                    Frame(
                        title='Database Table Details:',
                        body=HSplit(
                            width=80,
                            children=[
                                table_name,
                                column_names,
                            ]
                        ),
                    ),
                    VSplit(
                        children=[
                            Button('Add More Tables', handler=add_tables, width=40),
                            Button('Done', handler=end_tables, width=40),
                        ],
                    ),
                ],
            ),
        ]
    )

    layout = Layout(root_container)

    app = Application(layout=layout,
                      key_bindings=bindings,
                      full_screen=False)

    app_status = app.run()

    if not app_status:
        abort()

    return (app_status, table_name.text, column_names.text)


def handle_database():
    """Entrypoint for first interaction with user. Ask user to choose type of pypackage.

    NOTE: We're using python-prompt-toolkit which is both powerful and complicated, so we try to document its use asmuch as possible.
    """
    print(database_header)

    ############################################################################
    # TABLES
    ############################################################################
    all_table_details = {}
    while True:
        (table_status, table_name, column_names) = _ui_table()

        if table_status:
            # If table_status is not False, that means we have some valid table details.
            # Populate the table details into a dictionary.
            all_table_details[table_name] = {
                'name': table_name,
                'column_names': [column_name.strip() for column_name in column_names.split(',')],
                'column_details': None,
            }

            # Pass along all possible table details to the ui_columns function along with current table.
            columns_result = _ui_columns(table_name=table_name, all_table_details=all_table_details)

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
