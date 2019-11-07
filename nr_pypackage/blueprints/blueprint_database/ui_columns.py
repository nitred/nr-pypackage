"""Main entrypoint."""
from prompt_toolkit.application import Application
from prompt_toolkit.layout.containers import VSplit, HSplit
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import (
    TextArea,
    Label,
    Frame,
    Box,
    Checkbox,
    Dialog,
    Button,
    RadioList,
    MenuContainer,
    MenuItem,
    ProgressBar,
)
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.application.current import get_app
import sys
from prompt_toolkit import prompt
from copy import deepcopy
from functools import partial
from pprint import pprint, pformat


def abort():
    print("Aborted!")
    sys.exit(0)


column_attributes = {
    "primary_key": [False, True],
    "type": [
        "Integer",
        "Float",
        "Boolean",
        "DateTime(timezone=False)",
        "DateTime(timezone=True)",
        "TIMESTAMP(timezone=False)",
        "TIMESTAMP(timezone=True)",
        "String(32)",
        "String(128)",
        "String(256)",
        "String(512)",
        "String(1024)",
        "Unicode(32)",
        "Unicode(128)",
        "Unicode(256)",
        "Unicode(512)",
        "Unicode(1024)",
        "StringText",
        "UnicodeText",
        "LargeBinary",
        "Postgres_JSON",
        "Postgres_JSONB",
    ],
    "index": [False, True],
    "unique": [False, True],
    "nullable": [False, True],
    "type_ui": ["text", "file"],
    "load_parent_on_self": ["eager", "lazy"],
    "load_self_on_parent": ["lazy", "eager"],
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
    @bindings.add("c-c")
    def exit_c(event):
        """Ctrl-C to quit."""
        event.app.exit(result=False)

    return bindings


def update_label(column_details, column_details_labels, column_name, attr_key, attr_val, focus_obj):
    # update column attr details
    column_details[column_name][attr_key] = attr_val
    # update column attr label
    label = column_details_labels[column_name][attr_key]
    label.text = f"{attr_key:20s}: {attr_val}"
    # set focus back to the menu
    get_app().layout.focus(focus_obj.menu)


def get_column_menu_container(
    table_name,
    all_table_details,
    column_details,
    column_details_labels,
    column_details_container,
    bindings,
):
    # all possible column attributes
    all_column_attributes = {}
    for attr_key, all_attr_vals in column_attributes.items():
        if attr_key == "type":
            for _table_name_, table_details in all_table_details.items():
                if _table_name_ == table_name:
                    continue

                # Add all previous `table_name.table_column` as possible attribute values for columns of this table.
                table_column_attrs = [
                    f"{_table_name_}.{_column_name}"
                    for _column_name in table_details["column_names"]
                ]

                # Update all attr_vals with `table_name.table_column` to the existing default attribute values.
                all_attr_vals += table_column_attrs

        all_column_attributes[attr_key] = all_attr_vals

    # Placeholder Container for the column update menu.
    column_menu_container_body = TextArea(text="", multiline=True, focusable=False, read_only=True)

    class Focus(object):
        def __init__(self):
            self.menu = None

    focus_obj = Focus()

    column_menu_container = Frame(
        body=MenuContainer(
            key_bindings=bindings,
            body=column_menu_container_body,
            menu_items=[
                MenuItem(
                    text="EDIT COLUMN DETAILS",
                    children=[
                        MenuItem(
                            text=column_name,
                            children=[
                                MenuItem(
                                    text=attr_key,
                                    children=[
                                        MenuItem(
                                            text=f"{attr_val}",
                                            handler=partial(
                                                update_label,
                                                column_details=column_details,
                                                column_details_labels=column_details_labels,
                                                column_name=column_name,
                                                attr_key=attr_key,
                                                attr_val=attr_val,
                                                focus_obj=focus_obj,
                                            ),
                                        )
                                        for attr_val in all_column_attributes[attr_key]
                                    ],
                                )
                                for attr_key, attr_label in column_attrs.items()
                            ],
                        )
                        for column_name, column_attrs in column_details_labels.items()
                    ],
                )
            ],
        )
    )

    focus_obj.menu = column_menu_container

    return column_details, column_menu_container_body, column_menu_container


def get_column_details_container(column_names, column_details):
    # column names labels
    column_name_labels = {column_name: Label(text=column_name) for column_name in column_names}
    # column details labels
    # column_details_labels = { 'col_name': {attr_key: Label(), ...} }
    column_details_labels = {
        column_name: {
            attr_key: Label(text=f"{attr_key:20s}: {attr_val}")
            for attr_key, attr_val in column_details[column_name].items()
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
                    Frame(
                        HSplit(
                            children=[
                                attr_val
                                for attr_key, attr_val in column_details_labels[column_name].items()
                            ]
                        )
                    ),
                ]
            )
            for column_name in column_details_labels.keys()
        ],
    )

    return column_name_labels, column_details_labels, column_details_container


def get_column_details(table_name, all_table_details):
    # list of column names
    column_names = all_table_details[table_name]["column_names"]
    # column_name to column_attribute mapping
    column_details = {
        column_name: deepcopy(column_attributes_default) for column_name in column_names
    }
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
    (
        column_name_labels,
        column_details_labels,
        column_details_container,
    ) = get_column_details_container(column_names, column_details)

    column_details, column_menu_container_body, column_menu_container = get_column_menu_container(
        table_name,
        all_table_details,
        column_details,
        column_details_labels,
        column_details_container,
        bindings,
    )

    root_container = VSplit(
        width=80,
        children=[
            HSplit(
                padding=1,
                children=[
                    column_details_container,
                    VSplit(height=10, children=[column_menu_container,]),
                    VSplit(
                        children=[
                            Button("Add More Tables", handler=add_tables, width=40),
                            Button("Done", handler=end_tables, width=40),
                        ],
                    ),
                ],
            ),
        ],
    )

    layout = Layout(root_container)

    app = Application(layout=layout, key_bindings=bindings, full_screen=False)

    app.layout.focus(column_menu_container_body)

    table_status = app.run()

    if not table_status:
        abort()

    return table_status, column_details
