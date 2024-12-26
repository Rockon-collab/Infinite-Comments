# from app import create_app
# from dotenv import load_dotenv
# import os
# # from flask_migrate import MigrateCommand
# # from flask_script import Manager

# app = create_app() 
# # manager = Manager(app)
# # manager.add_command('db', MigrateCommand)
# load_dotenv()

# if __name__ == "__main__":
#     # manager.run(debug=True)
#     os.environ['FLASK_APP'] = 'run.py'
#     app.run(debug=True)



import os
from task_app import create_app
from dotenv import load_dotenv
from task_app import app

# from flask_migrate import MigrateCommand
# from flask_script import Manager

# Load environment variables from .env file
load_dotenv()

# Set environment variables
os.environ['FLASK_APP'] = 'run.py'  # Specify the Flask application entry point
os.environ['FLASK_ENV'] = 'development'  # Set the Flask environment to development

# app = create_app()

# Initialize manager and add migration commands
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    create_app()
    app.run()
