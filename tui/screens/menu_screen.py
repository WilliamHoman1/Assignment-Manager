from textual.screen import Screen
from textual.widgets import Button, Label, Footer
from textual.containers import Vertical
from textual.binding import Binding
from tui.screens.problems_screen import ProblemsScreen
from tui.screens.assignments_screen import AssignmentsScreen
from tui.screens.ai_screen import AIScreen
from tui.screens.instructions_screen import InstructionsScreen


class MenuScreen(Screen):
    """This is the main menu screen for my program. This is what pops up as soon as the user loads in.
    Multiple pathways are shown here like view problems and build assignments. Essentially,
    the starting GUI of my program."""

    BINDINGS = [
        Binding("question_mark,f1", "show_help", "Help"),
        Binding("q", "request_quit", "Quit"),
    ]

    CSS = """
    MenuScreen {
        background: $background;
        align: center middle;
    }

    #container {
        width: 60;
        height: auto;
        align: center middle;
    }

    #title {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin-bottom: 0;
        width: 100%;
    }

    #subtitle-heading {
        text-align: center;
        color: $primary;
        text-style: bold;
        margin-bottom: 1;
        width: 100%;
    }

    #subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
        width: 100%;
    }

    #divider {
        margin-bottom: 2;
        width: 100%;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
    }

    #problems {
        background: $accent;
    }

    #assignments {
        background: $primary;
    }

    #ai {
        background: $success;
    }

    #exit {
        background: $error;
    }
    """

    def compose(self):
        """Sets the buttons for the program as well as descriptors."""
        yield Vertical(
            Label("🎓 Georgia Highlands College", id="title"),
            Label("Code Assignment Builder", id="subtitle-heading"),
            Label(
                "This program automates the process of manually creating coding assignments for students across computer science courses!",
                id="subtitle"
            ),
            Label("─" * 50, id="divider"),
            Button("📋  View Problems", id="problems"),
            Button("📁  View Assignments", id="assignments"),
            Button("🤖  AI Assignment Builder", id="ai"),
            Button("🚪  Exit", id="exit"),
            id="container"
        )
        yield Footer()

    def action_show_help(self):
        """Calls on instructions_screen to show the help screen."""
        self.app.push_screen(InstructionsScreen())

    def action_request_quit(self):
        """Calls to exit the program."""
        self.app.exit()

    def on_button_pressed(self, event: Button.Pressed):
        """Actions for when a button is pressed by user."""
        if event.button.id == "problems":
            self.app.push_screen(ProblemsScreen())
        elif event.button.id == "assignments":
            self.app.push_screen(AssignmentsScreen())
        elif event.button.id == "ai":
            self.app.push_screen(AIScreen())
        elif event.button.id == "exit":
            self.app.exit()