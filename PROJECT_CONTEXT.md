# 物换物平台（Swap Platform）项目上下文

## 1. 项目简介

这是一个基于 **FastAPI + MySQL + JWT + LangChain/LangGraph** 开发的 AI 物换物平台。

项目目标：

1. 实现一个可以实际运行的物换物平台 MVP。
2. 完成用户注册、登录、JWT 身份认证。
3. 实现用户发布、查询、管理自己的物品。
4. 实现用户之间的换物请求。
5. 后期加入 AI 能力：
   - LLM 结构化提取
   - Embedding
   - 向量检索
   - 智能物品匹配
   - LangChain
   - LangGraph
6. 最终形成一个可以用于：
   - 项目展示
   - GitHub
   - 简历
   - 面试讲解
     的完整项目。

------

# 2. 技术栈

## 后端

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic

## 用户认证

- bcrypt
- PyJWT
- HTTPBearer
- `.env`

## 后续 AI

- LangChain
- LangGraph
- Embedding
- 向量数据库 / pgvector
- LLM

## 前端

目前暂时以 FastAPI Swagger 为主要测试方式。

后续再开发：

- HTML
- CSS
- JavaScript

------

# 3. 项目结构

当前项目结构：

```text
swap_platform/
│
├── .gitignore
├── requirements.txt
├── PROJECT_CONTEXT.md
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   │
│   └── routers/
│       ├── users.py
│       ├── items.py
│       └── swaps.py
│
└── frontend/
```

目前核心功能主要暂时写在：

```text
backend/main.py
```

后续随着项目变大，再逐渐拆分到 `routers/` 中。

------

# 4. 当前项目完成情况

截至 2026-09-03，目前已经完成：

-  FastAPI 项目创建
-  MySQL 数据库连接
-  SQLAlchemy 配置
-  User 数据表
-  用户注册
-  bcrypt 密码加密
-  用户登录
-  JWT Token 生成
-  JWT Token 验证
-  HTTPBearer
-  FastAPI Depends 依赖注入
-  `/me` 获取当前登录用户
-  Swagger 中使用 JWT 测试接口

目前正在进入：

-  物品模块
-  发布物品
-  查询物品
-  物品详情
-  修改/删除物品

------

# 5. 数据库配置

`backend/database.py`：

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
```

数据库连接信息放在 `.env` 中。

例如：

```text
DATABASE_URL=mysql+pymysql://用户名:密码@localhost/数据库名
```

实际密码不要写入 GitHub。

------

# 6. 环境变量

项目使用 `.env` 保存敏感信息。

例如：

```text
DATABASE_URL=...
SECRET_KEY=...
```

`.env` 必须加入：

```text
.gitignore
```

不能上传到 GitHub。

------

# 7. User 数据模型

当前 `backend/models.py`：

```python
from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )
```

当前用户表：

```text
users
-----------------------------
id
username
password
```

------

# 8. 用户注册

当前注册接口：

```text
POST /register
```

请求：

```json
{
    "username": "老王",
    "password": "666666"
}
```

注册流程：

```text
用户提交用户名和密码
        ↓
查询 MySQL
        ↓
判断用户名是否存在
        ↓
bcrypt.hashpw()
        ↓
密码生成哈希
        ↓
保存 User
        ↓
MySQL
```

核心代码：

```python
hashed_password = bcrypt.hashpw(
    user.password.encode("utf8"),
    bcrypt.gensalt()
).decode("utf8")
```

------

# 9. bcrypt 密码加密

这里使用的是直接调用 `bcrypt`，没有继续使用 Passlib。

原因：

之前使用 Passlib bcrypt 时出现：

```text
ValueError:
password cannot be longer than 72 bytes
```

之后改成直接使用：

```python
bcrypt.hashpw()
```

### 密码加密过程

```python
user.password
```

是 Python 的：

```text
str
```

bcrypt 接收：

```text
bytes
```

所以：

```python
user.password.encode("utf8")
```

把：

```text
str
↓
bytes
```

然后：

```python
bcrypt.gensalt()
```

生成随机盐。

再：

```python
bcrypt.hashpw(password, salt)
```

生成密码哈希。

最后：

```python
.decode("utf8")
```

把：

```text
bytes
↓
str
```

保存到数据库。

------

# 10. 用户登录

当前接口：

```text
POST /login
```

请求：

```json
{
    "username": "老王",
    "password": "666666"
}
```

登录流程：

```text
用户名
  ↓
MySQL 查询 User
  ↓
找到用户
  ↓
bcrypt.checkpw()
  ↓
验证密码
  ↓
验证成功
  ↓
create_access_token()
  ↓
生成 JWT
  ↓
返回 Token
```

密码验证：

```python
is_password_correct = bcrypt.checkpw(
    user.password.encode("utf8"),
    db_user.password.encode("utf8")
)
```

`checkpw()` 不是简单的：

```python
明文密码 == 数据库密码
```

而是使用 bcrypt 的算法验证：

```text
用户输入的密码
        ↓
bcrypt
        ↓
与数据库中的 bcrypt 哈希进行验证
        ↓
