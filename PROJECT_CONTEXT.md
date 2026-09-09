1. > # AI 智能以物换物平台 - PROJECT_CONTEXT
>
   > > 项目名称：AI 智能以物换物平台
   > > GitHub：`https://github.com/sekiro356/swap_platform.git`
   > > 当前阶段：**FastAPI 后端 + 数据分析 + 机器学习数据构造**
> > 开发原则：**不重新设计项目，按照当前结构逐步增加功能；一次完成一个小功能，并理解代码。**
   >
> ------
   >
> # 一、项目目标
   >
> 这是一个用于学习和简历展示的 **AI 智能以物换物平台**。
   >
> 基础目标：
   >
> ```text
   > 用户注册
   >    ↓
   > 用户登录
>    ↓
   > 发布物品
>    ↓
   > 发起交换
   >    ↓
   > 接受 / 拒绝交换
>    ↓
   > 记录交换结果
>    ↓
   > 数据分析
   >    ↓
   > 机器学习预测交换成功概率
>    ↓
   > 后续加入 Redis / RabbitMQ / LangChain / LangGraph / LLM
> ```
   >
> 最终希望形成一个能够用于：
   >
> - 简历项目
   > - 面试讲解
> - FastAPI 后端开发练习
   > - 数据分析练习
   > - 机器学习练习
   > - LangChain / LangGraph 实践
   > - LLM 应用实践
   >
   > 的完整项目。
   >
   > ------
   >
   > # 二、当前技术栈
   >
   > ## 后端
   >
   > - Python
   > - FastAPI
> - Uvicorn
   > - Pydantic
> - SQLAlchemy
   > - MySQL
   >
   > ## 用户认证
   >
   > - bcrypt
   > - JWT
   > - PyJWT
   > - HTTPBearer
   >
   > ## 数据分析
   >
   > - NumPy
   > - Pandas
   > - Matplotlib
   > - Seaborn
   >
   > ## 机器学习
>
   > 计划使用：
>
   > - scikit-learn
> - Logistic Regression 等基础分类模型
   > - One-Hot Encoding
> - train_test_split
   > - 模型评估
   >
   > ## 后续计划
   >
   > - Redis
   > - RabbitMQ
   > - Docker
   > - Linux
> - Nginx
   > - LangChain
> - LangGraph
   > - pgvector
> - LLM
   > - 长期记忆
>
   > ------
>
   > # 三、当前项目结构
>
   > 目前主要代码：
>
   > ```text
   > swap_platform/
   > │
   > ├── database.py
   > ├── models.py
   > ├── schemas.py
   > ├── auth.py
   > ├── main.py
   > ├── analysis.py
   > ├── .env
> │
   > └── data/
> ```
   >
> 目前暂时没有强行拆分机器学习代码。
   >
   > 机器学习数据构造直接放在：
   >
> ```text
   > analysis.py
> ```
   >
> 原因：
   >
> `analysis.py` 已经完成：
   >
> ```text
   > MySQL
   >  ↓
   > SQLAlchemy
   >  ↓
   > DataFrame
   >  ↓
   > 数据分析
   > ```
   >
   > 所以当前阶段直接复用：
   >
   > ```python
   > df_user
> df_items
   > df_swaps
> ```
   >
> 继续构造 ML 数据最方便。
   >
> 后期项目成熟以后，再考虑拆分：
   >
> ```text
   > analysis.py
   > ml_data.py
   > train_model.py
   > predict.py
   > ```
   >
> 目前**不重新设计**。
   >
> ------
   >
> # 四、数据库模型
   >
> ## users
   >
> ```text
   > id
   > username
   > password
   > ```
   >
   > 其中：
   >
   > ```text
   > username UNIQUE
   > password VARCHAR(255)
   > ```
>
   > 密码使用 bcrypt 哈希。
>
   > ------
>
   > ## items
>
   > 主要字段：
>
   > ```text
> id
   > name
   > description
   > category
> price
   > user_id
> status
   > ```
   >
   > 其中：
   >
   > ```text
   > category
   > ```
   >
   > 用于表示：
>
   > ```text
> 数码
   > 图书
   > 游戏
   > 生活用品
> ...
   > ```
