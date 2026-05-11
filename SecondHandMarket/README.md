# 中古·回想 - 高端二手交易平台

## 项目概述

"中古·回想"（SecondHandMarket）是一个定位高端的二手物品交易平台。项目设计风格以黑金古典为主调，融合怀旧胶片质感，营造出优雅、精致的交易氛围。平台采用模拟数据驱动，以 Flask 框架提供完整的 CRUD 功能，涵盖用户认证、商品发布与管理、收藏、搜索排序等核心交易场景。

> "中古"一词源自日语，意为"二手"；"回想"则传递出每一件旧物都承载着记忆与温度的品牌理念。

---

## 功能特性

| 模块 | 功能 | 说明 |
|------|------|------|
| 用户认证 | 注册 / 登录 / 退出 | 支持用户名或邮箱登录，基于 Session 会话管理 |
| 商品管理 | 发布 / 编辑 / 删除 | 支持标题、价格、分类、描述、多维度属性（品牌、型号、购买来源等） |
| 图片上传 | 单图上传 / 拖拽 / 预览 | 限制格式 png/jpg/jpeg/gif，最大 16MB |
| 商品浏览 | 列表 / 详情 / 翻页 | 卡片式商品网格，支持分类导航与分页 |
| 搜索排序 | 关键词搜索 / 排序筛选 | 按最新、价格正序/倒序排列 |
| 收藏系统 | 添加 / 取消收藏 | 基于 AJAX 的异步操作 |
| 个人中心 | 我的发布 / 收藏 / 消息 / 设置 | 多 Tab 切换式管理面板 |
| 卖家主页 | 查看卖家所有商品 | 卖家信息展示与商品集合 |
| 联系卖家 | 弹窗展示联系方式 | 手机号、微信号查看 |
| 系列推荐 | 同分类商品推荐 | 详情页底部展示 4 个相关推荐 |
| 仪表盘 | 轮播图 Banner | 3 张轮播图，5 秒自动切换，悬停暂停 |
| 分类导航 | 滑动指示器 | 带滑动指示条的 Tab 式分类筛选，支持 AJAX 无刷新加载 |

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端框架 | Flask 3.0 | Python Web 框架 |
| 模板引擎 | Jinja2 | 服务端渲染，模板继承 |
| 数据存储 | 内存字典 | 模拟数据，实际项目建议迁移至 MySQL / PostgreSQL |
| 前端样式 | 原生 CSS (自研) | 黑金古典风格，全响应式布局 |
| 前端交互 | 原生 JavaScript | 无框架依赖，ES6 语法 |
| 图标库 | Font Awesome 6.4 | 矢量图标 |
| 字体 | Google Fonts | Inter / Cormorant Garamond / Noto Serif SC |
| 依赖管理 | pip | requirements.txt |

---

## 项目结构

```
SecondHandMarket/
|-- run.py                  # 启动入口（python run.py）
|-- requirements.txt        # Python 依赖
|-- app_old.py              # 原单文件版本（留作参考）
|-- app/                    # 核心代码包
|   |-- __init__.py         # 应用工厂（create_app 函数）
|   |-- models.py           # 数据模型（users/items/favorites/messages）
|   |-- routes/
|   |   |-- __init__.py     # 注册所有 Blueprint
|   |   |-- auth.py         # 登录/注册/退出
|   |   |-- items.py        # 商品首页/详情/发布/编辑
|   |   |-- profile.py      # 个人中心/账号设置
|   |   |-- api.py          # JSON 接口（收藏/删除/异步加载）
|-- templates/              # Jinja2 模板
|   |-- base.html           # 基础模板（导航栏、Flash 消息、页脚）
|   |-- index.html          # 首页：轮播图 + 分类导航 + 商品网格 + 分页
|   |-- detail.html         # 商品详情：图片/信息/卖家卡片/相关推荐/联系弹窗
|   |-- publish.html        # 发布/编辑商品表单
|   |-- edit.html           # 编辑商品表单（独立模板）
|   |-- login.html          # 登录页
|   |-- register.html       # 注册页（含前端表单校验）
|   |-- profile.html        # 个人中心：四 Tab 管理面板
|-- static/                 # 静态资源
    |-- css/
    |   |-- style.css       # 全局样式（2287 行），黑金古典设计系统
    |-- js/
    |   |-- main.js         # 前端交互脚本，约 600 行
```

---

## 数据模型

### 用户 (users)

