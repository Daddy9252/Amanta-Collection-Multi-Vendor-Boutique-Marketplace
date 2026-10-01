from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, SelectField, SubmitField,
    TextAreaField, DecimalField, IntegerField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    role = SelectField('Role', choices=[('buyer', 'Buyer'), ('vendor', 'Vendor')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField('Description', validators=[Optional()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    size = SelectField('Size', choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')])
    color = StringField('Color', validators=[Optional(), Length(max=30)])
    stock = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', choices=[
        ('Dresses', 'Dresses'), ('Outerwear', 'Outerwear'),
        ('Tops', 'Tops'), ('Bottoms', 'Bottoms'), ('Accessories', 'Accessories')
    ])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Save Product')
