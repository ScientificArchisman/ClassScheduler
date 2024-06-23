import json
from chromosome_generator import generate_chromosome, Gene
import sys
import os
# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from data_structures import Course, Instructor, Room


def generate_population(population_size, courses, instructors, rooms):
    return [generate_chromosome(courses, instructors, rooms) for _ in range(population_size)]

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Course, Instructor, Room)):
            return obj.__dict__
        if isinstance(obj, Gene):
            return {
                "course": obj.course.__dict__,
                "instructor": obj.instructor.__dict__,
                "room": obj.room.__dict__,
                "day": obj.day,
                "time_slot": obj.time_slot
            }
        return json.JSONEncoder.default(self, obj)

def chromosome_to_json(chromosome):
    return json.dumps(chromosome, cls=CustomEncoder, indent=4)

def population_to_json(population):
    return json.dumps([json.loads(chromosome_to_json(chromosome)) for chromosome in population], indent=4)


# Example usage (for testing only)
if __name__ == "__main__":
    courses = [
        Course(1, "Math 101", 3, "Lecture Hall", 30),
        Course(2, "Chem 101", 2, "Lab", 25)
    ]
    instructors = [
        Instructor(1, "Dr. Smith", "Mon 9-11, Tue 1-3", "Mon 9-11", [1]),
        Instructor(2, "Dr. Johnson", "Mon 10-12, Wed 2-4", "Wed 2-4", [2])
    ]
    rooms = [
        Room(1, "Lecture Hall A", 100, "Mon 9-11, Tue 1-3"),
        Room(2, "Lab B", 30, "Mon 10-12, Wed 2-4")
    ]

    population_size = 10
    population = generate_population(population_size, courses, instructors, rooms)
    print(population_to_json(population))
