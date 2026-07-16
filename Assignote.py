import json
from datetime import date
import os
import sys

#Sort Modules in order from most urgent to least urgent
def due_date_sort(item):
    return date.fromisoformat(item['Due date'])

#Calculate due date function
def calculate_due_date(name, date_calculate):
    today = date.today()

    #Convert date_calculate string into a date data type
    due_date = date.fromisoformat(date_calculate)

    days_left = (due_date - today).days

    if days_left == 0:
        return f'{name}\nDue today (due on {due_date.strftime('%d %B %Y')})\n\n'

    elif days_left < 0:
        return f'{name}\nOverdue (due on {due_date.strftime('%d %B %Y')})\n\n'

    elif days_left == 1:
        return f'{name}\nDue tomorrow (due on {due_date.strftime('%d %B %Y')})\n\n'

    else:
        days_left = str(days_left)
        return f'{name}\nDue in {days_left} days (due on {due_date.strftime('%d %B %Y')})\n\n'

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#JSON file path
file_path = os.path.join(BASE_DIR, 'module_data.json')

#Notification building
text_file_path = os.path.join(BASE_DIR, 'modules.txt')
absolute_text_path = os.path.abspath(text_file_path)

#Load module data
try:
    with open(file_path, 'r') as file:
        modules = json.load(file)

        #module sorting
        modules.sort(key = due_date_sort)

        if not modules:
            with open(absolute_text_path, 'w') as TXT_file:
                TXT_file.write('No module data found. Use Noter to save your upcoming assignment and test data.')

                #Make sure information is written before displaying file
                TXT_file.flush()

            os.startfile(absolute_text_path)

            sys.exit()

except (FileNotFoundError, json.JSONDecodeError):
    with open(absolute_text_path, 'w') as TXT_file:
        TXT_file.write('There was a problem loading the json file. File not found/Decode error\n\nDon\'t panic, the file might not have been created yet.\n' \
        'Use Noter to save your upcoming assignment and test data.')

        #Make sure information is written before displaying file
        TXT_file.flush()

    os.startfile(absolute_text_path)

    sys.exit()

#Parse module data and build notification string
notification_string = 'Upcoming modules and tests:\n\n'

#For every dictionary in the list
for module in modules:
    module_name = module.get('Name')
    module_due_date = module.get('Due date')

    #If data is invalid/broken then skip it  
    if not module_name or not module_due_date:
        continue

    notification_string = notification_string + calculate_due_date(module_name, module_due_date)

#Write into text file
with open(text_file_path, 'w') as file:
    file.write(notification_string)

#Display notification
os.startfile(absolute_text_path)