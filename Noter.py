from datetime import date
import json
import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(BASE_DIR, "Task_data.json")

#Save module data function (stores created data into the file)
def save_data(module_name, module_month):
    assignment = {'Name': module_name,
                  'Due date': f'{module_month}'}

    #Load existing assignment data
    try:
        with open(file_path, 'r') as file:
            module_data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        module_data = []

    module_data.append(assignment)

    with open(file_path, 'w') as file:
        json.dump(module_data, file, indent=4)

#Add data function (creates data to be stored in the file)
def add_data():
    print('\nEnter assignment/test details (Enter \'x\' at any point to cancel)\n')

    assignment_name = input('Enter assignment/test name: ')

    if assignment_name.lower().strip() == 'x':
        print()
        return

    print('Enter due date')
    assignment_day = input('Enter day: ')

    if assignment_day.lower().strip() == 'x':
        print()
        return

    assignment_month = input('Enter month in numbers: ')

    if assignment_month.lower().strip() == 'x':
        print()
        return

    today = date.today()
    year = today.year

    #Conditions for checking whether input data contains digits only
    if not assignment_day.isdigit():
        print(f'\n{assignment_day} is not a valid day\n')

    elif not assignment_month.isdigit():
        print(f'\n{assignment_month}is not a valid month\n')

    else:
        assignment_day = int(assignment_day)
        assignment_month = int(assignment_month)

        #Day mustn't be bigger than 31
        if assignment_day > 31:
            print('\nThe day of the due date is out of bounds\n')

        #Month mustn't be bigger than 12
        elif assignment_month > 12:
            print('\nThe month of the due date is out of bounds\n')

        else:
            try:
                due_date = date(year, assignment_month, assignment_day)

            except ValueError:
                print(f'\nThis is not a valid date (impossible)\n')

            else:
                days_left = (due_date - today).days

                if days_left == 0:
                    print('\nModule is due today\n')

                elif days_left < 0:
                    print('\nModule is overdue\n')

                else:
                    save_data(assignment_name, due_date)
                    print('\nModule data has been saved successfully :)\n')

#View and delete data function
def view_and_delete():
    try:
        with open(file_path, 'r') as file:
            modules = json.load(file)

            if not modules:
                print('\nModule data not found\n')
                return

    except (FileNotFoundError, json.JSONDecodeError):
        print('There was a problem loading the json file')
        return

    print('\nModules:\n')

    #For every dictionary in the list
    for module in modules:
        module_name = module.get('Name')
        module_due_date = module.get('Due date')

        #If module name or module due date is missing (broken/missing data)
        if not module_name or not module_due_date:
            if not module_name:
                print(f'\nDue date: {module_due_date} does not have a module assigned to it\n')

            elif not module_due_date:
                print(f'\nModule: {module_name} has a missing due date\n')

            continue

        print(f'{module_name} due on {module_due_date}')

    print('\n1. Delete a module'
          '\n2. Back')

    data_option = input('\nSelect an option: ')

    if data_option.strip() == '1':
        module_to_delete = input('\nEnter the name of the module: ')

        if not module_to_delete:
            print('\nInvalid input')
            view_and_delete()

        else:
            module_exists = False

            for module in modules:
                module_finder = module.get('Name')

                if module_finder.strip().lower() == module_to_delete.strip().lower():
                    module_exists = True

            if module_exists:
                new_module_data = []

                for module in modules:
                    module_finder = module.get('Name')

                    if module_finder.strip().lower() == module_to_delete.strip().lower():
                        continue

                    new_module_data.append(module)

                with open(file_path, 'w') as file:
                    json.dump(new_module_data, file, indent=4)

                print('\nModule Successfully deleted')

            else:
                print('\nModule not found')

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
          '1. View and Delete module\n'
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
          '1. Log a module\n'
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