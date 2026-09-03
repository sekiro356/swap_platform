# 物换物平台（swap_platform）项目上下文

## 一、项目简介

项目名称：`swap_platform`

项目目标：开发一个完整的“以物换物平台”后端项目，并逐步加入数据分析、机器学习、NLP/LLM、LangChain/LangGraph、Redis、RabbitMQ、Docker、Linux、Nginx 等技术。

项目定位：

> 从基础 FastAPI CRUD 项目逐步升级为具备真实业务逻辑、权限控制、数据分析、机器学习和 AI 能力的综合项目。

最终用于：

- 项目实践
- 技术学习
- GitHub 展示
- 简历项目
- 面试项目介绍

------

# 二、当前技术栈

## 后端基础

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- MySQL

## 用户认证

- bcrypt
- JWT
- PyJWT
- HTTPBearer

## 后续计划

- Redis
- RabbitMQ
- NumPy
- Pandas
- Matplotlib
- Seaborn
- scikit-learn
- KNN
- XGBoost
- NLP
- Embedding
- 向量数据库 / pgvector
- LangChain
- LangGraph
- Docker
- Linux
- Nginx

------

# 三、当前项目结构

```text
swap_platform/
├── .gitignore
├── requirements.txt
├── requirements_full.txt
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── routers/
│       ├── users.py
│       ├── items.py
│       └── swaps.py
├── frontend/
└── PROJECT_CONTEXT.md
```

目前主要业务代码仍然集中在 `backend/main.py` 中。

后续项目变大后，再逐步将业务拆到 `routers/`。

------

# 四、数据库

当前使用：

- MySQL
- SQLAlchemy ORM

数据库连接通过 `.env` 中的 `DATABASE_URL` 配置。

`database.py` 负责：

```python
engine
SessionLocal
Base
```

并通过：

```python
Base.metadata.create_all(bind=engine)
```

启动时自动创建不存在的表。

------

# 五、当前数据库模型

## 1. User 用户表

```python
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
```

主要字段：

```text
id
username
password
```

密码数据库中保存的是 bcrypt 哈希，而不是明文密码。

------

## 2. Items 物品表

当前模型名称使用：

```python
class Items(Base):
```

表名：

```python
__tablename__ = 'items'
```

字段：

```text
id
name
description
category
price
user_id
```

当前模型：

```python
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
```

其中：

```text
user_id = 物品发布者
```

------

## 3. Swap 交换申请表

当前使用：

```python
class Swap(Base):
    __tablename__ = 'swap'
```

字段：

```text
id
requester_id
target_item_id
offered_item_id
status
```

含义：

```text
requester_id
→ 谁发起交换

target_item_id
→ 想要交换得到的物品

offered_item_id
→ 发起者拿出来交换的物品

status
→ 当前交换状态
```

目前状态：

```text
pending
accepted
rejected
```

当前默认：

```python
status = 'pending'
```

------

# 六、用户认证模块

## 注册

接口：

```text
POST /register
```

流程：

```text
客户端提交用户名、密码
        ↓
查询用户名是否存在
        ↓
bcrypt 加密密码
        ↓
保存 User
        ↓
返回注册成功
```

------

## 登录

接口：

```text
POST /login
```

流程：

```text
用户名 + 密码
       ↓
查询用户
       ↓
bcrypt.checkpw()
       ↓
密码正确
       ↓
create_access_token(user_id)
       ↓
返回 JWT
```

返回：

```json
{
    "messages": "登陆成功",
    "user_id": 2,
    "user_name": "xxx",
    "access_token": "xxxxx",
    "token_type": "bearer"
}
```

------

# 七、JWT 认证

`auth.py` 使用：

```python
HTTPBearer()
```

从请求头获取：

```text
Authorization: Bearer <JWT>
```

JWT 中保存：

```python
{
    "user_id": user_id,
    "exp": ...
}
```

通过：

