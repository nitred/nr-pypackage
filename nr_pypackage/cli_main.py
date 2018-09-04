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

from . import cli_package
import sys


main_doc = """
--------------------------------------------------------------------------------
                             NR-PYPACKAGE
--------------------------------------------------------------------------------
"""


def main():
    """Entrypoint for first interaction with user. Ask user to choose type of pypackage.

    NOTE: We're using python-prompt-toolkit which is both powerful and complicated, so we try to document its use asmuch as possible.
    """
    ############################################################################
    # LIST OF APPLICATIONS
    ############################################################################
    # Here we list out all possible applications we have that will be presented
    # as radio buttons.
    package_radios = RadioList(
        values=[
            # Tuple format: ("Why is this used? This is presented to the user.")
            ("package_simple", "Simple Python App"),
            # ("package_flask", "Simple Flask App"),
            ("package_blueprints", "Flask App with Blueprints"),
        ]
    )

    ############################################################################
    # KEY BINDINGS
    ############################################################################
    # Key bindings for this applications:
    # * radio buttons use key-bindings of up and down arrows for focus. (comes inbuilt)
    # * radio buttons use key-bindings of Enter to select. (comes inbuilt)
    # * tab and shift tab bindings to shift focus from one frame to the next.
    bindings = KeyBindings()
    bindings.add(Keys.Tab)(focus_next)
    bindings.add(Keys.BackTab)(focus_previous)

    # CTRL-C to quit the prompt-app.
    @bindings.add("c-c")
    def exit_c(event):
        """Ctrl-C to quit."""
        event.app.exit(result=False)

    # End App.
    def exit_app():
        get_app().exit(True)

    ############################################################################
    # Actually application container.
    ############################################################################
    # We use VSplit to not utilize the entire width of the window.
    root_container = VSplit(
        [
            HSplit(
                [
                    Frame(
                        title="Choose which package-type do you want?",
                        body=package_radios,
                        width=80,
                    ),
                    Button("Done", handler=exit_app),
                ],
                padding=1,
            )
        ]
    )

    layout = Layout(root_container)

    app = Application(layout=layout, key_bindings=bindings, full_screen=False)

    ############################################################################
    # Actually application container.
    ############################################################################
    print(main_doc)
    result = app.run()

    if result:
        cli_package.main(package_radios.current_value)
    else:
        print("Aborted!")
        sys.exit(0)


if __name__ == "__main__":
    main()
