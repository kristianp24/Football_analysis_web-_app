from sqlalchemy.orm import sessionmaker
import sqlalchemy 
from .credentials import USER, PASSWORD, HOST, DATABASE, PORT

def create_engine_and_sessions():
    engine = sqlalchemy.create_engine(f'mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session