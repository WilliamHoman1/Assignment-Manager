from textual.screen import Screen
from textual.widgets import DataTable
from services.database_service import DatabaseService


class ProblemsScreen(Screen):

    def compose(self):

        table = DataTable()
        table.add_columns("ID", "Title", "Topic", "Difficulty")

        db = DatabaseService()
        problems = db.get_problems()

        for p in problems:
            table.add_row(
                str(p["id"]),
                p["title"],
                p["topic"],
                p["difficulty"]
            )

        yield table