>
   > ------
   >
   > ## swaps
>
   > 主要字段：
>
   > ```text
   > id
   > requester_id
> target_item_id
   > offered_item_id
> status
   > ```
>
   > 含义：
>
   > ```text
> requester_id
   >     发起交换的用户
> 
   > target_item_id
   >     用户想要的物品
   > 
   > offered_item_id
   >     用户拿出来交换的物品
   > 
> status
   >     accepted / rejected 等
> ```
   >
   > ------
   >
   > # 五、FastAPI 当前功能
   >
> 目前已经实现 / 测试过：
   >
> ```text
   > GET  /
   > GET  /test-db
   > 
   > POST /register
   > POST /login
   > GET  /me
> 
   > POST /items
> 
   > PUT /swaps/{swap_id}/accept
   > ```
   >
   > 已经完成：
   >
   > - MySQL 连接
> - SQLAlchemy
   > - 用户注册
> - bcrypt 密码哈希
   > - 登录
> - JWT
   > - Bearer Token
> - `/me` 用户认证
   > - 发布物品
   > - 交换申请
   > - 接受交换
   >
   > Swagger：
   >
   > ```text
   > /docs
   > ```
   >
   > 已经进行过测试。
   >
   > ------
   >
   > # 六、测试数据
   >
   > 项目使用测试数据进行开发。
   >
   > 之前规划的中等规模：
   >
   > ```text
   > 20 个用户
   > 50 个物品
   > 50 个交换记录
   > ```
   >
   > 目前实际数据库中的交换数据曾经达到约 1500 条，用于机器学习特征构造。
   >
   > ------
>
   > # 七、数据分析已经完成的内容
>
   > `analysis.py` 已经实现：
>
   > ## 1. MySQL → DataFrame
>
   > ```python
   > df_user
   > df_items
   > df_swaps
   > ```
   >
   > 分别对应：
   >
   > ```text
   > 用户表
> 物品表
   > 交换表
> ```
   >
> ------
   >
> ## 2. 基础统计
   >
> 已经统计：
   >
> ```text
   > 用户数量
   > 物品数量
   > 交换记录数量
   > ```
   >
   > ------
   >
   > ## 3. 物品类别统计
>
   > 使用：
>
   > ```python
   > df_items['category'].value_counts()
   > ```
>
   > 统计不同类别物品数量。
>
   > ------
   >
   > ## 4. 用户发布物品数量
>
   > 使用：
>
   > ```python
> df_items.groupby('user_id').size()
   > ```
>
   > 统计每个用户发布了多少物品。
   >
   > ------
   >
   > ## 5. 用户行为分析
   >
> 已经构造：
   >
> ```text
   > item_count
   > swap_count
   > accepted_count
   > success_rate
   > ```
   >
   > 最终形成：
>
   > ```text
> user_behavior
   > ```
>
   > 用于分析：
>
   > ```text
> 用户
   > 拥有物品数量
   > 发起交换数量
   > 成功交换数量
   > 交换成功率
   > ```
>
   > ------
>
   > # 八、数据可视化已经完成
>
   > 已经绘制：
>
   > ## 用户拥有物品数量
>
   > ```text
> 每个用户的物品数量
   > ```
   >
   > ## 用户交换次数
   >
   > ```text
   > 用户交换次数
> ```
   >
> ## Top 10 用户
   >
> 比较：
   >
> ```text
   > 物品数量
> 交换次数
   > ```
   >
   > 使用两个柱状图并排显示。
   >
   > ------
>
   > ## 用户交换次数 + 成功率
>
   > 使用：
   >
   > ```python
   > ax1 = ...
   > ax2 = ax1.twinx()
   > ```
   >
   > 左 Y 轴：
   >
   > ```text
   > 交换次数
   > ```
   >
   > 右 Y 轴：
   >
> ```text
   > 交换成功率
> ```
   >
> 并使用：
   >
> ```python
   > PercentFormatter(1)
> ```
   >
   > 将：
   >
   > ```text
   > 0.4
   > ```
   >
   > 显示成：
   >
   > ```text
   > 40%
   > ```
   >
   > ------
   >
> ## 物品类别分布
   >
