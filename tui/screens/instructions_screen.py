from textual.screen import Screen
from textual.widgets import Button, Label, Markdown
from textual.containers import Vertical, ScrollableContainer

INSTRUCTIONS_MD = """\
# Code Assignment Builder — Help

## What this program does
Automates the creation and distribution of coding assignments for CS courses
at Georgia Highlands College. Problems are pulled from GitLab repositories
and organized into assignments for students.

## Workflow
1. **View Problems** — Browse all available problems synced from GitLab.
   Select one to preview its description and starter code.
2. **View Assignments** — See all assignments, their components, and which
   problem sets are attached.
3. **AI Assignment Builder** — Use the AI assistant to generate new problems or
assignments quick.

## Keyboard shortcuts
| Key | Action |
|-----|--------|
| `?` or `F1` | Open this help screen |
| `Escape` | Go back / close current screen |
| `Enter` | Select / confirm |
| `Q` | Quit from menu |

## Navigation tips
- Use arrow keys to move through lists.
- Press **Escape** from any screen to return to the previous one.
- The AI assistant can answer questions about any problem in plain English.
"""

class InstructionsScreen(Screen):
    """Instructions screen for user accessibility and navigation through the program. Provides
    answers if a user gets stuck."""

    CSS = """
    InstructionsScreen {
        background: $background;
        align: center middle;
    }

    #container {
        width: 70;
        height: 85vh;
        border: solid $accent;
        padding: 1 2;
    }

    #heading {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
        width: 100%;
    }

    #scroll {
        height: 1fr;
    }

    #close {
        width: 100%;
        margin-top: 1;
    }
    """

    def compose(self):
        yield Vertical(
            Label("❓  Help & Instructions", id="heading"),
            ScrollableContainer(
                Markdown(INSTRUCTIONS_MD),
                id="scroll"
            ),
            Button("Close  [Esc]", id="close"),
            id="container"
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "close":
            self.app.pop_screen()

    def on_key(self, event):
        if event.key == "escape":
            self.app.pop_screen()