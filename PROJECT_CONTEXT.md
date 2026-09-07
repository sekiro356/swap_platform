# AI 智能以物换物平台 - PROJECT_CONTEXT

## 1. 项目基本信息

- GitHub 仓库：`https://github.com/sekiro356/swap_platform.git`
- 分支：`master`
- 项目名称：AI 智能以物换物平台
- 后端：FastAPI
- 数据库：MySQL
- ORM：SQLAlchemy
- 密码：bcrypt
- 登录认证：JWT / PyJWT
- 请求认证：HTTPBearer
- 数据分析：Python + Pandas + Matplotlib + Seaborn
- 后续推荐：scikit-learn / KNN
- 后续 AI：Embedding、LangChain、LangGraph、RAG、Memory、Agent

原则：

> 继续在现有项目上开发，不重新设计项目，不随意重构已有代码。

当前主要目标：

```text
MySQL
  ↓
SQLAlchemy
  ↓
Python
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
  ↓
用户行为数据
  ↓
KNN 推荐
```

------

# 2. 已完成的核心业务

目前 FastAPI + MySQL 的核心业务已经基本完成。

## 用户

已经实现：

- 用户注册
- 用户登录
- 获取当前用户
- JWT 身份认证
- bcrypt 密码哈希

## 物品

`items` 表核心字段：

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

物品状态：

```text
available
unavailable
```

已经实现：

- 创建物品
- 查询物品
- 修改物品
- 删除物品
- 物品状态控制

------

# 3. 交换业务

`swap` 核心字段：

```text
id
requester_id
target_item_id
offered_item_id
status
```

字段含义：

```text
requester_id
    发起交换的用户

target_item_id
    发起者想要获得的物品

offered_item_id
    发起者拿出来交换的自己的物品
```

例如：

```text
用户 A：
拿自己的“数码产品”
交换
用户 B 的“书”

category_offered = 数码
category_target = 书
```

交换状态：

```text
pending
accepted
rejected
```

已经实现：

- 创建交换请求
- 查询交换记录
- 接受交换
- 拒绝交换
- 权限检查
- 状态检查
- 交换成功后锁定双方物品

------

# 4. 当前开发阶段：Week 2 数据分析

当前没有继续开发新业务，而是在已有数据库基础上做数据分析。

目标：

> 从真实业务数据中分析用户、物品、交换行为，为后面的推荐系统准备数据。

当前分析文件：

```text
backend/analysis.py
```

目前代码采用：

```python
db = SessionLocal()
...
db.close()
```

暂时不进行 `get_db()` 等结构重构。

------

# 5. analysis.py 当前数据读取

```python
import pandas as pd
from models import User, Items, Swap
from database import SessionLocal

db = SessionLocal()

users = db.query(User).all()

df_user = pd.DataFrame([
    {
        'id': user.id,
        'username': user.username
    }
    for user in users
])

items = db.query(Items).all()

df_items = pd.DataFrame([
    {
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'price': item.price,
        'user_id': item.user_id,
        'status': item.status
    }
    for item in items
])

swaps = db.query(Swap).all()

df_swaps = pd.DataFrame([
    {
        'id': swap.id,
        'requester_id': swap.requester_id,
        'target_item_id': swap.target_item_id,
        'offered_item_id': swap.offered_item_id,
        'status': swap.status
    }
    for swap in swaps
])

db.close()
```

曾经出现：

```python
users = db.query(User).all
```

错误：

```text
TypeError: 'method' object is not iterable
```

原因：

```text
.all
```

是方法本身。

```text
.all()
```

才是调用方法并获取查询结果。

------

# 6. 基础数据统计

已经完成：

```python
print('\n用户数量: ', len(df_user))
print('\n物品数量: ', len(df_items))
print('\n交换记录数量: ', len(df_swaps))

print(df_items['category'].value_counts())
print(df_swaps['status'].value_counts())
```

可以统计：

```text
用户数量
物品数量
交换记录数量
不同物品类别数量
不同交换状态数量
```

------

# 7. 用户拥有物品数量

已经完成：

```python
item_count = (
    df_items
    .groupby('user_id')
    .size()
    .reset_index(name='item_count')
)
```

