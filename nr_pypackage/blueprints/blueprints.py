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

from .blueprint_auth import handle_auth
from .blueprint_database import handle_database

blueprint_handlers = {
    'auth': handle_auth,
    'database': handle_database,
}


blueprints_doc = """
--------------------------------------------------------------------------------
                          NR-PYPACKAGE-BLUEPRINTS
--------------------------------------------------------------------------------
"""


def handle_blueprints():
    """Entrypoint for first interaction with user. Ask user to choose type of pypackage.

    NOTE: We're using python-prompt-toolkit which is both powerful and complicated, so we try to document its use asmuch as possible.
    """
    ############################################################################
    # LIST OF BLUEPRINTS
    ############################################################################
    # Here we list out all possible blueprints we have that will be presented
    # as checkboxes.
    blueprint_order = ['auth', 'database']
    blueprints = {
        'auth': Checkbox(text='Authentication against LDAP'),
        'database': Checkbox(text='Database'),
    }
    blueprint_checkboxes = []
    for bp in blueprint_order:
        blueprints[bp].checked = False
        blueprint_checkboxes.append(blueprints[bp])

    ############################################################################
    # KEY BINDINGS
    ############################################################################
    # Key bindings for this applications:
    # * radio buttons use inbuilt key-bindings of up and down arrows for focus and enter for selection.
    # * tab and shift tab bindings to shift focus from one frame to the next.
    bindings = KeyBindings()
    bindings.add(Keys.Down)(focus_next)
    bindings.add(Keys.Tab)(focus_next)
    bindings.add(Keys.Up)(focus_previous)
    bindings.add(Keys.BackTab)(focus_previous)

    # CTRL-C to quit the prompt-app.
    @bindings.add('c-c')
    def exit_c(event):
        """Ctrl-C to quit."""
        event.app.exit(result=False)

    # End App.
    def exit_app():
        get_app().exit(result=True)

    ############################################################################
    # Actually application container.
    ############################################################################
    # We use VSplit to not utilize the entire width of the window.
    root_container = VSplit([
        HSplit([Frame(title='Choose which blueprints do you want?',
                      body=HSplit(children=blueprint_checkboxes),
                      width=80),
                Button('Done',
                       handler=exit_app)],
               padding=1),
    ])

    layout = Layout(root_container)

    app = Application(layout=layout,
                      key_bindings=bindings,
                      full_screen=False)

    ############################################################################
    # Actually application container.
    ############################################################################
    # print(blueprints_doc)
    result = app.run()

    if result:
        blueprint_options = {}
        for blueprint_name, blueprint_checkbox in blueprints.items():
            if blueprint_checkbox.checked:
                blueprint_handler = blueprint_handlers[blueprint_name]
                blueprint_options[blueprint_name] = blueprint_handler(include=True)
            else:
                blueprint_options[blueprint_name] = {'include': False}

        return blueprint_options
    else:
        print("Aborted!")
        sys.exit(0)

    return blueprint_options


if __name__ == "__main__":
    handle_blueprints()
