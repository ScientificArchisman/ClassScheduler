import sys 
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from chromosome_generator import Gene

# Define penalty values
HARD_CONSTRAINT_PENALTY = 1000
SOFT_CONSTRAINT_PENALTY = 10

def calculate_fitness(chromosome, prerequisites):
    fitness = 0
    
    # Track room and instructor usage
    room_usage = {}
    instructor_usage = {}
    student_schedule = {}
    instructor_courses = {}
    instructor_schedule = {}

    for gene in chromosome:
        course = gene.course
        instructor = gene.instructor
        room = gene.room
        day = gene.day
        time_slot = gene.time_slot

        # Check instructor availability
        if day not in instructor.availability or time_slot not in instructor.availability[day]:
            fitness += HARD_CONSTRAINT_PENALTY

        # Check room availability
        if day not in room.available_slots or time_slot not in room.available_slots[day]:
            fitness += HARD_CONSTRAINT_PENALTY

        # Check room capacity
        if course.enrolled_students > room.capacity:
            fitness += HARD_CONSTRAINT_PENALTY

        # Track room usage
        if (day, time_slot) not in room_usage:
            room_usage[(day, time_slot)] = room.id
        else:
            fitness += HARD_CONSTRAINT_PENALTY

        # Track instructor usage
        if (day, time_slot) not in instructor_usage:
            instructor_usage[(day, time_slot)] = instructor.id
        else:
            fitness += HARD_CONSTRAINT_PENALTY

        # Track student schedules
        for student_id in course.enrolled_students:
            if student_id not in student_schedule:
                student_schedule[student_id] = {}
            if day not in student_schedule[student_id]:
                student_schedule[student_id][day] = {}
            student_schedule[student_id][day][time_slot] = room.id

        # Check consecutive classes for students
        for student_id in course.enrolled_students:
            if student_id in student_schedule:
                if check_consecutive_classes(student_schedule[student_id], day, time_slot):
                    fitness += SOFT_CONSTRAINT_PENALTY

        # Track instructor's courses
        if instructor.id not in instructor_courses:
            instructor_courses[instructor.id] = []
        if course.id not in instructor_courses[instructor.id]:
            fitness += HARD_CONSTRAINT_PENALTY

        # Check preferred time slots
        if f"{day} {time_slot}" not in instructor.preferred_slots:
            fitness += SOFT_CONSTRAINT_PENALTY

        # Minimize instructor gaps
        instructor_gaps = count_instructor_gaps(instructor_schedule, instructor.id, day, time_slot)
        fitness += SOFT_CONSTRAINT_PENALTY * instructor_gaps

        # Update instructor schedule
        if instructor.id not in instructor_schedule:
            instructor_schedule[instructor.id] = {}
        if day not in instructor_schedule[instructor.id]:
            instructor_schedule[instructor.id][day] = []
        instructor_schedule[instructor.id][day].append(time_slot)

    # Spread classes evenly across the week
    class_distribution = count_classes_per_day(chromosome)
    fitness += SOFT_CONSTRAINT_PENALTY * check_class_distribution(class_distribution)
    
    # Balance room usage
    room_distribution = count_room_usage(chromosome)
    fitness += SOFT_CONSTRAINT_PENALTY * check_room_usage(room_distribution)
    
    # Preferred rooms for courses
    for gene in chromosome:
        course = gene.course
        room = gene.room
        if room.name != course.required_room:
            fitness += SOFT_CONSTRAINT_PENALTY
    
    # Minimize room changes for students
    for student_id in course.enrolled_students:
        if student_id in student_schedule and check_room_changes(student_schedule[student_id], room.id):
            fitness += SOFT_CONSTRAINT_PENALTY
    
    # Even workload distribution for instructors
    instructor_workload = count_instructor_workload(chromosome)
    fitness += SOFT_CONSTRAINT_PENALTY * check_instructor_workload(instructor_workload)
    
    # Class size balance
    class_size_balance = check_class_size_balance(chromosome)
    fitness += SOFT_CONSTRAINT_PENALTY * class_size_balance

    # Check prerequisites
    for student_id in student_schedule:
        if not prerequisites_met(student_schedule[student_id], prerequisites):
            fitness += HARD_CONSTRAINT_PENALTY

    return fitness

# Helper functions for fitness calculation

