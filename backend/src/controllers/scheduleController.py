# backend/src/controllers/scheduleController.py
from flask import Blueprint, request, jsonify
from app import db
from models.scheduleModel import Subject, Room, TimeSlot, Instructor, Schedule

schedule_blueprint = Blueprint('schedule', __name__)

@schedule_blueprint.route('/schedules', methods=['GET'])
def get_schedules():
    schedules = Schedule.query.all()
    result = [{'id': s.id, 'subject': s.subject.name, 'room': s.room.name, 'time_slot': s.time_slot.day + ' ' + str(s.time_slot.start_time) + '-' + str(s.time_slot.end_time), 'instructor': s.instructor.name} for s in schedules]
    return jsonify(result)

@schedule_blueprint.route('/schedules', methods=['POST'])
def create_schedule():
    data = request.get_json()
    new_schedule = Schedule(
        subject_id=data['subject_id'],
        room_id=data['room_id'],
        time_slot_id=data['time_slot_id'],
        instructor_id=data['instructor_id']
    )
    db.session.add(new_schedule)
    db.session.commit()
    return jsonify({'message': 'Schedule created successfully'}), 201
