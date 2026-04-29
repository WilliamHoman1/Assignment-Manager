from textual.screen import Screen
from textual.widgets import Button, Label, Input
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.app import ComposeResult
from textual import on

from AI_Bot.ai_assistant import AIAssistant
from services.database_service import DatabaseService


class AIScreen(Screen):
    """Sets up layout for the AI chatbot screen."""

    CSS = """
    AIScreen {
        layout: vertical;
    }

    #chat-history {
        height: 1fr;
        border: solid $primary;
        padding: 1 2;
        margin: 1;
        overflow-y: auto;
        background: $surface;
    }

    .message-user {
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
    }

    .message-ai {
        color: $text;
        margin-bottom: 1;
    }

    #input-row {
        height: auto;
        padding: 0 1;
    }

    #chat-input {
        width: 1fr;
    }

    #send-btn {
        width: auto;
        background: $accent;
    }

    #action-row {
        height: auto;
        padding: 0 1 1 1;
    }

    #build-btn {
        width: auto;
        background: $success;
        margin-right: 1;
    }

    #clear-btn {
        width: auto;
        margin-right: 1;
    }

    #back-btn {
        width: auto;
    }
    """

    def __init__(self):
        """Initializes the AI screen. Sets up AIAssistant instance with the
        database."""
        super().__init__()
        self.assistant = AIAssistant(DatabaseService())

    def compose(self) -> ComposeResult:
        """Builds the AI screen."""
        yield ScrollableContainer(id="chat-history")
        with Horizontal(id="input-row"):
            yield Input(placeholder="Describe the assignment you want...", id="chat-input")
            yield Button("Send", variant="primary", id="send-btn")
        with Horizontal(id="action-row"):
            yield Button("View Assignment", variant="success", id="build-btn", disabled=True)
            yield Button("Clear Chat", variant="default", id="clear-btn")
            yield Button("Back", variant="default", id="back-btn")

    def add_message(self, role: str, text: str):
        """Add a message to chat history"""
        history = self.query_one("#chat-history", ScrollableContainer)
        css_class = "message-user" if role == "user" else "message-ai"
        prefix = "You: " if role == "user" else "AI: "
        history.mount(Label(f"{prefix}{text}", classes=css_class))
        history.scroll_end(animate=False)

    @on(Button.Pressed, "#send-btn")
    @on(Input.Submitted, "#chat-input")
    async def handle_send(self):
        chat_input = self.query_one("#chat-input", Input)
        user_text = chat_input.value.strip()
        if not user_text:
            return

        chat_input.value = ""
        self.add_message("user", user_text)
        self.refresh()

        history = self.query_one("#chat-history", ScrollableContainer)
        thinking = Label("AI: Thinking...", classes="message-ai", id="thinking")
        history.mount(thinking)
        history.scroll_end(animate=False)

        self.run_worker(self._get_ai_response(user_text), exclusive=True)

    async def _get_ai_response(self, user_text: str):
        """AI response function"""
        response = self.assistant.chat(user_text)

        try:
            self.query_one("#thinking").remove()
        except Exception:
            pass

        self.add_message("ai", response)

        # Extract action from response
        action = self.assistant.extract_action(response)
        if not action:
            return

        action_type = action.get("action")

        # Handle select problems
        if action_type == "select_problems":
            selected = action.get("selected_problems", [])
            if selected:
                self.app.selected_problems = selected
                self.query_one("#build-btn", Button).disabled = False
                self.add_message("ai", f"✓ {len(selected)} problem(s) queued. Press 'View Assignment' to review and build.")

        # Handle remove problem
        elif action_type == "remove_problem":
            problem_id = action.get("problem_id")
            if problem_id and hasattr(self.app, "selected_problems"):
                if problem_id in self.app.selected_problems:
                    self.app.selected_problems.remove(problem_id)
                    self.add_message("ai", f"✓ Removed {problem_id} from the current assignment.")
                else:
                    self.add_message("ai", f"'{problem_id}' wasn't in the current assignment.")
            else:
                self.add_message("ai", "No problems are currently selected.")

        # Handle remove all problems
        elif action_type == "remove_all_problems":
            if hasattr(self.app, "selected_problems") and self.app.selected_problems:
                count = len(self.app.selected_problems)
                self.app.selected_problems = []
                self.query_one("#build-btn", Button).disabled = True
                self.add_message("ai", f"✓ Removed all {count} problem(s) from the assignment.")
            else:
                self.add_message("ai", "There are no problems currently selected.")

        # Handle create assignment
        elif action_type == "create_assignment":
            build_now = action.get("build_now", False)
            ps_number = action.get("problem_set_number", 1)

            if not hasattr(self.app, "selected_problems") or not self.app.selected_problems:
                self.add_message("ai", "No problems are selected yet. Please select problems first.")
                return

            if build_now:
                self.add_message("ai", "Building your GitLab assignment now...")
                self.run_worker(self._build_assignment(ps_number), exclusive=True)
            else:
                self.query_one("#build-btn", Button).disabled = False
                self.add_message("ai", "No problem! Click 'View Assignment' to review and build when ready.")
        # Handle create problem
        elif action_type == "create_problem":
            new_problem = action.get("problem")

            if not new_problem:
                self.add_message("ai", "Something went wrong — no problem data was returned.")
                return

            db = self.assistant.db

            if db.problem_exists(new_problem["id"]):
                self.add_message("ai", f"A problem with ID '{new_problem['id']}' already exists. Try asking again.")
                return

            try:
                db.add_problem(new_problem)
                if not hasattr(self.app, "selected_problems"):
                    self.app.selected_problems = []
                self.app.selected_problems.append(new_problem["id"])
                self.query_one("#build-btn", Button).disabled = False
                self.add_message("ai",
                                 f"✓ '{new_problem['title']}' generated and added to your assignment! Click 'View Assignment' to review it.")
            except Exception as e:
                self.add_message("ai", f"Error saving problem: {str(e)}")

    async def _build_assignment(self, ps_number: int):
        """Trigger GitLab build directly from chat"""
        try:
            import time
            from services.assignment_service import AssignmentService
            service = AssignmentService()
            timestamp = int(time.time())
            assignment_id = f"problem_set_lab_{ps_number}_{timestamp}"
            url = service.create_assignment(
                assignment_id=assignment_id,
                title=f"Problem Set Lab {ps_number}",
                problem_ids=self.app.selected_problems,
                problem_set_number=ps_number
            )
            self.add_message("ai", f"✓ Assignment built successfully! GitLab URL: {url}")
        except Exception as e:
            self.add_message("ai", f"Error: {str(e)}")

    @on(Button.Pressed, "#build-btn")
    def handle_build(self):
        """Trigger GitLab build directly from chat"""
        from tui.screens.assignments_screen import AssignmentsScreen
        self.app.push_screen(AssignmentsScreen())

    @on(Button.Pressed, "#clear-btn")
    def handle_clear(self):
        """Clears chat history"""
        self.assistant.reset_conversation()
        self.app.selected_problems = []
        self.query_one("#chat-history", ScrollableContainer).remove_children()
        self.query_one("#build-btn", Button).disabled = True

    @on(Button.Pressed, "#back-btn")
    def handle_back(self):
        """Back to main menu"""
        self.app.pop_screen()