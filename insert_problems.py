import sqlite3

# Template for inserting sample problems into database, gets database set up

def insert_sample_problems(db_name='assignments.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    sample_problems = [
        ('P001', 'For Loop Basics', 'for loop', 'easy', 'python', 'instructions/P001.md', 'tests/P001_tests.py'),
        ('P002', 'While Loop Practice', 'while loop', 'medium', 'python', 'instructions/P002.md', 'tests/P002_tests.py'),
        ('P003', 'List Operations', 'lists', 'medium', 'python', 'instructions/P003.md', 'tests/P003_tests.py')
    ]

    c.executemany('INSERT OR IGNORE INTO problems VALUES (?,?,?,?,?,?,?)', sample_problems)

    conn.commit()
    conn.close()
    print("Sample problems inserted.")

if __name__ == "__main__":
    insert_sample_problems()


    # Insert problems from gitlab API, still messing around with

#import sqlite3
#import os

#def insert_problems_from_repo(
    #db_name='assignments.db',
    #base_dir='/Users/williamhoman/PycharmProjects/Project_wazevedo/cs2-problem-repo/PS_Lab1_v2_zmielko-main'
#):
  #  conn = sqlite3.connect(db_name)
   # c = conn.cursor()

 #   src_dir = os.path.join(base_dir, "src")
  #  tests_dir = os.path.join(base_dir, "tests")

  #  print(f"Looking for src: {src_dir}")

   # for filename in os.listdir(src_dir):
    #    if not filename.endswith(".py"):
      #      continue

      #  problem_id = filename.replace(".py", "")
      #  instructions_path = os.path.join(src_dir, filename)

      #  test_filename = f"test_{filename}"
       # tests_path = os.path.join(tests_dir, test_filename)
#
     #   if not os.path.exists(tests_path):
       #     tests_path = ""

       # title = problem_id.replace("_", " ").title()

      #  c.execute("""
        #    INSERT OR IGNORE INTO problems
        #    (id, title, topic, difficulty, language, instructions, unit_tests)
        #    VALUES (?, ?, ?, ?, ?, ?, ?)
       # """, (
    #        problem_id,
     #       title,
      #      "",
       #     "",
       #     "python",
       #     instructions_path,
        #    tests_path
       # ))

   # conn.commit()
   # conn.close()
   # print("Problems loaded.")

#if __name__ == "__main__":
   # insert_problems_from_repo()