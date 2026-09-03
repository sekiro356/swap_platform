继续做之前的 AI 智能以物换物平台项目。

请按照之前确定的项目目标、技术栈、功能范围、开发思路和当前进度继续，不要重新设计项目。

开发方式保持之前一样：一步一步做，每次只推进一个小功能，同时把涉及的代码解释清楚，不要一次给我整个项目。

如果需要确认项目当前状态，以 `PROJECT_CONTEXT.md` 和 GitHub 最新代码为准。



# AI 智能以物换物平台（swap_platform）

## 1. 项目目标
1～2个月完成一个能运行、能演示、能写进简历、能用于面试的项目。

## 2. 当前技术栈
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- JWT
- HTML/CSS/JavaScript

后续：
- Redis
- RabbitMQ
- Embedding
- 向量检索
- LangChain
- LangGraph

## 3. 当前核心功能
- 用户注册
- 用户登录
- JWT认证
- 发布物品
- 浏览/搜索物品
- 查看物品详情
- 发起换物
- 接受/拒绝换物
- 换物完成

## 4. 后续AI功能
- LLM提取商品结构化信息
- Embedding
- 向量搜索
- AI智能换物推荐
- LangChain
- LangGraph AI换物助手

## 5. 当前架构
Browser
↓
FastAPI
↓
SQLAlchemy
↓
MySQL

后续：
FastAPI
↓
LLM / Embedding
↓
Vector Search
↓
LangChain / LangGraph

## 6. 当前项目结构

swap_platform/
├── .gitignore
├── requirements.txt
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

## 7. 当前进度

已经完成/学习：
- FastAPI基本运行
- MySQL数据库创建
- SQLAlchemy连接MySQL
- engine
- SessionLocal
- Base
- User模型
- UserCreate Schema
- 注册接口
- Git初始化
- GitHub仓库

当前注册流程：

用户提交注册信息
↓
FastAPI
↓
UserCreate
↓
SessionLocal
↓
查询用户名
↓
创建User
↓
db.add()
↓
db.commit()
↓
db.refresh()
↓
db.close()

## 8. 当前User模型

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

## 9. 当前UserCreate

class UserCreate(BaseModel):
    username: str
    password: str

UserCreate是API请求数据，不是数据库表。

User是数据库ORM模型。

## 10. 重要开发原则

- 一次只做一个小步骤
- 不要一次生成整个项目
- 每一步都解释关键代码
- 优先结合当前项目解释知识点
- 不要过早复杂化
- 项目优先于零散理论
- 当前目标是面试项目，不是商业化产品

## 11. 安全

数据库密码、API Key、JWT Secret等必须放到.env。

.gitignore：

.env
__pycache__/
*.pyc
.idea/
.venv/
venv/

不要把真实密码提交到GitHub。

## 12. 推荐开发顺序

用户系统：
密码哈希
↓
注册完善
↓
登录
↓
JWT
↓
当前用户

商品系统：
Item
↓
CRUD
↓
搜索
↓
详情

换物系统：
Swap
↓
发起
↓
接受
↓
拒绝
↓
完成

AI：
LLM
↓
结构化
↓
Embedding
↓
向量检索
↓
智能推荐
↓
LangChain
↓
LangGraph

## 13. 当前下一步

把注册接口中的明文密码改成bcrypt哈希。

然后：

密码哈希
↓
登录
↓
JWT
↓
获取当前用户