内存字典存储，键为用户 ID，默认预置 10 个模拟用户。

```python
{
    'id': int,              # 用户 ID（主键）
    'username': str,        # 用户名
    'email': str,           # 邮箱
    'phone': str,           # 手机号
    'password': str,        # 密码（明文存储，生产环境需哈希处理）
    'avatar': str,          # 头像标识
    'city': str,            # 所在城市
    'bio': str,             # 个人简介
    'created_at': str       # 注册时间
}
```

### 商品 (items)

内存字典存储，键为商品 ID，默认预置 85 个高端商品，涵盖六大分类。

```python
{
    'id': int,                  # 商品 ID（主键）
    'title': str,               # 商品标题
    'description': str,         # 商品描述
    'price': float,             # 价格
    'category': str,            # 分类（枚举值之一）
    'image': str or None,       # 图片文件名
    'location': str,            # 交易地点
    'seller_id': int,           # 卖家用户 ID
    'seller_name': str,         # 卖家名称
    'views': int,               # 浏览量
    'created_at': str,          # 发布时间
    'contact_phone': str/None,  # 联系手机
    'contact_wechat': str/None, # 微信号
    'brand': str/None,          # 品牌
    'model': str/None,          # 型号
    'purchase_time': str/None,  # 购买时间
    'purchase_source': str/None # 购买来源
}
```

### 商品分类

| 路由 Key | 中文名称 | 预置数量 |
|----------|----------|----------|
| electronics | 数码电子 | 15 件 |
| books | 图书教材 | 10 件 |
| clothes | 服装鞋帽 | 15 件 |
| furniture | 家具家居 | 15 件 |
| sports | 运动户外 | 15 件 |
| others | 其他臻品 | 15 件 |

### 其他数据

- **favorites**: `{ user_id: [item_id, ...] }` 结构，记录每个用户收藏的商品 ID 列表
- **messages**: `{ user_id: [message, ...] }` 结构，记录用户收到的消息

---

## 路由清单

### 页面路由

| 路由 | 方法 | Blueprint | 视图函数 | 说明 | 需登录 |
|------|------|-----------|----------|------|--------|
| `/` | GET | items | `index` | 首页，支持 `category`/`search`/`sort`/`page` 参数 | 否 |
| `/item/<int:item_id>` | GET | items | `item_detail` | 商品详情页 | 否 |
| `/publish` | GET/POST | items | `publish` | 发布商品 | 是 |
| `/item/<int:item_id>/edit` | GET/POST | items | `edit_item` | 编辑商品（仅卖家） | 是 |
| `/auth/login` | GET/POST | auth | `login` | 用户登录 | 否 |
| `/auth/register` | GET/POST | auth | `register` | 用户注册 | 否 |
| `/auth/logout` | GET | auth | `logout` | 退出登录 | 否 |
| `/profile/` | GET | profile | `index` | 个人中心 | 是 |
| `/profile/settings` | POST | profile | `settings` | 更新账号设置 | 是 |
| `/user/<int:user_id>` | GET | items | `user_items` | 查看用户发布的商品 | 否 |

### API 路由

| 路由 | 方法 | Blueprint | 视图函数 | 说明 | 需登录 |
|------|------|-----------|----------|------|--------|
| `/api/favorites` | POST | api | `add_favorite` | 添加收藏 | 是 |
| `/api/favorites/<int:item_id>` | DELETE | api | `remove_favorite` | 取消收藏 | 是 |
| `/api/items` | GET | api | `api_items` | 获取商品列表 JSON（支持分类/排序） | 否 |
| `/api/items/<int:item_id>` | DELETE | api | `delete_item_api` | 删除商品（仅卖家） | 是 |

### 上下文注入

| 变量 | 说明 |
|------|------|
| `now` | 当前时间 (`datetime.now()`) |
| `site_name` | 站点名称："中古·回想" |

---

## 设计系统

### 品牌色板

| 色值 | 用途 | CSS 变量 |
|------|------|----------|
| `#0d0d0d` | 深色背景底色 | `--bg-primary` |
| `#f5f0e8` | 正文文字色 | `--text-primary` |
| `#d4af37` | 金色强调色 | `--accent-warm` |
| `#c9a227` | 金色强调色(深) | `--accent-gold` |
| `#8b7355` | 金色辅助色 | `--accent-gold-dark` |
| `#2d2d2d` | 边框色 | `--border-color` |
| `#4a3f2a` | 金色边框 | `--border-gold` |

### 字体系统

