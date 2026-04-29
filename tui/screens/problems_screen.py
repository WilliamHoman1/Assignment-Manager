from textual.screen import Screen
from textual.widgets import DataTable, Button
from textual.containers import Vertical, Horizontal
from services.database_service import DatabaseService
from tui.screens.problem_preview import ProblemPreview


class ProblemsScreen(Screen):
    """Handles the 'view problems' screen."""

    def compose(self):
        """Creates the table and shows available problems."""
        self.table = DataTable()
        self.table.cursor_type = "row"
        self.table.add_columns("ID", "Title", "Topic", "Difficulty")

        db = DatabaseService()
        problems = db.get_problems()

        for p in problems:
            self.table.add_row(
                str(p["id"]),
                p["title"],
                p["topic"],
                p["difficulty"]
            )

        self.highlighted_problem_id = None

        yield self.table
        with Horizontal():
            yield Button("Add to Assignment", id="add", variant="success", disabled=True)
            yield Button("Remove Problem", id="remove", variant="error", disabled=True)
            yield Button("Back", id="back")

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted):
        row = self.table.get_row(event.row_key)
        if row:
            self.highlighted_problem_id = row[0]
            self.query_one("#remove", Button).disabled = False
            self.query_one("#add", Button).disabled = False

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        """Handles when user selects a row — opens preview."""
        row = self.table.get_row(event.row_key)
        if not row:
            return

        problem_id = row[0]
        db = DatabaseService()
        problem = db.get_problem(problem_id)
        if not problem:
            return

        self.app.push_screen(ProblemPreview(problem))

    def on_button_pressed(self, event: Button.Pressed):
        """Handles button presses."""
        if event.button.id == "back":
            self.app.pop_screen()


        elif event.button.id == "add":

            if self.highlighted_problem_id:

                if not hasattr(self.app, "selected_problems"):
                    self.app.selected_problems = []

                if self.highlighted_problem_id not in self.app.selected_problems:

                    self.app.selected_problems.append(self.highlighted_problem_id)

                    self.notify(f"Added {self.highlighted_problem_id} to assignment")

                else:

                    self.notify("Problem already in assignment")

                from tui.screens.assignments_screen import AssignmentsScreen

                self.app.push_screen(AssignmentsScreen())
                
        elif event.button.id == "remove":
            if self.highlighted_problem_id:
                db = DatabaseService()
                db.delete_problem(self.highlighted_problem_id)
                self.notify(f"Removed {self.highlighted_problem_id}")
                # Refresh screen
                self.app.pop_screen()
                self.app.push_screen(ProblemsScreen())