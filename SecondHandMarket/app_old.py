"""
中古·回想 - 二手交易市场
Flask 后端示例
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 请更换为随机密钥

# 配置
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 最大上传限制

# ============== 模拟数据（实际项目中请使用数据库）==============

# 模拟用户数据
users = {
    1: {
        'id': 1, 'username': '程序员老王', 'email': 'laowang@qq.com',
        'phone': '13800138001', 'password': 'password123', 'avatar': '[程序员]',
        'city': '北京', 'bio': '全栈开发，喜欢折腾数码产品', 'created_at': '2023-03-15'
    },
    2: {
        'id': 2, 'username': '咖啡不加糖', 'email': 'coffee@163.com',
        'phone': '13900139002', 'password': 'password123', 'avatar': '[设计师]',
        'city': '上海', 'bio': '设计师，重度咖啡爱好者，断舍离中', 'created_at': '2023-06-22'
    },
    3: {
        'id': 3, 'username': '西北偏北', 'email': 'xibei@gmail.com',
        'phone': '13700137003', 'password': 'password123', 'avatar': '[户外]',
        'city': '西安', 'bio': '户外爱好者，登山徒步露营', 'created_at': '2023-01-10'
    },
    4: {
        'id': 4, 'username': '南方小渔', 'email': 'fish@126.com',
        'phone': '13600136004', 'password': 'password123', 'avatar': '[学生]',
        'city': '广州', 'bio': '在读研究生，喜欢读书和摄影', 'created_at': '2023-09-05'
    },
    5: {
        'id': 5, 'username': '城市浪人', 'email': 'wave@qq.com',
        'phone': '13500135005', 'password': 'password123', 'avatar': '[潮人]',
        'city': '深圳', 'bio': '滑板少年，潮牌收集者', 'created_at': '2024-01-18'
    },
    6: {
        'id': 6, 'username': '西湖龙井', 'email': 'longjing@163.com',
        'phone': '13400134006', 'password': 'password123', 'avatar': '[茶艺]',
        'city': '杭州', 'bio': '茶文化爱好者，偶尔出闲置茶具', 'created_at': '2023-05-30'
    },
    7: {
        'id': 7, 'username': '火锅英雄', 'email': 'hotpot@qq.com',
        'phone': '13300133007', 'password': 'password123', 'avatar': '[美食]',
        'city': '成都', 'bio': '自由摄影师，美食达人', 'created_at': '2023-11-12'
    },
    8: {
        'id': 8, 'username': '江边看日落', 'email': 'sunset@126.com',
        'phone': '13200132008', 'password': 'password123', 'avatar': '[文艺]',
        'city': '武汉', 'bio': '大学生，喜欢阅读和历史', 'created_at': '2024-02-28'
    },
    9: {
        'id': 9, 'username': '山城旧物', 'email': 'shan@163.com',
        'phone': '13100131009', 'password': 'password123', 'avatar': '[收藏]',
        'city': '重庆', 'bio': '中古爱好者，家里有很多宝贝', 'created_at': '2023-08-17'
    },
    10: {
        'id': 10, 'username': '金陵十三少', 'email': 'nanjing@qq.com',
        'phone': '13000130010', 'password': 'password123', 'avatar': '[复古]',
        'city': '南京', 'bio': '复古家具收藏，爱逛旧货市场', 'created_at': '2023-04-03'
    },
}

# 模拟商品数据
items = {
    1: {
        'id': 1,
        'title': 'iPhone 15 Pro Max 256G',
        'description': '国行原封未拆，带发票，AC+延保两年',
        'price': 8800.0,
        'category': '数码电子',
        'image': None,
        'location': '深圳南山区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 331,
        'created_at': '2024-02-01',
        'contact_phone': None,
        'contact_wechat': '南方小渔_wx',
        'brand': 'Apple',
        'model': 'iPhone 15 Pro Max',
        'purchase_time': '2024-01-15',
        'purchase_source': 'Apple官网'
    },
    2: {
        'id': 2,
        'title': 'iPhone 14 Pro 256G',
        'description': '成色完美无划痕，电池健康95%+，箱说全',
        'price': 6600.0,
        'category': '数码电子',
        'image': None,
        'location': '北京朝阳区',
        'seller_id': 1,
        'seller_name': '程序员老王',
        'views': 482,
        'created_at': '2024-02-19',
        'contact_phone': None,
        'contact_wechat': '程序员老王_wx',
        'brand': 'Apple',
        'model': 'iPhone 14 Pro',
        'purchase_time': '2023-09-20',
        'purchase_source': '京东'
    },
    3: {
        'id': 3,
        'title': 'MacBook Pro 16寸 M3 Max',
        'description': '顶配64G+1TB，专业工作站，仅拆封测试',
        'price': 22900.0,
        'category': '数码电子',
        'image': None,
        'location': '西安碑林区',
        'seller_id': 9,
        'seller_name': '山城旧物',
        'views': 253,
        'created_at': '2024-01-18',
        'contact_phone': '13031429110',
        'contact_wechat': '山城旧物_wx'
    },
    4: {
        'id': 4,
        'title': 'MacBook Air 15寸 M3',
        'description': '午夜色，16G+512G，电池循环个位数',
        'price': 9400.0,
        'category': '数码电子',
        'image': None,
        'location': '广州天河区',
        'seller_id': 3,
        'seller_name': '西北偏北',
        'views': 334,
        'created_at': '2024-07-11',
        'contact_phone': '14160992979',
        'contact_wechat': '西北偏北_wx'
    },
    5: {
        'id': 5,
        'title': 'iPad Pro 12.9寸 M2',
        'description': '蜂窝版256G，配妙控键盘，AppleCare+',
        'price': 6600.0,
        'category': '数码电子',
        'image': None,
        'location': '重庆江北区',
        'seller_id': 10,
        'seller_name': '金陵十三少',
        'views': 402,
        'created_at': '2024-06-28',
        'contact_phone': '19826753883',
        'contact_wechat': '金陵十三少_wx'
    },
    6: {
        'id': 6,
        'title': 'AirPods Max',
        'description': '银色，配智能耳机套，音质完美无磕碰',
        'price': 3100.0,
        'category': '数码电子',
        'image': None,
        'location': '重庆江北区',
        'seller_id': 10,
        'seller_name': '金陵十三少',
        'views': 350,
        'created_at': '2024-02-18',
        'contact_phone': '13598753260',
        'contact_wechat': '金陵十三少_wx'
    },
    7: {
        'id': 7,
        'title': '索尼 A7M4 机身',
        'description': '快门<5000次，CMOS完美，配原装配件',
        'price': 12900.0,
        'category': '数码电子',
        'image': None,
        'location': '上海静安区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 288,
        'created_at': '2024-05-03',
        'contact_phone': '17631831063',
        'contact_wechat': '咖啡不加糖_wx'
    },
    8: {
        'id': 8,
        'title': '索尼 FE 24-70mm F2.8 GM II',
        'description': '镜片三无，对焦迅速，箱说发票齐全',
        'price': 11700.0,
        'category': '数码电子',
        'image': None,
        'location': '杭州上城区',
        'seller_id': 5,
        'seller_name': '城市浪人',
        'views': 736,
        'created_at': '2024-06-07',
        'contact_phone': '15181691040',
        'contact_wechat': '城市浪人_wx'
    },
    9: {
        'id': 9,
        'title': '索尼 FE 85mm F1.4 GM',
        'description': '人像镜皇，虚化柔美，配UV镜',
        'price': 9900.0,
        'category': '数码电子',
        'image': None,
        'location': '武汉武昌区',
        'seller_id': 7,
        'seller_name': '火锅英雄',
        'views': 523,
        'created_at': '2024-04-06',
        'contact_phone': '15853524491',
        'contact_wechat': '火锅英雄_wx'
    },
    10: {
        'id': 10,
        'title': '佳能 EOS R6 Mark II',
        'description': '准新成色，专业全画幅，视频拍照双修',
        'price': 13200.0,
        'category': '数码电子',
        'image': None,
        'location': '成都武侯区',
        'seller_id': 6,
        'seller_name': '西湖龙井',
        'views': 82,
        'created_at': '2024-04-27',
        'contact_phone': '17038538251',
        'contact_wechat': '西湖龙井_wx'
    },
    11: {
        'id': 11,
        'title': '佳能 RF 50mm F1.2L',
        'description': '大光圈定焦，夜景神器，成色完美',
        'price': 12300.0,
        'category': '数码电子',
        'image': None,
        'location': '南京玄武区',
        'seller_id': 8,
        'seller_name': '江边看日落',
        'views': 708,
        'created_at': '2024-08-13',
        'contact_phone': '19845264581',
        'contact_wechat': '江边看日落_wx'
    },
    12: {
        'id': 12,
        'title': '大疆 Mavic 3 Pro',
        'description': '畅飞套装，三摄旗舰，随心换一年',
        'price': 14300.0,
        'category': '数码电子',
        'image': None,
        'location': '成都锦江区',
        'seller_id': 6,
        'seller_name': '西湖龙井',
        'views': 458,
        'created_at': '2024-07-19',
        'contact_phone': '19322201654',
        'contact_wechat': '西湖龙井_wx'
    },
    13: {
        'id': 13,
        'title': '大疆 Mini 4 Pro',
        'description': '带屏遥控器版，轻巧便携，4K画质',
        'price': 4500.0,
        'category': '数码电子',
        'image': None,
        'location': '广州海珠区',
        'seller_id': 3,
        'seller_name': '西北偏北',
        'views': 692,
        'created_at': '2024-02-05',
        'contact_phone': '17889978790',
        'contact_wechat': None
    },
    14: {
        'id': 14,
        'title': '徕卡 Q3',
        'description': '德味浓郁，6000万像素，Summilux镜头',
        'price': 41800.0,
        'category': '数码电子',
        'image': None,
        'location': '北京西城区',
        'seller_id': 1,
        'seller_name': '程序员老王',
        'views': 616,
        'created_at': '2024-09-09',
        'contact_phone': '19845812670',
        'contact_wechat': '程序员老王_wx'
    },
    15: {
        'id': 15,
        'title': '哈苏 X2D 100C',
        'description': '中画幅一亿像素，自然色彩解决方案',
        'price': 54200.0,
        'category': '数码电子',
        'image': None,
        'location': '杭州滨江区',
        'seller_id': 5,
        'seller_name': '城市浪人',
        'views': 164,
        'created_at': '2024-11-11',
        'contact_phone': None,
        'contact_wechat': None
    },
    16: {
        'id': 16,
        'title': '大黄页绝版收藏1950s',
        'description': '民国广告画册，品相完好，历史文献价值',
        'price': 10900.0,
        'category': '图书教材',
        'image': None,
        'location': '广州海珠区',
        'seller_id': 3,
        'seller_name': '西北偏北',
        'views': 562,
        'created_at': '2024-12-09',
        'contact_phone': '16895758349',
        'contact_wechat': '西北偏北_wx'
    },
    17: {
        'id': 17,
        'title': '芥子园画谱乾隆刻本',
        'description': '线装古籍，名家旧藏，木刻版画精美',
        'price': 12100.0,
        'category': '图书教材',
        'image': None,
        'location': '成都锦江区',
        'seller_id': 6,
        'seller_name': '西湖龙井',
        'views': 206,
        'created_at': '2024-10-07',
        'contact_phone': '19710076758',
        'contact_wechat': '西湖龙井_wx'
    },
    18: {
        'id': 18,
        'title': '毛泽东选集第一版',
        'description': '解放社原版，红塑皮，收藏价值高',
        'price': 7900.0,
        'category': '图书教材',
        'image': None,
        'location': '上海静安区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 69,
        'created_at': '2024-06-16',
        'contact_phone': '16942138745',
        'contact_wechat': '咖啡不加糖_wx'
    },
    19: {
        'id': 19,
        'title': '红楼梦脂砚斋评本',
        'description': '影印线装，收藏级版本，配函套',
        'price': 4400.0,
        'category': '图书教材',
        'image': None,
        'location': '上海徐汇区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 130,
        'created_at': '2024-04-19',
        'contact_phone': '19826879290',
        'contact_wechat': None
    },
    20: {
        'id': 20,
        'title': '十万个为什么初版全套',
        'description': '60年代第一版，童年回忆，品相完好',
        'price': 3000.0,
        'category': '图书教材',
        'image': None,
        'location': '广州越秀区',
        'seller_id': 3,
        'seller_name': '西北偏北',
        'views': 612,
        'created_at': '2024-11-16',
        'contact_phone': '15782383095',
        'contact_wechat': '西北偏北_wx'
    },
    21: {
        'id': 21,
        'title': '国家地理百年合订本',
        'description': '1920-2020经典合订，摄影史上的瑰宝',
        'price': 5100.0,
        'category': '图书教材',
        'image': None,
        'location': '成都武侯区',
        'seller_id': 6,
        'seller_name': '西湖龙井',
        'views': 458,
        'created_at': '2024-12-10',
        'contact_phone': '16140158366',
        'contact_wechat': '西湖龙井_wx'
    },
    22: {
        'id': 22,
        'title': '安塞尔亚当斯摄影集',
        'description': '限量签名版，银盐印相工艺说明',
        'price': 3000.0,
        'category': '图书教材',
        'image': None,
        'location': '西安雁塔区',
        'seller_id': 9,
        'seller_name': '山城旧物',
        'views': 652,
        'created_at': '2024-06-01',
        'contact_phone': '13740728046',
        'contact_wechat': None
    },
    23: {
        'id': 23,
        'title': '全唐诗宋版影印',
        'description': '四库全书底本，宣纸线装，书房珍藏',
        'price': 6500.0,
        'category': '图书教材',
        'image': None,
        'location': '上海徐汇区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 388,
        'created_at': '2024-01-28',
        'contact_phone': '15782374753',
        'contact_wechat': '咖啡不加糖_wx'
    },
    24: {
        'id': 24,
        'title': '辞海第一版',
        'description': '1936年初版，中国现代辞书开山之作',
        'price': 2500.0,
        'category': '图书教材',
        'image': None,
        'location': '南京玄武区',
        'seller_id': 8,
        'seller_name': '江边看日落',
        'views': 640,
        'created_at': '2024-12-19',
        'contact_phone': '15422660194',
        'contact_wechat': '江边看日落_wx'
    },
    25: {
        'id': 25,
        'title': '设计师原稿手稿',
        'description': '知名设计师手绘原稿，附签名证书',
        'price': 6500.0,
        'category': '图书教材',
        'image': None,
        'location': '武汉武昌区',
        'seller_id': 7,
        'seller_name': '火锅英雄',
        'views': 412,
        'created_at': '2024-11-14',
        'contact_phone': '14218135295',
        'contact_wechat': '火锅英雄_wx'
    },
    26: {
        'id': 26,
        'title': 'Hermes Birkin 30',
        'description': '金棕色金扣，Togo皮，刻印U，票证齐全',
        'price': 132700.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '深圳南山区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 161,
        'created_at': '2024-12-11',
        'contact_phone': None,
        'contact_wechat': '南方小渔_wx'
    },
    27: {
        'id': 27,
        'title': 'Hermes Kelly 28',
        'description': '大象灰银扣，Epsom皮，经典保值款',
        'price': 97600.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '深圳南山区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 523,
        'created_at': '2024-03-09',
        'contact_phone': '14216789850',
        'contact_wechat': '南方小渔_wx'
    },
    28: {
        'id': 28,
        'title': 'Chanel Classic Flap',
        'description': '黑金牛皮中号，芯片款，全套包装',
        'price': 62700.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '广州越秀区',
        'seller_id': 3,
        'seller_name': '西北偏北',
        'views': 292,
        'created_at': '2024-01-03',
        'contact_phone': '18117869910',
        'contact_wechat': '西北偏北_wx'
    },
    29: {
        'id': 29,
        'title': 'Chanel 2.55 Reissue',
        'description': '做旧牛皮，复古链条，经典款',
        'price': 45300.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '杭州滨江区',
        'seller_id': 5,
        'seller_name': '城市浪人',
        'views': 449,
        'created_at': '2024-07-01',
        'contact_phone': '19230776478',
        'contact_wechat': '城市浪人_wx'
    },
    30: {
        'id': 30,
        'title': 'LV Speedy 30老花',
        'description': '植鞣革蜜蜡色，无干裂，配锁头钥匙',
        'price': 8700.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '重庆南岸区',
        'seller_id': 10,
        'seller_name': '金陵十三少',
        'views': 109,
        'created_at': '2024-05-07',
        'contact_phone': '13716729990',
        'contact_wechat': '金陵十三少_wx'
    },
    31: {
        'id': 31,
        'title': 'LV Neverfull MM',
        'description': '经典老花，容量大，通勤必备',
        'price': 8800.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '广州天河区',
        'seller_id': 3,
        'seller_name': '西北偏北',
        'views': 593,
        'created_at': '2024-08-17',
        'contact_phone': '15319196777',
        'contact_wechat': None
    },
    32: {
        'id': 32,
        'title': 'Dior Lady Dior中号',
        'description': '黑色羊皮藤格纹，优雅百搭',
        'price': 37700.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '武汉洪山区',
        'seller_id': 7,
        'seller_name': '火锅英雄',
        'views': 290,
        'created_at': '2024-02-22',
        'contact_phone': '13593131979',
        'contact_wechat': '火锅英雄_wx'
    },
    33: {
        'id': 33,
        'title': 'Gucci Marmont中号',
        'description': '黑色丝绒，复古金扣，近新成色',
        'price': 12600.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '重庆南岸区',
        'seller_id': 10,
        'seller_name': '金陵十三少',
        'views': 647,
        'created_at': '2024-07-22',
        'contact_phone': '17042035886',
        'contact_wechat': '金陵十三少_wx'
    },
    34: {
        'id': 34,
        'title': 'Prada Galleria中号',
        'description': 'Saffiano皮革，十字纹，经典杀手包',
        'price': 17100.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '杭州滨江区',
        'seller_id': 5,
        'seller_name': '城市浪人',
        'views': 737,
        'created_at': '2024-07-05',
        'contact_phone': '13911250299',
        'contact_wechat': '城市浪人_wx'
    },
    35: {
        'id': 35,
        'title': '劳力士Submariner',
        'description': '绿水鬼，2023全套，贴膜使用',
        'price': 90000.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '上海徐汇区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 152,
        'created_at': '2024-10-19',
        'contact_phone': '17419233013',
        'contact_wechat': '咖啡不加糖_wx'
    },
    36: {
        'id': 36,
        'title': '劳力士Datejust 41',
        'description': '蓝盘钻刻，五珠链，保卡2022',
        'price': 69400.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '广州越秀区',
        'seller_id': 3,
        'seller_name': '西北偏北',
        'views': 341,
        'created_at': '2024-04-12',
        'contact_phone': '19711049999',
        'contact_wechat': '西北偏北_wx'
    },
    37: {
        'id': 37,
        'title': '卡地亚Tank Must',
        'description': '大号机械，蓝钢指针，鳄鱼皮表带',
        'price': 23400.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '上海浦东新区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 729,
        'created_at': '2024-09-10',
        'contact_phone': '14946553958',
        'contact_wechat': '咖啡不加糖_wx'
    },
    38: {
        'id': 38,
        'title': '欧米茄Seamaster',
        'description': '海马300，007同款，陶瓷圈',
        'price': 24300.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '成都锦江区',
        'seller_id': 6,
        'seller_name': '西湖龙井',
        'views': 784,
        'created_at': '2024-10-07',
        'contact_phone': '19475569635',
        'contact_wechat': '西湖龙井_wx'
    },
    39: {
        'id': 39,
        'title': '加拿大鹅Expedition',
        'description': '远征款亚洲版，狼毛领，极地防寒',
        'price': 9000.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '武汉武昌区',
        'seller_id': 7,
        'seller_name': '火锅英雄',
        'views': 699,
        'created_at': '2024-01-03',
        'contact_phone': None,
        'contact_wechat': '火锅英雄_wx'
    },
    40: {
        'id': 40,
        'title': 'Moncler Maya',
        'description': '经典亮面羽绒服，95%鹅绒，成色新',
        'price': 10500.0,
        'category': '服装鞋帽',
        'image': None,
        'location': '南京秦淮区',
        'seller_id': 8,
        'seller_name': '江边看日落',
        'views': 215,
        'created_at': '2024-11-09',
        'contact_phone': '14420099059',
        'contact_wechat': '江边看日落_wx'
    },
    41: {
        'id': 41,
        'title': 'Herman Miller Aeron',
        'description': '人体工学椅顶配，全功能调节，护腰',
        'price': 11800.0,
        'category': '家具家居',
        'image': None,
        'location': '北京海淀区',
        'seller_id': 1,
        'seller_name': '程序员老王',
        'views': 608,
        'created_at': '2024-12-05',
        'contact_phone': '14615614174',
        'contact_wechat': '程序员老王_wx'
    },
    42: {
        'id': 42,
        'title': 'Herman Miller Sayl',
        'description': '设计师款，Y-Tower支撑，多色可选',
        'price': 5100.0,
        'category': '家具家居',
        'image': None,
        'location': '成都锦江区',
        'seller_id': 6,
        'seller_name': '西湖龙井',
        'views': 90,
        'created_at': '2024-06-26',
        'contact_phone': '17585146293',
        'contact_wechat': '西湖龙井_wx'
    },
    43: {
        'id': 43,
        'title': '宜家POANG波昂椅',
        'description': '桦木贴面，头层牛皮，经典北欧风',
        'price': 2800.0,
        'category': '家具家居',
        'image': None,
        'location': '深圳南山区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 208,
        'created_at': '2024-10-24',
        'contact_phone': '18213326769',
        'contact_wechat': '南方小渔_wx'
    },
    44: {
        'id': 44,
        'title': 'B&O Beoplay A9',
        'description': '四代圆盘音响，房间自适应调音',
        'price': 16400.0,
        'category': '家具家居',
        'image': None,
        'location': '深圳福田区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 471,
        'created_at': '2024-12-11',
        'contact_phone': None,
        'contact_wechat': '南方小渔_wx'
    },
    45: {
        'id': 45,
        'title': 'B&O Beosound 2',
        'description': '圆锥铝制，360度音效，家居艺术品',
        'price': 15100.0,
        'category': '家具家居',
        'image': None,
        'location': '深圳南山区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 531,
        'created_at': '2024-01-28',
        'contact_phone': '16940547349',
        'contact_wechat': '南方小渔_wx'
    },
    46: {
        'id': 46,
        'title': '戴森V15 Detect',
        'description': '激光探测，智能调速，配全套吸头',
        'price': 3900.0,
        'category': '家具家居',
        'image': None,
        'location': '武汉武昌区',
        'seller_id': 7,
        'seller_name': '火锅英雄',
        'views': 247,
        'created_at': '2024-01-22',
        'contact_phone': '16557130035',
        'contact_wechat': None
    },
    47: {
        'id': 47,
        'title': '戴森HP09空气净化',
        'description': '冷暖净化三合一，甲醛实时监测',
        'price': 5800.0,
        'category': '家具家居',
        'image': None,
        'location': '西安碑林区',
        'seller_id': 9,
        'seller_name': '山城旧物',
        'views': 745,
        'created_at': '2024-09-13',
        'contact_phone': '16333966966',
        'contact_wechat': '山城旧物_wx'
    },
    48: {
        'id': 48,
        'title': '西门子洗碗机13套',
        'description': '晶蕾烘干，除菌99.99%，嵌入独立两用',
        'price': 5600.0,
        'category': '家具家居',
        'image': None,
        'location': '重庆江北区',
        'seller_id': 10,
        'seller_name': '金陵十三少',
        'views': 161,
        'created_at': '2024-05-02',
        'contact_phone': '18591363974',
        'contact_wechat': '金陵十三少_wx'
    },
    49: {
        'id': 49,
        'title': '博世洗烘套装',
        'description': '活氧洗，热泵烘，进口品质',
        'price': 10000.0,
        'category': '家具家居',
        'image': None,
        'location': '深圳福田区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 640,
        'created_at': '2024-02-13',
        'contact_phone': None,
        'contact_wechat': '南方小渔_wx'
    },
    50: {
        'id': 50,
        'title': '造作山雪沙发三人位',
        'description': '设计品牌，进口牛皮，羽绒填充',
        'price': 16200.0,
        'category': '家具家居',
        'image': None,
        'location': '深圳福田区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 786,
        'created_at': '2024-09-22',
        'contact_phone': '17293638503',
        'contact_wechat': '南方小渔_wx'
    },
    51: {
        'id': 51,
        'title': '梵几黑胡桃木餐桌',
        'description': '实木榫卯，环保木蜡油，东方美学',
        'price': 20100.0,
        'category': '家具家居',
        'image': None,
        'location': '杭州上城区',
        'seller_id': 5,
        'seller_name': '城市浪人',
        'views': 177,
        'created_at': '2024-11-28',
        'contact_phone': '18149682169',
        'contact_wechat': '城市浪人_wx'
    },
    52: {
        'id': 52,
        'title': '吱音抽屉柜',
        'description': '原创设计，白橡木，收纳空间大',
        'price': 8200.0,
        'category': '家具家居',
        'image': None,
        'location': '武汉江汉区',
        'seller_id': 7,
        'seller_name': '火锅英雄',
        'views': 480,
        'created_at': '2024-03-07',
        'contact_phone': '16864502486',
        'contact_wechat': '火锅英雄_wx'
    },
    53: {
        'id': 53,
        'title': '野兽派香薰蜡烛',
        'description': '艺术家联名款，大豆蜡，扩香持久',
        'price': 3100.0,
        'category': '家具家居',
        'image': None,
        'location': '深圳福田区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 343,
        'created_at': '2024-01-10',
        'contact_phone': '17172409658',
        'contact_wechat': '南方小渔_wx'
    },
    54: {
        'id': 54,
        'title': 'Diptyque浆果香薰',
        'description': '法国进口，Baies经典香，70g装',
        'price': 3700.0,
        'category': '家具家居',
        'image': None,
        'location': '西安碑林区',
        'seller_id': 9,
        'seller_name': '山城旧物',
        'views': 268,
        'created_at': '2024-08-22',
        'contact_phone': '15198429450',
        'contact_wechat': '山城旧物_wx'
    },
    55: {
        'id': 55,
        'title': 'Marvis牙膏收藏套装',
        'description': '12种口味限量版，复古铝管包装',
        'price': 2000.0,
        'category': '家具家居',
        'image': None,
        'location': '重庆江北区',
        'seller_id': 10,
        'seller_name': '金陵十三少',
        'views': 729,
        'created_at': '2024-05-17',
        'contact_phone': None,
        'contact_wechat': '金陵十三少_wx'
    },
    56: {
        'id': 56,
        'title': 'Trek Domane SL6',
        'description': '碳纤维公路车，IsoSpeed减震，Shimano 105',
        'price': 28800.0,
        'category': '运动户外',
        'image': None,
        'location': '深圳南山区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 280,
        'created_at': '2024-11-10',
        'contact_phone': None,
        'contact_wechat': '南方小渔_wx'
    },
    57: {
        'id': 57,
        'title': 'Specialized Tarmac SL7',
        'description': '顶级竞赛公路车，S-Works级别',
        'price': 42700.0,
        'category': '运动户外',
        'image': None,
        'location': '南京鼓楼区',
        'seller_id': 8,
        'seller_name': '江边看日落',
        'views': 124,
        'created_at': '2024-10-28',
        'contact_phone': '17976354180',
        'contact_wechat': '江边看日落_wx'
    },
    58: {
        'id': 58,
        'title': 'Giant TCR Advanced',
        'description': '台湾原产，PRO级套件，爬坡利器',
        'price': 21200.0,
        'category': '运动户外',
        'image': None,
        'location': '北京朝阳区',
        'seller_id': 1,
        'seller_name': '程序员老王',
        'views': 721,
        'created_at': '2024-04-05',
        'contact_phone': '19672350830',
        'contact_wechat': '程序员老王_wx'
    },
    59: {
        'id': 59,
        'title': '小布Brompton C Line',
        'description': '英伦折叠车，16寸，城市通勤神器',
        'price': 12200.0,
        'category': '运动户外',
        'image': None,
        'location': '南京玄武区',
        'seller_id': 8,
        'seller_name': '江边看日落',
        'views': 174,
        'created_at': '2024-09-08',
        'contact_phone': '17069401199',
        'contact_wechat': '江边看日落_wx'
    },
    60: {
        'id': 60,
        'title': '鸟车Birdy R20',
        'description': '德国设计，18寸，折叠后可登机',
        'price': 12500.0,
        'category': '运动户外',
        'image': None,
        'location': '西安碑林区',
        'seller_id': 9,
        'seller_name': '山城旧物',
        'views': 486,
        'created_at': '2024-12-17',
        'contact_phone': '19070407340',
        'contact_wechat': '山城旧物_wx'
    },
    61: {
        'id': 61,
        'title': 'Patagonia冲锋衣',
        'description': 'Gore-Tex Pro，高山级防护，终身保修',
        'price': 4000.0,
        'category': '运动户外',
        'image': None,
        'location': '杭州上城区',
        'seller_id': 5,
        'seller_name': '城市浪人',
        'views': 702,
        'created_at': '2024-04-27',
        'contact_phone': '18620399639',
        'contact_wechat': '城市浪人_wx'
    },
    62: {
        'id': 62,
        'title': '始祖鸟Beta AR',
        'description': '硬壳冲锋衣，Gore-Tex，温哥华产',
        'price': 5900.0,
        'category': '运动户外',
        'image': None,
        'location': '成都武侯区',
        'seller_id': 6,
        'seller_name': '西湖龙井',
        'views': 328,
        'created_at': '2024-05-08',
        'contact_phone': '14941039390',
        'contact_wechat': None
    },
    63: {
        'id': 63,
        'title': '始祖鸟Atom LT',
        'description': '棉服经典款，Coreloft保暖，轻量',
        'price': 3200.0,
        'category': '运动户外',
        'image': None,
        'location': '深圳南山区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 773,
        'created_at': '2024-12-05',
        'contact_phone': '18965804273',
        'contact_wechat': '南方小渔_wx'
    },
    64: {
        'id': 64,
        'title': '北面1996 Nuptse',
        'description': '美版700蓬，经典面包服，boxy版型',
        'price': 2600.0,
        'category': '运动户外',
        'image': None,
        'location': '武汉江汉区',
        'seller_id': 7,
        'seller_name': '火锅英雄',
        'views': 480,
        'created_at': '2024-04-27',
        'contact_phone': '17874019136',
        'contact_wechat': None
    },
    65: {
        'id': 65,
        'title': 'Patagonia Retro-X',
        'description': '抓绒外套，经典复古，环保再生材料',
        'price': 2000.0,
        'category': '运动户外',
        'image': None,
        'location': '武汉江汉区',
        'seller_id': 7,
        'seller_name': '火锅英雄',
        'views': 449,
        'created_at': '2024-06-10',
        'contact_phone': '15875529051',
        'contact_wechat': '火锅英雄_wx'
    },
    66: {
        'id': 66,
        'title': 'Burton单板雪板',
        'description': 'Custom系列，全能板，配固定器',
        'price': 5300.0,
        'category': '运动户外',
        'image': None,
        'location': '北京海淀区',
        'seller_id': 1,
        'seller_name': '程序员老王',
        'views': 547,
        'created_at': '2024-05-14',
        'contact_phone': '18132151928',
        'contact_wechat': '程序员老王_wx'
    },
    67: {
        'id': 67,
        'title': 'Salomon双板套装',
        'description': 'S/Max系列，钛合金边刃，高速稳定',
        'price': 7900.0,
        'category': '运动户外',
        'image': None,
        'location': '北京海淀区',
        'seller_id': 1,
        'seller_name': '程序员老王',
        'views': 596,
        'created_at': '2024-03-20',
        'contact_phone': '14096268397',
        'contact_wechat': '程序员老王_wx'
    },
    68: {
        'id': 68,
        'title': 'Sea to Summit帐篷',
        'description': '超轻双人帐，15D尼龙，四季可用',
        'price': 4300.0,
        'category': '运动户外',
        'image': None,
        'location': '广州天河区',
        'seller_id': 3,
        'seller_name': '西北偏北',
        'views': 522,
        'created_at': '2024-03-28',
        'contact_phone': '18853868501',
        'contact_wechat': '西北偏北_wx'
    },
    69: {
        'id': 69,
        'title': 'MSR Hubba Hubba',
        'description': '户外奥斯卡，双人三季，重量仅1.7kg',
        'price': 4600.0,
        'category': '运动户外',
        'image': None,
        'location': '杭州西湖区',
        'seller_id': 5,
        'seller_name': '城市浪人',
        'views': 481,
        'created_at': '2024-07-09',
        'contact_phone': '13656970882',
        'contact_wechat': '城市浪人_wx'
    },
    70: {
        'id': 70,
        'title': 'Osprey Atmos AG 65',
        'description': '反重力背负，透气腰带，重装徒步',
        'price': 2900.0,
        'category': '运动户外',
        'image': None,
        'location': '北京朝阳区',
        'seller_id': 1,
        'seller_name': '程序员老王',
        'views': 717,
        'created_at': '2024-11-03',
        'contact_phone': '13293394260',
        'contact_wechat': '程序员老王_wx'
    },
    71: {
        'id': 71,
        'title': '乐高泰坦尼克号',
        'description': '10294套装，9090颗粒，1.3米长',
        'price': 3800.0,
        'category': '其他',
        'image': None,
        'location': '上海徐汇区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 534,
        'created_at': '2024-04-05',
        'contact_phone': '16259512272',
        'contact_wechat': '咖啡不加糖_wx'
    },
    72: {
        'id': 72,
        'title': '乐高霍格沃茨城堡',
        'description': '71043套装，6020颗粒，魔法世界',
        'price': 3100.0,
        'category': '其他',
        'image': None,
        'location': '上海浦东新区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 785,
        'created_at': '2024-10-20',
        'contact_phone': '13351870192',
        'contact_wechat': '咖啡不加糖_wx'
    },
    73: {
        'id': 73,
        'title': '乐高兰博基尼Sian',
        'description': '42115套装，V12发动机，1:8比例',
        'price': 3300.0,
        'category': '其他',
        'image': None,
        'location': '深圳南山区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 456,
        'created_at': '2024-11-13',
        'contact_phone': '16123676961',
        'contact_wechat': '南方小渔_wx'
    },
    74: {
        'id': 74,
        'title': '万代PG独角兽高达',
        'description': '完美形态，精神感应框架发光，可爆甲',
        'price': 2200.0,
        'category': '其他',
        'image': None,
        'location': '重庆渝中区',
        'seller_id': 10,
        'seller_name': '金陵十三少',
        'views': 750,
        'created_at': '2024-05-28',
        'contact_phone': '13556600900',
        'contact_wechat': '金陵十三少_wx'
    },
    75: {
        'id': 75,
        'title': 'Hot Toys钢铁侠MK85',
        'description': '1/6兵人，合金压铸，战损配件',
        'price': 3500.0,
        'category': '其他',
        'image': None,
        'location': '上海徐汇区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 429,
        'created_at': '2024-07-22',
        'contact_phone': '18375793759',
        'contact_wechat': None
    },
    76: {
        'id': 76,
        'title': '泡泡玛特MOLLY限量',
        'description': '大娃限量款，艺术家联名，带证书',
        'price': 2800.0,
        'category': '其他',
        'image': None,
        'location': '南京秦淮区',
        'seller_id': 8,
        'seller_name': '江边看日落',
        'views': 700,
        'created_at': '2024-07-12',
        'contact_phone': None,
        'contact_wechat': '江边看日落_wx'
    },
    77: {
        'id': 77,
        'title': 'Bearbrick 1000%',
        'description': '积木熊，艺术家联名款，潮流收藏',
        'price': 11800.0,
        'category': '其他',
        'image': None,
        'location': '南京鼓楼区',
        'seller_id': 8,
        'seller_name': '江边看日落',
        'views': 601,
        'created_at': '2024-10-26',
        'contact_phone': '16453258988',
        'contact_wechat': '江边看日落_wx'
    },
    78: {
        'id': 78,
        'title': 'KAWS Companion',
        'description': 'Open Edition，搪胶公仔，潮流艺术',
        'price': 16000.0,
        'category': '其他',
        'image': None,
        'location': '深圳福田区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 511,
        'created_at': '2024-02-09',
        'contact_phone': '17313852048',
        'contact_wechat': '南方小渔_wx'
    },
    79: {
        'id': 79,
        'title': '村上隆太阳花',
        'description': '限量版画，签名编号，荧光色',
        'price': 13000.0,
        'category': '其他',
        'image': None,
        'location': '深圳福田区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 549,
        'created_at': '2024-06-06',
        'contact_phone': '16584597009',
        'contact_wechat': '南方小渔_wx'
    },
    80: {
        'id': 80,
        'title': '草间弥生南瓜',
        'description': '波点艺术，限量雕塑，亲笔签名',
        'price': 8300.0,
        'category': '其他',
        'image': None,
        'location': '深圳罗湖区',
        'seller_id': 4,
        'seller_name': '南方小渔',
        'views': 137,
        'created_at': '2024-09-07',
        'contact_phone': '16073900135',
        'contact_wechat': '南方小渔_wx'
    },
    81: {
        'id': 81,
        'title': 'Supreme Box Logo',
        'description': '卫衣经典款，FW23，全新带吊',
        'price': 7000.0,
        'category': '其他',
        'image': None,
        'location': '上海静安区',
        'seller_id': 2,
        'seller_name': '咖啡不加糖',
        'views': 67,
        'created_at': '2024-08-26',
        'contact_phone': '16999115205',
        'contact_wechat': '咖啡不加糖_wx'
    },
    82: {
        'id': 82,
        'title': 'Palace Tri-Ferg',
        'description': '卫衣/外套，滑板品牌，限定配色',
        'price': 4300.0,
        'category': '其他',
        'image': None,
        'location': '西安碑林区',
        'seller_id': 9,
        'seller_name': '山城旧物',
        'views': 616,
        'created_at': '2024-06-16',
        'contact_phone': '17257219209',
        'contact_wechat': '山城旧物_wx'
    },
    83: {
        'id': 83,
        'title': 'Stanley冰霸杯套装',
        'description': '限量色组合，40oz+20oz，保温保冷',
        'price': 3400.0,
        'category': '其他',
        'image': None,
        'location': '杭州西湖区',
        'seller_id': 5,
        'seller_name': '城市浪人',
        'views': 363,
        'created_at': '2024-08-09',
        'contact_phone': None,
        'contact_wechat': '城市浪人_wx'
    },
    84: {
        'id': 84,
        'title': 'Wedgwood浮雕餐具',
        'description': '英国皇室御用，骨瓷茶具套装',
        'price': 4400.0,
        'category': '其他',
        'image': None,
        'location': '广州天河区',
        'seller_id': 3,
        'seller_name': '西北偏北',
        'views': 756,
        'created_at': '2024-12-18',
        'contact_phone': '19790099897',
        'contact_wechat': '西北偏北_wx',
        'brand': 'Wedgwood',
        'model': 'Wild Strawberry',
        'purchase_time': '2023-06-10',
        'purchase_source': '英国官网'
    },
    85: {
        'id': 85,
        'title': 'Meissen蓝洋葱',
        'description': '德国梅森，手绘瓷器，第一刀标',
        'price': 7300.0,
        'category': '其他',
        'image': None,
        'location': '杭州西湖区',
        'seller_id': 5,
        'seller_name': '城市浪人',
        'views': 248,
        'created_at': '2024-02-27',
        'contact_phone': '19826989677',
        'contact_wechat': '城市浪人_wx'
    },
}

# 总计 85 个高端商品


# 模拟收藏数据
favorites = {}

# 模拟消息数据
messages = {}

# ============== 辅助函数 ==============

def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """获取当前登录用户"""
    user_id = session.get('user_id')
    if user_id:
        return users.get(user_id)
    return None

# ============== 路由 ==============

@app.route('/')
def index():
    """首页 - 商品列表"""
    # 获取查询参数
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    
    # 筛选商品
    item_list = list(items.values())
    
    if category:
        # 分类映射
        category_map = {
            'electronics': '数码电子',
            'books': '图书教材',
            'clothes': '服装鞋帽',
            'furniture': '家具家居',
            'sports': '运动户外',
            'others': '其他'
        }
        cat_name = category_map.get(category, category)
        item_list = [item for item in item_list if item['category'] == cat_name]
    
    if search:
        item_list = [item for item in item_list 
                    if search.lower() in item['title'].lower() 
                    or search.lower() in item['description'].lower()]
    
    # 排序
    if sort == 'price_asc':
        item_list.sort(key=lambda x: x['price'])
    elif sort == 'price_desc':
        item_list.sort(key=lambda x: x['price'], reverse=True)
    else:  # newest
        item_list.sort(key=lambda x: x['created_at'], reverse=True)
    
    # 分页（简化版）
    per_page = 12
    total = len(item_list)
    start = (page - 1) * per_page
    end = start + per_page
    item_list = item_list[start:end]
    
    # 创建分页对象（简化版）
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
    
    # 分类标题映射
    category_titles = {
        'electronics': '数码电子',
        'books': '图书教材',
        'clothes': '服装鞋帽',
        'furniture': '家具家居',
        'sports': '运动户外',
        'others': '其他臻品'
    }
    category_title = category_titles.get(category, '') if category else ''

    return render_template('index.html',
                         items=item_list,
                         pagination=pagination,
                         users=users,
                         current_category=category,
                         current_sort=sort,
                         category_title=category_title)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    """商品详情页"""
    item = items.get(item_id)
    if not item:
        flash('商品不存在', 'danger')
        return redirect(url_for('index'))
    
    # 增加浏览量
    item['views'] = item.get('views', 0) + 1
    
    # 获取相关推荐（同分类的其他商品）
    related_items = [
        i for i in items.values() 
        if i['category'] == item['category'] and i['id'] != item_id
    ][:4]
    
    # 添加卖家额外信息
    seller = users.get(item['seller_id'], {})
    item['seller_avatar'] = seller.get('avatar', '[用户]')
    item['seller_bio'] = seller.get('bio', '')
    item['seller_joined'] = seller.get('created_at', '')
    item['seller_items_count'] = len([i for i in items.values() if i['seller_id'] == item['seller_id']])
    
    return render_template('detail.html', item=item, related_items=related_items)

@app.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    """发布商品"""
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
        
        # 验证
        if not title or not price or not category or not description:
            flash('请填写所有必填项', 'danger')
            return redirect(url_for('publish'))
        
        # 处理图片上传
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        # 分类映射
        category_map = {
            'electronics': '数码电子',
            'books': '图书教材',
            'clothes': '服装鞋帽',
            'furniture': '家具家居',
            'sports': '运动户外',
            'others': '其他'
        }
        
        # 创建新商品
        new_id = max(items.keys()) + 1 if items else 1
        user = get_current_user()
        
        items[new_id] = {
            'id': new_id,
            'title': title,
            'description': description,
            'price': price,
            'category': category_map.get(category, category),
            'image': image,
            'location': location,
            'seller_id': user['id'],
            'seller_name': user['username'],
            'views': 0,
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'contact_phone': contact_phone or None,
            'contact_wechat': contact_wechat or None,
            'brand': brand or None,
            'model': model or None,
            'purchase_time': purchase_time or None,
            'purchase_source': purchase_source or None
        }
        
        flash('商品发布成功！', 'success')
        return redirect(url_for('item_detail', item_id=new_id))
    
    return render_template('publish.html')

@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """编辑商品"""
    item = items.get(item_id)
    if not item:
        flash('商品不存在', 'danger')
        return redirect(url_for('index'))
    
    if item['seller_id'] != session.get('user_id'):
        flash('无权编辑此商品', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # 更新商品信息
        item['title'] = request.form.get('title', '').strip()
        item['price'] = request.form.get('price', type=float)
        item['description'] = request.form.get('description', '').strip()
        item['location'] = request.form.get('location', '').strip()
        item['brand'] = request.form.get('brand', '').strip() or None
        item['model'] = request.form.get('model', '').strip() or None
        item['purchase_time'] = request.form.get('purchase_time', '').strip() or None
        item['purchase_source'] = request.form.get('purchase_source', '').strip() or None
        
        flash('商品更新成功！', 'success')
        return redirect(url_for('item_detail', item_id=item_id))
    
    return render_template('publish.html', item=item)  # 可以创建单独的编辑模板

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # 验证用户（简化版）
        user = None
        for u in users.values():
            if u['username'] == username or u['email'] == username:
                if u['password'] == password:  # 实际项目中需要验证哈希
                    user = u
                    break
        
        if user:
            session['user_id'] = user['id']
            flash('登录成功！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """注册"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        
        # 验证
        if not username or not email or not password:
            flash('请填写所有必填项', 'danger')
            return redirect(url_for('register'))
        
        # 检查用户名和邮箱是否已存在
        for u in users.values():
            if u['username'] == username:
                flash('用户名已存在', 'danger')
                return redirect(url_for('register'))
            if u['email'] == email:
                flash('邮箱已被注册', 'danger')
                return redirect(url_for('register'))
        
        # 创建新用户
        new_id = max(users.keys()) + 1 if users else 1
        users[new_id] = {
            'id': new_id,
            'username': username,
            'email': email,
            'phone': phone or None,
            'password': password,  # 实际项目中需要哈希存储
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        
        flash('注册成功！请登录', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """退出登录"""
    session.pop('user_id', None)
    flash('已退出登录', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    """个人中心"""
    user = get_current_user()
    user_id = user['id']
    
    # 获取用户的商品
    my_items = [item for item in items.values() if item['seller_id'] == user_id]
    
    # 获取用户的收藏
    user_favorites = favorites.get(user_id, [])
    favorite_items = [items.get(fid) for fid in user_favorites if fid in items]
    
    # 获取用户的消息
    user_messages = messages.get(user_id, [])
    
    return render_template('profile.html', 
                         user=user, 
                         my_items=my_items, 
                         favorites=favorite_items,
                         messages=user_messages)

@app.route('/user/<int:user_id>')
def user_items(user_id):
    """用户主页 - 查看其他用户的商品"""
    user = users.get(user_id)
    if not user:
        flash('用户不存在', 'danger')
        return redirect(url_for('index'))
    
    user_items_list = [item for item in items.values() if item['seller_id'] == user_id]
    
    return render_template('index.html', items=user_items_list)  # 可以创建专门的用户主页模板

# ============== API 路由 ==============

@app.route('/api/favorites', methods=['POST'])
@login_required
def add_favorite():
    """添加收藏"""
    data = request.get_json()
    item_id = data.get('item_id')
    user_id = session.get('user_id')
    
    if item_id not in items:
        return jsonify({'success': False, 'message': '商品不存在'})
    
    if user_id not in favorites:
        favorites[user_id] = []
    
    if item_id in favorites[user_id]:
        return jsonify({'success': False, 'message': '已经收藏过了'})
    
    favorites[user_id].append(item_id)
    return jsonify({'success': True, 'message': '收藏成功'})

@app.route('/api/favorites/<int:item_id>', methods=['DELETE'])
@login_required
def remove_favorite(item_id):
    """取消收藏"""
    user_id = session.get('user_id')
    
    if user_id in favorites and item_id in favorites[user_id]:
        favorites[user_id].remove(item_id)
        return jsonify({'success': True, 'message': '已取消收藏'})
    
    return jsonify({'success': False, 'message': '收藏不存在'})

@app.route('/api/items')
def api_items():
    """获取商品列表 API（支持分类筛选和排序）"""
    category = request.args.get('category', '')
    sort = request.args.get('sort', 'newest')
    
    item_list = list(items.values())
    
    if category:
        category_map = {
            'electronics': '数码电子',
            'books': '图书教材',
            'clothes': '服装鞋帽',
            'furniture': '家具家居',
            'sports': '运动户外',
            'others': '其他'
        }
        cat_name = category_map.get(category, category)
        item_list = [item for item in item_list if item['category'] == cat_name]
    
    # 排序
    if sort == 'price_asc':
        item_list.sort(key=lambda x: x['price'])
    elif sort == 'price_desc':
        item_list.sort(key=lambda x: x['price'], reverse=True)
    else:
        item_list.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({
        'success': True,
        'items': item_list
    })

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item_api(item_id):
    """删除商品 API"""
    item = items.get(item_id)
    if not item:
        return jsonify({'success': False, 'message': '商品不存在'})
    
    if item['seller_id'] != session.get('user_id'):
        return jsonify({'success': False, 'message': '无权删除'})
    
    del items[item_id]
    return jsonify({'success': True, 'message': '删除成功'})

# ============== 错误处理 ==============

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    flash('页面不存在', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    flash('服务器内部错误', 'danger')
    return redirect(url_for('index'))

# ============== 上下文处理器 ==============

@app.context_processor
def inject_globals():
    """向模板注入全局变量"""
    return {
        'now': datetime.now(),
        'site_name': '中古·回想'
    }














# ============== 启动 ==============

if __name__ == '__main__':
    # 确保上传目录存在
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
