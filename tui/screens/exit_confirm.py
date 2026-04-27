from textual.screen import ModalScreen
from textual.widgets import Label, Button
from textual.containers import Vertical


class ExitConfirm(ModalScreen):
    """An exit confirmation screen."""

    def compose(self):
        """Sets up the screen"""
        yield Vertical(
            Label("Are you sure you want to exit?"),
            Button("Yes", id="yes"),
            Button("No", id="no"),
        )

    def on_button_pressed(self, event):
        """Handles the event of when the user wants to exit."""

        if event.button.id == "yes":
            self.app.exit()

        else:
            self.app.pop_screen()