# 物换物平台（swap_platform）项目上下文

## 一、项目简介

项目名称：`swap_platform`

项目目标：开发一个完整的“以物换物平台”后端项目，并逐步加入：

- 数据分析
- 机器学习
- NLP / LLM
- Embedding
- LangChain / LangGraph
- Redis
- RabbitMQ
- Docker
- Linux
- Nginx

项目定位：

> 从基础 FastAPI CRUD 项目逐步升级为具备真实业务逻辑、权限控制、数据分析、机器学习和 AI 能力的综合项目。

最终用于：

- 项目实践
- 技术学习
- GitHub 展示
- 简历项目
- 面试项目介绍

------

# 二、当前项目阶段

截至 **2026-09-04**：

```text
第一阶段：FastAPI 后端基础 + 核心交换业务
状态：基本完成
```

目前已经完成：

```text
用户
├── 注册
├── 登录
├── bcrypt 密码哈希
├── JWT 身份认证
└── 当前用户查询

物品
├── 发布
├── 查询全部
├── 查询单个
├── 修改
├── 删除
└── 物品状态管理

交换
├── 发起交换
├── 查询交换
├── 接受交换
├── 拒绝交换
├── 权限控制
├── 状态控制
└── 交换完成后锁定双方物品
```

第一阶段已经完成，不需要继续扩展基础交换功能。

下一阶段进入：

```text
数据分析
```

------

# 三、当前技术栈

## 后端

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
- Redis
- RabbitMQ
- Docker
- Linux
- Nginx

------

# 四、当前项目结构

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

目前主要业务代码仍然集中在：

```text
backend/main.py
```

暂时不要进行大规模重构。

等核心功能和数据分析完成后，再根据实际需要逐步拆分。

------

# 五、数据库

当前数据库：

```text
MySQL
```

ORM：

```text
SQLAlchemy
```

数据库连接通过 `.env` 中的：

```text
DATABASE_URL
```

配置。

`database.py` 主要提供：

```python
engine
SessionLocal
Base
```

启动时：

```python
Base.metadata.create_all(bind=engine)
```

用于创建不存在的数据库表。

注意：

> `Base.metadata.create_all()` 只负责创建不存在的表，不会自动修改已经存在的表结构。

因此以后给已有表增加字段，需要通过 SQL：

```sql
ALTER TABLE ...
```

同步数据库结构。

------

# 六、当前数据库模型

## 1. User 用户表

主要字段：

```text
id
username
password
```

密码使用 bcrypt 哈希保存。

数据库中：

```text
password ≠ 明文密码
```

而是 bcrypt 生成的哈希字符串。

------

# 七、Items 物品表

模型：

```python
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    user_id = Column(Integer, nullable=False)

    status = Column(String(20), nullable=False, default='available')
```

字段：

```text
id
    物品 ID

name
    物品名称

description
    物品描述

category
    物品分类

price
    物品价格

user_id
    物品发布者

status
    当前物品是否还能参与交换
```

------

## Items.status

当前使用：

```text
available
unavailable
```

含义：

```text
available
    可以参与交换

unavailable
    已经交换完成，不能再次参与交换
```

数据库已经同步增加：

```sql
status VARCHAR(20) NOT NULL DEFAULT 'available'
```

新发布物品默认：

```text
available
```

------

# 八、Swap 交换申请表

模型：

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
    发起交换的用户

target_item_id
    发起者想要的物品

offered_item_id
    发起者拿出来交换的物品

status
    当前交换申请状态
```

当前状态：

```text
pending
accepted
rejected
```

流程：

```text
pending
   ↓
   ├── accepted
   │
   └── rejected
```

------

# 九、用户认证模块

## 1. 注册

接口：

```http
POST /register
```

流程：

```text
用户名 + 密码
       ↓
查询用户名是否存在
       ↓
bcrypt 哈希密码
       ↓
创建 User
       ↓
保存数据库
       ↓
返回注册成功
```

------

## 2. 登录

接口：

```http
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

------

## 3. 当前用户

接口：

```http
GET /me
```

使用：

```python
Depends(get_current_user)
```

获取当前用户。

因此：

```python
current_user.id
```

就是当前登录用户 ID。

------

# 十、JWT 认证

`auth.py` 使用：

```text
HTTPBearer
```

请求头：