True / False
```

------

# 11. JWT

已经安装：

```text
PyJWT
```

JWT 相关代码放在：

```text
backend/auth.py
```

------

# 12. JWT 配置

当前：

```python
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
```

SECRET_KEY 放在 `.env`。

不能把真实 SECRET_KEY 上传到 GitHub。

------

# 13. JWT 生成

当前：

```python
def create_access_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
```

JWT 中目前保存：

```text
user_id
exp
```

例如：

```json
{
    "user_id": 2,
    "exp": "过期时间"
}
```

生成过程：

```text
user_id
   ↓
payload
   ↓
SECRET_KEY + HS256
   ↓
JWT Token
```

------

# 14. JWT 验证

当前：

```python
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token 无效"
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token 已过期"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token 无效"
        )

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    db.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="用户不存在"
        )

    return user
```

------

# 15. HTTPBearer

当前：

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()
```

作用：

从 HTTP 请求中获取：

```text
Authorization
```

例如：

```text
Authorization: Bearer eyJhbGci...
```

然后：

```python
credentials.credentials
```

得到真正的：

```text
eyJhbGci...
```

------

# 16. `/me` 当前登录用户接口

当前接口：

```text
GET /me
```

代码：

```python
@app.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.id,
        "username": current_user.username
    }
```

这里：

```python
Depends(get_current_user)
```

意味着：

```text
请求 /me
   ↓
FastAPI
   ↓
执行 get_current_user()
   ↓
验证 JWT
   ↓
查询数据库
   ↓
得到 User 对象
   ↓
注入 current_user
   ↓
执行 get_me()
```

------

# 17. JWT 功能已经实际测试成功

2026-09-03 已经通过 Swagger 完成测试。

登录后获得 JWT：

```text
access_token
```

Swagger Authorize 时需要注意：

### 正确

只填写：

```text
eyJhbGciOi...
```

Swagger 会自动生成：

```text
Authorization: Bearer eyJhbGciOi...
```

### 错误

不要自己填写：

```text
Bearer eyJhbGciOi...
```

否则可能导致：

```text
Authorization: Bearer Bearer eyJhbGciOi...
```

之前就因为这个问题导致：

```text
401 Unauthorized
```

------

# 18. `/me` 测试结果

当前已经成功：

```text
GET /me
```

返回：

```json
{
    "user_id": 2,
    "username": "老王"
}
```

HTTP 状态码：

```text
200 OK
```

这说明：

```text
登录
 ↓
JWT 生成
 ↓
Swagger 携带 JWT
 ↓
HTTPBearer
 ↓
jwt.decode
 ↓
得到 user_id
 ↓
MySQL 查询 User
 ↓
返回当前用户
```

整个 JWT 认证链路已经跑通。

------

# 19. 当前 main.py 核心功能

当前 `backend/main.py` 已经包含：

```python
from fastapi import FastAPI, Depends
import uvicorn
from database import engine, Base, SessionLocal
from models import User
from schemas import UserCreate, UserLogin
import bcrypt
from auth import create_access_token, get_current_user


app = FastAPI()

Base.metadata.create_all(bind=engine)
```

已经存在：

```text
GET  /
GET  /test-db
POST /register
POST /login
GET  /me
```

------

# 20. 当前 API

| 方法   | 接口                   | 功能         | 状态 |
| ------ | ---------------------- | ------------ | ---- |
| GET    | `/`                    | 首页测试     | ✅    |
| GET    | `/test-db`             | 测试 MySQL   | ✅    |
| POST   | `/register`            | 用户注册     | ✅    |
| POST   | `/login`               | 用户登录     | ✅    |
| GET    | `/me`                  | 获取当前用户 | ✅    |
| POST   | `/items`               | 发布物品     | ⏳    |
| GET    | `/items`               | 查询物品     | ⏳    |
| GET    | `/items/{id}`          | 物品详情     | ⏳    |
| PUT    | `/items/{id}`          | 修改物品     | ⏳    |
| DELETE | `/items/{id}`          | 删除物品     | ⏳    |
| POST   | `/swaps`               | 发起换物     | ⏳    |
| POST   | `/swaps/{id}/accept`   | 接受换物     | ⏳    |
| POST   | `/swaps/{id}/reject`   | 拒绝换物     | ⏳    |
| POST   | `/swaps/{id}/complete` | 完成换物     | ⏳    |

------

# 21. 下一阶段：物品模块

下一步不再继续修改 JWT。

开始开发：

```text
Item
```

也就是平台上的：

```text
物品
```

第一阶段目标：

```text
POST /items
```

让登录用户可以发布自己的物品。

例如：

```json
{
    "title": "机械键盘",
    "description": "用了半年，成色很好",
    "category": "数码",
    "wanted_item": "想换一个鼠标"
}
```

数据库：

```text
items
---------------------------------------------------------
id | user_id | title | description | category | wanted_item
```

------

# 22. 发布物品的核心逻辑

发布物品时：

```text
用户登录
   ↓
获得 JWT
   ↓
POST /items
   ↓
HTTPBearer
   ↓
验证 JWT
   ↓
得到 current_user
   ↓
current_user.id
   ↓
创建 Item
   ↓
保存到 MySQL
```

