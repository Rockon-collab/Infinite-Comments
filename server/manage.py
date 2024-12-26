# import os
# from app import create_app, db
# from flask_migrate import Migrate
# from flask.cli import FlaskGroup

# # Set environment variables for Flask
# os.environ['FLASK_APP'] = 'run.py'
# os.environ['FLASK_ENV'] = 'development'

# # Create app instance
# app = create_app()

# # Initialize Flask-Migrate
# migrate = Migrate(app, db)

# # Initialize FlaskGroup for command line
# cli = FlaskGroup(app)

# if __name__ == "__main__":
#     cli()

import os
from task_app import create_app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup
# from flask import click

# Set environment variables for Flask
os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_ENV'] = 'development'

# Create app instance
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize FlaskGroup for command line
cli = FlaskGroup(app)

@cli.command('migrate_db')
def db_all():
    """Run db init, migrate, and upgrade in one command."""
    try:
        print("Running db init...")
        os.system('python manage.py db init') 
        print("Running db migrate...")
        os.system('python manage.py db migrate')
        print("Running db upgrade...")
        os.system('python manage.py db upgrade')  
        print("All migration steps completed successfully.")
    except Exception as e:
        print(f"Error during migrations: {e}")

if __name__ == "__main__":
    cli()
