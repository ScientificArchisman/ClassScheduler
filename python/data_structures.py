class Course:
    def __init__(self, id, name, duration, required_room):
        self.id = id
        self.name = name
        self.duration = duration
        self.required_room = required_room

    def __str__(self):
        return f"Course(ID: {self.id}, Name: {self.name}, Duration: {self.duration}, Required Room: {self.required_room})"

class Instructor:
    def __init__(self, id, name, availability, preferred_slots, courses):
        self.id = id
        self.name = name
        self.availability = availability
        self.preferred_slots = preferred_slots
        self.courses = courses

    def __str__(self):
        return f"Instructor(ID: {self.id}, Name: {self.name}, Availability: {self.availability}, Preferred Slots: {self.preferred_slots}, Courses: {self.courses})"

class Room:
    def __init__(self, id, name, capacity, available_slots):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.available_slots = available_slots

    def __str__(self):
        return f"Room(ID: {self.id}, Name: {self.name}, Capacity: {self.capacity}, Available Slots: {self.available_slots})"

class Student:
    def __init__(self, id, name, enrolled_courses):
        self.id = id
        self.name = name
        self.enrolled_courses = enrolled_courses

    def __str__(self):
        return f"Student(ID: {self.id}, Name: {self.name}, Enrolled Courses: {self.enrolled_courses})"
