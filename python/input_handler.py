import os
import json
from cffi import FFI
from validate import validate_data

ffi = FFI()
ffi.cdef("""
char* ReadDataFromTxt(const char* filePath);
char* ReadDataFromExcel(const char* filePath);
""")

shared_lib_path = os.path.join(os.path.dirname(__file__), "../class_scheduler_go/class_scheduler.so")
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

    courses = read_data(course_file, required_course_fields)
    instructors = read_data(instructor_file, required_instructor_fields)
    rooms = read_data(room_file, required_room_fields)
    students = read_data(student_file, required_student_fields)

    return courses, instructors, rooms, students

def input_data_manually(required_fields):
    data = []
    print(f"Please enter data for the following fields: {', '.join(required_fields)}")
    while True:
        entry = {}
        for field in required_fields:
            entry[field] = input(f"Enter {field}: ")
        data.append(entry)
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
    courses = input_data_manually(required_course_fields)
    print("Enter instructor data:")
    instructors = input_data_manually(required_instructor_fields)
    print("Enter room data:")
    rooms = input_data_manually(required_room_fields)
    print("Enter student data:")
    students = input_data_manually(required_student_fields)

    return courses, instructors, rooms, students
