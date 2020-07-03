import csv
import click
from flask.cli import AppGroup
from src.models import db, Category, Meal, User
from werkzeug.security import generate_password_hash


create = AppGroup('create')


@create.command('user')
@click.argument('email')
@click.argument('password')
def create_user(email, password):
    user = User.query.filter(User.email == email).first()
    if user:
        print('Пользователь уже существует')
        return
    db.session.add(User(email=email, password=generate_password_hash(password=password), role=False))
    db.session.commit()


@create.command('admin')
@click.argument('email')
@click.argument('password')
def create_admin(email, password):
    user = User.query.filter(User.email == email).first()
    if user:
        print('Пользователь уже существует')
        return
    db.session.add(User(email=email, password=generate_password_hash(password=password), role=True))
    db.session.commit()


@create.command('meals')
def init_db():
    with open('../delivery_categories.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            db.session.add(Category(**row))
        db.session.commit()
    with open('../delivery_items.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            db.session.add(Meal(**row))
        db.session.commit()


