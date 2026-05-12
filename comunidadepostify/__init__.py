
import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy 
import cloudinary

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(app.instance_path, 'comunidade.db')}"

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_cadastro'
login_manager.login_message_category = 'alert-info'

# Garante que a pasta instance exista para não dar erro de caminho
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

#verifica de o banco de dados esta criado
from comunidadepostify import models
engine = sqlalchemy.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
inspetor = sqlalchemy.inspect(engine)
print(f"Tabelas encontradas: {inspetor.get_table_names()}")
if not inspetor.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Base de dados Criada")
else:
    print("Base de dados ja existente")

from comunidadepostify import routes