# backend/src/manage.py
from flask.cli import FlaskGroup
from backend.src.app import create_app, db 

def create_app_with_cli():
    return create_app()

cli = FlaskGroup(create_app=create_app_with_cli)

if __name__ == "__main__":
    cli()
