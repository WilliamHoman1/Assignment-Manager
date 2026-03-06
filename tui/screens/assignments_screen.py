from textual.screen import Screen
from textual.widgets import DataTable, Button
from services.database_service import DatabaseService


class AssignmentsScreen(Screen):

    def compose(self):

        self.table = DataTable()
        self.table.add_columns("ID", "Title", "Action")

        problems = getattr(self.app, "selected_problems", [])
        db = DatabaseService()

        for pid in problems:
            problem = db.get_problem(pid)
            if problem:
                self.table.add_row(
                    problem["id"],
                    problem["title"],
                    "Remove"
                )

        yield self.table

        yield Button("Build Assignment", id="build")
        yield Button("Back", id="back")
        yield Button("Return to Menu", id="menu")

    def on_data_table_cell_selected(self, event: DataTable.CellSelected):

        # use row key (not coordinate index)
        row = self.table.get_row(event.cell_key.row_key)

        if not row:
            return

        problem_id = row[0]
        action = row[2]

        if action == "Remove":

            if problem_id in self.app.selected_problems:
                self.app.selected_problems.remove(problem_id)

            self.notify("Problem removed")

            # refresh screen
            self.app.pop_screen()
            self.app.push_screen(AssignmentsScreen())

    def on_button_pressed(self, event: Button.Pressed):

        if event.button.id == "back":
            self.app.pop_screen()

        if event.button.id == "menu":
            self.app.pop_screen()  # assignments
            if len(self.app._screen_stack) > 0:
                self.app.pop_screen()  # return to menu

        if event.button.id == "build":
            from services.assignment_service import AssignmentService

            service = AssignmentService()

            url = service.create_assignment(
                "assignment_001",
                "New Assignment",
                self.app.selected_problems
            )

            self.notify(f"Assignment built: {url}")