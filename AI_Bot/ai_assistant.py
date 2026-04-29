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
        problems = self.db.get_problems()
        return json.dumps(problems, indent=2)

    def chat(self, user_message):
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
            "2. REMOVE PROBLEM: When asked to remove a specific problem:\n"
            "```json\n"
            "{{\n"
            '  "action": "remove_problem",\n'
            '  "problem_id": "problem_id_here"\n'
            "}}\n"
            "```\n\n"
            "3. REMOVE ALL PROBLEMS: When asked to clear the assignment:\n"
            "```json\n"
            "{{\n"
            '  "action": "remove_all_problems"\n'
            "}}\n"
            "```\n\n"
            "4. CREATE ASSIGNMENT: When asked to build/create the assignment:\n"
            "```json\n"
            "{{\n"
            '  "action": "create_assignment",\n'
            '  "build_now": true,\n'
            '  "problem_set_number": 1\n'
            "}}\n"
            "```\n\n"
            "5. GENERATE NEW PROBLEM: When the professor uses any of the following phrases or similar intent: "
            "'create a problem', 'generate a problem', 'make a new problem', 'create a new problem', "
            "'generate a new problem', 'make a problem', 'new problem', 'add a new problem to the database', "
            "or any request asking you to invent or create an original coding problem from scratch, respond with:\n"
            "```json\n"
            "{{\n"
            '  "action": "create_problem",\n'
            '  "problem": {{\n'
            '    "id": "unique_snake_case_id",\n'
            '    "title": "Problem Title",\n'
            '    "difficulty": "easy|medium|hard",\n'
            '    "topic": "e.g. loops, functions, recursion",\n'
            '    "language": "python",\n'
            '    "supplemental_files": null,\n'
            '    "use_test_files_package": 0,\n'
            '    "instructions": "## Problem N - Title - Xpts\\n- **Attributes:** [Unit Test(s) Provided] - [AI - Research Only]\\n- **Provided File:** `src/problem_placeholder.py`\\n- **Provided Tests:** `tests/test_problem_placeholder.py`\\n\\nProblem description here...\\n\\n### Point Breakdown\\n1. [Xpts] Requirement one.\\n2. [Xpts] Requirement two.",\n'
            '    "src_code": "def function_name(param):\\n    \\"\\"\\"\\n    Docstring describing the function.\\n    :param param: description\\n    :return: description\\n    \\"\\"\\"\\n    # Your code here\\n    pass\\n\\n\\nif __name__ == \\"__main__\\":\\n    print(function_name(example))",\n'
            '    "unit_tests": "import problem_placeholder\\nimport pytest\\n\\n\\nclass TestProblemPlaceholder:\\n    def test_case_one(self):\\n        assert problem_placeholder.function_name(arg) == expected\\n\\n    def test_case_two(self):\\n        assert problem_placeholder.function_name(arg2) == expected2\\n"\n'
            "  }}\n"
            "}}\n"
            "```\n\n"
            "CRITICAL RULES for generate problem:\n"
            "- Use EXACTLY these key names: id, title, difficulty, topic, language, supplemental_files, use_test_files_package, instructions, src_code, unit_tests\n"
            "- Do NOT use: description, starter_code, test_cases, solution\n"
            "- instructions must be a markdown string, NOT a file path\n"
            "- src_code must be a full Python file with a docstring and if __name__ == '__main__' block\n"
            "- unit_tests must be a complete pytest file using 'import problem_placeholder' — NOT a list of test cases\n"
            "- The system will automatically rename problem_placeholder to the correct problem number at build time\n"
            "When you generate a new problem, do NOT ask the professor to add it to the assignment separately. "
            "Always output ONLY the create_problem JSON block. The system will automatically save it and add it "
            "to the assignment. Never follow a create_problem response with a select_problems block.\n"
        )






        self.conversation_history.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def extract_action(self, response_text):
        try:
            last_start = response_text.rfind("```json")  # rfind = last occurrence
            if last_start == -1:
                return None
            end = response_text.find("```", last_start + 6)
            if end == -1:
                return None
            json_str = response_text[last_start + 7:end].strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass
        return None

    def extract_selected_problems(self, response_text):
        action = self.extract_action(response_text)
        if action and action.get("action") == "select_problems":
            return action.get("selected_problems", [])
        return []

    def reset_conversation(self):
        self.conversation_history = []
        self.pending_action = None