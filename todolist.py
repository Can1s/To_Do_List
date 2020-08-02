from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
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
    today = datetime.today()
    tasks = session.query(Table).filter(Table.deadline == today.date()).all()  # a list of tasks
    print(f"Today {today.strftime('%d %b')}:")
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        for i in range(len(tasks)):
            print(f"{i + 1}. {tasks[i].task}")
    print()


def print_weeks_tasks():
    for i in range(7):
        date = datetime.today().date() + timedelta(days=i)
        tasks = session.query(Table).filter(Table.deadline == date).all()
        print(f"{date.strftime('%A %d %b')}:")
        if len(tasks) == 0:
            print("Nothing to do!")
        else:
            for j in range(len(tasks)):
                print(f"{j + 1}. {tasks[j].task}")
        print()


def print_all_tasks():
    print("All tasks:")
    tasks = session.query(Table.task, Table.deadline).order_by(Table.deadline).all()
    for i in range(len(tasks)):
        print(f"{i + 1}. {tasks[i][0]}. {tasks[i][1].strftime('%#d %b')}")
    print()


def print_missed_tasks():
    today = datetime.today()
    missed_tasks = session.query(Table.task, Table.deadline).filter(Table.deadline < today.date()).all()
    print("Missed tasks:")
    if len(missed_tasks) == 0:
        print("Nothing is missed!")
    else:
        for i in range(len(missed_tasks)):
            print(f"{i + 1}. {missed_tasks[i][0]}. {missed_tasks[i][1].strftime('%#d %b')}")
    print()


def add_task():
    print("Enter task")
    new_task = input()
    print("Enter deadline")
    year, month, day = input().split("-")
    new_deadline = datetime(int(year), int(month), int(day))
    new_row = Table(task=new_task, deadline=new_deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()


def delete_task():
    delete_tasks = session.query(Table.id, Table.task, Table.deadline).order_by(Table.deadline).all()
    print("Choose the number of the task you want to delete:")
    for i in range(len(delete_tasks)):
        print(f"{i + 1}. {delete_tasks[i][1]}. {delete_tasks[i][2].strftime('%#d %b')}")
    del_number = int(input()) - 1
    del_row = delete_tasks[del_number]
    session.query(Table).filter(Table.id == del_row[0]).delete()
    session.commit()
    print("The task has been deleted!")
    print()


def print_menu():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")


def main():
    while True:
        print_menu()
        action = int(input())
        if action == 1:
            print_today_tasks()
        elif action == 2:
            print_weeks_tasks()
        elif action == 3:
            print_all_tasks()
        elif action == 4:
            print_missed_tasks()
        elif action == 5:
            add_task()
        elif action == 6:
            delete_task()
        elif action == 0:
            print()
            print("Bye!")
            exit()
            break


main()
