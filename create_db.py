import sqlite3

def create_database(db_name='assignments.db'):
    """Creates sqlite3 database"""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id TEXT PRIMARY KEY,
            title TEXT,
            topic TEXT,
            difficulty TEXT,
            language TEXT,
            instructions TEXT,
            unit_tests TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id TEXT PRIMARY KEY,
            title TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS assignment_problems (
            assignment_id TEXT,
            problem_id TEXT,
            FOREIGN KEY (assignment_id) REFERENCES assignments(id),
            FOREIGN KEY (problem_id) REFERENCES problems(id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created with tables.")

# Only runs when file executed directly
if __name__ == "__main__":
    create_database()