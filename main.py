
# Run in terminal with python3 main.py
#
# cd ~/PycharmProjects/Project_wazevedo
# python3 main.py

from scripts.create_db import create_database
from tui.app import AssignmentManagerApp
from dotenv import load_dotenv
load_dotenv()  # loads GITLAB_TOKEN from .env

# To load in Textual web app
# cd ~/PycharmProjects/Project_wazevedo
# python3 -c "from textual_serve.server import Server; Server('python3 main.py').serve()"
if __name__ == "__main__":
    app = AssignmentManagerApp()
    app.run()