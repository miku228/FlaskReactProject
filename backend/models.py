from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()

def get_uuid():
	return uuid4().hex

class User(db.Model):
  __tablename__ = "Users"
  id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uuid)
  firstname = db.Column(db.Text)
  lastname = db.Column(db.Text)
  username = db.Column(db.Text, unique=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.Text, nullable=False)

