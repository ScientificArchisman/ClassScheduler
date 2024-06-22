import os
import sys
from input_handler import get_data_from_files, get_data_manually
from schedule import create_schedule, check_constraints, output_schedule

def get_shared_lib_path():
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        base_path = sys._MEIPASS
    else:
        # Running in a normal Python environment
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, 'class_scheduler.so')


class TextColors:
    HEADER = '\033[96m'
    OKBLUE = '\033[90m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_welcome_message():
    print(f"{TextColors.HEADER}{TextColors.BOLD}")
    print("""
  ▄████ ▓█████ ███▄    █▓█████▄▄▄█████▓ ██▓ ▄████▄       ██████ ▄████▄   ██░ ██ ▓█████ ▓█████▄  █    ██  ██▓    ▓█████  ██▀███  
 ██▒ ▀█▒▓█   ▀ ██ ▀█   █▓█   ▀▓  ██▒ ▓▒▓██▒▒██▀ ▀█     ▒██    ▒▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ██▌ ██  ▓██▒▓██▒    ▓█   ▀ ▓██ ▒ ██▒
▒██░▄▄▄░▒███  ▓██  ▀█ ██▒███  ▒ ▓██░ ▒░▒██▒▒▓█    ▄    ░ ▓██▄  ▒▓█    ▄ ▒██▀▀██░▒███   ░██   █▌▓██  ▒██░▒██░    ▒███   ▓██ ░▄█ ▒
░▓█  ██▓▒▓█  ▄▓██▒  ▐▌██▒▓█  ▄░ ▓██▓ ░ ░██░▒▓▓▄ ▄██▒     ▒   ██▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ░▓█▄   ▌▓▓█  ░██░▒██░    ▒▓█  ▄ ▒██▀▀█▄  
░▒▓███▀▒░▒████▒██░   ▓██░▒████▒ ▒██▒ ░ ░██░▒ ▓███▀ ░   ▒██████▒▒ ▓███▀ ░░▓█▒░██▓░▒████▒░▒████▓ ▒▒█████▓ ░██████▒░▒████▒░██▓ ▒██▒
 ░▒   ▒ ░░ ▒░ ░ ▒░   ▒ ▒░░ ▒░ ░ ▒ ░░   ░▓  ░ ░▒ ▒  ░   ▒ ▒▓▒ ▒ ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░ ▒▒▓  ▒ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░░░ ▒░ ░░ ▒▓ ░▒▓░
  ░   ░  ░ ░  ░ ░░   ░ ▒░░ ░  ░   ░     ▒ ░  ░  ▒      ░ ░▒  ░ ░ ░  ▒    ▒ ░▒░ ░ ░ ░  ░ ░ ▒  ▒ ░░▒░ ░ ░ ░ ░ ▒  ░ ░ ░  ░  ░▒ ░ ▒░
░ ░   ░    ░     ░   ░ ░   ░    ░       ▒ ░░           ░  ░  ░ ░         ░  ░░ ░   ░    ░ ░  ░  ░░░ ░ ░   ░ ░      ░     ░░   ░ 
      ░    ░  ░        ░   ░  ░         ░  ░ ░               ░ ░ ░       ░  ░  ░   ░  ░   ░       ░         ░  ░   ░  ░   ░     
                                           ░                   ░                        ░                                       

""")                                                                          
    print(f"{TextColors.ENDC}")
    print(f"{TextColors.OKGREEN}Welcome to the Class Scheduler Application{TextColors.ENDC}")
    print(f"{TextColors.OKBLUE}Created by: Archisman Chakraborti{TextColors.ENDC}")
    print(f"{TextColors.BOLD}{TextColors.UNDERLINE}=========================================={TextColors.ENDC}")
    print("This application schedules classes and exams based on provided data.")
    print("\nExample Data Formats:")
    print("\nCourses (id, name, duration, required_room):")
    print(f"{TextColors.OKCYAN}1\tMath 101\t3\tLecture Hall{TextColors.ENDC}")
    print(f"{TextColors.OKCYAN}2\tChem 101\t2\tLab{TextColors.ENDC}")
    print("\nInstructors (id, name, availability, preferred_slots, courses):")
    print(f"{TextColors.OKCYAN}1\tDr. Smith\tMon 9-11, Tue 1-3\tMon 9-11\t1{TextColors.ENDC}")
    print(f"{TextColors.OKCYAN}2\tDr. Johnson\tMon 10-12, Wed 2-4\tWed 2-4\t2{TextColors.ENDC}")
    print("\nRooms (id, name, capacity, available_slots):")
    print(f"{TextColors.OKCYAN}1\tLecture Hall A\t100\tMon 9-11, Tue 1-3{TextColors.ENDC}")
    print(f"{TextColors.OKCYAN}2\tLab B\t30\tMon 10-12, Wed 2-4{TextColors.ENDC}")
    print("\nStudents (id, name, enrolled_courses):")
    print(f"{TextColors.OKCYAN}1\tAlice\t1, 2{TextColors.ENDC}")
    print(f"{TextColors.OKCYAN}2\tBob\t1{TextColors.ENDC}")

def display_constraints():
    constraints_file = os.path.join(os.path.dirname(__file__), '../constraints.md')
    with open(constraints_file, 'r') as file:
        constraints = file.read()
    print(constraints)

def main_menu():
    print("\nPlease select an option:")
    print("1. Enter data paths")
    print("2. Enter data manually")
    print("3. View constraints")
    print("0. Exit")
    choice = input("Enter your choice: ")
    return choice

def main():
    print_welcome_message()

    while True:
        choice = main_menu()
        if choice == '1':
            courses, instructors, rooms, students = get_data_from_files()
            break
        elif choice == '2':
            courses, instructors, rooms, students = get_data_manually()
            break
        elif choice == '3':
            display_constraints()
        elif choice == '0':
            print("Exiting the application.")
            sys.exit()
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 0.")

    # Print the data
    print("\nCourses:")
    for course in courses:
        print(course)

    print("\nInstructors:")
    for instructor in instructors:
        print(instructor)

    print("\nRooms:")
    for room in rooms:
        print(room)

    print("\nStudents:")
    for student in students:
        print(student)

if __name__ == "__main__":
    main()