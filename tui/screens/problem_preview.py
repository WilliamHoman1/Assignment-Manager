from textual.screen import Screen
from textual.widgets import Static, Button, TextArea
from textual.containers import Vertical, Horizontal, ScrollableContainer
from tui.screens.assignments_screen import AssignmentsScreen
from tui.screens.fullscreen_preview import FullscreenPreview


class ProblemPreview(Screen):

    def __init__(self, problem):
        super().__init__()
        self.problem = problem

    def compose(self):
        yield ScrollableContainer(
            Vertical(

                # Title
                Static(f"Problem Preview: {self.problem['title']}", classes="title"),

                # Instructions section
                Static("Instructions", classes="section-header"),
                TextArea(
                    self.problem["instructions"],
                    read_only=True,
                    id="instructions_box"
                ),
                Button("View Fullscreen", id="fs-instructions", variant="default"),

                # Code section
                Static("Code", classes="section-header"),
                TextArea(
                    self.problem["src_code"] or "No code available",
                    read_only=True,
                    id="code_box"
                ),
                Button("View Fullscreen", id="fs-code", variant="default"),

                # Unit Tests section
                Static("Unit Tests", classes="section-header"),
                TextArea(
                    self.problem["unit_tests"],
                    read_only=True,
                    id="tests_box"
                ),
                Button("View Fullscreen", id="fs-tests", variant="default"),

                # Buttons row
                Horizontal(
                    Button("Add to Assignment", id="add", variant="success"),
                    Button("Back", id="back", variant="primary"),
                    classes="button-row"
                )
            )
        )

    def on_button_pressed(self, event: Button.Pressed):

        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "add":
            if not hasattr(self.app, "selected_problems"):
                self.app.selected_problems = []
            self.app.selected_problems.append(self.problem["id"])
            self.notify("Problem added to assignment")
            self.app.push_screen(AssignmentsScreen())

        elif event.button.id == "fs-instructions":
            self.app.push_screen(FullscreenPreview("Instructions", self.problem["instructions"]))

        elif event.button.id == "fs-code":
            self.app.push_screen(FullscreenPreview("Code", self.problem["src_code"] or "No code available"))

        elif event.button.id == "fs-tests":
            self.app.push_screen(FullscreenPreview("Unit Tests", self.problem["unit_tests"]))