```python
get_current_user()
```

解析 JWT，并查询数据库中的 User。

因此：

```python
current_user.id
```

就是当前登录用户的 ID。

------

# 八、Swagger 鉴权

在 Swagger：

```text
http://127.0.0.1:8000/docs
```

点击：

```text
Authorize
```

只输入：

```text
JWT_TOKEN
```

不要手动输入：

```text
Bearer JWT_TOKEN
```

因为 `HTTPBearer` 会自动处理 `Bearer`。

------

# 九、Item 物品模块

目前已经完成基础 CRUD。

## 1. 发布物品

```text
POST /items
```

需要 JWT。

当前登录用户自动成为：

```python
user_id = current_user.id
```

客户端不需要传 `user_id`。

------

## 2. 查询全部物品

```text
GET /items
```

目前不要求登录。

返回所有物品。

------

## 3. 查询单个物品

```text
GET /items/{item_id}
```

目前不要求登录。

------

## 4. 修改物品

```text
PUT /items/{item_id}
```

需要 JWT。

并且：

```python
db_item.user_id == current_user.id
```

只有物品所有者可以修改。

否则：

```text
403
无权限修改此物品
```

------

## 5. 删除物品

```text
DELETE /items/{item_id}
```

需要 JWT。

同样必须满足：

```python
db_item.user_id == current_user.id
```

只有物品所有者可以删除。

------

# 十、Swap 交换模块

目前已经开始开发。

## 1. 发起交换申请

接口：

```text
POST /swaps
```

请求：

```json
{
    "target_item_id": 8,
    "offered_item_id": 3
}
```

其中：

```text
target_item_id
→ 想要的物品

offered_item_id
→ 自己拿出来交换的物品
```

后端自动获取：

```python
requester_id = current_user.id
```

并设置：

```python
status = 'pending'
```

------

## 2. 已实现的业务校验

### 不能拿别人的物品交换

检查：

```python
offered_item.user_id != current_user.id
```

如果成立：

```text
403
不能拿别人的物品进行交换
```

------

### 不能和自己的物品交换

检查：

```python
target_item.user_id == current_user.id
```

如果成立：

```text
不能和自己的物品进行交换
```

------

## 3. 查询交换申请

接口：

```text
GET /swaps
```

需要 JWT。

查询两类数据：

```text
① 当前用户发起的交换

② 别人向当前用户物品发起的交换
```

核心查询：

```python
swaps = db.query(Swap).join(
    Items,
    Swap.target_item_id == Items.id
).filter(
    (Swap.requester_id == current_user.id) |
    (Items.user_id == current_user.id)
).all()
```

其中：

```text
join
→ 将 Swap 和 Items 连接起来

|
→ OR / 或者

current_user.id
→ 当前登录用户的 ID
```

------

# 十一、最近遇到的问题

## SQLAlchemy Table 重复定义

曾经出现：

```text
sqlalchemy.exc.InvalidRequestError:
Table 'users' is already defined for this MetaData instance.
```

原因最终定位为 `main.py` 同时存在：

```python
from backend.models import Swap
from models import User, Items, Swap
```

导致同一个 models 文件可能被 Python 按不同模块路径加载。

正确做法：

```python
from models import User, Items, Swap
```

不要同时混用：

```python
from backend.models import ...
```

当前项目保持现有的：

```python
from models import ...
from database import ...
from auth import ...
```

导入方式即可。

------

# 十二、当前代码风格

目前为了方便学习，数据库 Session 使用：

```python
db = SessionLocal()
```

操作完成后：

```python
db.close()
```

暂时不急着改成更复杂的数据库依赖注入。

等基础业务完成后，再统一优化：

```python
get_db()
```

------

# 十三、当前项目业务流程

目前已经形成：

```text
用户注册
   ↓
用户登录
   ↓
获得 JWT
   ↓
Swagger 携带 JWT
   ↓
发布物品
   ↓
查询物品
   ↓
修改 / 删除自己的物品
   ↓
发起交换申请
   ↓
查看交换申请
```

