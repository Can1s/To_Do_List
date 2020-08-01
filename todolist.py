from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')  # Create file of DB
Base = declarative_base()


# Create class Table
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# Create table in DB
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_today_tasks():
    tasks = session.query(Table).all()  # a list of tasks
    print("Today:")
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        for i in range(len(tasks)):
            print(f"{i + 1}. {tasks[i].task}")
    print()


def add_task():
    print("Enter task")
    new_task = input()
    new_row = Table(task=new_task)
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()


def print_menu():
    print("""1) Today's tasks
2) Add task
0) Exit""")


def main():
    while True:
        print_menu()
        action = int(input())
        if action == 1:
            print_today_tasks()
        elif action == 2:
            add_task()
        elif action == 0:
            print()
            print("Bye!")
            exit()
            break


main()