```text
Authorization: Bearer <JWT>
```

JWT 中包含：

```text
user_id
exp
```

通过：

```python
get_current_user()
```

解析 token，并查询数据库中的 User。

------

# 十一、Swagger

开发测试地址：

```text
http://127.0.0.1:8000/docs
```

Swagger 中点击：

```text
Authorize
```

输入：

```text
JWT_TOKEN
```

不需要手动输入：

```text
Bearer JWT_TOKEN
```

因为 `HTTPBearer` 会自动处理。

------

# 十二、物品模块

## 1. 发布物品

```http
POST /items
```

需要 JWT。

创建物品时：

```python
user_id=current_user.id
```

因此用户无法通过请求体伪造物品所有者。

新物品默认：

```text
status = available
```

------

## 2. 查询全部物品

```http
GET /items
```

不需要 JWT。

------

## 3. 查询单个物品

```http
GET /items/{item_id}
```

不需要 JWT。

------

## 4. 修改物品

```http
PUT /items/{item_id}
```

需要 JWT。

只有：

```python
db_item.user_id == current_user.id
```

才能修改。

否则：

```text
403
无权限修改此物品
```

------

## 5. 删除物品

```http
DELETE /items/{item_id}
```

需要 JWT。

同样只有物品所有者可以删除。

------

# 十三、交换模块

交换模块目前已经完成。

------

## 1. 发起交换

接口：

```http
POST /swaps
```

请求：

```json
{
    "target_item_id": 8,
    "offered_item_id": 3
}
```

含义：

```text
target_item_id
    我想要的物品

offered_item_id
    我提供的物品
```

后端自动确定：

```python
requester_id = current_user.id
```

新申请：

```text
status = pending
```

------

# 十四、发起交换时的业务校验

目前已经实现以下检查。

## 1. 目标物品必须存在

```python
if not target_item:
```

------

## 2. 自己提供的物品必须存在

```python
if not offered_item:
```

------

## 3. 不能拿别人的物品交换

```python
if offered_item.user_id != current_user.id:
```

返回：

```text
403
不能拿别人的物品进行交换
```

------

## 4. 自己提供的物品必须是 available

```python
if offered_item.status != 'available':
```

返回：

```text
400
您提供的物品已经无法进行交换
```

------

## 5. 目标物品必须是 available

```python
if target_item.status != 'available':
```

返回：

```text
400
目标物品已无法进行交换
```

------

## 6. 不能和自己的物品交换

```python
if target_item.user_id == current_user.id:
```

返回：

```text
不能和自己的物品进行交换
```

------

# 十五、查询交换申请

接口：

```http
GET /swaps
```

需要 JWT。

当前用户可以看到两类交换：

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

------

# 十六、接受交换

接口：

```http
PUT /swaps/{swap_id}/accept
```

接受流程：

```text
查询 Swap
    ↓
Swap 是否存在
    ↓
status 是否为 pending
    ↓
查询 target_item
    ↓
查询 offered_item
    ↓
两个物品是否存在
    ↓
当前用户是不是 target_item 主人
    ↓
检查两个物品是否还是 available
    ↓
Swap → accepted
    ↓
target_item → unavailable
offered_item → unavailable
    ↓
commit
```

------

## 接受权限

只有：

```text
target_item.user_id == current_user.id
```

才能接受。

否则：

```text
403
无权接受此交换
```

------

## 防止重复处理

只有：

```text
pending
```

状态可以接受。

如果已经：

```text
accepted
```

或者：

```text
rejected
```

再次处理：

```text
400
该交换申请已经处理过了
```

------

## 接受后锁定物品

成功接受后：

```python
swap.status = 'accepted'

target_item.status = 'unavailable'
offered_item.status = 'unavailable'
```

因此：

```text
双方物品
    ↓
unavailable
```

不能再次发起交换。

------

# 十七、拒绝交换

接口：

```http
PUT /swaps/{swap_id}/reject
```

只有目标物品主人可以拒绝。

判断：

```python
target_item.user_id == current_user.id
```

否则：

```text
403
无权拒绝此交换
```

只有：

```text
pending
```

状态可以拒绝。

拒绝后：

```text
pending
   ↓
rejected
```

**拒绝不会修改物品状态。**

因为交换没有成功，所以双方物品仍然保持：

```text
available
```

