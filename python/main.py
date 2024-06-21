import os
import sys
from input_handler import get_data_from_files, get_data_manually
from schedule import create_schedule, check_constraints, output_schedule

def print_welcome_message():
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
    print("Welcome to the Class Scheduler Application")
    print("Created by: Archisman Chakraborti")
    print("==========================================")
    print("This application schedules classes and exams based on provided data.")
    print("\nExample Data Formats:")
    print("\nCourses (id, name, duration, required_room):")
    print("1\tMath 101\t3\tLecture Hall")
    print("2\tChem 101\t2\tLab")
    print("\nInstructors (id, name, availability, preferred_slots, courses):")
    print("1\tDr. Smith\tMon 9-11, Tue 1-3\tMon 9-11\t1")
    print("2\tDr. Johnson\tMon 10-12, Wed 2-4\tWed 2-4\t2")
    print("\nRooms (id, name, capacity, available_slots):")
    print("1\tLecture Hall A\t100\tMon 9-11, Tue 1-3")
    print("2\tLab B\t30\tMon 10-12, Wed 2-4")
    print("\nStudents (id, name, enrolled_courses):")
    print("1\tAlice\t1, 2")
    print("2\tBob\t1")

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

    # Placeholder for scheduling logic
    # schedule = create_schedule(courses, instructors, rooms, students)
    # if check_constraints(schedule):
    #     output_schedule(schedule)
    # else:
    #     print("Failed to generate a valid schedule.")

if __name__ == "__main__":
    main()
