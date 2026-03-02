from create_db import create_database
from insert_problems import insert_sample_problems
from build_assignment import create_assignment
from export_assignment import export_assignment

#Creates database w sample problems

def main():
    create_database()
    insert_sample_problems()
    create_assignment('A001', 'Week 1 Lab', ['for loop', 'while loop'])
    export_assignment('A001')


if __name__ == "__main__":
    main()