可以继续参与其他交换。

------

# 十八、当前交换业务流程

完整流程：

```text
用户 A
  ↓
发布物品 A
  ↓
用户 B
  ↓
发布物品 B
  ↓
A 发起交换申请
  ↓
pending
  ↓
B 查看申请
  ↓
 ┌───────────────┐
 ↓               ↓
接受             拒绝
 ↓               ↓
accepted        rejected
 ↓
A物品 unavailable
B物品 unavailable
```

------

# 十九、当前已经解决的业务漏洞

目前已经增加了以下业务保护：

```text
✅ A 不能拿 B 的物品作为自己的交换物品

✅ A 不能拿自己的物品和自己的物品交换

✅ unavailable 物品不能再次发起交换

✅ 只有目标物品主人才能接受

✅ 只有目标物品主人才能拒绝

✅ accepted 之后不能再次处理

✅ rejected 之后不能再次处理

✅ 接受交换后双方物品变成 unavailable

✅ 接受交换前再次检查双方物品是否仍然 available
```

------

# 二十、第一阶段测试

交换模块需要覆盖以下测试。

## 正常流程

```text
A 登录
 ↓
A 发布物品 A
 ↓
B 登录
 ↓
B 发布物品 B
 ↓
A 申请交换 B 的物品
 ↓
pending
 ↓
B 查询 /swaps
 ↓
B 接受
 ↓
accepted
 ↓
A/B 两个物品 → unavailable
```

------

## 拒绝流程

```text
A 发起交换
 ↓
pending
 ↓
B 拒绝
 ↓
rejected
```

双方物品仍然：

```text
available
```

------

## 非法流程

测试：

```text
A 拿 B 的物品作为 offered_item
```

应该：

```text
403
```

测试：

```text
A 和自己的物品交换
```

应该拒绝。

测试：

```text
A 使用 unavailable 物品发起交换
```

应该：

```text
400
```

测试：

```text
C 接受 A → B 的交换
```

应该：

```text
403
```

测试：

```text
C 拒绝 A → B 的交换
```

应该：

```text
403
```

测试：

```text
已经 accepted 的申请再次 accept
```

应该：

```text
400
```

测试：

```text
已经 rejected 的申请再次 reject
```

应该：

```text
400
```

------

# 二十一、代码风格

目前数据库操作仍然采用：

```python
db = SessionLocal()
```

操作完成：

```python
db.close()
```

暂时不进行：

```python
get_db()
```

等基础业务更加稳定后，再统一进行数据库依赖注入优化。

------

# 二十二、已遇到并解决的问题

## SQLAlchemy Table 重复定义

曾经出现：

```text
sqlalchemy.exc.InvalidRequestError:
Table 'users' is already defined for this MetaData instance.
```

原因：

同一个 models 文件被不同模块路径加载，例如同时使用：

```python
from backend.models import ...
```

和：

```python
from models import ...
```

会导致 Python 可能将其当成不同模块加载。

当前统一使用：

```python
from models import User, Items, Swap
from database import engine, Base, SessionLocal
from auth import create_access_token, get_current_user
```

不要混用：

```python
from backend.models import ...
```

------

# 二十三、Git

当前主分支：

```text
master
```

远程仓库：

```text
https://github.com/sekiro356/swap_platform.git
```

第一阶段完成后：

```bash
git add .
git commit -m "完成交换申请模块"
git push origin master
```

Git 提交完成后，第一阶段正式结束。

------

# 二十四、下一阶段：数据分析

下一阶段不直接进入复杂 AI。

首先利用当前项目已经产生的数据进行数据分析。

整体路线：

```text
MySQL
 ↓
读取真实业务数据
 ↓
Pandas
 ↓
数据清洗
 ↓
数据统计
 ↓
Matplotlib / Seaborn
 ↓
业务分析
```

------

## 计划分析的数据

### 用户数据

例如：

```text
用户数量
用户注册情况
用户活跃度
```

### 物品数据

例如：

```text
物品数量
物品分类分布
不同分类的数量
价格分布
不同用户发布物品数量
```

### 交换数据

例如：

```text
交换申请数量
pending 数量
accepted 数量
rejected 数量
交换成功率
不同分类的交换次数
```

------

# 二十五、机器学习阶段

数据分析完成后进入机器学习。

计划使用：

```text
scikit-learn
```

