# Scheduling Constraints

## Hard Constraints
1. **Instructor Availability**:
   - An instructor can only be scheduled during their available time slots.
   - Example: If Dr. Smith is available only on Mon 9-11 and Tue 1-3, they cannot be scheduled outside these times.

2. **Room Capacity**:
   - A room should not be scheduled beyond its capacity.
   - Example: If a room has a capacity of 30, you cannot schedule a class of 35 students in that room.

3. **No Double Booking of Rooms**:
   - A room cannot be booked for more than one class at the same time.
   - Example: Lecture Hall A cannot host two different classes simultaneously.

4. **No Double Booking of Instructors**:
   - An instructor cannot be scheduled to teach more than one class at the same time.
   - Example: Dr. Johnson cannot be teaching Math 101 and Chem 101 at the same time.

5. **Classroom Availability**:
   - Classes can only be scheduled during the time slots when the room is available.
   - Example: If Lab B is available only on Mon 10-12, classes cannot be scheduled in that room outside these hours.

6. **Course Duration**:
   - Each class must be scheduled for its full duration without being interrupted.
   - Example: If Math 101 is a 3-hour course, it should be scheduled in a 3-hour time block.

7. **Prerequisite Courses**:
   - A student must have completed prerequisite courses before enrolling in advanced courses.
   - Example: A student must complete Math 101 before taking Math 201.

8. **Instructor Course Assignment**:
   - Instructors can only teach courses they are assigned to.
   - Example: Dr. Smith can only teach Math 101 and not Chem 101 if they are not assigned to it.

9. **Time Slot Conflicts for Students**:
   - Students cannot be enrolled in multiple classes scheduled at the same time.
   - Example: A student enrolled in Math 101 at Mon 9-11 cannot be enrolled in another class at the same time.

## Soft Constraints
1. **Preferred Time Slots for Instructors**:
   - Schedule classes in the preferred time slots of instructors where possible.
   - Example: Dr. Smith prefers to teach on Mon 9-11, so schedule Math 101 in that slot if feasible.

2. **Minimize Consecutive Classes for Students**:
   - Avoid scheduling too many back-to-back classes for students.
   - Example: If possible, avoid scheduling three consecutive classes for a student.

3. **Spread Classes Evenly Across the Week**:
   - Distribute classes evenly throughout the week to avoid overloading any particular day.
   - Example: Avoid scheduling all classes on Monday and leaving other days empty.

4. **Balance Room Usage**:
   - Use all available rooms evenly to prevent overuse of certain rooms.
   - Example: Ensure Lecture Hall A and Lecture Hall B are used equally.

5. **Preferred Rooms for Courses**:
   - Schedule classes in the preferred rooms if possible.
   - Example: Schedule Chem 101 in Lab B if it is the preferred room for that course.

6. **Student Preferences**:
   - Consider student preferences for class times and instructors where feasible.
   - Example: If many students prefer morning classes, schedule more classes in the morning.

7. **Minimize Instructor Gaps**:
   - Avoid large gaps in instructors' schedules.
   - Example: If Dr. Johnson has a class from 9-10, avoid scheduling their next class at 3 PM if possible.

8. **Minimize Room Changes for Students**:
   - Schedule classes such that students do not have to change rooms frequently within short time spans.
   - Example: Schedule consecutive classes for a student in the same room or nearby rooms.

9. **Even Workload Distribution for Instructors**:
   - Distribute the teaching workload evenly among instructors.
   - Example: Ensure Dr. Smith and Dr. Johnson have a similar number of teaching hours.

10. **Class Size Balance**:
    - Try to balance the number of students in each class.
    - Example: Avoid having one class with 5 students and another with 50 students if possible.

## Implementation Notes
- **Hard Constraints** must be incorporated into the initial design of the scheduling algorithm to ensure that any generated schedule is feasible.
- **Soft Constraints** can be used to score and optimize the schedule. The algorithm should aim to maximize the satisfaction of soft constraints while strictly adhering to hard constraints.
- **Priority Levels**: Assign priority levels to soft constraints to guide the optimization process. High-priority soft constraints should be given more weight during optimization.
- **Conflict Resolution**: Develop strategies to resolve conflicts when constraints are violated. For hard constraints, immediate adjustments are necessary. For soft constraints, re-evaluation and minor adjustments might suffice.
- **Testing**: Create comprehensive test cases to ensure that the algorithm adheres to all constraints. Test with edge cases and large datasets to validate performance and correctness.


    