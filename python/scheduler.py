import argparse
import json
from cffi import FFI

ffi = FFI()
ffi.cdef("""
char* ReadDataFromTxt(const char* filePath);
char* ReadDataFromExcel(const char* filePath);
""")
C = ffi.dlopen("./class_scheduler_go/class_scheduler.so")

def read_data_from_txt(file_path):
    c_file_path = ffi.new("char[]", file_path.encode('utf-8'))
    result = C.ReadDataFromTxt(c_file_path)
    result_str = ffi.string(result).decode('utf-8')
    if result_str.startswith("error:"):
        raise RuntimeError(result_str)
    return json.loads(result_str)

def read_data_from_excel(file_path):
    c_file_path = ffi.new("char[]", file_path.encode('utf-8'))
    result = C.ReadDataFromExcel(c_file_path)
    result_str = ffi.string(result).decode('utf-8')
    if result_str.startswith("error:"):
        raise RuntimeError(result_str)
    return json.loads(result_str)

def read_data(file_path):
    if file_path.endswith('.txt'):
        return read_data_from_txt(file_path)
    elif file_path.endswith('.xlsx'):
        return read_data_from_excel(file_path)
    else:
        raise ValueError('Unsupported file format')

def main(course_file, instructor_file, room_file, student_file):
    try:
        courses = read_data(course_file)
        instructors = read_data(instructor_file)
        rooms = read_data(room_file)
        students = read_data(student_file)

        print("\nCourses:", courses)
        print("\nInstructors:", instructors)
        print("\nRooms:", rooms)
        print("\nStudents:", students)
    except FileNotFoundError as fnf_error:
        print(f"File error: {fnf_error}")
    except ValueError as ve_error:
        print(f"Value error: {ve_error}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Class and Examination Scheduler")
    parser.add_argument('--courses', type=str, required=True, help='Path to the courses file (txt or xlsx)')
    parser.add_argument('--instructors', type=str, required=True, help='Path to the instructors file (txt or xlsx)')
    parser.add_argument('--rooms', type=str, required=True, help='Path to the rooms file (txt or xlsx)')
    parser.add_argument('--students', type=str, required=True, help='Path to the students file (txt or xlsx)')
    
    args = parser.parse_args()
    
    main(args.courses, args.instructors, args.rooms, args.students)
