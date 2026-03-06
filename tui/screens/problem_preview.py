from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical
from tui.screens.assignments_screen import AssignmentsScreen

class ProblemPreview(Screen):

    def __init__(self, problem):
        super().__init__()
        self.problem = problem

    def compose(self):

        yield Vertical(
            Static(f"Title: {self.problem['title']}"),
            Static("Instructions"),
            Static(self.problem["instructions"]),
            Static("Tests"),
            Static(self.problem["unit_tests"]),
            Button("Add to Assignment", id="add"),
            Button("Back", id="back")
        )

    def on_button_pressed(self, event: Button.Pressed):

        if event.button.id == "back":
            self.app.pop_screen()

        if event.button.id == "add":

            # Store selected problem in app state
            if not hasattr(self.app, "selected_problems"):
                self.app.selected_problems = []

            self.app.selected_problems.append(self.problem["id"])

            # Provide feedback (optional)
            self.notify("Problem added to assignment")

            # Return to problem list
            self.app.push_screen(AssignmentsScreen())