- **西文无衬线**: `Inter` (正文 UI)
- **中文衬线**: `Noto Serif SC` (标题 / 装饰元素)
- **展示字体**: `Cormorant Garamond` (品牌文字)
- **等宽字体**: `JetBrains Mono` (监控 / 代码)

### 设计语言

- 深色背景 + 金色点缀，营造黑金复古美学
- 纸质纹理微网格 + 径向渐变光晕，模拟旧纸张质感
- 按钮使用金色渐变，磨砂描边按钮配合玻璃态效果
- 边框使用伪元素渐变实现双线装饰效果
- 全站低饱和度色彩风格，搭配优雅的转场动画
- 响应式设计支持，覆盖 1024px / 768px / 480px 断点

---

## 页面展示

### 首页

- 顶部粘性导航栏 + 移动端汉堡菜单
- 3 张轮播 Banner（自动切换，5 秒间隔，悬停暂停）
- 横向分类 Tab 导航（带滑动指示器动画，支持 AJAX 无刷切换）
- 商品卡片网格（默认 4 列，响应式缩减）
- 自定义下拉选择框（排序：最新 / 价格升降）
- 搜索框（支持回车触发）
- 分页器（每页 12 件）

### 商品详情页

- 左侧商品大图 / 右侧信息面板
- 元数据展示：分类、品牌、型号、购买时间/来源
- 商品描述 + 操作按钮（联系卖家 / 收藏 / 编辑 / 删除）
- 卖家信息卡片（头像、简介、统计、进入卖家主页）
- 相关推荐（同分类商品，卡片横排）
- 联系弹窗（展示电话/微信 + 留言表单）

### 个人中心

- 左侧侧边栏：用户信息卡 + 功能导航
- 四 Tab 内容区：
  - 我的发布：列表展示，支持查看/编辑/删除
  - 我的收藏：商品卡片网格，支持移除
  - 我的消息：消息列表，未读标记
  - 账号设置：修改信息 / 密码（前端占位）

---

## 安装与运行

### 环境要求

- Python >= 3.8
- pip 包管理器

### 安装步骤

```bash
# 1. 进入项目目录
cd SecondHandMarket

# 2. 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python run.py
```

服务启动后访问 http://localhost:5000

### 预置账号

可使用以下任一账号登录（密码统一为 `password123`）：

| 用户名 | 邮箱 | 城市 | 个性标签 |
|--------|------|------|----------|
| 程序员老王 | laowang@qq.com | 北京 | 全栈开发，数码控 |
| 咖啡不加糖 | coffee@163.com | 上海 | 设计师，咖啡爱好者 |
| 西北偏北 | xibei@gmail.com | 西安 | 户外运动 |
| 南方小渔 | fish@126.com | 广州 | 研究生，摄影 |
| 城市浪人 | wave@qq.com | 深圳 | 滑板潮人 |
| 西湖龙井 | longjing@163.com | 杭州 | 茶文化 |
| 火锅英雄 | hotpot@qq.com | 成都 | 摄影美食 |
| 江边看日落 | sunset@126.com | 武汉 | 文艺大学生 |
| 山城旧物 | shan@163.com | 重庆 | 中古收藏 |
| 金陵十三少 | nanjing@qq.com | 南京 | 复古家具 |

---

## 注意事项

1. **数据存储**：当前使用内存字典存储数据，服务重启后数据丢失。建议在正式环境中集成 MySQL / PostgreSQL 等数据库。
2. **密码安全**：目前密码以明文存储和验证，生产环境务必使用 `werkzeug.security` 的 `generate_password_hash` 和 `check_password_hash` 加密处理。
3. **Secret Key**：`app.secret_key = 'your-secret-key-here'` 需替换为随机密钥。
4. **图片上传**：上的图片保存在 `static/images/` 目录下，生产环境建议使用对象存储服务（如阿里云 OSS、AWS S3）。
5. **依赖安装**：前端字体和图标库依赖 Google Fonts 和 CDN，若在内网环境需自行处理资源托管。

---

## 扩展建议

- 接入 SQLAlchemy ORM 实现持久化数据库
- 添加图片多图上传和画廊展示功能
- 实现即时通讯（WebSocket）替代留言系统
- 添加订单系统和交易流程管理
- 集成支付宝/微信支付支持
- 增加管理员后台管理系统
- 实现用户评分和信誉体系
- 添加商品状态跟踪（在售/已售/下架）

---

## License

MIT License