from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import User, Item, Favorite, get_current_user, login_required

profile_bp = Blueprint('profile', __name__, template_folder='../templates')


@profile_bp.route('/')
@login_required
def index():
    user = get_current_user()

    my_items = Item.query.filter_by(seller_id=user.id).all()

    fav_records = Favorite.query.filter_by(user_id=user.id).all()
    favorite_items = [Item.query.get(fav.item_id) for fav in fav_records if Item.query.get(fav.item_id)]

    user_messages = []

    return render_template('profile.html',
                         user=user,
                         my_items=my_items,
                         favorites=favorite_items,
                         messages=user_messages)


@profile_bp.route('/settings', methods=['POST'])
@login_required
def settings():
    user = get_current_user()

    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()

    if email:
        user.email = email
    user.phone = phone or None

    db.session.commit()

    flash('设置已更新', 'success')
    return redirect(url_for('profile.index'))