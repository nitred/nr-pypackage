from prompt_toolkit import prompt
from prompt_toolkit.application import Application
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import FloatContainer, VSplit
from prompt_toolkit.widgets import TextArea, Label, Frame, Box, Checkbox, Dialog, Button, RadioList, MenuContainer, MenuItem, ProgressBar
from prompt_toolkit import PromptSession

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.application.current import get_app

checkboxes = {
    text: Checkbox(text) for text in ['a', 'b', 'c', 'd']
}

a = Checkbox()


def update_slah(a):
    global slah
    slah[a] = 'yay'


bindings = KeyBindings()
bindings.add(Keys.Down)(focus_next)
bindings.add(Keys.Up)(focus_previous)


@bindings.add('c-q')
def exit_q(event):
    event.app.exit()


def do_exit():
    get_app().exit()


root_container = VSplit([
    HSplit([
        HSplit([checkbox for _, checkbox in checkboxes.items()]),  # H
        Button('Done', handler=do_exit)
    ], padding=1),  # H
])  # V


# root_container = HSplit([
#     MenuContainer(body=root_container,
#                   menu_items=[
#                       MenuItem('A'),
#                       MenuItem('B'),
#                       MenuItem('C'),
#                       MenuItem('D'),
#                       MenuItem('E'),
#                       MenuItem('Exit', handler=do_exit),
#                   ])
# ])


layout = Layout(root_container)

app = Application(layout=layout, key_bindings=bindings, full_screen=False)

result = app.run()  # You won't be able to Exit this app

for k, v in checkboxes.items():
    print(k, v.checked)
