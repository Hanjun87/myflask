from datetime import datetime, date
from functools import wraps
from flask import session, flash, redirect, url_for
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(20), default='[用户]')
    city = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.Date, default=date.today)

    items = db.relationship('Item', backref='seller', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'avatar': self.avatar,
            'city': self.city,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Date, default=date.today)
    contact_phone = db.Column(db.String(20), nullable=True)
    contact_wechat = db.Column(db.String(50), nullable=True)
    brand = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    purchase_time = db.Column(db.String(50), nullable=True)
    purchase_source = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        seller_name = self.seller.username if self.seller else ''
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image': self.image,
            'location': self.location,
            'seller_id': self.seller_id,
            'seller_name': seller_name,
            'views': self.views,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'contact_phone': self.contact_phone,
            'contact_wechat': self.contact_wechat,
            'brand': self.brand,
            'model': self.model,
            'purchase_time': self.purchase_time,
            'purchase_source': self.purchase_source,
        }


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


CATEGORY_MAP = {
    'electronics': '数码电子',
    'books': '图书教材',
    'clothes': '服装鞋帽',
    'furniture': '家具家居',
    'sports': '运动户外',
    'others': '其他'
}

CATEGORY_TITLES = {
    'electronics': '数码电子',
    'books': '图书教材',
    'clothes': '服装鞋帽',
    'furniture': '家具家居',
    'sports': '运动户外',
    'others': '其他臻品'
}