"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class ProdConfig(Config):
    """Production config."""
    FLASK_ENV = "production"
    FLASK_DEBUG = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')

    # Database MongoDB 
    #MONGODB_SETTINGS = environ.get('MONGODB_SETTINGS')     non funziona!!!

    #IMPORTANTE : usare come host il nome che viene dato al container di MongoDB su Docker 
    MONGODB_SETTINGS = {"db":"my-local-db", "host":"mongo_container", "port":27017}    


class DevConfig(Config):
    """Development config."""
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    DATABASE_URI = environ.get('DEV_DATABASE_URI')

    # Database MongoDB 
    #MONGODB_SETTINGS = environ.get('MONGODB_SETTINGS')     #non funziona!!!
    MONGODB_SETTINGS = {"db":"my-local-db", "host":"localhost", "port":27017}    

    #non funziona ATLAS!!!
    # AUTHENTICATION_SOURCE = environ.get('AUTHENTICATION_SOURCE')     
    # MONGODB_HOST = environ.get('MONGODB_HOST')
    # MONGODB_PORT = environ.get('MONGODB_PORT')
    # MONGODB_USERNAME = environ.get('MONGODB_USERNAME')
    # MONGODB_PASSWORD = environ.get('MONGODB_PASSWORD')