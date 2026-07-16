# Assignote

Assignote is a Python desktop application for tracking assignments, tests and exams. It was designed and developed by me to help manage my academic workload more efficiently by keeping track of upcoming due dates in one place.

Instead of having to check a calendar and manually calculate how much time remains before each deadline, Assignote automatically displays the number of days remaining until each assignment, test or exam, along with the due date itself for extra validity. This provides a quick and convenient overview of upcoming academic commitments, making it easier to prioritise tasks and manage time effectively.

Note:

The scripts were designed to work both as python scripts and standalone executable applications created with PyInstaller.

## How to run

1. Run Noter.py first.
2. Add one or more deadline.
3. Close Noter when you are finished.
4. Run Assignote.py to display all saved academic tasks and their deadlines.

## How it works

Assignote consists of two Python scripts that work together:

- **Noter.py** is used to add, view and delete academic data from a terminal. This script is responsible for creating and updating the Task_data.json file.
- **Assignote.py** displays all saved tasks along with their due dates and the number of days remaining for each task in Tasks.txt, which won't exist when the script hasn't been used yet.

In short:
- **Noter** is used to record academic data.
- **Assignote** is used to display the data.

Note!

If you run "Assignote.py" before adding any data, the program will display the message, "No task data found." This simply means that no assignments have been recorded yet. Use Noter.py to add your first assignment before running Assignote.py.

## Features

- Add academic tasks, including their due dates
- View saved tasks
- Delete individual tasks
- Wipe task data from the system completely
- Sort tasks by due date, ranging from most urgent to least urgent for convenience
- Store task data using JSON
- Display tasks using .txt

## Technologies

- Python
- JSON
- txt