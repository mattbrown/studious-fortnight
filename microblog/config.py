import os


DATABASE_USER = os.environ.get('DATABASE_USER') or 'admin'
DATABASE_PASSWORD  = os.environ.get('DATABASE_PASSWORD') or 'root'
DATABASE_URL = os.environ.get('DATABASE_URL') or 'localhost:5432'
DATABASE_NAME = os.environ.get('DATABASE_USER') or 'microblog'

SQLALCHEMY_DATABASE_URI = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URL}/{DATABASE_NAME}'