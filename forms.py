
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')

class PredictionForm(FlaskForm):
    city = StringField('City Name', validators=[DataRequired(), Length(min=2, max=100)])
    population = IntegerField('Population', validators=[DataRequired(), NumberRange(min=1000, max=10000000)])
    temperature_increase = FloatField('Projected Temperature Increase by 2030 (°C)', 
validators=[DataRequired(), NumberRange(min=0.1, max=5.0)])
    urban_density = SelectField('Urban Density', 
choices=[('low', 'Low Density'), 
                                        ('medium', 'Medium Density'), 
                                        ('high', 'High Density')],
validators=[DataRequired()])
    infrastructure = SelectField('Infrastructure Age', 
                                choices=[('new', 'New (< 10 years)'), 
('moderate', 'Moderate (10-30 years)'), 
('aging', 'Aging (> 30 years)')],
                                validators=[DataRequired()])
    submit = SubmitField('Predict Risk')
