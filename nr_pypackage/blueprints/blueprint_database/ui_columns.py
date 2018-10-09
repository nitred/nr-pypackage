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
from copy import deepcopy


def abort():
    print("Aborted!")
    sys.exit(0)


column_attributes = {
    'primary_key': [False, True],
    'type': ['Integer', 'Float', 'String', 'Boolean', 'Unicode', 'DateTime'],
    'unique': [False, True]
}

column_attributes_default = {k: v[0] for k, v in column_attributes.items()}


column_header = """
--------------------------------------------------------------------------------
{header:^80}
--------------------------------------------------------------------------------
"""


def get_key_bindings():
    bindings = KeyBindings()
    bindings.add(Keys.Tab)(focus_next)
    bindings.add(Keys.Enter)(focus_next)
    bindings.add(Keys.BackTab)(focus_previous)

    # CTRL-C to quit the prompt-app.
    @bindings.add('c-c')
    def exit_c(event):
        """Ctrl-C to quit."""
        event.app.exit(result=False)

    return bindings


def get_column_details_container(column_names, column_details):
    # column names labels
    column_name_labels = {column_name: Label(text=column_name) for column_name in column_names}
    # column details labels
    column_details_labels = {
        column_name: {
            attr_key: Label(text=f"{attr_key}: {attr_val}") for attr_key, attr_val in column_details[column_name].items()
        }
        for column_name in column_names
    }
    # container for representing column details properly
    column_details_container = HSplit(
        children=[
            VSplit(
                children=[
                    # On the left side, we have just the column name and its label.
                    Frame(column_name_labels[column_name]),
                    # On the right handed side we have attr_key: attr_val label for every column
                    Frame(HSplit(
                        children=[
                            attr_val for attr_key, attr_val in column_details_labels[column_name].items()
                        ]
                    ))
                ])
            for column_name in column_details_labels.keys()
        ],
    )

    return column_name_labels, column_details_labels, column_details_container


def get_column_details(table_name, all_table_details):
    # list of column names
    column_names = all_table_details[table_name]['column_names']
    # column_name to column_attribute mapping
    column_details = {column_name: deepcopy(column_attributes_default) for column_name in column_names}
    # column details containers
    return column_names, column_details


def ui_columns(table_name, all_table_details):
    # Header
    print(column_header.format(header=f"COLUMN DETAILS FOR {table_name}"))

    # Bindings
    bindings = get_key_bindings()

    def add_tables():
        get_app().exit(result="add_tables")

    def end_tables():
        get_app().exit(result="end_tables")

    # column details
    column_names, column_details = get_column_details(table_name, all_table_details)
    # column details container
    column_name_labels, column_details_labels, column_details_container = get_column_details_container(column_names,
                                                                                                       column_details)

    def generate_column_text():
        from pprint import pformat
        return pformat(column_details, width=40)

    column_text_container = Frame(
        TextArea(
            text=generate_column_text(),
            read_only=True,
            focusable=False,
        )
    )

    def update_column_text_container():
        column_text_container.text = generate_column_text()

    column_menu_container_body = TextArea(
        text='',
        multiline=True,
        focusable=False,
        read_only=True
    )

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

    column_menu_container = Frame(
        body=MenuContainer(
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