下一步：

```text
别人收到交换申请
        ↓
验证是否是目标物品的主人
        ↓
接受 / 拒绝
        ↓
pending
   ↙       ↘
accepted  rejected
```

------

# 十四、本周剩余任务

当前 Swap 模块还剩：

## 1. 接受交换

```text
PUT /swaps/{swap_id}/accept
```

要求：

> 只有目标物品的所有者才能接受交换。

------

## 2. 拒绝交换

```text
PUT /swaps/{swap_id}/reject
```

要求：

> 只有目标物品的所有者才能拒绝交换。

------

## 3. 完整测试

测试：

```text
用户A
 ↓
发布物品A

用户B
 ↓
发布物品B

A
 ↓
申请交换B的物品

B
 ↓
查看交换申请

B
 ↓
接受/拒绝

Swap状态：
pending → accepted
或
pending → rejected
```

同时测试非法操作：

```text
A不能拿B的物品交换
A不能和自己的物品交换
A不能接受自己发出的交换申请
非目标物品所有者不能接受/拒绝
```

------

# 十五、本周 Git 提交

Swap 模块完成后：

```bash
git add .
git commit -m "完成交换申请模块"
git push origin master
```

------

# 十六、后续项目路线

## 阶段一：后端基础

```text
FastAPI
SQLAlchemy
MySQL
Pydantic
JWT
bcrypt
```

状态：

```text
基本完成
```

------

## 阶段二：核心业务

```text
User
Item
Swap
```

当前：

```text
User       ✅
Item       ✅
Swap       🔄
```

------

## 阶段三：数据分析

使用真实业务数据：

```text
NumPy
Pandas
Matplotlib
Seaborn
```

分析内容例如：

```text
用户数量
物品分类分布
物品价格分布
交换次数
热门物品类别
用户活跃度
交换成功率
```

------

## 阶段四：机器学习

使用项目真实数据进行：

```text
特征工程
↓
scikit-learn
↓
KNN
↓
物品推荐 / 相似物品
```

数据量足够后再考虑：

```text
XGBoost
```

------

## 阶段五：NLP / LLM

对用户自然语言描述的物品进行：

```text
文本清洗
↓
关键词 / 属性提取
↓
Embedding
↓
语义相似度
↓
智能匹配
```

例如用户输入：

```text
“九成新苹果无线耳机，想换一个机械键盘”
```

系统提取：

```text
类别：数码
物品：无线耳机
品牌：苹果
成色：九成新
交换意向：机械键盘
```

------

## 阶段六：LangChain / LangGraph

加入：

```text
Tool
Agent
RAG
Memory
Workflow
```

实现例如：

```text
智能交换助手
```

可以帮助用户：

```text
查询物品
分析物品
寻找合适交换对象
推荐相似物品
回答平台相关问题
```

------

## 阶段七：工程化

加入：

```text
Redis
RabbitMQ
Docker
Linux
Nginx
```

最终形成：

```text
FastAPI
   ↓
Nginx
   ↓
Redis
   ↓
RabbitMQ
   ↓
MySQL
   ↓
AI / ML 服务
```

------

# 十七、项目最终目标

最终项目不只是：

```text
登录
CRUD
```

而是：

```text
用户
 ↓
发布物品
 ↓
浏览物品
 ↓
交换申请
 ↓
权限控制
 ↓
交换状态管理
 ↓
数据分析
 ↓
机器学习推荐
 ↓
NLP物品理解
 ↓
Embedding语义匹配
 ↓
LangChain / LangGraph AI助手
 ↓
Redis / RabbitMQ
 ↓
Docker + Linux + Nginx部署
```

最终形成一个可以用于：

> **简历 + GitHub + 面试讲解**

的完整 AI + 后端综合项目。