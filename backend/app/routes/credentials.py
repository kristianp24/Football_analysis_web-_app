import dotenv
import os
dotenv.load_dotenv(dotenv_path='backend/app/.env')

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')