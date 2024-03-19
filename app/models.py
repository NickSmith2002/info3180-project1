from . import db
from flask_wtf.file import FileAllowed
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired

class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    bedrooms = db.Column(db.String)
    bathrooms = db.Column(db.String)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(255), nullable=False)

    def __init__(self, title, description, bedrooms, bathrooms, location, price, type, photo):
        self.title = title
        self.description = description
        self.bathrooms = bathrooms
        self.bedrooms = bedrooms
        self.location = location
        self.price = price
        self.type = type
        self.photo = photo        

class NewPropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired()])
    bedrooms = StringField('Number of Bedrooms', validators=[DataRequired()])
    bathrooms = StringField('Number of Bathrooms', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    type = SelectField('Type', choices=[('House', 'House'), ('Apartment', 'Apartment')])
    description = TextAreaField('Description', validators=[DataRequired()])
    photo = FileField('Photo', validators=[DataRequired(),FileAllowed(['jpg', 'png', 'jpeg'])])