from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import Item, User, get_current_user, login_required, allowed_file, CATEGORY_MAP, CATEGORY_TITLES
from datetime import datetime, date
import os
from flask import current_app

items_bp = Blueprint('items', __name__, template_folder='../templates')


@items_bp.route('/')
def index():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)

    query = Item.query

    if category:
        cat_name = CATEGORY_MAP.get(category, category)
        query = query.filter(Item.category == cat_name)

    if search:
        query = query.filter(
            Item.title.contains(search) | Item.description.contains(search)
        )

    if sort == 'price_asc':
        query = query.order_by(Item.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Item.price.desc())
    else:
        query = query.order_by(Item.created_at.desc())

    per_page = 12
    total = query.count()
    item_list = query.offset((page - 1) * per_page).limit(per_page).all()

    class Pagination:
        def __init__(self, page, per_page, total):
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = (total + per_page - 1) // per_page
            self.has_prev = page > 1
            self.has_next = page < self.pages
            self.prev_num = page - 1
            self.next_num = page + 1

        def iter_pages(self):
            for i in range(1, self.pages + 1):
                yield i

    pagination = Pagination(page, per_page, total) if total > per_page else None
    category_title = CATEGORY_TITLES.get(category, '') if category else ''

    users = {u.id: u for u in User.query.all()}

    return render_template('index.html',
                         items=item_list,
                         pagination=pagination,
                         users=users,
                         current_category=category,
                         current_sort=sort,
                         category_title=category_title)


@items_bp.route('/item/<int:item_id>')
def item_detail(item_id):
    item = Item.query.get(item_id)
    if not item:
        flash('商品不存在', 'danger')
        return redirect(url_for('items.index'))

    item.views += 1
    db.session.commit()

    related_items = Item.query.filter(
        Item.category == item.category,
        Item.id != item_id
    ).limit(4).all()

    seller = User.query.get(item.seller_id)

    return render_template('detail.html', item=item, related_items=related_items, users={})


@items_bp.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        price = request.form.get('price', type=float)
        category = request.form.get('category', '')
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        contact_phone = request.form.get('contact_phone', '').strip()
        contact_wechat = request.form.get('contact_wechat', '').strip()
        brand = request.form.get('brand', '').strip()
        model = request.form.get('model', '').strip()
        purchase_time = request.form.get('purchase_time', '').strip()
        purchase_source = request.form.get('purchase_source', '').strip()

        if not title or not price or not category or not description:
            flash('请填写所有必填项', 'danger')
            return redirect(url_for('items.publish'))

        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
                upload_folder = current_app.config['UPLOAD_FOLDER']
                file.save(os.path.join(upload_folder, filename))
                image = filename

        user = get_current_user()

        item = Item(
            title=title,
            description=description,
            price=price,
            category=CATEGORY_MAP.get(category, category),
            image=image,
            location=location,
            seller_id=user.id,
            views=0,
            created_at=date.today(),
            contact_phone=contact_phone or None,
            contact_wechat=contact_wechat or None,
            brand=brand or None,
            model=model or None,
            purchase_time=purchase_time or None,
            purchase_source=purchase_source or None,
        )
        db.session.add(item)
        db.session.commit()

        flash('商品发布成功！', 'success')
        return redirect(url_for('items.item_detail', item_id=item.id))

    return render_template('publish.html')


@items_bp.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        flash('商品不存在', 'danger')
        return redirect(url_for('items.index'))

    if item.seller_id != session.get('user_id'):
        flash('无权编辑此商品', 'danger')
        return redirect(url_for('items.index'))

    if request.method == 'POST':
        item.title = request.form.get('title', '').strip()
        item.price = request.form.get('price', type=float)
        item.description = request.form.get('description', '').strip()
        item.location = request.form.get('location', '').strip()
        item.brand = request.form.get('brand', '').strip() or None
        item.model = request.form.get('model', '').strip() or None
        item.purchase_time = request.form.get('purchase_time', '').strip() or None
        item.purchase_source = request.form.get('purchase_source', '').strip() or None

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
                upload_folder = current_app.config['UPLOAD_FOLDER']
                file.save(os.path.join(upload_folder, filename))
                item.image = filename

        db.session.commit()

        flash('商品更新成功！', 'success')
        return redirect(url_for('items.item_detail', item_id=item_id))

    return render_template('publish.html', item=item)


@items_bp.route('/user/<int:user_id>')
def user_items(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('用户不存在', 'danger')
        return redirect(url_for('items.index'))

    user_items_list = Item.query.filter_by(seller_id=user_id).all()

    return render_template('index.html', items=user_items_list)