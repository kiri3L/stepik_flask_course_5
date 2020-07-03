from src.app import app
from flask import render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from src.forms import LoginPasswordForm, UserForm
from src.models import User, Category, Order, Meal, PositionInOrder
from src.app import db


"""
    скрипт для залива данных в базу
    команды фласка
    имена миграций
    тестирование
    деплой на хероку
    комит на гитхаб
    
    дополнительно:
    почистить код вьюх (заменить разные названия одного и того же на одинаковые)
    переписать render_cart_page чтобы выглядела поприличней
"""


def get_cart_info():
    return f"Корзина ({session.get('cart_items_count', 0)} блюд, {session.get('cart_price', 0)} руб.)"


def create_cart_info():
    cart = session.get('cart', {})
    positions = []
    cart_items_count = session.get('cart_items_count', 0)
    cart_price = session.get('cart_price', 0)
    for meal_id, count_dish in cart.items():
        meal = Meal.query.get(meal_id)
        positions.append({'id': meal_id,
                          'title': meal.title,
                          'count_dish': count_dish,
                          'price': meal.price})
    return {'order': positions,
            'dish_count': cart_items_count,
            'order_price': cart_price}


@app.route('/')
def render_main_page():
    is_logged = session.get('user_id') is not None
    categories = Category.query.order_by(Category.id)
    menu = dict()
    for category in categories:
        menu[category.title] = Meal.query.filter(Meal.category_id == category.id)
    return render_template('market/main.html', is_logged=is_logged, menu=menu, cart_info=get_cart_info())


@app.route('/cart/', methods=['GET', 'POST'])
def render_cart_page():
    user_id = session.get('user_id')
    if user_id is None:
        is_logged = False
    else:
        is_logged = True
    user = User.query.get(user_id)
    cart_info = create_cart_info()
    user_form = UserForm(obj=user)
    is_empty = session.get('cart_items_count', 0) == 0
    pos_deleted = session.get('pos_deleted', False)
    if pos_deleted:
        session['pos_deleted'] = False
    if is_empty:
        return render_template('market/cart.html',
                               user_form=user_form,
                               pos_deleted=pos_deleted,
                               is_logged=is_logged,
                               is_empty=is_empty,
                               **cart_info)
    if user_form.validate_on_submit():
        user_form.populate_obj(user)
        return create_order(user, cart_info)
    return render_template('market/cart.html',
                           user_form=user_form,
                           pos_deleted=pos_deleted,
                           is_logged=is_logged,
                           is_empty=is_empty,
                           **cart_info)


def create_order(user, cart_info):
    order = Order(date=datetime.now(),
                  total_price=cart_info['order_price'],
                  state=0,
                  user=user)
    db.session.add(order)
    for position in cart_info['order']:
        meal = Meal.query.get(position['id'])
        if meal is None:
            db.session.remove()
            return render_template('404.html'), 404
        p = PositionInOrder(meal=meal, order=order, count_dish=position['count_dish'])
        db.session.add(p)
        order.positions.append(p)
    session.pop('cart')
    session.pop('cart_items_count')
    session.pop('cart_price')
    db.session.commit()
    return redirect('/ordered/')


@app.route('/ordered/')
def render_ordered_page():
    return render_template('market/ordered.html')


@app.route('/account/')
def render_account_page():
    if not session.get('user_id'):
        return redirect('/login/')
    orders = Order.query.filter(Order.user_id == session['user_id'])
    return render_template('market/account.html', is_logged=True, orders=orders)


@app.route('/addtocart/<int:id>/')
def add_to_cart(id):
    meal = Meal.query.get_or_404(id)

    cart = session.get('cart', {})
    id = str(id)
    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1
    session['cart'] = cart

    cart_price = session.get('cart_price', 0)
    cart_price += meal.price
    session['cart_price'] = cart_price

    cart_items_count = session.get('cart_items_count', 0)
    cart_items_count += 1
    session['cart_items_count'] = cart_items_count
    return redirect('/')


@app.route('/remove_from_cart/<int:id>/')
def remove_from_cart(id):
    meal = Meal.query.get_or_404(id)
    cart = session.get('cart', {})
    id = str(id)
    if id in cart:
        cart_price = session.get('cart_price', 0)
        cart_items_count = session.get('cart_items_count', 0)
        cart_price -= meal.price * cart[id]
        cart_items_count -= cart[id]
        cart.pop(id)
        session['cart'] = cart
        session['cart_price'] = cart_price
        session['cart_items_count'] = cart_items_count
        session['pos_deleted'] = True
    return redirect('/cart/')
# ------------------------- Login Logout Registration ----------------------------


@app.route('/login/', methods=['GET', 'POST'])
def render_login_page():
    if session.get('user_id'):
        redirect('/account/')
    form = LoginPasswordForm()
    if form.validate_on_submit():
        return login(form)
    return render_template('authentication/login.html', form=form, is_registration=False)


@app.route('/logout/')
def render_logout_page():
    session.pop('user_id')
    return redirect('/login/')


@app.route('/registration/', methods=['GET', 'POST'])
def render_registration_page():
    if session.get('user_id'):
        redirect('/account')
    form = LoginPasswordForm()
    if form.validate_on_submit():
        return registration(form)
    return render_template('authentication/login.html', form=form, is_registration=True)


def registration(form):
    login = form.login.data
    password = form.password.data

    if User.query.filter(User.name == login).first():
        form.login.errors.append('Пользователь с таким логином уже существует')
        return render_template('authentication/login.html', form=form, is_registration=True)

    user = User(email=login, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    return redirect('/account/')


def login(form):
    login = form.login.data
    password = form.password.data

    user = User.query.filter(User.email == login).first()

    if user is None:
        form.login.errors.append('Нет пользователя с таким логином')
        return render_template('authentication/login.html', form=form, is_registration=False)

    if not check_password_hash(user.password, password):
        form.login.errors.append('Неверный пароль')
        return render_template('authentication/login.html', form=form, is_registration=False)

    session['user_id'] = user.id
    return redirect('/account/')




# @app.route('/order/')
# def order():
#     return render_template('market/ordered.html')