重点：

用户不需要自己提交：

```json
{
    "user_id": 2
}
```

而是后端从 JWT 中自动获取：

```python
current_user.id
```

这样可以避免用户伪造：

```text
user_id
```

------

# 23. 后续 Item 数据模型

预计：

```python
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        nullable=False
    )

    title = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=False
    )

    category = Column(
        String(50),
        nullable=False
    )

    wanted_item = Column(
        String(255)
    )
```

具体字段后续根据实际开发调整。

------

# 24. 项目后续路线

## 第一阶段：基础后端

```text
用户
 ↓
注册
 ↓
登录
 ↓
JWT
 ↓
当前用户
```

当前已经完成。

------

## 第二阶段：物品系统

```text
发布物品
 ↓
查询物品
 ↓
物品详情
 ↓
修改物品
 ↓
删除物品
```

当前准备开始。

------

## 第三阶段：换物系统

```text
用户 A
 ↓
看到用户 B 的物品
 ↓
发起换物请求
 ↓
用户 B 接受 / 拒绝
 ↓
双方确认
 ↓
换物完成
```

------

## 第四阶段：Redis / RabbitMQ

后续可以加入：

- Redis
- RabbitMQ

用于：

```text
缓存
消息
异步任务
```

------

## 第五阶段：AI 物品理解

用户输入：

```text
“我有一个用了两年的罗技机械键盘，
想换一个游戏鼠标。”
```

LLM 提取：

```json
{
    "item": "机械键盘",
    "category": "数码",
    "condition": "使用两年",
    "wanted": "游戏鼠标"
}
```

------

## 第六阶段：Embedding

将物品信息转换成向量：

```text
物品文本
   ↓
Embedding Model
   ↓
Vector
```

例如：

```text
机械键盘
 ↓
[0.12, -0.31, 0.52, ...]
```

------

## 第七阶段：向量检索

用户发布：

```text
机械键盘
```

系统寻找：

```text
鼠标
键盘
耳机
显示器
游戏手柄
```

等语义上相关的物品。

------

## 第八阶段：智能换物推荐

最终形成：

```text
用户物品
   ↓
Embedding
   ↓
向量检索
   ↓
候选物品
   ↓
LLM 分析
   ↓
匹配度评分
   ↓
推荐换物对象
```

------

## 第九阶段：LangChain / LangGraph

最终加入 AI Agent：

```text
用户
 ↓
AI Agent
 ↓
判断用户需求
 ↓
查询物品
 ↓
向量检索
 ↓
分析匹配度
 ↓
推荐物品
 ↓
用户确认
```

LangGraph 可以负责：

```text
状态管理
 ↓
节点
 ↓
条件路由
 ↓
工具调用
 ↓
人工确认
 ↓
长期记忆
```

------

# 25. 当前开发原则

这个项目采用：

```text
先把传统后端做完整
        ↓
再加入 AI
```

不要一开始就把：

```text
FastAPI
MySQL
Redis
RabbitMQ
LangChain
LangGraph
Embedding
向量数据库
```

全部混在一起。

当前优先级：

```text
用户系统
 ↓
物品系统
 ↓
换物系统
 ↓
Redis / RabbitMQ
 ↓
Embedding / 向量检索
 ↓
LangChain
 ↓
LangGraph
 ↓
AI 智能推荐
```

------

# 26. 当前进度节点

### 已完成

```text
MySQL
  ↓
SQLAlchemy
  ↓
User
  ↓
注册
  ↓
bcrypt
  ↓
登录
  ↓
JWT
  ↓
HTTPBearer
  ↓
/me
```

### 当前正在做

```text
Item
 ↓
POST /items
```

### 下一步

```text
GET /items
GET /items/{id}
PUT /items/{id}
DELETE /items/{id}
```

然后进入：

```text
Swap
```

------

# 27. Git 工作流

GitHub：

```text
swap_platform
```

当前分支：

```text
master
```

正常开发流程：

```bash
git add .
git commit -m "本次修改内容"
git push origin master
```

例如完成商品发布功能后：

```bash
git add .
git commit -m "完成物品发布功能"
git push origin master
```

如果只想提交指定文件，也可以：

```bash
git add backend/main.py backend/models.py backend/schemas.py
git commit -m "完成物品发布功能"
git push origin master
```

------

# 28. Git 注意事项

不要提交：

```text
.env
```

不要把：

```text
DATABASE_URL
SECRET_KEY
API_KEY
```

等真实敏感信息上传到 GitHub。

`.gitignore` 至少应该包含：

```text
.env
__pycache__/
*.pyc
.venv/
venv/
.idea/
```

------

# 29. 当前最重要的状态

截至 2026-09-03：

**用户认证模块已经完成并验证成功。**

特别是：

```text
/register
/login
/me
```

已经可以正常工作。

因此下一次继续项目时：

> **不要重新设计项目，不要重新做 JWT。**

直接从：

```text
Item 数据模型
        ↓
Item Schema
        ↓
POST /items
        ↓
JWT 获取当前用户
        ↓
保存物品到 MySQL
```

开始。

目标是让第一个真实的“物换物平台业务功能”跑起来。