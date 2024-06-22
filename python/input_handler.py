import os
import json
from cffi import FFI
from validate import validate_data
from data_structures import Course, Instructor, Room, Student
import sys

ffi = FFI()
ffi.cdef("""
char* ReadDataFromTxt(const char* filePath);
char* ReadDataFromExcel(const char* filePath);
""")

def get_shared_lib_path():
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        base_path = sys._MEIPASS
    else:
        # Running in a normal Python environment
        base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path,  "class_scheduler_go", 'class_scheduler.so')

shared_lib_path = get_shared_lib_path()
C = ffi.dlopen(shared_lib_path)

def read_data_from_txt(file_path):
    c_file_path = ffi.new("char[]", file_path.encode('utf-8'))
    result = C.ReadDataFromTxt(c_file_path)
    result_str = ffi.string(result).decode('utf-8')
    if result_str.startswith("error:"):
        raise RuntimeError(result_str)
    data = json.loads(result_str)
    return data

def read_data_from_excel(file_path):
    c_file_path = ffi.new("char[]", file_path.encode('utf-8'))
    result = C.ReadDataFromExcel(c_file_path)
    result_str = ffi.string(result).decode('utf-8')
    if result_str.startswith("error:"):
        raise RuntimeError(result_str)
    data = json.loads(result_str)
    return data

def read_data(file_path, required_fields):
    if file_path.endswith('.txt'):
        data = read_data_from_txt(file_path)
    elif file_path.endswith('.xlsx'):
        data = read_data_from_excel(file_path)
    else:
        raise ValueError('Unsupported file format')
    validate_data(data, required_fields)
    return data

def get_data_from_files():
    course_file = input("Enter path for courses file: ")
    instructor_file = input("Enter path for instructors file: ")
    room_file = input("Enter path for rooms file: ")
    student_file = input("Enter path for students file: ")

    required_course_fields = ['id', 'name', 'duration', 'required_room']
    required_instructor_fields = ['id', 'name', 'availability', 'preferred_slots', 'courses']
    required_room_fields = ['id', 'name', 'capacity', 'available_slots']
    required_student_fields = ['id', 'name', 'enrolled_courses']

    courses = [Course(**entry) for entry in read_data(course_file, required_course_fields)]
    instructors = [Instructor(**entry) for entry in read_data(instructor_file, required_instructor_fields)]
    rooms = [Room(**entry) for entry in read_data(room_file, required_room_fields)]
    students = [Student(**entry) for entry in read_data(student_file, required_student_fields)]

    return courses, instructors, rooms, students

def input_data_manually(required_fields, cls):
    data = []
    print(f"Please enter data for the following fields: {', '.join(required_fields)}")
    while True:
        entry = {}
        for field in required_fields:
            entry[field] = input(f"Enter {field}: ")
        data.append(cls(**entry))
        cont = input("Do you want to add another entry? (yes/no): ")
        if cont.lower() != 'yes':
            break
    return data

def get_data_manually():
    required_course_fields = ['id', 'name', 'duration', 'required_room']
    required_instructor_fields = ['id', 'name', 'availability', 'preferred_slots', 'courses']
    required_room_fields = ['id', 'name', 'capacity', 'available_slots']
    required_student_fields = ['id', 'name', 'enrolled_courses']

    print("Enter course data:")
    courses = input_data_manually(required_course_fields, Course)
    print("Enter instructor data:")
    instructors = input_data_manually(required_instructor_fields, Instructor)
    print("Enter room data:")
    rooms = input_data_manually(required_room_fields, Room)
    print("Enter student data:")
    students = input_data_manually(required_student_fields, Student)

    return courses, instructors, rooms, students
