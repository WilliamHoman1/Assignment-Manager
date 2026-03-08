from scripts.create_db import create_database
#from scripts.insert_problems import insert_sample_problems
#from services.assignment_service import create_assignment
#from services.database_service import export_assignment

# Creates database w sample problems

#def main():
   # create_database()
   # insert_sample_problems()
  #  create_assignment('A001', 'Week 1 Lab', ['for loop', 'while loop'])
  #  export_assignment('A001')


#if __name__ == "__main__":
    #main()
# Run in terminal with python3 main.py
# cd ~/PycharmProjects/Project_wazevedo
# python3 main.py

from scripts.create_db import create_database
from tui.app import AssignmentManagerApp
from dotenv import load_dotenv
load_dotenv()  # loads GITLAB_TOKEN from .env

if __name__ == "__main__":
    app = AssignmentManagerApp()
    app.run()