from textual.screen import Screen
from textual.widgets import Button
from textual.containers import Vertical
from tui.screens.problems_screen import ProblemsScreen
from tui.screens.assignments_screen import AssignmentsScreen


class MenuScreen(Screen):

    def compose(self):
        yield Vertical(
            Button("View Problems", id="problems"),
            Button("View Assignments", id="assignments"),
            Button("Exit", id="exit"),
        )

    def on_button_pressed(self, event: Button.Pressed):

        if event.button.id == "problems":
            self.app.push_screen(ProblemsScreen())

        if event.button.id == "assignments":
            self.app.push_screen(AssignmentsScreen())

        if event.button.id == "exit":
            self.app.exit()