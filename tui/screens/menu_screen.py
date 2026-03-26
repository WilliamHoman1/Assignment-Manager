from textual.screen import Screen
from textual.widgets import Button, Label
from textual.containers import Vertical
from tui.screens.problems_screen import ProblemsScreen
from tui.screens.assignments_screen import AssignmentsScreen
from tui.screens.ai_screen import AIScreen


class MenuScreen(Screen):

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

    def on_button_pressed(self, event: Button.Pressed):

        if event.button.id == "problems":
            self.app.push_screen(ProblemsScreen())

        if event.button.id == "assignments":
            self.app.push_screen(AssignmentsScreen())

        if event.button.id == "ai":
            self.app.push_screen(AIScreen())

        if event.button.id == "exit":
            self.app.exit()