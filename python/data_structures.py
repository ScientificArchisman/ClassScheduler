class Course:
    def __init__(self, id, name, duration, required_room, enrolled_students):
        self.id = id
        self.name = name
        self.duration = duration
        self.required_room = required_room
        self.enrolled_students = enrolled_students

    def __str__(self):
        return f"Course(ID: {self.id}, Name: {self.name}, Duration: {self.duration}, Required Room: {self.required_room}, Enrolled Students: {self.enrolled_students})"

class Instructor:
    def __init__(self, id, name, availability, preferred_slots, courses):
        self.id = id
        self.name = name
        self.availability = self.parse_availability(availability)
        self.preferred_slots = self.parse_preferred_slots(preferred_slots)
        self.courses = courses

    def parse_availability(self, availability):
        # Convert availability string to a more manageable format (e.g., dictionary)
        availability_dict = {}
        for slot in availability.split(","):
            day, times = slot.strip().split()
            availability_dict.setdefault(day, []).append(times)
        return availability_dict

    def parse_preferred_slots(self, preferred_slots):
        # Convert preferred slots string to a list
        return [slot.strip() for slot in preferred_slots.split(",")]

    def __str__(self):
        return f"Instructor(ID: {self.id}, Name: {self.name}, Availability: {self.availability}, Preferred Slots: {self.preferred_slots}, Courses: {self.courses})"

class Room:
    def __init__(self, id, name, capacity, available_slots):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.available_slots = self.parse_available_slots(available_slots)

    def parse_available_slots(self, available_slots):
        # Convert available slots string to a more manageable format (e.g., dictionary)
        available_slots_dict = {}
        for slot in available_slots.split(","):
            day, times = slot.strip().split()
            available_slots_dict.setdefault(day, []).append(times)
        return available_slots_dict

    def __str__(self):
        return f"Room(ID: {self.id}, Name: {self.name}, Capacity: {self.capacity}, Available Slots: {self.available_slots})"

class Student:
    def __init__(self, id, name, enrolled_courses):
        self.id = id
        self.name = name
        self.enrolled_courses = enrolled_courses

    def __str__(self):
        return f"Student(ID: {self.id}, Name: {self.name}, Enrolled Courses: {self.enrolled_courses})"
