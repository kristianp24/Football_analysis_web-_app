import sqlalchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import inspect
from models.base import Base

def create_or_check_database(app):
    
    engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    if not database_exists(engine.url):
        create_database(engine.url)
        print("Database created.")
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Existing tables: {tables}")  

    if not tables or (len(tables) == 1 and tables[0] == 'users'):
        Base.metadata.create_all(engine)
        print("Tables created.")
    else:
        print("Tables already exist.")
    
    # with app.app_context():
    #     print("Applying migrations...")
    #     upgrade()
    #     print("Migrations applied.")
    
    return engine



