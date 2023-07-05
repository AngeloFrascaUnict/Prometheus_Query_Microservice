# Flask configuration

# from os import environ, path
# from dotenv import load_dotenv

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

class Config:
    SECRET_KEY = "GDtfD^&$%@^8tgYjD"
    #SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')

    ENVIRONMENT = "development"

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    FLASK_APP = "applicationModule"
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    
    MONGODB_SETTINGS = {"db":"my-local-db", "host":"localhost", "port":27017}   

    # Configurazione Docker di MongoDB : usare come host il nome che viene dato al container di MongoDB su Docker 
    #MONGODB_SETTINGS = {"db":"my-local-db", "host":"mongo_container", "port":27017} 

