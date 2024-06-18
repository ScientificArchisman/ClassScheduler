# backend/src/routes/scheduleRoutes.py
from flask import Flask
from controllers.scheduleController import schedule_blueprint

def configure_routes(app: Flask):
    app.register_blueprint(schedule_blueprint)
