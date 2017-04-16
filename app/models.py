from app import db, ma
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
  __tablename__    = 'users'
  id               = db.Column(db.Integer, primary_key=True)
  email            = db.Column(db.String(120), unique=True, index=True)
  password_hash    = db.Column(db.String(128))
  is_authenticated = db.Column(db.Boolean)
  is_active        = db.Column(db.Boolean)


  def __init__(self, name, email):
    self.name = name
    self.email = email
    self.is_authenticated = True
    self.is_active = True


  def __repr__(self):
    return '<User %r>' % self.name

  def hash_password(self, password):
    self.password_hash = pwd_context.encrypt(password)

  def verify_password(self, password):
    return pwd_context.verify(password, self.password_hash)

  def get_id(self):
    return self.id


class Server(db.Model):
  __tablename__    = 'server'
  id               = db.Column(db.Integer, primary_key=True)
  name             = db.Column(db.String(255), unique=True)
  maker            = db.Column(db.String(30))
  model            = db.Column(db.String(50))
  serial_number    = db.Column(db.String(30))
  os               = db.Column(db.String(10))

  def __init__(self, name, maker, model, serial_number,os ):
    self.name = name
    self.maker = maker
    self.model = model
    self.serial_number = serial_number
    self.os = os


  def __repr__(self):
    return '<Server %r>' % self.name

  def get_id(self):
    return self.id


class DataCenter(db.Model):
    __tablename__ = 'data_center'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    location = db.Column(db.String(80))
    capacity = db.Column(db.Integer)
    tier = db.Column(db.Integer)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.is_authenticated = True
        self.is_active = True

    def __repr__(self):
        return '<DataCenter %r>' % self.name

    def get_id(self):
        return self.email

class DataCenterServer(db.Model):
    __tablename__ = 'data_center_server'
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer )
    data_center_id = db.Column(db.Integer )

    def __init__(self,server_id, data_center_id):
        self.data_center_id = data_center_id
        self.server_id = server_id

    def __repr__(self):
        return '<DataCenterServer %r>' % self.id

    def get_id(self):
        return self.id

class UserSchema(ma.ModelSchema):
  class Meta:
    model = User


class ServerSchema(ma.ModelSchema):
  class Meta:
    model = Server

class DataCenterShema(ma.ModelSchema):
    class Meta:
        model = DataCenter

class DataCentterServerSchema(ma.ModelSchema):
    class Meta:
        model = DataCenterServer