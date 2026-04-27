from textual.screen import Screen
from textual.widgets import TextArea, Button, Static
from textual.containers import Vertical


class FullscreenPreview(Screen):
    """Handles viewing source code, tests, and instructions
    in fullscreen."""

    def __init__(self, title: str, content: str):
        """Sets up variables and initializes."""
        super().__init__()
        self.preview_title = title
        self.preview_content = content

    CSS = """
    FullscreenPreview {
        layout: vertical;
    }

    #fs-title {
        text-style: bold;
        color: $accent;
        padding: 1 2;
    }

    #fs-content {
        height: 1fr;
    }

    #close-btn {
        margin: 1 2;
        width: auto;
    }
    """

    def compose(self):
        """Composes the screen."""
        yield Vertical(
            Static(self.preview_title, id="fs-title"),
            TextArea(self.preview_content, read_only=True, id="fs-content"),
            Button("Close", id="close-btn", variant="primary")
        )

    def on_button_pressed(self, event):
        """Handles when the user wants to exit fullscreen."""
        if event.button.id == "close-btn":
            self.app.pop_screen()