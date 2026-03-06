from textual.screen import Screen
from textual.widgets import DataTable
from services.database_service import DatabaseService
from tui.screens.problem_preview import ProblemPreview


class ProblemsScreen(Screen):

    def compose(self):

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

        yield self.table

    def on_data_table_row_selected(self, event: DataTable.RowSelected):

        row = self.table.get_row(event.row_key)

        if not row:
            return

        problem_id = row[0]

        db = DatabaseService()
        problem = db.get_problem(problem_id)

        if not problem:
            return

        # open preview screen
        self.app.push_screen(ProblemPreview(problem))