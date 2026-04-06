# screens/assignments_screen.py
from textual.screen import Screen
from textual.widgets import DataTable, Button, Input, Label
from services.database_service import DatabaseService
from services.assignment_service import AssignmentService


class AssignmentsScreen(Screen):

    def compose(self):
        # Table of selected problems
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

        # Input for problem set number
        yield Label("Enter Problem Set Number:")
        self.ps_input = Input(placeholder="1")
        yield self.ps_input

        # Buttons
        yield Button("Build Assignment", id="build")
        yield Button("Back", id="back")
        yield Button("Return to Menu", id="menu")

    def on_data_table_cell_selected(self, event: DataTable.CellSelected):
        # Handle removing problems
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

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "menu":
            self.app.pop_screen()  # assignments
            if len(self.app._screen_stack) > 0:
                self.app.pop_screen()  # return to menu


        elif event.button.id == "build":

            import time

            ps_number_str = self.ps_input.value.strip()

            if not ps_number_str.isdigit():
                self.notify("Please enter a valid Problem Set Number")

                return

            ps_number = int(ps_number_str)

            timestamp = int(time.time())

            service = AssignmentService()

            url = service.create_assignment(

                assignment_id=f"problem_set_lab_{ps_number}_{timestamp}",

                title=f"Problem Set Lab {ps_number}",

                problem_ids=self.app.selected_problems,

                problem_set_number=ps_number

            )

            self.notify(f"Assignment built: {url}")