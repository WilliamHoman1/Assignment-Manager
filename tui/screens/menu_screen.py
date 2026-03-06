from textual.screen import Screen
from textual.widgets import Button
from tui.screens.problems_screen import ProblemsScreen
from tui.screens.exit_confirm import ExitConfirm
from textual.containers import Vertical


class MenuScreen(Screen):

    def compose(self):
        yield Vertical(
            Button("View Problems", id="problems"),
            Button("Exit", id="exit"),
        )

    def on_button_pressed(self, event: Button.Pressed):

        if event.button.id == "exit":
            self.app.push_screen(ExitConfirm())

        if event.button.id == "problems":
            self.app.push_screen(ProblemsScreen())