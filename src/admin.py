from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from src.models import User, Meal, Order, Category, db
from flask import session

admin = Admin()


def check_admin_status():
    user_id = session.get('user_id')
    if user_id is None:
        return False
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return False
    return user.role


class UserModelView(ModelView):
    exclude = ['password']

    def is_accessible(self):
        return check_admin_status()


class OrderModelView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False

    def is_accessible(self):
        return check_admin_status()


class MealModelView(ModelView):

    def is_accessible(self):
        return check_admin_status()


class CategoryModelView(ModelView):

    def is_accessible(self):
        return check_admin_status()


admin.add_view(UserModelView(User, db.session))
admin.add_view(OrderModelView(Order, db.session))
admin.add_view(MealModelView(Meal, db.session))
admin.add_view(CategoryModelView(Category, db.session))


