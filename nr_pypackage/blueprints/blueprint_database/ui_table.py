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


table_header = """
--------------------------------------------------------------------------------
                               TABLE CREATION
1. column_names have to contain a column named "id".
2. "collectively unique columns" should contain more than one column name.
--------------------------------------------------------------------------------
"""


def ui_table():
    print(table_header)
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

    def table_done():
        get_app().exit(result="table_done")

    ############################################################################
    # TABLE DETAILS
    ############################################################################
    table_name = TextArea(prompt='table_name                    : ', multiline=False)
    column_names = TextArea(prompt='column_names (comma separated): ', multiline=False)
    unique_columns = TextArea(prompt='collectively unique columns   : ', multiline=False)

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
                                unique_columns,
                            ]
                        ),
                    ),
                    VSplit(
                        children=[
                            Button('Done', handler=table_done, width=80),
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

    table_status = app.run()

    if not table_status:
        abort()

    return (table_status, table_name.text, column_names.text, unique_columns.text)