然后与用户表合并：

```python
df_user_analysis = df_user.merge(
    item_count,
    left_on='id',
    right_on='user_id',
    how='left'
)
```

处理没有物品的用户：

```python
df_user_analysis['item_count'] = (
    df_user_analysis['item_count']
    .fillna(0)
    .astype(int)
)
```

已经理解：

### groupby

```python
df_items.groupby('user_id')
```

按照用户 ID 分组。

### size

```python
.size()
```

统计每组有多少条记录。

### reset_index

```python
.reset_index(name='item_count')
```

把分组结果重新变成 DataFrame，并给统计结果命名。

### merge

用于把不同 DataFrame 的数据连接起来。

### how='left'

表示：

> 左边 DataFrame 的数据全部保留。

所以没有物品的用户也会保留下来，然后：

```python
NaN → 0
```

------

# 8. 用户交换次数

已经完成：

```python
user_swap_count = (
    df_swaps
    .groupby('requester_id')
    .size()
    .reset_index(name='swap_count')
)
```

含义：

> 统计每个用户发起了多少次交换。

------

# 9. 用户成功交换次数

已经完成：

```python
user_accepted_count = (
    df_swaps[df_swaps['status'] == 'accepted']
    .groupby('requester_id')
    .size()
    .reset_index(name='accepted_count')
)
```

其中：

```python
df_swaps['status'] == 'accepted'
```

得到的是一个布尔 Series。

例如：

```text
True
False
True
False
```

然后：

```python
.sum()
```

可以统计 True 的数量。

------

# 10. 用户交换行为分析

先合并交换次数和成功次数：

```python
user_swap_analysis = user_swap_count.merge(
    user_accepted_count,
    on='requester_id',
    how='left'
)
```

处理没有成功交换的用户：

```python
user_swap_analysis['accepted_count'] = (
    user_swap_analysis['accepted_count']
    .fillna(0)
    .astype(int)
)
```

计算成功率：

```python
user_swap_analysis['success_rate'] = (
    user_swap_analysis['accepted_count']
    / user_swap_analysis['swap_count']
)
```

当前测试数据类似：

```text
requester_id    swap_count    accepted_count    success_rate

2               1             1                 1
3               1             0                 0
5               1             0                 0
```

注意：

目前每个用户的交换次数还比较少，因此成功率暂时只能作为演示分析，不能作为可靠的用户画像。

------

# 11. 用户名合并

把 requester_id 对应到用户名：

```python
user_swap_analysis = user_swap_analysis.merge(
    df_user[['id', 'username']],
    left_on='requester_id',
    right_on='id',
    how='left'
)

user_swap_analysis = user_swap_analysis.drop(columns='id')
```

理解：

```text
requester_id
     ↓
User.id
     ↓
username
```

------

# 12. 最终用户行为表

已经将：

```text
用户信息
+
物品数量
+
交换次数
+
成功交换次数
+
交换成功率
```

合并成：

```python
user_behavior = df_user_analysis.merge(
    user_swap_analysis[
        ['requester_id', 'swap_count', 'accepted_count', 'success_rate']
    ],
    left_on='id',
    right_on='requester_id',
    how='left'
)
```

处理空值：

```python
user_behavior['swap_count'] = (
    user_behavior['swap_count']
    .fillna(0)
    .astype(int)
)

user_behavior['accepted_count'] = (
    user_behavior['accepted_count']
    .fillna(0)
    .astype(int)
)

user_behavior['success_rate'] = (
    user_behavior['success_rate']
    .fillna(0)
)
```

当前数据结构类似：

```text
id    username    item_count    swap_count    accepted_count    success_rate

2     老王        ...           1             1                 1
3     小明        ...           1             0                 0
4     佐助        ...           0             0                 0
5     鸣人        ...           1             0                 0
```

其中：

```text
佐助没有交换记录
```

但因为使用：

```python
how='left'
```

所以用户仍然保留，只是交换相关数据为空，之后填成 0。

------

# 13. 交换类别关系分析

目标：

> 分析用户拿什么类别的物品，去交换什么类别的物品。

首先根据：

```text
target_item_id
```

找到目标物品类别。

