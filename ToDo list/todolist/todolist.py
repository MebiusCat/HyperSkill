from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

# initialising the parent class for a table
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'{self.task}'


class ToDoList:
    menu_list = "1) Today's tasks\n2) Week's tasks\n3) All tasks\n" \
                "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n"

    def __init__(self):
        """
        initialising the database and gui
        """
        # table and database initialising
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)

        # Session and interaction with database initialising
        self.session = sessionmaker(bind=self.engine)()

        # menu
        self.menu = {'1': self.show_today_tasks, '2': self.show_week_tasks,
                     '3': self.all_tasks, '4': self.show_missed_tasks,
                     '5': self.add_task, '6': self.delete_task,
                     '0': self.exit}

    def __repr__(self):
        pass

    def show_today_tasks(self):
        today = datetime.today()
        tasks = self.session.query(Task)\
                    .filter(Task.deadline == today.date()).all()
        print(f"Today {today.strftime('%d %b')}:")
        if tasks:
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task}")
            print()
        else:
            print("Nothing to do!\n")

    def show_week_tasks(self):
        today = datetime.today()

        for _ in range(7):
            tasks = self.session.query(Task)\
                                .filter(Task.deadline == today.date()).all()
            print(f"{today.strftime('%A %d %b')}")
            if tasks:
                for i, task in enumerate(tasks):
                    print(f"{i+1}. {task}")
                print()
            else:
                print("Nothing to do!\n")

            today += timedelta(days=1)

    def all_tasks(self):
        tasks = self.session.query(Task).order_by(Task.deadline).all()
        if tasks:
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task}. {task.deadline.strftime('%d %b')}")
            print()
        else:
            print("Nothing to do!\n")

    def show_missed_tasks(self):
        today = datetime.today()
        tasks = self.session.query(Task)\
                    .filter(Task.deadline < today.date())\
                    .order_by(Task.deadline).all()
        print("Missed tasks:")
        if tasks:
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task}. {task.deadline.strftime('%d %b')}")
        else:
            print("Nothing is missed!")
        print()

    def add_task(self):
        text = input("Enter task\n")
        deadline_text = input("Enter deadline\n")
        deadline = datetime.strptime(deadline_text, '%Y-%m-%d')
        self.session.add(Task(task=text, deadline=deadline))
        self.session.commit()
        print("The task has been added!\n")

    def delete_task(self):
        tasks = self.session.query(Task)\
                    .order_by(Task.deadline).all()
        print("Choose the number of the task you want to delete:")
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task}. {task.deadline.strftime('%d %b')}")
        task_id = int(input())
        self.session.delete(tasks[task_id-1])
        self.session.commit()
        print("The task has been deleted!")

    def exit(self):
        print('Bye!')
        exit()

    def main(self):
        while True:
            choice: str = input(self.menu_list)
            print()
            self.menu.get(choice, lambda: print('Unknown option.'))()


ToDoList().main()
