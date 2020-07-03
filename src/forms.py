import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Email, InputRequired, ValidationError
from wtforms.ext.appengine.db import model_form

from src.models import User


def password_validator(form, field):
    s = field.data

    if len(s) >= 8 \
            and re.search('[A-ZА-Я]', s,)\
            and re.search('[a-zа-я]', s)\
            and re.search('[0-9]', s):
        return
    raise ValidationError(message='Пароль слишком простой.'
                                  + 'Пароль должен содержать не меньше 8 символов.'
                                  + 'Пароль должен состоять из цифр и букв в верхнем и нижнем регистре.')


class LoginPasswordForm(FlaskForm):
    login = StringField('Логин', [Email(message='Невалидный email')])
    password = PasswordField('Пароль', [password_validator])


class UserForm(FlaskForm):
    name = StringField('Имя', [InputRequired('Поле не должно быть пустым')])
    email = StringField('Электропочта', [Email('Неверный email')])
    phone = StringField('Телефон', [InputRequired('Поле не должно быть пустым')])
    address = StringField('Адрес', [InputRequired('Поле не должно быть пустым')])
