from flask import Blueprint, request, jsonify, session
from app.extensions import db
from app.models import Item, User, Favorite, CATEGORY_MAP

api_bp = Blueprint('api', __name__)


@api_bp.route('/favorites', methods=['POST'])
def add_favorite():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': '请先登录'}), 401

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '请求数据无效'}), 400

        item_id = data.get('item_id')

        if not Item.query.get(item_id):
            return jsonify({'success': False, 'message': '商品不存在'}), 404

        existing = Favorite.query.filter_by(user_id=user_id, item_id=item_id).first()
        if existing:
            return jsonify({'success': False, 'message': '已经收藏过了'})

        fav = Favorite(user_id=user_id, item_id=item_id)
        db.session.add(fav)
        db.session.commit()
        return jsonify({'success': True, 'message': '收藏成功'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@api_bp.route('/favorites/<int:item_id>', methods=['DELETE'])
def remove_favorite(item_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': '请先登录'}), 401

        fav = Favorite.query.filter_by(user_id=user_id, item_id=item_id).first()
        if fav:
            db.session.delete(fav)
            db.session.commit()
            return jsonify({'success': True, 'message': '已取消收藏'})

        return jsonify({'success': False, 'message': '收藏不存在'}), 404

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@api_bp.route('/items')
def api_items():
    category = request.args.get('category', '')
    sort = request.args.get('sort', 'newest')

    query = Item.query

    if category:
        cat_name = CATEGORY_MAP.get(category, category)
        query = query.filter(Item.category == cat_name)

    if sort == 'price_asc':
        query = query.order_by(Item.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Item.price.desc())
    else:
        query = query.order_by(Item.created_at.desc())

    item_list = [item.to_dict() for item in query.all()]

    return jsonify({
        'success': True,
        'items': item_list
    })


@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item_api(item_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': '请先登录'}), 401

        item = Item.query.get(item_id)
        if not item:
            return jsonify({'success': False, 'message': '商品不存在'}), 404

        if item.seller_id != user_id:
            return jsonify({'success': False, 'message': '无权删除'}), 403

        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500