> 统计：
   >
> ```text
   > 不同类别物品数量
> ```
   >
> 并绘制柱状图。
   >
> ------
   >
> ## 不同类别交换次数
   >
> 已经将：
   >
   > ```text
   > target_item_id
   > ```
   >
   > 关联到：
   >
   > ```text
   > category
   > ```
   >
   > 统计不同类别发生交换的次数。
   >
   > ------
   >
   > ## 不同类别交换成功率
   >
> 已经统计：
   >
> ```text
   > category_accept_count
   > category_success_rate
   > ```
   >
   > 并绘制成功率柱状图。
>
   > ------
>
   > # 九、数据分析中的一个重要问题：ID 与 NaN
>
   > 在构造机器学习数据时曾经发现：
>
   > ```text
   > target_category    277 NaN
   > target_price       277 NaN
   > ```
   >
   > 原因是：
   >
   > ```text
   > swaps.target_item_id
> ```
   >
> 中存在一些 ID，在：
   >
   > ```text
   > items.id
   > ```
   >
   > 中找不到对应物品。
   >
> 使用：
   >
> ```python
   > df_swaps[
>     ~df_swaps['target_item_id'].isin(df_items['id'])
   > ]
> ```
   >
   > 检查后发现确实存在大量孤立的物品 ID。
   >
   > 后来发现原因与测试数据重新生成有关：
   >
   > ```text
   > 旧物品 ID：1 ~ 56
   > 删除后重新插入物品
   > 新物品 ID：57 ...
   > ```
   >
   > MySQL 的：
   >
   > ```text
   > AUTO_INCREMENT
   > ```
   >
   > 不会因为删除数据自动从 1 重新开始。
   >
   > 因此旧的 swaps 仍然引用旧 item ID，导致：
   >
   > ```text
   > swaps.target_item_id
   >         ↓
   > items.id 找不到
   >         ↓
   > LEFT JOIN
   >         ↓
   > NaN
   > ```
   >
   > 已经解决测试数据一致性问题。
   >
   > 重要认识：
   >
   > > ID 从 57 开始本身并不是问题，真正的问题是外键引用必须对应存在的物品。
   >
   > 如果以后重新生成完整测试数据：
   >
   > ```text
   > users
> items
   > swaps
> ```
   >
   > 必须保证三者数据一致。
   >
   > ------
   >
   > # 十、当前机器学习目标
   >
   > 机器学习部分的目标已经确定：
   >
> > **预测某一个用户发起的一次具体交换请求最终成功的概率。**
   >
> 例如：
   >
> ```text
   > 用户 A
> 
   > 目标物品：
   > 数码产品
   > 价格：500
   > 
   > 提供物品：
   > 图书
   > 价格：50
   > 
   > 用户历史成功率：
   > 60%
   > 
   > 图书 → 数码
   > 历史成功率：
   > 35%
   > 
   > 价格比例：
   > 50 / 500 = 0.1
   > ```
   >
   > 模型最终可能预测：
   >
   > ```text
   > 交换成功概率 = 18%
   > ```
   >
   > ------
   >
   > # 十一、机器学习特征设计
   >
   > 最终计划使用：
   >
> ```text
   > user_swap_count
> user_accepted_count
   > user_success_rate
   > 
   > target_price
   > offered_price
   > price_diff
   > price_diff_abs
   > price_ratio
> 
   > target_category
> offered_category
   > 
   > category_swap_count
   > category_success_rate
   > 
   > label
> ```
   >
> ------
   >
> # 十二、数据泄漏是当前 ML 中的重要原则
   >
> 机器学习预测当前交换时：
   >
> ```text
   > 只能使用当前交换发生之前的信息
> ```
   >
   > 不能使用：
   >
> ```text
   > 当前交换结果
> 未来交换结果
   > 未来统计数据
   > ```
   >
   > 例如：
   >
   > 某用户最终：
   >
   > ```text
   > 100 次交换
   > 60 次成功
   > ```
>
   > 不能用：
>
   > ```text
> 100
   > 60
> 60%
   > ```
   >
   > 去预测他的第 20 次交换。
>
   > 因为第 20 次交换发生的时候：
