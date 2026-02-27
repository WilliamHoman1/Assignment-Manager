import sqlite3

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