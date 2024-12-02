import os
from flask import Flask
from backend.models import *

app=None #initiallly it will be none

def create_app():
    service_app = Flask(__name__)  # Flask app object
    service_app.debug = True
    service_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///household.sqlite3"

    service_app.secret_key='abdvwqeihdvc'
    UPLOAD_FOLDER = os.path.join(os.getcwd(),'static', 'pdfs')  # Folder where uploaded pdfs will be stored
    service_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    service_app.app_context().push() #if app access by other modules
    db.init_app(service_app)
    print("MAD1 PROJECT STARTED.......")
    return service_app

app=create_app()
import init_db
from backend.auth import *

from backend.admin_home import *
from backend.customer_home import *
from backend.professional_home import *

from backend.admin_search import *
from backend.customer_search import *
from backend.professional_search import *

from backend.admin_summary import *
from backend.customer_summary import *
from backend.professional_summary import *


if __name__ == '__main__':
    app.run()






    

