from textual.app import App
from tui.screens.menu_screen import MenuScreen


class AssignmentManagerApp(App):


    def on_mount(self):
        self.selected_problems = []
        self.push_screen(MenuScreen())