首先从比较容易理解的：

```text
KNN
```

开始。

目标：

```text
用户喜欢什么
      ↓
物品特征
      ↓
计算相似度
      ↓
推荐相似物品
```

之后再根据实际数据规模决定是否使用：

```text
XGBoost
```

------

# 二十六、NLP / Embedding 阶段

后续对物品描述进行文本处理。

例如用户发布：

```text
九成新苹果无线耳机，想换一个机械键盘
```

可以逐步提取：

```text
物品：
无线耳机

品牌：
苹果

成色：
九成新

类别：
数码

交换意向：
机械键盘
```

进一步：

```text
文本
 ↓
Embedding
 ↓
向量
 ↓
相似度计算
 ↓
寻找语义相似的物品
```

最终实现更智能的交换匹配。

------

# 二十七、LangChain / LangGraph 阶段

后续将项目接入：

```text
LangChain
LangGraph
```

计划实现：

```text
Tool
Agent
RAG
Memory
Workflow
```

最终可以实现：

```text
智能交换助手
```

例如：

```text
用户：
帮我找适合拿耳机交换的机械键盘

        ↓

AI 查询物品数据库

        ↓

分析用户物品

        ↓

Embedding / 相似度匹配

        ↓

推荐交换对象
```

------

# 二十八、工程化阶段

后续加入：

```text
Redis
RabbitMQ
Docker
Linux
Nginx
```

逐步学习：

```text
缓存
消息队列
异步任务
容器化
Linux 部署
反向代理
系统架构
```

最终目标类似：

```text
                Nginx
                  ↓
               FastAPI
              ↙       ↘
           Redis     MySQL
              ↓
          RabbitMQ
              ↓
        AI / ML 服务
```

具体架构等项目实际发展到该阶段后再决定。

------

# 二十九、最终项目路线

整体路线：

```text
第一阶段
FastAPI
SQLAlchemy
MySQL
JWT
bcrypt
CRUD
        ↓
第二阶段
用户
物品
交换
权限控制
业务状态
        ↓
第三阶段
Pandas
NumPy
Matplotlib
Seaborn
数据分析
        ↓
第四阶段
scikit-learn
KNN
推荐系统
        ↓
第五阶段
NLP
Embedding
语义匹配
        ↓
第六阶段
LangChain
LangGraph
RAG
Memory
Agent
        ↓
第七阶段
Redis
RabbitMQ
Docker
Linux
Nginx
        ↓
最终
AI + 后端 + 数据分析 + 机器学习
综合项目
```

------

# 三十、后续开发原则

继续开发时：

1. **不重新设计已经完成的功能。**
2. 每次只实现一个小功能。
3. 修改前先说明为什么修改。
4. 基于当前代码继续开发。
5. 不一次性重写整个项目。
6. 出现 Bug 时先解释原因，再修改。
7. 每完成一个功能都进行测试。
8. 功能稳定后再 Git commit。
9. 暂时不进行不必要的架构重构。
10. 后续学习的技术尽量与这个物换物项目结合。
11. 不为了“堆技术”而加入 Redis、RabbitMQ、AI 等组件。
12. 先理解基础原理，再把技术真正用到项目业务中。

------

# 三十一、当前结论

截至 **2026-09-04**：

```text
第一阶段：完成 ✅
```

当前项目已经从单纯的：

```text
FastAPI CRUD
```

发展为：

```text
用户认证
    ↓
物品管理
    ↓
交换申请
    ↓
权限控制
    ↓
交换状态管理
    ↓
物品状态管理
```

核心交换流程已经闭环：

```text
pending
   ↓
accepted / rejected
```

其中接受交换后：

```text
双方物品
   ↓
unavailable
```

因此已经具备一个基本真实业务系统的雏形。

------

# 三十二、当前下一步

**下一阶段从数据分析开始。**

第一步计划：

```text
从 MySQL 读取当前物换物平台的数据
        ↓
使用 Pandas 转换成 DataFrame
        ↓
查看用户、物品、交换数据
        ↓
进行第一批基础统计
```

暂时不急着加入：

```text
Redis
RabbitMQ
LangChain
LangGraph
```

先把：

```text
后端业务
   ↓
真实数据
   ↓
数据分析
   ↓
机器学习
   ↓
AI
```

这条路线真正跑通。