>
   > ```text
   > 后面的 80 次交换
   > ```
   >
   > 根本还没有发生。
   >
   > 这就是：
   >
   > ```text
   > Data Leakage
   > 数据泄漏
   > ```
   >
> ------
   >
> # 十三、当前 ML 数据构造进度
   >
> 目前继续使用：
   >
> ```text
   > analysis.py
   > ```
   >
> 中的：
   >
> ```python
   > df_user
   > df_items
   > df_swaps
> ```
   >
> 不重新查询数据库。
   >
   > ------
   >
   > ## 第一步：加入目标物品信息
   >
   > 代码：
   >
   > ```python
   > ml_data = df_swaps.merge(
   >     df_items[['id', 'category', 'price']],
   >     left_on='target_item_id',
>     right_on='id',
   >     how='left'
> )
   > 
> ml_data = ml_data.rename(
   >     columns={
>         'category': 'target_category',
   >         'price': 'target_price'
   >     }
   > )
> 
   > ml_data = ml_data.drop(columns='id')
> ```
   >
> 得到：
   >
> ```text
   > target_category
> target_price
   > ```
   >
   > ------
>
   > # 十四、加入提供物品信息
>
   > 继续：
   >
   > ```python
   > ml_data = ml_data.merge(
   >     df_items[['id', 'category', 'price']],
   >     left_on='offered_item_id',
>     right_on='id',
   >     how='left'
> )
   > 
   > ml_data = ml_data.rename(
   >     columns={
>         'category': 'offered_category',
   >         'price': 'offered_price'
>     }
   > )
> 
   > ml_data = ml_data.drop(columns='id')
> ```
   >
> 得到：
   >
   > ```text
   > offered_category
   > offered_price
   > ```
   >
   > ------
   >
   > # 十五、价格关系特征
   >
   > 已经完成：
   >
   > ```python
   > ml_data['price_diff'] = (
>     ml_data['offered_price'] -
   >     ml_data['target_price']
> )
   > 
   > ml_data['price_diff_abs'] = (
   >     ml_data['price_diff'].abs()
   > )
   > 
   > ml_data['price_ratio'] = (
   >     ml_data['offered_price'] /
   >     ml_data['target_price']
   > )
   > ```
   >
   > 三个特征含义：
   >
   > ```text
   > price_diff
   > ```
>
   > 有方向的价格差：
>
   > ```text
> 提供价格 - 目标价格
   > ```
>
   > 例如：
   >
   > ```text
> 100 - 500 = -400
   > ```
>
   > 说明提供物品比目标物品便宜 400。
>
   > ------
   >
   > ```text
> price_diff_abs
   > ```
>
   > 绝对价格差：
   >
   > ```text
> |-400| = 400
   > ```
>
   > 只表示价格差距，不表示方向。
>
   > ------
>
   > ```text
> price_ratio
   > ```
>
   > 价格比例：
>
   > ```text
> offered_price / target_price
   > ```
   >
   > 例如：
   >
   > ```text
> 100 / 500 = 0.2
   > ```
>
   > 表示提供物品价格是目标物品的 20%。
>
   > ------
   >
   > # 十六、用户历史行为特征
   >
   > 已经完成：
>
   > ```text
> user_swap_count
   > user_accepted_count
> user_success_rate
   > ```
>
   > ------
>
   > ## user_swap_count
>
   > 代码：
   >
   > ```python
   > ml_data = ml_data.sort_values(
   >     'id'
   > ).reset_index(drop=True)
> 
   > ml_data['user_swap_count'] = (
>     ml_data.groupby('requester_id').cumcount()
   > )
> ```
   >
   > 含义：
   >
> > 当前交换发生之前，这个用户已经发起过多少次交换。
   >
> 例如：
   >
   > ```text
   > 第1次交换 → 0
> 第2次交换 → 1
   > 第3次交换 → 2
> 第4次交换 → 3
   > ```
   >
   > ------
>
   > ## sort_values
>
   > ```python
   > ml_data.sort_values('id')
   > ```
   >
   > 按照：
   >
> ```text
   > id
> ```
   >
   > 从小到大排序。
   >
> 当前项目暂时使用自增：
   >
> ```text
   > swap.id
   > ```
   >
