import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AIAssistant:
    def __init__(self, database_service):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.db = database_service
        self.conversation_history = []
        self.pending_action = None

    def _get_problems_context(self):
        """Fetch all problems from DB to give Claude full context"""
        problems = self.db.get_problems()
        return json.dumps(problems, indent=2)

    def chat(self, user_message):
        """Send a message and get a response from Claude"""
        problems_context = self._get_problems_context()

        system_prompt = (
            "You are an assistant helping a professor at Georgia Highlands College build coding assignments.\n\n"
            f"You have access to the following problem database:\n{problems_context}\n\n"
            "You can help the professor with the following actions:\n\n"
            "1. SELECT PROBLEMS: When the professor asks to build or select problems, choose appropriate ones and respond with:\n"
            "A brief explanation, then a JSON block:\n"
            "```json\n"
            "{{\n"
            '  "action": "select_problems",\n'
            '  "selected_problems": ["problem_id_1", "problem_id_2"]\n'
            "}}\n"
            "```\n\n"
            "2. REMOVE PROBLEM: When the professor asks to remove a specific problem, respond with:\n"
            "A brief explanation, then a JSON block:\n"
            "```json\n"
            "{{\n"
            '  "action": "remove_problem",\n'
            '  "problem_id": "problem_id_here"\n'
            "}}\n"
            "```\n\n"
            "3. REMOVE ALL PROBLEMS: When the professor asks to remove all problems or clear the assignment, respond with:\n"
            "A brief explanation, then a JSON block:\n"
            "```json\n"
            "{{\n"
            '  "action": "remove_all_problems"\n'
            "}}\n"
            "```\n\n"
            "4. CREATE ASSIGNMENT: When the professor asks to build or create the assignment, first ask:\n"
            "'Would you like me to build the GitLab assignment now, or would you like to review the problems first?'\n"
            "If they say build now, respond with:\n"
            "```json\n"
            "{{\n"
            '  "action": "create_assignment",\n'
            '  "build_now": true,\n'
            '  "problem_set_number": 1\n'
            "}}\n"
            "```\n"
            "If they say review first, respond with:\n"
            "```json\n"
            "{{\n"
            '  "action": "create_assignment",\n'
            '  "build_now": false\n'
            "}}\n"
            "```\n\n"
            "Only include problem IDs that exist in the database above.\n"
            "If the professor is just chatting or asking questions, respond helpfully without a JSON block."
        )

        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def extract_action(self, response_text):
        """Parse action JSON from Claude's response if present"""
        try:
            start = response_text.find("```json")
            end = response_text.find("```", start + 6)
            if start != -1 and end != -1:
                json_str = response_text[start + 7:end].strip()
                data = json.loads(json_str)
                return data
        except (json.JSONDecodeError, ValueError):
            pass
        return None

    def extract_selected_problems(self, response_text):
        """Legacy method — kept for compatibility"""
        action = self.extract_action(response_text)
        if action and action.get("action") == "select_problems":
            return action.get("selected_problems", [])
        return []

    def reset_conversation(self):
        """Clear chat history for a fresh session"""
        self.conversation_history = []
        self.pending_action = None