def check_consecutive_classes(schedule, day, time_slot):
    time_slot_mapping = {
        "9-10": 1,
        "10-11": 2,
        "11-12": 3,
        "12-1": 4,
        "3-4": 5,
        "4-5": 6,
        "5-6": 7,
        "6-7": 8
    }
    
    current_time = time_slot_mapping.get(time_slot)
    if current_time is None:
        return False

    for slot in schedule.get(day, []):
        if time_slot_mapping.get(slot) in [current_time - 1, current_time + 1]:
            return True
    return False

def count_classes_per_day(chromosome):
    class_distribution = {}
    for gene in chromosome:
        day = gene.day
        if day in class_distribution:
            class_distribution[day] += 1
        else:
            class_distribution[day] = 1
    return class_distribution

def check_class_distribution(distribution):
    total_classes = sum(distribution.values())
    num_days = len(distribution)
    average_classes_per_day = total_classes / num_days

    penalty = 0
    for day, count in distribution.items():
        deviation = abs(count - average_classes_per_day)
        penalty += deviation
    
    return penalty

def count_room_usage(chromosome):
    room_distribution = {}
    for gene in chromosome:
        room_id = gene.room.id
        if room_id in room_distribution:
            room_distribution[room_id] += 1
        else:
            room_distribution[room_id] = 1
    return room_distribution

def check_room_usage(distribution):
    total_usage = sum(distribution.values())
    num_rooms = len(distribution)
    average_usage_per_room = total_usage / num_rooms

    penalty = 0
    for room_id, usage in distribution.items():
        deviation = abs(usage - average_usage_per_room)
        penalty += deviation
    
    return penalty

def count_instructor_gaps(schedule, instructor_id, day, time_slot):
    time_slot_mapping = {
        "9-10": 1,
        "10-11": 2,
        "11-12": 3,
        "12-1": 4,
        "3-4": 5,
        "4-5": 6,
        "5-6": 7,
        "6-7": 8
    }

    if instructor_id not in schedule:
        schedule[instructor_id] = {}

    if day not in schedule[instructor_id]:
        schedule[instructor_id][day] = []

    current_time = time_slot_mapping.get(time_slot)
    if current_time is not None:
        schedule[instructor_id][day].append(current_time)

    sorted_slots = sorted(schedule[instructor_id][day])
    gaps = 0
    for i in range(1, len(sorted_slots)):
        if sorted_slots[i] != sorted_slots[i - 1] + 1:
            gaps += 1

    return gaps

def check_room_changes(schedule, room_id):
    room_changes = 0

    for day, time_slots in schedule.items():
        previous_room = None
        if not isinstance(time_slots, dict):
            continue  # Skip if time_slots is not a dictionary

        sorted_slots = sorted(time_slots.keys())
        
        for slot in sorted_slots:
            current_room = time_slots[slot]
            if previous_room and current_room != previous_room:
                room_changes += 1
            previous_room = current_room

    return room_changes

def count_instructor_workload(chromosome):
    instructor_workload = {}

    for gene in chromosome:
        instructor_id = gene.instructor.id
        if instructor_id in instructor_workload:
            instructor_workload[instructor_id] += 1
        else:
            instructor_workload[instructor_id] = 1
    
    return instructor_workload

def check_instructor_workload(workload):
    total_workload = sum(workload.values())
    num_instructors = len(workload)
    average_workload = total_workload / num_instructors

    penalty = 0
    for instructor_id, classes in workload.items():
        deviation = abs(classes - average_workload)
        penalty += deviation
    
    return penalty

def check_class_size_balance(chromosome):
    total_students = 0
    num_classes = len(chromosome)
    class_sizes = []

    for gene in chromosome:
        class_size = len(gene.course.enrolled_students)
        class_sizes.append(class_size)
        total_students += class_size

    average_class_size = total_students / num_classes

    penalty = 0
    for size in class_sizes:
        deviation = abs(size - average_class_size)
        penalty += deviation
    
    return penalty

def prerequisites_met(schedule, prerequisites):
    completed_courses = set()

    for day in sorted(schedule.keys()):
        time_slots = schedule[day]
        for time_slot in sorted(time_slots.keys()):
            course_id = time_slots[time_slot]

            if course_id in prerequisites:
                for prereq in prerequisites[course_id]:
                    if prereq not in completed_courses:
                        return False

            completed_courses.add(course_id)

    return True