> 作为交换先后顺序。
   >
> ------
   >
> ## reset_index
   >
> ```python
   > .reset_index(drop=True)
> ```
   >
> 重新整理 DataFrame 行号：
   >
   > ```text
   > 0
   > 1
   > 2
   > 3
   > ...
   > ```
   >
   > `drop=True`：
   >
   > > 不保留旧行号。
   >
   > ------
   >
   > # 十七、user_accepted_count
   >
> 代码：
   >
> ```python
   > ml_data['user_accepted_count'] = (
>     ml_data.groupby('requester_id')['status']
   >     .transform(
>         lambda x:
   >             x.eq('accepted')
   >             .cumsum()
   >             .shift(fill_value=0)
>     )
   > )
> ```
   >
   > 含义：
   >
> > 当前交换发生之前，该用户已经成功过多少次。
   >
> ------
   >
   > ## eq
   >
   > ```python
> x.eq('accepted')
   > ```
>
   > 相当于：
>
   > ```python
   > x == 'accepted'
   > ```
>
   > 得到：
>
   > ```text
   > True
   > False
> True
   > ```
>
   > ------
   >
   > ## cumsum
   >
   > 累计求和。
   >
   > 例如：
   >
> ```text
   > True
> False
   > True
> True
   > ```
   >
   > 相当于：
>
   > ```text
> 1
   > 0
   > 1
   > 1
> ```
   >
> 累计：
   >
   > ```text
   > 1
   > 1
   > 2
   > 3
   > ```
>
   > ------
>
   > ## shift
>
   > ```python
> .shift()
   > ```
   >
   > 将结果向下移动一行。
>
   > 目的是：
>
   > > 不使用当前交换的结果，只使用当前交换之前的历史结果。
>
   > 例如：
   >
   > ```text
> cumsum：
   > 
> 0
   > 1
> 2
   > 2
   > 
   > shift：
> 
   > 0
> 0
   > 1
> 2
   > ```
   >
   > 所以：
>
   > ```text
> shift
   > ```
   >
   > 本身并不等于“历史特征”。
   >
   > 准确理解是：
>
   > > **把当前计算结果往后移动，让当前行只能看到上一条记录之前已经累计的数据，从而排除当前记录。**
>
   > 这是防止数据泄漏的重要技巧。
>
   > ------
>
   > # 十八、transform
   >
   > ```python
> groupby(...).transform(...)
   > ```
>
   > 作用：
>
   > > 分组计算，但结果保持和原 DataFrame 一样的行数。
>
   > 例如：
   >
   > ```text
   > 原数据 1000 行
   >         ↓
   > groupby
   >         ↓
   > 每个用户单独计算
>         ↓
   > transform
>         ↓
   > 仍然返回 1000 行
   > ```
   >
   > 这样计算出来的结果可以直接：
   >
   > ```python
> ml_data['user_accepted_count'] = ...
   > ```
>
   > ------
   >
   > # 十九、lambda
>
   > 例如：
>
   > ```python
   > lambda x: x + 1
   > ```
>
   > 可以理解成：
>
   > ```python
> def func(x):
   >     return x + 1
> ```
   >
   > 所以：
   >
> ```python
   > transform(
>     lambda x:
   >         x.eq('accepted')
   >         .cumsum()
   >         .shift(fill_value=0)
   > )
> ```
   >
> 本质上就是：
   >
   > > 对每一个用户的 status 数据执行这一套计算。
   >
   > ------
   >
> # 二十、user_success_rate
   >
> 已经完成：
   >
   > ```python
   > ml_data['user_success_rate'] = (
   >     ml_data['user_accepted_count'] /
>     ml_data['user_swap_count']
   > )
> 
   > ml_data['user_success_rate'] = (
   >     ml_data['user_success_rate'].fillna(0)
   > )
> ```
   >
> 公式：
   >
   > ```text
   > 历史成功次数
   > ──────────────
   > 历史交换次数
   > ```
>
   > 第一次交换：
>
   > ```text
> 0 / 0
   > ```
>
   > 会产生：
   >
   > ```text
> NaN
   > ```
