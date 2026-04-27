from textual.app import App
from tui.screens.menu_screen import MenuScreen


class AssignmentManagerApp(App):
    """Defines root Textual Application class."""


    def on_mount(self):
        """Initializes menu screen and problems. Sets up
        initial state."""
        self.selected_problems = []
        self.push_screen(MenuScreen())