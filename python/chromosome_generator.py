import random
import json
from data_structures import Course, Instructor, Room

class Gene:
    def __init__(self, course, instructor, room, day, time_slot):
        self.course = course
        self.instructor = instructor
        self.room = room
        self.day = day
        self.time_slot = time_slot

    def __str__(self):
        return f"Gene(Course: {self.course.name}, Instructor: {self.instructor.name}, Room: {self.room.name}, Day: {self.day}, Time Slot: {self.time_slot})"

def generate_chromosome(courses, instructors, rooms):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    periods = ["9-10", "10-11", "11-12", "12-1", "3-4", "4-5", "5-6", "6-7"]
    time_space_slots = [{"day": day, "time_slot": slot} for day in days_of_week for slot in periods]

    random.shuffle(courses)
    chromosome = []

    for course in courses:
        time_slot = random.choice(time_space_slots)
        instructor = random.choice(instructors)
        room = random.choice(rooms)
        gene = Gene(
            course=course,
            instructor=instructor,
            room=room,
            day=time_slot["day"],
            time_slot=time_slot["time_slot"]
        )
        chromosome.append(gene)

    return chromosome

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

    chromosome = generate_chromosome(courses, instructors, rooms)
    print(chromosome_to_json(chromosome))