```python
swap_analysis = df_swaps.merge(
    df_items[['category', 'id']],
    left_on='target_item_id',
    right_on='id',
    how='left'
)
```

然后根据：

```text
offered_item_id
```

找到提供物品类别：

```python
swap_analysis = swap_analysis.merge(
    df_items[['category', 'id']],
    left_on='offered_item_id',
    right_on='id',
    how='left',
    suffixes=('_target', '_offered')
)
```

这里必须进行两次 merge。

原因：

```text
target_item_id
        ↓
目标物品
        ↓
category_target

offered_item_id
        ↓
提供物品
        ↓
category_offered
```

两个 ID 不一样，因此需要分别查询 `df_items`。

------

# 14. left_on / right_on

已经重点理解：

```python
left_on='target_item_id'
right_on='id'
```

意思：

```text
左边 DataFrame：
target_item_id

        ↕ 匹配

右边 DataFrame：
id
```

也就是：

```text
target_item_id = Items.id
```

第二次：

```python
left_on='offered_item_id'
right_on='id'
```

也就是：

```text
offered_item_id = Items.id
```

`right_on` 两次都是：

```python
'id'
```

因为右边的 `df_items` 主键都是 `id`。

------

# 15. 交换类别关系统计

已经完成：

```python
swap_relation = (
    swap_analysis
    .groupby(['category_offered', 'category_target'])
    .size()
    .reset_index(name='swap_count')
)
```

当前测试数据得到过：

```text
category_target    category_offered    swap_count

书                 数码                1
数码               数码                2
```

含义：

```text
数码 → 书
发生 1 次

数码 → 数码
发生 2 次
```

------

# 16. 交换类别比例

已经完成：

```python
swap_relation['ratio'] = (
    swap_relation['swap_count']
    / swap_relation['swap_count'].sum()
)
```

得到过：

```text
数码 → 书       0.333333
数码 → 数码     0.666667
```

也就是：

```text
数码 → 书       33.33%
数码 → 数码     66.67%
```

这个分析比单纯计算平均价格更有业务意义。

目前暂时不重点做：

```text
所有物品平均价格
```

因为不同类别之间价格差异较大，直接求平均容易得到没有业务意义的结论。

当前更关注：

```text
用户行为
类别偏好
交换关系
交换成功情况
```

------

# 17. Matplotlib 可视化

已经开始使用 Matplotlib。

中文显示设置：

```python
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
```

如果电脑没有微软雅黑，可以尝试：

```python
plt.rcParams['font.sans-serif'] = ['SimHei']
```

------

# 18. 用户物品数量图

已经完成：

```python
plt.bar(
    user_behavior['username'],
    user_behavior['item_count']
)

plt.xlabel('用户')
plt.ylabel('物品数量')
plt.title('每个用户的物品数量')

plt.show()
```

------

# 19. 用户交换次数图

已经完成：

```python
plt.bar(
    user_behavior['username'],
    user_behavior['swap_count']
)

plt.xlabel('用户')
plt.ylabel('交换次数')
plt.title('用户交换次数')

plt.show()
```

------

# 20. 两个指标放在一张图

目前正在学习分组柱状图。

代码：

```python
x = range(len(user_behavior['username']))

plt.bar(
    [i - 0.2 for i in x],
    user_behavior['item_count'],
    width=0.4,
    label='物品数量'
)

plt.bar(
    [i + 0.2 for i in x],
    user_behavior['swap_count'],
    width=0.4,
    label='交换次数'
)

plt.xticks(x, user_behavior['username'])
plt.xlabel('用户')
plt.ylabel('数量')
plt.title('用户物品数量与交换次数')
plt.legend()

plt.show()
```

核心理解：

```text
x = [0, 1, 2, 3]
```

代表：

```text
第1个用户 → 0
第2个用户 → 1
第3个用户 → 2
第4个用户 → 3
```

如果两组柱子都直接使用：

```python
plt.bar(x, ...)
```

那么两个柱子会重叠。

所以：

```python
[i - 0.2 for i in x]
```

把第一组柱子向左移动。

而：

```python
[i + 0.2 for i in x]
```

把第二组柱子向右移动。

`width=0.4` 是柱子的宽度。

因为：

```text
0.4 / 2 = 0.2
```

