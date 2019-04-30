import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = os.environ.get('API_KEY') or ''
    LANGUAGES = ['en', 'zh']
    ELASTICSEARCH_URL = "http://" + os.environ.get('ELASTICSEARCH_HOST') + ":"\
                        + os.environ.get('ELASTICSEARCH_PORT')
    INDEX_NAME = os.environ.get('INDEX_NAME')
    
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
    REDIS_DECODE_RES = os.environ.get('REDIS_DECODE_RES')
