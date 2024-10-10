from flask import Flask
from backend.models import *

app=None #initiallly it will be none

def create_app():
    service_app = Flask(__name__)  # Flask app object
    service_app.debug = True
    service_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///household.sqlite3"
    service_app.secret_key='abdvwqeihdvc'
    uploader = 'uploaded_files'
    service_app.config['UPLOAD_FOLDER'] = uploader
    service_app.app_context().push() #if app access by other modules
    db.init_app(service_app)
    print("MAD1 PROJECT STARTED.......")
    return service_app

app=create_app()
from backend.controllers import *


if __name__ == '__main__':
    app.run()






    