>
   > 因此暂时：
   >
   > ```python
   > .fillna(0)
   > ```
   >
   > 处理。
   >
> ------
   >
> # 二十一、类别方向历史特征
   >
   > 现在已经完成：
   >
   > ```text
   > category_swap_count
   > category_accepted_count
> category_success_rate
   > ```
>
   > ------
>
   > ## category_swap_count
>
   > 代码：
   >
   > ```python
> ml_data['category_swap_count'] = (
   >     ml_data
>     .groupby(
   >         [
>             'target_category',
   >             'offered_category'
   >         ]
   >     )
   >     .cumcount()
   > )
   > ```
   >
> 含义：
   >
> > 当前交换发生之前，相同的“目标类别 → 提供类别”已经出现过多少次。
   >
   > 例如：
   >
> ```text
   > 数码 → 图书
> 数码 → 图书
   > 数码 → 图书
   > ```
   >
   > 对应：
   >
> ```text
   > 0
> 1
   > 2
> ```
   >
> ------
   >
   > # 二十二、category_accepted_count
   >
   > 代码：
>
   > ```python
> ml_data['category_accepted_count'] = (
   >     ml_data
   >     .groupby(
   >         [
   >             'target_category',
   >             'offered_category'
>         ]
   >     )['status']
>     .transform(
   >         lambda x:
   >             x.eq('accepted')
   >             .cumsum()
   >             .shift(fill_value=0)
   >     )
> )
   > ```
>
   > 含义：
   >
   > > 当前交换发生之前，这个类别交换方向已经成功过多少次。
   >
   > 例如：
>
   > ```text
> 数码 → 图书
   > 
> 第1次 accepted
   > 第2次 rejected
   > 第3次 accepted
   > 第4次 当前交换
   > ```
   >
   > 当前第4次看到：
>
   > ```text
> category_swap_count = 3
   > category_accepted_count = 2
> ```
   >
> 而不是把当前第4次的结果计算进去。
   >
> ------
   >
   > # 二十三、category_success_rate
   >
   > 代码：
   >
> ```python
   > ml_data['category_success_rate'] = (
>     ml_data['category_accepted_count'] /
   >     ml_data['category_swap_count']
   > )
   > 
   > ml_data['category_success_rate'] = (
   >     ml_data['category_success_rate'].fillna(0)
   > )
   > ```
   >
   > 公式：
>
   > ```text
> 类别方向历史成功次数
   > ────────────────────
   > 类别方向历史交换次数
   > ```
   >
   > 例如：
   >
   > ```text
> 图书 → 数码
   > 
> 历史交换 20 次
   > 成功 7 次
   > 
   > category_success_rate
   > = 7 / 20
> = 35%
   > ```
>
   > ------
>
   > # 二十四、label
>
   > 已经完成：
>
   > ```python
> ml_data['label'] = (
   >     ml_data['status'] == 'accepted'
> ).astype(int)
   > ```
>
   > 转换：
>
   > ```text
> accepted → 1
   > rejected → 0
> ```
   >
> `label` 是机器学习中的：
   >
   > ```text
   > 目标变量
   > Target
> ```
   >
> 模型需要学习：
   >
   > ```text
   > 特征 X
   >    ↓
   > 模型
   >    ↓
> 预测 label / 成功概率
   > ```
>
   > ------
>
   > # 二十五、目前 ml_data 的结构
   >
   > 目前大致已经形成：
   >
> ```text
   > id
> requester_id
   > target_item_id
> offered_item_id
   > status
> 
   > target_category
> target_price
   > 
> offered_category
   > offered_price
> 
   > price_diff
   > price_diff_abs
   > price_ratio
   > 
> user_swap_count
   > user_accepted_count
> user_success_rate
   > 
> category_swap_count
   > category_accepted_count
> category_success_rate
   > 
   > label
   > ```
   >
   > 其中：
   >
   > ```text
> category_accepted_count
   > ```
>
   > 主要是为了计算：
   >
   > ```text
   > category_success_rate
   > ```
>
   > 它暂时属于中间计算字段。
>
   > ------
   >
   > # 二十六、下一步
>
   > 当前已经完成：
