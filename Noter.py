from datetime import date
import json
import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(BASE_DIR, "Task_data.json")

#Month assigning function
def assign_month(month):
    months = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6,
              'july': 7,
              'august': 8,
              'september': 9,
              'october': 10,
              'november': 11,
              'december': 12}

    month_number = 0

    for name, number in months.items():

        #Conditions for whether month name is correct (full or abbreviated)
        if (month.lower().strip() == name) or (month.lower().strip() == name[:3]):
            month_number = number
            break

    if month_number == 0:
        return month_number

    else:
        return month_number

#Save task data function (stores created data into the file)
def save_data(task_name, task_date):
    task = {'Name': task_name,
                  'Due date': f'{task_date}'}

    #Load existing assignment data
    try:
        with open(file_path, 'r') as file:
            task_data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        task_data = []

    task_data.append(task)

    with open(file_path, 'w') as file:
        json.dump(task_data, file, indent=4)

#Add data function (creates data to be stored in the file)
def add_data():
    print('\nEnter task details (Enter \'x\' at any point to cancel)\n')

    task_name = input('Enter task name: ')

    if task_name.lower().strip() == 'x':
        print()
        return

    print('Enter due date')
    task_day = input('Enter day: ')

    if task_day.lower().strip() in ('x', ''):
        print()
        return

    task_month_input = input('Enter month (full word or 3 letter abbreviation): ')

    if task_month_input.lower().strip() in ('x', ''):
        print()
        return

    else:
        #If month is entered as an integer
        if task_month_input.isdigit():
            task_month = task_month_input

        #If month is entered as a string
        else:
            task_month = assign_month(task_month_input)

            if task_month == 0:
                print('That is not a valid month')
                return

    #Current date initialising
    today = date.today()
    year = today.year

    #Condition for checking whether input data contains digits only
    if not task_day.isdigit():
        print(f'\n{task_day} is not a valid day\n')

    else:
        task_day = int(task_day)
        task_month = int(task_month)

        #Day mustn't be bigger than 31
        if task_day > 31:
            print('\nThe day of the due date is out of bounds\n')

        #Month mustn't be bigger than 12
        elif task_month > 12:
            print('\nThe month of the due date is out of bounds\n')

        else:
            try:
                due_date = date(year, task_month, task_day)

            except ValueError:
                print(f'\nThis is not a valid date (impossible)\n')

            else:
                days_left = (due_date - today).days

                if days_left == 0:
                    print('\nTask is due today\n')
                    return

                elif days_left < 0:
                    print('\nTask is overdue')
                    new_date = input('Would you like to schedule it for the next year? (y/n): ')

                    if new_date.lower().strip() == 'y':
                        year += 1

                        due_date = date(year, task_month, task_day)

                    elif new_date.lower().strip() == 'n':
                        print()
                        return

                    else:
                        print('Invalid input')
                        return

                save_data(task_name, due_date)
                print('\nTask data has been saved successfully :)\n')

#View and delete data function
def view_and_delete():
    try:
        with open(file_path, 'r') as file:
            tasks = json.load(file)

            if not tasks:
                print('\nTask data not found\n')
                return

    except (FileNotFoundError, json.JSONDecodeError):
        print('There was a problem loading the json file')
        return

    print('\nTasks:\n')

    #For every dictionary in the list
    for task in tasks:
        task_name = task.get('Name')
        task_due_date = task.get('Due date')

        #If task name or task due date is missing (broken/missing data)
        if not task_name or not task_due_date:
            if not task_name:
                print(f'\nDue date: {task_due_date} does not have a task assigned to it\n')

            elif not task_due_date:
                print(f'\nTask: {task_name} has a missing due date\n')

            continue

        print(f'{task_name} due on {task_due_date}')

    print('\n1. Delete a task'
          '\n2. Back')

    data_option = input('\nSelect an option: ')

    #Delete task
    if data_option.strip() == '1':
        task_to_delete = input('\nEnter the name of the task: ')

        if not task_to_delete:
            print('\nInvalid input')
            view_and_delete()

        else:
            task_found = False

            for index, task in enumerate(tasks):
                task_finder = task.get('Name')

                if task_finder.strip().lower() == task_to_delete.strip().lower():
                    index_of_task = index
                    tasks.pop(index_of_task)
                    task_found = True
                    
                    break

            with open(file_path, 'w') as file:
                json.dump(tasks, file, indent=4)

            print('\nTask Successfully deleted')

            if not task_found:
                print('\nTask not found')

    elif data_option.strip() == '2':
        pass

    else:
        print('\nInvalid input')
        view_and_delete()

    data_controls()

#Wipe data function
def wipe_data():
    print('\nAre you sure?\n'
          '1. Yes\n'
          '2. Cancel')

    confirm = input('Select an option: ')

    if confirm.strip() == '1':
        try:
            with open(file_path, 'w') as file:
                json.dump([], file)

        except (FileNotFoundError, json.JSONDecodeError):
            print('Error retrieving file')

        print('\nData deleted successfully')

    elif confirm.strip() == '2':
        print('\nRequest cancelled')

    else:
        print('\nInvalid input')

    data_controls()

#Data controls function
def data_controls():
    print('\n====Data Controls====\n\n'
          '1. View and Delete task\n'
          '2. Wipe Data\n'
          '3. Back\n')

    select_control = input('Select an option: ')

    if select_control.strip() == '1':
        view_and_delete()

    elif select_control.strip() == '2':
        wipe_data()

    elif select_control.strip() == '3':
        print()

    else:
        print('\nInvalid input\n')

while True:
    print('====Assignote====\n\n'
          '1. Log a task\n'
          '2. Data Controls\n'
          '3. Close Program')

    option = input('Select an option: ')

    if option.strip() == '1':
        add_data()

    elif option.strip() == '2':
        data_controls()

    elif option.strip() == '3':
        print('\nSystem shutting down. Have a good day :)')
        sys.exit()

    else:
        print('\nInvalid input\n')