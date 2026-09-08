1. # AI 智能以物换物平台 - PROJECT_CONTEXT

   > 本文件用于记录项目当前状态、技术路线、数据库结构、已经完成的功能、开发规范以及下一步计划。
   >
   > **后续继续开发时，优先阅读本文件，避免重新设计已经完成的功能。**

   ------

   # 一、项目基本信息

   ## 1.1 项目名称

   **AI 智能以物换物平台**

   项目目录：

   ```text
   swap_platform
   ```

   GitHub：

   ```text
   https://github.com/sekiro356/swap_platform.git
   ```

   主分支：

   ```text
   master
   ```

   ------

   # 二、项目定位

   这是一个以物换物平台。

   用户可以：

   ```text
   注册账号
       ↓
   登录
       ↓
   发布物品
       ↓
   浏览其他用户物品
       ↓
   发起交换
       ↓
   物品持有者接受 / 拒绝
       ↓
   完成交换
   ```

   项目后续会逐步加入：

   ```text
   数据分析
       ↓
   机器学习
       ↓
   推荐系统
       ↓
   NLP / Embedding
       ↓
   LLM
       ↓
   LangChain / LangGraph
       ↓
   Redis / RabbitMQ
       ↓
   Docker / Linux / Nginx
   ```

   最终目标不是单纯实现一个 CRUD 网站，而是形成一个：

   > **具有后端业务能力 + 数据分析能力 + 机器学习推荐能力 + LLM/Agent 能力 + 工程部署能力的综合项目。**

   主要用于：

   - 简历项目
   - 校招 / 社招面试
   - 展示 Python / FastAPI 能力
   - 展示 MySQL / SQLAlchemy 能力
   - 展示 Pandas / 数据分析能力
   - 展示机器学习能力
   - 展示 LangChain / LangGraph / LLM 能力
   - 展示 Redis / RabbitMQ / Docker / Linux / Nginx 等工程能力

   ------

   # 三、开发原则

   后续开发必须遵循以下原则。

   ## 3.1 不重新设计已经完成的功能

   已经完成并测试过的功能，不要因为后面加入新技术而随意重写。

   例如：

   ```text
   用户注册
   用户登录
   JWT
   bcrypt
   物品创建
   交换请求
   接受交换
   拒绝交换
   ```

   这些属于已经完成的基础业务。

   后面加入推荐系统时，只需要：

   ```text
   新增推荐模块
   ```

   而不是重新设计整个项目。

   ------

   ## 3.2 一次只完成一个小功能

   开发方式：

   ```text
   解释为什么做
       ↓
   修改少量代码
       ↓
   运行
       ↓
   测试
       ↓
   确认没问题
       ↓
   再进行下一步
   ```

   不要一次性增加很多功能。

   ------

   ## 3.3 先理解，再写代码

   用户希望理解：

   ```text
   为什么这样写？
   这个函数干什么？
   这个参数是什么意思？
   数据怎么流动？
   ```

   而不是单纯复制代码。

   ------

   ## 3.4 遇到 Bug 先解释原因

   出现错误时：

   ```text
   错误信息
       ↓
   分析原因
       ↓
   确定问题位置
       ↓
   修改
       ↓
   重新运行
   ```

   不要直接丢一大段修改后的代码。

   ------

   ## 3.5 新技术必须和项目业务结合

   例如：

   不能为了简历写：

   ```text
   使用 KNN
   ```

   而应该真正做：

   ```text
   物品特征
       ↓
   KNN
       ↓
   相似物品
       ↓
   推荐
   ```

   同理：

   ```text
   Redis
   ```

   应该用于缓存等真实业务。

   ```text
   RabbitMQ
   ```

   应该用于异步任务 / 消息通信。

   ```text
   LangGraph
   ```

   应该用于多步骤 Agent / 工作流。

   ------

   # 四、当前技术栈

   ## 4.1 已经使用

   ### 后端

   ```text
   Python
   FastAPI
   Uvicorn
   Pydantic
   ```

   ### 数据库

   ```text
   MySQL
   SQLAlchemy
   PyMySQL
   ```

   ### 用户认证

   ```text
   bcrypt
   JWT
   HTTPBearer
   PyJWT
   ```

   ### 数据分析

   ```text
   Pandas
   NumPy
   Matplotlib
   Seaborn
   ```

   ------

   # 五、后续技术路线

   计划逐步加入：

   ```text
   scikit-learn
       ↓
   KNN
       ↓
   推荐系统
       ↓
   NLP
       ↓
   Embedding
       ↓
   向量相似度
       ↓
   LangChain
       ↓
   LangGraph
       ↓
   LLM
       ↓
   Redis
       ↓
   RabbitMQ
       ↓
   Docker
       ↓
   Linux
       ↓
   Nginx
   ```

   ------

   # 六、当前项目结构

   目前后端主要文件：

   ```text
   backend/
   ├── main.py
   ├── models.py
   ├── schemas.py
   ├── database.py
   ├── auth.py
   ├── analysis.py
   └── ...
   ```

   ------

   # 七、核心文件作用

   ## 7.1 `main.py`

   FastAPI 主程序。

   主要负责：

   ```text
   创建 FastAPI 应用
   定义 API
   处理请求
   调用数据库
   调用认证函数
   处理业务逻辑
   ```

   启动方式：

   ```bash
   uvicorn main:app --reload
   ```

   Swagger：

   ```text
   http://127.0.0.1:8000/docs
   ```

   ------

   ## 7.2 `database.py`

   负责：

   ```text
   MySQL 数据库连接
   SQLAlchemy Engine
   SessionLocal
   Base
   ```

   整体关系：

   ```text
   FastAPI
      ↓
   SQLAlchemy Session
      ↓
   MySQL
   ```

   ------

   ## 7.3 `models.py`

   定义数据库模型。

   目前主要有：

   ```text
   User
   Items
   Swap
   ```

   这些 SQLAlchemy Model 对应 MySQL 中的表。

   ------

   ## 7.4 `schemas.py`

   负责 Pydantic 数据验证。

   主要包括：

   ```text
   UserCreate
   UserLogin
   ItemCreate
   SwapCreat
   ```

   其中 `ItemCreate` 对物品类别进行了限制。

   ------

   ## 7.5 `auth.py`

   负责：

   ```text
   密码认证
   JWT Token
   获取当前用户
   ```

   主要逻辑：

   ```text
   登录
    ↓
   验证用户名密码
    ↓
   创建 JWT
    ↓
   客户端携带 Token
    ↓
   HTTPBearer
    ↓
   解析 Token
    ↓
   获取当前用户
   ```

   ------

   ## 7.6 `analysis.py`

   数据分析脚本。

   负责：

   ```text
   MySQL
    ↓
   SQLAlchemy
    ↓
   Python
    ↓
   Pandas DataFrame
    ↓
   数据统计
    ↓
   业务分析
    ↓
   Matplotlib 可视化
   ```

   目前数据分析阶段已经基本完成。

   ------

   # 八、数据库设计

   目前主要有三个核心表。

   ------

   # 8.1 users 用户表

   SQLAlchemy Model：

   ```python
   class User(Base):
       __tablename__ = 'users'
   
       id = Column(Integer, primary_key=True, index=True)
   
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

   字段：

   | 字段     | 类型         | 作用                |
   | -------- | ------------ | ------------------- |
   | id       | int          | 用户 ID，主键，自增 |
   | username | varchar(50)  | 用户名，唯一        |
   | password | varchar(255) | 密码哈希值          |

   注意：

   数据库中的 `password` **不是明文密码**。

   注册时：

   ```text
   明文密码
       ↓
   bcrypt
       ↓
   密码哈希
       ↓
   MySQL
   ```

   登录时：

   ```text
   用户输入密码
       ↓
   bcrypt.checkpw()
       ↓
   验证数据库中的哈希
   ```

   ------

   # 8.2 items 物品表

   SQLAlchemy Model：

   ```python
   class Items(Base):
       __tablename__ = 'items'
   
       id = Column(
           Integer,
           primary_key=True,
           index=True
       )
   
       name = Column(
           String(200),
           nullable=False
       )
   
       description = Column(
           String(1000),
           nullable=False
       )
   
       category = Column(
           String(50),
           nullable=False
       )
   
       price = Column(
           Integer,
           nullable=False
       )
   
       user_id = Column(
           Integer,
           nullable=False
       )
   
       status = Column(
           String(20),
           nullable=False,
           default='available'
       )
   ```

   字段：

   | 字段        | 类型          | 作用      |
   | ----------- | ------------- | --------- |
   | id          | int           | 物品 ID   |
   | name        | varchar(200)  | 物品名称  |
   | description | varchar(1000) | 物品描述  |
   | category    | varchar(50)   | 物品类别  |
   | price       | int           | 物品价格  |
   | user_id     | int           | 发布者 ID |
   | status      | varchar(20)   | 物品状态  |

   ------

   # 8.3 swaps 交换表

   SQLAlchemy Model：

   ```python
   class Swap(Base):
       __tablename__ = 'swaps'
   
       id = Column(
           Integer,
           primary_key=True,
           index=True
       )
   
       requester_id = Column(
           Integer,
           nullable=False
       )
   
       target_item_id = Column(
           Integer,
           nullable=False
       )
   
       offered_item_id = Column(
           Integer,
           nullable=False
       )
   
       status = Column(
           String(20),
           default='pending',
           nullable=False
       )
   ```

   字段：

   | 字段            | 作用           |
   | --------------- | -------------- |
   | id              | 交换记录 ID    |
   | requester_id    | 发起交换的用户 |
   | target_item_id  | 想获得的物品   |
   | offered_item_id | 用户提供的物品 |
   | status          | 交换状态       |

   状态：

   ```text
   pending
   accepted
   rejected
   ```

   ------

   # 九、FastAPI 后端已经完成的功能

   ------

   ## 9.1 用户注册

   接口：

   ```text
   POST /register
   ```

   主要流程：

   ```text
   用户提交 username + password
           ↓
   Pydantic 验证
           ↓
   检查用户名是否存在
           ↓
   bcrypt.hashpw()
           ↓
   保存到 users
   ```

   ------

   # 9.2 用户登录

   接口：

   ```text
   POST /login
   ```

   主要流程：

   ```text
   username + password
           ↓
   查询用户
           ↓
   bcrypt.checkpw()
           ↓
   验证成功
           ↓
   create_access_token(user_id)
           ↓
   返回 JWT
   ```

   ------

   # 9.3 当前用户

   接口：

   ```text
   GET /me
   ```

   需要：

   ```text
   Authorization: Bearer <token>
   ```

   主要流程：

   ```text
   HTTP Bearer Token
          ↓
   JWT 解码
          ↓
   获取 user_id
          ↓
   查询用户
          ↓
   返回当前用户
   ```

   ------

   # 9.4 数据库测试

   接口：

   ```text
   GET /test-db
   ```

   用于测试 MySQL 是否能够正常连接。

   ------

   # 9.5 创建物品

   接口：

   ```text
   POST /items
   ```

   提交：

   ```text
   name
   description
   category
   price
   ```

   创建成功后：

   ```text
   user_id
   ```

   来自当前登录用户。

   ------

   # 十、物品类别设计

   目前统一使用以下 12 个类别：

   ```text
   数码
   书籍
   服饰
   鞋靴
   家电
   家居生活
   美妆个护
   运动户外
   玩具
   乐器
   办公用品
   其他
   ```

   `schemas.py` 中使用 Pydantic `Literal`：

   ```python
   category: Literal[
       '数码',
       '书籍',
       '服饰',
       '鞋靴',
       '家电',
       '家居生活',
       '美妆个护',
       '运动户外',
       '玩具',
       '乐器',
       '办公用品',
       '其他'
   ]
   ```

   作用：

   > 后端只允许这 12 种类别。

   例如：

   ```text
   电子产品
   ```

   不是允许值。

   请求会返回：

   ```text
   HTTP 422
   ```

   并产生：

   ```text
   literal_error
   ```

   ------

   # 十一、历史数据清洗

   需要特别注意：

   Pydantic 的 `Literal`：

   > 只能限制以后 API 新提交的数据。

   它不会自动修改数据库里已经存在的数据。

   因此历史数据中曾经出现：

   ```text
   书
   生活用品
   游戏
   ```

   这些旧类别。

   已经执行数据库清洗：

   ```sql
   书 → 书籍
   生活用品 → 家居生活
   游戏 → 其他
   ```

   目前历史类别已经完成标准化。

   ------

   # 十二、交换业务

   目前交换业务已经基本完成。

   核心字段：

   ```text
   requester_id
   target_item_id
   offered_item_id
   status
   ```

   业务含义：

   假设：

   ```text
   用户 A
   ```

   想要：

   ```text
   用户 B 的 iPhone
   ```

   A 提供：

   ```text
   自己的耳机
   ```

   那么：

   ```text
   requester_id = A
   target_item_id = iPhone
   offered_item_id = 耳机
   status = pending
   ```

   B 可以：

   ```text
   accepted
   ```

   或者：

   ```text
   rejected
   ```

   ------

   # 十三、数据分析阶段

   当前数据分析阶段的目标：

   > 使用真实数据库数据完成基础数据分析，并通过可视化发现平台中的用户行为、物品类别和交换行为规律。

   数据流：

   ```text
   MySQL
     ↓
   SQLAlchemy
     ↓
   查询 User / Items / Swap
     ↓
   转换为 DataFrame
     ↓
   Pandas
     ↓
   统计分析
     ↓
   Matplotlib
     ↓
   业务结论
   ```

   ------

   # 十四、analysis.py 数据获取

   用户表：

   ```python
   users = db.query(User).all()
   ```

   转换：

   ```python
   df_user
   ```

   包含：

   ```text
   id
   username
   ```

   ------

   物品表：

   ```python
   items = db.query(Items).all()
   ```

   转换：

   ```python
   df_items
   ```

   主要包含：

   ```text
   id
   name
   category
   price
   user_id
   status
   ```

   ------

   交换表：

   ```python
   swaps = db.query(Swap).all()
   ```

   转换：

   ```python
   df_swaps
   ```

   主要包含：

   ```text
   id
   requester_id
   target_item_id
   offered_item_id
   status
   ```

   ------

   # 十五、已经完成的数据统计

   ## 15.1 用户数量

   ```python
   len(df_user)
   ```

   ------

   ## 15.2 物品数量

   ```python
   len(df_items)
   ```

   ------

   ## 15.3 交换记录数量

   ```python
   len(df_swaps)
   ```

   ------

   ## 15.4 物品类别分布

   ```python
   df_items['category'].value_counts()
   ```

   用于统计：

   ```text
   不同类别
       ↓
   物品数量
   ```

   ------

   # 十六、用户物品数量分析

   使用：

   ```python
   df_items.groupby('user_id').size()
   ```

   统计：

   > 每个用户发布了多少物品。

   然后使用 `merge()` 将统计结果和用户表关联：

   ```python
   df_user_analysis = df_user.merge(
       item_count,
       left_on='id',
       right_on='user_id',
       how='left'
   )
   ```

   得到：

   ```text
   id
   username
   user_id
   item_count
   ```

   没有发布物品的用户：

   ```python
   fillna(0)
   ```

   最终：

   ```text
   用户 → 发布物品数量
   ```

   ------

   # 十七、用户交换行为分析

   统计用户发起的交换次数：

   ```python
   df_swaps.groupby('requester_id').size()
   ```

   得到：

   ```text
   requester_id
   swap_count
   ```

   统计用户成功交换次数：

   ```python
   df_swaps[
       df_swaps['status'] == 'accepted'
   ].groupby('requester_id').size()
   ```

   得到：

   ```text
   requester_id
   accepted_count
   ```

   然后计算：

   ```python
   success_rate = accepted_count / swap_count
   ```

   最终得到：

   ```text
   用户
   交换次数
   成功次数
   成功率
   ```

   ------

   # 十八、用户行为分析表

   最终形成：

   ```text
   user_behavior
   ```

   主要字段：

   ```text
   id
   username
   item_count
   swap_count
   accepted_count
   success_rate
   ```

   它可以用来分析：

   ```text
   用户发布了多少东西？
   用户发起了多少次交换？
   成功了多少次？
   成功率是多少？
   ```

   ------

   # 十九、交换类别分析

   通过：

   ```text
   target_item_id
   ```

   把交换表和物品表关联。

   得到：

   ```text
   交换记录
       ↓
   目标物品
       ↓
   目标物品类别
   ```

   然后统计：

   ```python
   category_target.value_counts()
   ```

   得到：

   ```text
   不同物品类别
       ↓
   交换次数
   ```

   ------

   # 二十、目标类别 + 提供类别分析

   进一步同时获取：

   ```text
   category_target
   category_offered
   ```

   也就是：

   ```text
   用户想要什么类别
   +
   用户提供什么类别
   ```

   例如：

   ```text
   数码 → 书籍
   数码 → 服饰
   书籍 → 数码
   ```

   然后：

   ```python
   groupby(
       ['category_target', 'category_offered']
   )
   ```

   统计不同类别组合出现的次数。

   最终得到：

   ```text
   category_target
   category_offered
   swap_count
   ratio
   ```

   这个结果对后续推荐系统有价值。

   ------

   # 二十一、交换成功率分析

   类别成功率计算逻辑：

   ```text
   某类别成功交换次数
   -------------------
   某类别总交换次数
   ```

   代码思想：

   ```python
   category_success_rate = (
       df_swaps[df_swaps['status'] == 'accepted']
       .groupby('category_target')
       .size()
       /
       df_swaps.groupby('category_target').size()
   )
   ```

   当前得到的结果：

   ```text
   书籍      35.29%
   其他      40.00%
   家居生活    57.14%
   数码      46.15%
   服饰      27.27%
   ```

   当前样本：

   ```text
   最高：家居生活
   最低：服饰
   ```

   注意：

   目前数据主要用于项目开发和测试，样本规模有限。

   因此不能直接得出：

   > “服饰类一定最难交换。”

   更严谨的说法：

   > “从当前样本来看，服饰类交换成功率相对较低，后续需要更多真实数据进一步验证。”

   ------

   # 二十二、已经完成的可视化

   目前已经完成以下图表。

   ------

   ## 22.1 每个用户发布物品数量

   ```text
   横轴：用户
   纵轴：物品数量
   ```

   使用：

   ```python
   plt.bar(
       user_behavior['username'],
       user_behavior['item_count']
   )
   ```

   ------

   ## 22.2 用户交换次数

   ```text
   横轴：用户
   纵轴：交换次数
   ```

   ------

   ## 22.3 Top 10 用户：物品数量与交换次数

   采用分组柱状图。

   目的：

   > 找出平台中比较活跃的用户。

   数据：

   ```text
   item_count
   swap_count
   ```

   ------

   ## 22.4 用户交换次数 + 交换成功率

   使用双 Y 轴：

   ```text
   左 Y 轴：
   交换次数
   
   右 Y 轴：
   交换成功率
   ```

   核心：

   ```python
   fig, ax1 = plt.subplots()
   
   ax2 = ax1.twinx()
   ```

   成功率格式：

   ```python
   PercentFormatter(1)
   ```

   例如：

   ```text
   0.57
   ```

   显示：

   ```text
   57%
   ```

   ------

   ## 22.5 物品类别分布

   ```text
   横轴：物品类别
   纵轴：物品数量
   ```

   用于观察平台物品主要集中在哪些类别。

   ------

   ## 22.6 不同类别的交换次数

   ```text
   横轴：物品类别
   纵轴：交换次数
   ```

   用于分析：

   > 哪些类别的物品更容易产生交换行为。

   ------

   ## 22.7 不同类别的交换成功率

   ```text
   横轴：物品类别
   纵轴：交换成功率
   ```

   使用：

   ```python
   plt.gca().yaxis.set_major_formatter(
       PercentFormatter(1)
   )
   ```

   其中：

   ```text
   plt.gca()
   ```

   表示：

   > 获取当前 Axes。

   如果已经有：

   ```python
   fig, ax = plt.subplots()
   ```

   则可以直接：

   ```python
   ax.yaxis
   ```

   ------

   # 二十三、Matplotlib 已学习的重要知识

   目前已经掌握：

   ```text
   plt.figure()
   plt.subplots()
   plt.bar()
   plt.plot()
   plt.xlabel()
   plt.ylabel()
   plt.title()
   plt.xticks()
   plt.legend()
   plt.tight_layout()
   plt.gca()
   ax.yaxis
   ax.twinx()
   PercentFormatter
   ```

   以及：

   ```python
   zip()
   ```

   和：

   ```python
   ax.text()
   ```

   等基本用法。

   ------

   # 二十四、数据分析阶段当前状态

   数据分析阶段：

   **基本完成。**

   目前已经覆盖：

   ```text
   数据获取             ✅
   DataFrame 转换       ✅
   数据清洗             ✅
   基础统计             ✅
   用户行为分析         ✅
   物品类别分析         ✅
   交换行为分析         ✅
   类别成功率分析       ✅
   类别关联分析         ✅
   Matplotlib 可视化    ✅
   业务结论             ✅
   ```

   因此：

   > **不再为了增加图表数量而继续画图。**

   数据分析阶段的目标已经达到。

   ------

   # 二十五、当前已知注意事项

   ## 25.1 数据库 Session 要关闭

   `analysis.py` 中：

   ```python
   db = SessionLocal()
   ```

   分析结束后需要：

   ```python
   db.close()
   ```

   避免数据库 Session 长时间占用。

   ------

   ## 25.2 `success_rate` 中的 0

   目前：

   ```python
   fillna(0)
   ```

   会让没有任何交换记录的用户显示：

   ```text
   0%
   ```

   但从数学角度：

   ```text
   0 / 0
   ```

   其实没有定义。

   后续如果做更加正式的数据分析，可以改成：

   ```text
   无交换记录
   ```

   而不是：

   ```text
   0%
   ```

   当前阶段暂时不需要修改。

   ------

   ## 25.3 类别成功率不是 12 个类别都有

   当前：

   ```text
   category_success_rate
   ```

   只会显示：

   > 实际产生过交换记录的类别。

   如果某个类别目前：

   ```text
   交换次数 = 0
   ```

   那么它不会出现在结果中。

   后续如果需要完整报表，再统一补齐 12 个类别。

   当前阶段暂时不需要处理。

   ------

   # 二十六、下一阶段：KNN 推荐系统

   数据分析完成之后，开始进入：

   # 机器学习阶段

   第一个目标：

   > 给平台增加“相似物品推荐”功能。

   ------

   # 二十七、为什么先做 KNN

   当前平台已经有：

   ```text
   物品名称
   物品描述
   物品类别
   物品价格
   ```

   这些数据可以用来判断物品之间的相似程度。

   例如：

   ```text
   物品 A：
   
   名称：小米手机
   类别：数码
   价格：1500
   ```

   和：

   ```text
   物品 B：
   
   名称：华为手机
   类别：数码
   价格：1800
   ```

   可能比较相似。

   而：

   ```text
   物品 C：
   
   名称：篮球鞋
   类别：鞋靴
   价格：300
   ```

   相似度可能比较低。

   因此可以实现：

   ```text
   用户查看某个物品
           ↓
   提取该物品特征
           ↓
   KNN 寻找距离最近的物品
           ↓
   推荐相似物品
   ```

   ------

   # 二十八、KNN 推荐系统计划

   按照小步骤进行。

   ## 第 1 步：理解 KNN

   先理解：

   ```text
   KNN 是什么？
   ```

   以及：

   ```text
   “最近”是什么意思？
   ```

   ------

   ## 第 2 步：确定物品特征

   例如：

   ```text
   category
   price
   ```

   后续可能加入：

   ```text
   name
   description
   ```

   ------

   ## 第 3 步：把数据转换成数值

   机器学习模型不能直接处理：

   ```text
   数码
   书籍
   服饰
   ```

   需要进行数值化。

   ------

   ## 第 4 步：使用 sklearn

   计划使用：

   ```python
   from sklearn.neighbors import NearestNeighbors
   ```

   或者根据学习过程使用 KNN 相关 API。

   ------

   ## 第 5 步：寻找相似物品

   输入：

   ```text
   item_id
   ```

   输出：

   ```text
   相似物品列表
   ```

   例如：

   ```text
   item_id = 10
   
   推荐：
   
   item 23
   item 31
   item 42
   ```

   ------

   # 二十九、最终计划形成推荐 API

   后续可以封装成：

   ```text
   GET /recommend/{item_id}
   ```

   例如：

   ```text
   GET /recommend/10
   ```

   返回：

   ```json
   {
       "item_id": 10,
       "recommendations": [
           23,
           31,
           42
       ]
   }
   ```

   最终形成：

   ```text
   FastAPI
       ↓
   推荐函数
       ↓
   KNN
       ↓
   物品相似度
       ↓
   推荐结果
   ```

   ------

   # 三十、KNN 后续升级

   基础 KNN 推荐完成后，再加入文本信息。

   例如物品：

   ```text
   名称：
   小米 14 手机
   
   描述：
   九成新，运行流畅，适合日常使用
   ```

   进行：

   ```text
   文本
    ↓
   Embedding
    ↓
   向量
    ↓
   相似度
    ↓
   推荐
   ```

   这样推荐系统就可以从：

   ```text
   类别 + 价格
   ```

   升级为：

   ```text
   名称
   +
   描述
   +
   类别
   +
   价格
   ```

   甚至进一步理解：

   ```text
   语义相似度
   ```

   ------

   # 三十一、后续 NLP / Embedding

   计划：

   ```text
   物品名称
   +
   物品描述
           ↓
   Embedding 模型
           ↓
   向量
           ↓
   向量相似度
           ↓
   推荐
   ```

   后续可以考虑：

   ```text
   pgvector
   ```

   或者其他向量数据库 / 向量存储方案。

   ------

   # 三十二、LangChain / LangGraph 阶段

   推荐系统基础完成后，再进入 LLM。

   可能实现：

   ## 智能物品分析

   用户发布：

   ```text
   “iPhone 13，电池健康 85%，九成新”
   ```

   LLM 分析：

   ```text
   类别
   物品特点
   成色
   适合交换的物品
   ```

   ------

   ## 智能推荐解释

   不是只返回：

   ```text
   推荐 iPhone 12
   ```

   而是：

   ```text
   推荐 iPhone 12，
   因为它和你当前物品都属于数码类别，
   价格接近，并且物品描述中的功能需求比较相似。
   ```

   ------

   ## 用户意图理解

   例如用户输入：

   ```text
   “我想拿一个闲置的机械键盘换个平板”
   ```

   系统理解：

   ```text
   用户提供：
   机械键盘
   
   用户想要：
   平板
   
   目标类别：
   数码
   ```

   然后结合推荐系统寻找合适物品。

   ------

   # 三十三、LangGraph 计划

   后续可以设计类似：

   ```text
   用户输入
      ↓
   意图识别
      ↓
   提取物品信息
      ↓
   查询数据库
      ↓
   推荐系统
      ↓
   LLM 分析推荐结果
      ↓
   生成回答
   ```

   这类多步骤流程比较适合 LangGraph。

   ------

   # 三十四、Redis 计划

   Redis 后续主要用于真实业务场景。

   例如：

   ```text
   热门物品缓存
   热门类别缓存
   推荐结果缓存
   登录相关数据
   ```

   例如：

   ```text
   用户请求推荐
       ↓
   Redis 中有缓存？
      ↙       ↘
    有         没有
    ↓           ↓
   直接返回    KNN计算
                ↓
             Redis缓存
   ```

   ------

   # 三十五、RabbitMQ 计划

   RabbitMQ 后续用于异步任务。

   例如：

   ```text
   用户发布物品
         ↓
   发送消息
         ↓
   RabbitMQ
         ↓
   异步任务
         ↓
   生成 Embedding
   ```

   这样不会让用户等待整个 Embedding 计算过程。

   也可以用于：

   ```text
   推荐计算
   数据统计
   通知
   日志任务
   ```

   ------

   # 三十六、Docker / Linux / Nginx

   最终部署路线：

   ```text
   FastAPI
      ↓
   Docker
      ↓
   Linux
      ↓
   Nginx
      ↓
   反向代理
      ↓
   对外提供服务
   ```

   数据库、Redis、RabbitMQ 等也可以逐渐容器化。

   ------

   # 三十七、最终项目架构目标

   最终希望形成：

   ```text
                      用户
                       │
                       ▼
                     Nginx
                       │
                       ▼
                    FastAPI
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
        MySQL        Redis      RabbitMQ
          │                         │
          │                         ▼
          │                     异步任务
          │
          ▼
      数据分析
          │
          ▼
     Pandas / NumPy
          │
          ▼
     KNN 推荐系统
          │
          ▼
    NLP / Embedding
          │
          ▼
    LangChain / LangGraph
          │
          ▼
         LLM
   ```

   ------

   # 三十八、项目开发阶段总进度

   当前整体路线：

   ```text
   第一阶段：FastAPI + MySQL
           ✅ 已完成
   
   第二阶段：用户认证
           ✅ 已完成
   
   第三阶段：物品管理
           ✅ 已完成
   
   第四阶段：交换业务
           ✅ 已完成
   
   第五阶段：Pandas 数据分析
           ✅ 已完成
   
   第六阶段：Matplotlib / Seaborn 可视化
           ✅ 已基本完成
   
   第七阶段：业务分析
           ✅ 已完成
   
   第八阶段：KNN 推荐系统
           ⏳ 下一阶段
   
   第九阶段：NLP / Embedding
           ⏳
   
   第十阶段：LangChain / LangGraph
           ⏳
   
   第十一阶段：Redis
           ⏳
   
   第十二阶段：RabbitMQ
           ⏳
   
   第十三阶段：Docker
           ⏳
   
   第十四阶段：Linux / Nginx
           ⏳
   ```

   ------

   # 三十九、当前开发位置

   **当前项目已经结束基础数据分析阶段。**

   目前不要：

   ```text
   ❌ 重新设计数据库
   ❌ 重写 FastAPI
   ❌ 重写交换业务
   ❌ 为了数量继续画图
   ❌ 一次加入大量新技术
   ```

   当前应该：

   ```text
   KNN 推荐系统
       ↓
   第一步
       ↓
   理解 KNN 如何判断两个物品相似
   ```

   ------

   # 四十、下一次继续开发时的起点

   下一次继续本项目时：

   **不要从 FastAPI 重新开始。**

   直接从：

   ```text
   【KNN 推荐系统】
   ```

   开始。

   第一步先解释：

   ```text
   1. KNN 是什么？
   2. KNN 中的 K 是什么？
   3. 什么叫“邻居”？
   4. 什么叫“距离”？
   5. 两个物品怎么转换成数字？
   6. 两个物品的距离怎么算？
   7. 为什么距离越近就可以认为越相似？
   ```

   然后再结合当前项目的：

   ```text
   Items
   ├── name
   ├── description
   ├── category
   ├── price
   └── user_id
   ```

   一步一步实现：

   ```text
   物品数据
    ↓
   特征
    ↓
   数值向量
    ↓
   KNN
    ↓
   相似物品
    ↓
   推荐函数
    ↓
   FastAPI 推荐接口
   ```

   ------

   # 四十一、Git 使用规范

   每完成一个稳定功能：

   ```bash
   git status
   ```

   查看修改。

   然后：

   ```bash
   git add .
   ```

   提交：

   ```bash
   git commit -m "完成XXX功能"
   ```

   推送：

   ```bash
   git push origin master
   ```

   推荐提交方式：

   ```text
   完成用户注册
   完成 JWT 登录认证
   完成交换接受功能
   完成数据分析
   完成物品类别清洗
   完成 KNN 推荐基础功能
   ```

   不要把大量不同功能混在一个 Commit 中。

   ------

   # 四十二、当前项目核心学习目标

   这个项目最终不是为了简单地：

   ```text
   把代码写出来
   ```

   而是希望真正掌握：

   ```text
   Python
    ↓
   Web 后端
    ↓
   数据库
    ↓
   数据分析
    ↓
   机器学习
    ↓
   推荐系统
    ↓
   NLP
    ↓
   LLM
    ↓
   Agent
    ↓
   系统工程
   ```

   最终形成一个完整的技术链：

   ```text
   数据产生
      ↓
   数据库存储
      ↓
   后端业务
      ↓
   数据分析
      ↓
   机器学习
      ↓
   推荐
      ↓
   LLM
      ↓
   Agent
      ↓
   缓存 / 消息队列
      ↓
   Docker
      ↓
   Linux
      ↓
   Nginx
      ↓
   完整可部署项目
   ```

   ------

   # 四十三、当前最重要的一句话

   > **FastAPI 基础业务已经完成，Pandas + Matplotlib 数据分析阶段已经基本完成，下一阶段正式进入 KNN 推荐系统。**

   后续开发遵循：

   > **一步一功能 → 解释原理 → 写代码 → 测试 → 确认 → 再继续。**