>
   > ```text
   > MySQL
   >  ↓
> DataFrame
   >  ↓
> 数据分析
   >  ↓
   > 机器学习数据构造
   >  ↓
> 用户历史特征
   >  ↓
> 价格特征
   >  ↓
> 类别特征
   >  ↓
   > 历史类别成功率
   >  ↓
   > label
> ```
   >
> 下一步正式进入：
   >
> # X 和 y
   >
> 需要把数据整理成：
   >
   > ```python
   > X = 特征
   > y = label
> ```
   >
> 例如：
   >
> ```text
   > X：
> 
   > user_swap_count
> user_accepted_count
   > user_success_rate
   > target_price
   > offered_price
   > price_diff
> price_diff_abs
   > price_ratio
> target_category
   > offered_category
   > category_swap_count
   > category_success_rate
   > y：
   > 
> label
   > ```
>
   > 然后进行：
   >
   > ```text
> 类别特征 One-Hot Encoding
   >         ↓
> 训练集 / 测试集划分
   >         ↓
> 机器学习模型
   >         ↓
> 训练
   >         ↓
   > 准确率 / Precision / Recall 等评估
   >         ↓
> 预测某次交换成功概率
   > ```
>
   > ------
   >
   > # 二十七、One-Hot Encoding 计划
>
   > 当前：
>
   > ```text
> target_category
   > offered_category
> ```
   >
   > 仍然是字符串。
   >
   > 例如：
   >
   > ```text
   > target_category
   > 数码
   > 图书
   > 游戏
   > ```
   >
   > 不能直接拿给大多数 sklearn 模型。
   >
   > 后续使用：
   >
> ```text
   > One-Hot Encoding
> ```
   >
   > 例如：
   >
> ```text
   > target_category_数码
> target_category_图书
   > target_category_游戏
   > ```
   >
> 而不是简单：
   >
> ```text
   > 数码 = 1
> 图书 = 2
   > 游戏 = 3
> ```
   >
> 因为：
   >
> ```text
   > 数码 > 图书 > 游戏
> ```
   >
   > 这种数字大小关系本身没有实际意义。
   >
   > 后续正式训练时，优先考虑：
   >
   > ```python
   > OneHotEncoder
   > ColumnTransformer
   > ```
   >
   > 避免训练集和测试集类别不一致的问题。
   >
   > ------
>
   > # 二十八、当前开发原则
>
   > 用户希望：
>
   > - 一次只做一个小步骤
> - 不一次性给整个项目代码
   > - 每写一段代码解释一段
> - 代码要结合当前项目
   > - 遇到错误先解决错误
> - 不重新设计现有项目
   > - 尽量复用已经存在的 DataFrame
> - 解释每个陌生函数
   > - 适合整理进学习笔记
>
   > 因此后续开发继续遵循：
   >
   > ```text
> 一个功能
   >  ↓
> 写代码
   >  ↓
   > 运行
   >  ↓
> 检查结果
   >  ↓
> 解释
   >  ↓
> 下一步
   > ```
>
   > ------
>
   > # 二十九、目前总体进度
   >
   > 大致可以理解为：
>
   > ```text
> 第一阶段：FastAPI 基础
   > ████████████████████ 100%
   > 
   > 第二阶段：业务逻辑
> ████████████████████ 100%
   > 
> 第三阶段：数据分析
   > ████████████████████ 100%
   > 
   > 第四阶段：机器学习数据准备
> ████████████████░░░░ 约 80%
   > 
> 第五阶段：模型训练
   > ░░░░░░░░░░░░░░░░░░░░ 还未开始
> 
   > 第六阶段：模型接入 FastAPI
   > ░░░░░░░░░░░░░░░░░░░░
   > 
> 第七阶段：Redis / RabbitMQ
   > ░░░░░░░░░░░░░░░░░░░░
> 
   > 第八阶段：LangChain / LangGraph
   > ░░░░░░░░░░░░░░░░░░░░
   > 
> 第九阶段：LLM / 智能推荐
   > ░░░░░░░░░░░░░░░░░░░░
> ```
   >
> **当前最准确的位置：**
   >
> > 正在完成第四阶段「机器学习数据准备」，下一步就是整理 `X` 和 `y`，然后进行类别 One-Hot 编码。