所以使用：

```text
左边：i - 0.2
右边：i + 0.2
```

正好让两个宽度为 0.4 的柱子并排。

例如：

```text
用户1中心位置 = 0

        左柱        右柱
         ↓           ↓
       -0.2         +0.2
         █           █
         █           █
         █           █
-----------------------------→
       物品数量     交换次数
```

------

# 21. Matplotlib 用户太多的问题

已经讨论：

如果用户很多，横坐标用户名会变得拥挤。

问题不在：

```python
x = range(...)
```

而在：

```text
用户数量太多
```

不建议做类似网页的“分页”。

数据分析中更常见的是：

```text
Top N
排序
筛选
```

例如取交换次数最高的前 10 个用户：

```python
top_users = (
    user_behavior
    .sort_values('swap_count', ascending=False)
    .head(10)
)
```

后续如果用户数量变多，可以继续做：

```text
Top 10 用户
Top 20 用户
按交换次数排序
按物品数量排序
```

而不是把所有用户全部画在一张图里。

------

# 22. 当前已经掌握的 Pandas

目前已经实际使用并理解：

```text
DataFrame
Series
groupby
size
reset_index
merge
left_on
right_on
how='left'
fillna
astype
drop
value_counts
sort_values
head
```

以及：

```python
df['column']
```

获取 DataFrame 某一列。

已经遇到并解决：

```python
if not df_user_analysis['user_id']:
```

导致：

```text
ValueError:
The truth value of a Series is ambiguous
```

原因：

```text
df['user_id']
```

得到的是整个 Series，不是一个单独的 True / False。

------

# 23. 当前已经掌握的 Matplotlib

目前已经开始使用：

```text
plt.bar()
plt.xlabel()
plt.ylabel()
plt.title()
plt.xticks()
plt.legend()
plt.show()
```

并正在理解：

```text
x 位置
bar width
柱子左右偏移
分组柱状图
```

特别是：

```python
[i - 0.2 for i in x]
[i + 0.2 for i in x]
```

本质上是在调整柱子的横坐标位置，让两组柱子并排显示。

------

# 24. 当前项目阶段

当前进度：

```text
Week 1
后端核心业务
        ↓
已基本完成

Week 2
数据分析
        ↓
正在进行

    ├── MySQL 数据读取       ✅
    ├── Pandas DataFrame     ✅
    ├── 基础统计              ✅
    ├── 用户物品数量          ✅
    ├── 用户交换次数          ✅
    ├── 用户成功交换次数      ✅
    ├── 用户交换成功率        ✅
    ├── 用户行为表            ✅
    ├── 交换类别关系          ✅
    ├── 类别交换比例          ✅
    ├── Matplotlib 基础       ✅
    ├── 分组柱状图            🔄
    └── 更进一步的业务分析    ⏳

Week 3
推荐系统
        ↓
scikit-learn
KNN
用户/物品特征
        ↓

后续
Embedding
LangChain
LangGraph
RAG
Memory
Agent
```

------

# 25. 下一步

当前不要直接跳到 KNN。

优先继续完成 Week 2：

```text
当前分组柱状图
        ↓
Top N 用户可视化
        ↓
交换类别可视化
        ↓
进一步用户行为分析
        ↓
整理推荐系统需要的特征
        ↓
再进入 KNN
```

下一步建议继续：

> **把当前 `user_behavior` 做一个 Top N 用户分析/可视化。**

之后再逐步把分析结果转成 KNN 推荐所需要的数据。

------

# 26. 项目开发原则

后续继续本项目时：

1. 不重新设计已有项目。
2. 不随意重构已有代码。
3. 优先在现有代码基础上增加功能。
4. 一次学习一个小步骤。
5. 每写一段代码先运行确认。
6. 用户问某个语法时，先解释当前语法，不要直接跳到后面的高级内容。
7. 数据分析优先关注业务意义，不为了使用某个 Pandas 函数而强行分析。
8. 推荐系统建立在前面的真实用户行为数据之上。
9. 当前阶段重点是 Pandas + Matplotlib + 业务分析，不急着进入 LangChain/LangGraph。
10. 每次继续项目时，以本文件和当前实际代码为准。