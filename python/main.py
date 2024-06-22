import os
import sys
from input_handler import get_data_from_files, get_data_manually
from data_structures import Course, Instructor, Room, Student
from chromosome_generator import generate_chromosome, chromosome_to_json, Gene

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

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
 ██████╗ ███████╗███╗   ██╗███████╗████████╗██╗ ██████╗    ███████╗ ██████╗██╗  ██╗███████╗██████╗ ██╗   ██╗██╗     ███████╗██████╗ 
██╔════╝ ██╔════╝████╗  ██║██╔════╝╚══██╔══╝██║██╔════╝    ██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔════╝██╔══██╗
██║  ███╗█████╗  ██╔██╗ ██║█████╗     ██║   ██║██║         ███████╗██║     ███████║█████╗  ██║  ██║██║   ██║██║     █████╗  ██████╔╝
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝     ██║   ██║██║         ╚════██║██║     ██╔══██║██╔══╝  ██║  ██║██║   ██║██║     ██╔══╝  ██╔══██╗
╚██████╔╝███████╗██║ ╚████║███████╗   ██║   ██║╚██████╗    ███████║╚██████╗██║  ██║███████╗██████╔╝╚██████╔╝███████╗███████╗██║  ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
                                                                                                                                    
""")
    print(f"{TextColors.ENDC}")
    print(f"{TextColors.OKGREEN}Welcome to the Class Scheduler Application{TextColors.ENDC}")
    print(f"{TextColors.OKBLUE}Created by: Archisman Chakraborti{TextColors.ENDC}")
    print(f"{TextColors.BOLD}{TextColors.UNDERLINE}=========================================={TextColors.ENDC}")
    print("This application schedules classes and exams based on provided data.")
    print("\nExample Data Formats:")
    print("\nCourses (id, name, duration, required_room, enrolled_students):")
    print(f"{TextColors.OKCYAN}1\tMath 101\t3\tLecture Hall\t30{TextColors.ENDC}")
    print(f"{TextColors.OKCYAN}2\tChem 101\t2\tLab\t25{TextColors.ENDC}")
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
    constraints_file = os.path.join(os.path.dirname(__file__), 'constraints.md')
    with open(constraints_file, 'r') as file:
        constraints = file.read()
    print(constraints)

def main_menu(has_data):
    print("\nPlease select an option:")
    if not has_data:
        print("1. Enter data paths")
        print("2. Enter data manually")
        print("0. Exit")
    else:
        print("1. Generate chromosome")
        print("2. View constraints")
        print("3. Back")
        print("0. Exit")
    choice = input("Enter your choice: ")
    return choice

def display_chromosome(chromosome):
    for gene in chromosome:
        print(f"Course: {gene.course.name}, Instructor: {gene.instructor.name}, Room: {gene.room.name}, Day: {gene.day}, Time Slot: {gene.time_slot}")

def main():
    print_welcome_message()

    has_data = False
    courses, instructors, rooms, students = [], [], [], []

    while True:
        choice = main_menu(has_data)
        if not has_data:
            if choice == '1':
                courses, instructors, rooms, students = get_data_from_files()
                has_data = True
            elif choice == '2':
                courses, instructors, rooms, students = get_data_manually()
                has_data = True
            elif choice == '0':
                print("Exiting the application.")
                sys.exit()
            else:
                print("Invalid choice. Please enter 1, 2, or 0.")
        else:
            clear_terminal()
            print("\nData has been entered successfully. Please select an option:")
            choice = main_menu(has_data)
            if choice == '1':
                chromosome_data = generate_chromosome(courses, instructors, rooms)
                print("\nGenerated Chromosome:")
                display_chromosome(chromosome_data)
                print("\nChromosome JSON:")
                print(chromosome_to_json(chromosome_data))
            elif choice == '2':
                display_constraints()
            elif choice == '3':
                has_data = False
                clear_terminal()
            elif choice == '0':
                print("Exiting the application.")
                sys.exit()
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 0.")

if __name__ == "__main__":
    main()
