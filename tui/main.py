from textual.app import App
from textual.widgets import Header, Footer, DataTable
import sqlite3
import os

# Use same DB path as old_flask_app.py
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#DB_PATH = os.path.join(BASE_DIR, "assignments.db")


#def get_problems():
   # """Query problems from the shared database"""
   # conn = sqlite3.connect(DB_PATH)
   # cursor = conn.execute("SELECT id, problem, status FROM assignments")
   # conn.close()
   # return rows


#class AssignmentApp(App):

 #   def compose(self):
      #  yield Header()
      #  self.table = DataTable()
     #   yield self.table
     #   yield Footer()

   # def on_mount(self):
       # self.table.add_columns("ID", "Problem", "Status")

       # for row in get_problems():
       #     self.table.add_row(row[0], row[1], row[2])



#if __name__ == "__main__":
   #AssignmentApp().run()

