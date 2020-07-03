from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# meals_orders_association = db.Table('meals_orders',
#                                     db.Column('meal_id',
#                                               db.Integer,
#                                               db.ForeignKey('meal.id')
#                                               ),
#                                     db.Column('order_id',
#                                               db.Integer,
#                                               db.ForeignKey('order.id')
#                                               ),
#                                     db.Column('count_dish',
#                                               db.Integer
#                                               )
#                                    )


class PositionInOrder(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), primary_key=True)
    count_dish = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', back_populates='positions')
    meal = db.relationship('Meal', back_populates='positions')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    role = db.Column(db.Boolean, default=False, nullable=False)

    orders = db.relationship('Order', back_populates='user')


class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)
    picture = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship('Category', back_populates='meals')
    positions = db.relationship('PositionInOrder',
                                back_populates='meal')


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    meals = db.relationship('Meal', back_populates='category')


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    state = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='orders')
    positions = db.relationship('PositionInOrder',
                                back_populates='order')



