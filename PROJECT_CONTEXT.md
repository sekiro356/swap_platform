# AI 智能以物换物平台 - PROJECT_CONTEXT

> **用途：跨对话项目上下文**
>
> 本文件是本项目当前开发状态、技术路线、代码结构和后续开发计划的主要参考。
>
> 后续继续开发时：
>
> - **不要重新设计项目**
> - **不要重复已经完成的功能**
> - **不要为了“证明代码没问题”反复制造测试数据**
> - **不要把已经实现的逻辑重新写一遍**
> - 每次只推进 **一个完整的小功能**
> - 优先复用现有代码
> - 修改前先确认当前代码结构，避免因为移动文件、改 import 等问题绕圈
> - 如果某个功能已经实现，只需要在后续功能中直接调用，不要重新实现

------

# 一、项目基本信息

## 1. 项目名称

**AI 智能以物换物平台**

项目目录：

```text
swap_platform
```

GitHub：

```text
https://github.com/sekiro356/swap_platform.git
```

当前主要分支：

```text
master
```

------

# 二、项目目标

这是一个用于：

- 实际运行
- 简历展示
- AI 项目面试
- 后续继续扩展

的 **AI 智能以物换物平台**。

项目不是为了做一个非常复杂的商业级平台，而是希望在 1～2 个月左右形成一个：

> **可以运行、可以演示、可以解释技术实现、能够体现 AI 能力的完整项目。**

------

# 三、总体技术路线

项目整体计划：

```text
FastAPI
   ↓
MySQL
   ↓
用户 / 物品 / 交换业务
   ↓
数据分析
   ↓
机器学习
   ↓
交换成功概率预测
   ↓
FastAPI 接入 AI 预测
   ↓
后续扩展推荐 / NLP / LLM
   ↓
LangChain / LangGraph
   ↓
Redis / RabbitMQ
   ↓
Docker / Linux / Nginx
```

当前重点已经从：

```text
基础后端
```

进入：

```text
机器学习
```

并且已经完成了第一版交换成功预测模型。

------

# 四、当前后端技术栈

已经使用：

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- MySQL
- PyMySQL
- bcrypt
- JWT / PyJWT
- HTTPBearer
- Pandas
- NumPy
- Matplotlib
- scikit-learn
- joblib

后续计划：

- Redis
- RabbitMQ
- Docker
- Linux
- Nginx
- NLP
- LLM
- LangChain
- LangGraph

------

# 五、当前后端核心结构

当前项目核心文件包括：

```text
backend/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
└── routers/
```

ML 相关代码目前正在整理。

为了避免 Python 包导入问题，当前决定：

> **ML 相关文件先统一放在项目根目录/已有明确位置，暂时不要为了“结构漂亮”继续移动文件。**

如果文件移动后导致：

```text
ModuleNotFoundError
```

优先解决实际 import 问题，不要为了目录结构再次大规模调整。

------

# 六、数据库

数据库：

```text
swap_platform
```

使用：

```text
MySQL
```

SQLAlchemy：

```python
create_engine(...)
SessionLocal = sessionmaker(...)
Base = declarative_base()
```

`.env` 已经用于保存敏感配置。

------

# 七、核心数据库模型

## 1. User

用户表：

```text
users
```

核心字段：

```text
id
username
password
```

其中：

```text
username
```

唯一。

密码使用 bcrypt 哈希，不保存明文密码。

------

## 2. Items

物品表：

```text
items
```

核心字段：

```text
id
name
description
category
price
user_id
status
```

目前项目中的物品类别包括：

```text
图书
数码
服装
生活用品
美妆
运动
```

------

## 3. Swap

交换记录表：

```text
swaps
```

核心信息包括：

```text
id
requester_id
target_item_id
offered_item_id
status
```

交换状态目前包括：

```text
pending
accepted
rejected
```

------

# 八、已经完成的后端功能

## 1. FastAPI 基础

已经完成：

```text
/
```

欢迎接口。

以及：

```text
/test-db
```

数据库连接测试。

------

## 2. 用户注册

已经完成：

```text
/register
```

包括：

- 用户名重复检查
- bcrypt 密码哈希
- 写入 MySQL

------

## 3. JWT 登录认证

已经完成 JWT。

核心逻辑：

```text
登录
 ↓
生成 JWT
 ↓
Bearer Token
 ↓
HTTPBearer
 ↓
get_current_user()
 ↓
获取当前用户
```

已经测试：

```text
/me
```

可以正确返回：

```json
{
    "user_id": 2,
    "username": "老王"
}
```

JWT 已经完成。

------

# 九、交换业务

已经完成：

- 创建交换
- 接受交换
- 拒绝交换
- pending / accepted / rejected 状态管理

之前的：

```text
PUT /swaps/{swap_id}/accept
```

问题已经解决。

当前数据库中已经有足够的测试数据用于机器学习开发。

------

# 十、数据分析阶段已经完成

已经使用：

```text
SQLAlchemy
    ↓
MySQL
    ↓
Pandas DataFrame
    ↓
数据分析
    ↓
Matplotlib
```

完成了：

- 用户数量分析
- 物品数量分析
- 交换数量分析
- 用户交换行为
- 用户发布物品数量
- 类别统计
- 类别之间交换方向统计
- 交换状态统计
- 用户行为可视化
- 类别交换可视化

------

# 十一、类别交换方向分析

项目已经实现：

```text
target_category
offered_category
```

例如：

```text
图书 → 数码
数码 → 图书
数码 → 数码
```

这些是不同的交换方向。

因此类别统计不能只统计：

```text
数码
```

而需要统计：

```text
目标类别 → 提供类别
```

之前已经使用两次物品表关联实现过这一逻辑。

这个逻辑已经验证正确。

**后续不要重新解释或重新测试这个基础逻辑，直接复用。**

------

# 十二、机器学习阶段

当前已经进入：

# Week 3：机器学习

目标：

> 根据一笔交换请求的特征，预测这笔交换最终成功的概率。

标签：

```text
accepted = 1
其他 = 0
```

------

# 十三、机器学习特征

当前模型使用 12 个原始特征。

## 用户历史行为

```text
user_swap_count
user_accepted_count
user_success_rate
```

含义：

### user_swap_count

当前交换之前，该用户历史上参与过多少次交换。

### user_accepted_count

当前交换之前，该用户历史上成功过多少次交换。

### user_success_rate

```text
user_accepted_count / user_swap_count
```

历史上没有交换时：

```text
0
```

------

# 十四、价格特征

当前使用：

```text
target_price
offered_price
price_diff
price_diff_abs
price_ratio
```

定义：

```python
price_diff = offered_price - target_price
price_diff_abs = abs(price_diff)
price_ratio = offered_price / target_price
```

例如：

```text
目标物品：300
提供物品：450
```

得到：

```text
price_diff = 150
price_diff_abs = 150
price_ratio = 1.5
```

这个定义后续必须保持一致。

------

# 十五、类别特征

原始类别特征：

```text
target_category
offered_category
```

以及类别方向历史特征：

```text
category_swap_count
category_success_rate
```

其中：

```text
category_swap_count
```

表示：

> 当前交换之前，相同“目标类别 → 提供类别”的历史交换次数。

例如当前：

```text
数码 → 数码
```

则统计历史：

```text
数码 → 数码
```

而不是所有：

```text
数码
```

------

# 十六、数据泄漏处理

机器学习中特别注意：

> 当前交换的结果不能参与当前交换的预测特征。

因此：

```text
user_swap_count
user_accepted_count
user_success_rate
category_swap_count
category_success_rate
```

都必须使用：

> 当前交换发生之前的历史数据。

不能把当前交换的：

```text
accepted / rejected
```

提前放进特征。

这一点已经在原始特征工程中处理。

------

# 十七、当前核心特征工程函数

当前已有：

```python
def build_ml_features(df_swaps, df_items):
    ...
```

它已经负责：

```text
df_swaps
+
df_items
        ↓
目标物品关联
        ↓
提供物品关联
        ↓
价格特征
        ↓
用户历史特征
        ↓
类别方向历史特征
        ↓
label
        ↓
ml_data
```

它是当前项目已经完成的核心特征工程。

**不要重新复制一份完全相同的 merge 和特征计算代码。**

后续如果要支持新交换预测，应优先考虑复用/提取现有逻辑，而不是复制代码。

------

# 十八、当前 X / y 构造

已有：

```python
def build_xy(ml_data):
    ...
```

目前 X 包括：

```text
user_swap_count
user_accepted_count
user_success_rate

target_price
offered_price
price_diff
price_diff_abs
price_ratio

target_category
offered_category

category_swap_count
category_success_rate
```

y：

```text
label
```

------

# 十九、One-Hot Encoding

当前使用：

```python
pd.get_dummies(
    X,
    columns=[
        'target_category',
        'offered_category'
    ],
    dtype=int
)
```

已经得到最终模型输入特征。

------

# 二十、最终模型特征

当前模型最终使用：

```text
[
'user_swap_count',
'user_accepted_count',
'user_success_rate',
'target_price',
'offered_price',
'price_diff',
'price_diff_abs',
'price_ratio',
'category_swap_count',
'category_success_rate',

'target_category_图书',
'target_category_数码',
'target_category_服装',
'target_category_生活用品',
'target_category_美妆',
'target_category_运动',

'offered_category_图书',
'offered_category_数码',
'offered_category_服装',
'offered_category_生活用品',
'offered_category_美妆',
'offered_category_运动'
]
```

总计：

```text
22 个最终模型输入特征
```

------

# 二十一、feature_columns

已经增加：

```python
feature_columns = X.columns.tolist()
```

并保存：

```python
joblib.dump(
    feature_columns,
    'feature_columns.pkl'
)
```

作用：

> 保证以后新交换 One-Hot 后的特征列顺序和训练模型完全一致。

------

# 二十二、模型训练

训练流程：

```text
X / y
 ↓
train_test_split
 ↓
stratify=y
 ↓
StandardScaler
 ↓
LogisticRegression
```

当前 Logistic Regression：

```python
LogisticRegression(
    class_weight='balanced',
    random_state=22
)
```

使用：

```text
class_weight='balanced'
```

解决交换成功/失败类别不平衡问题。

------

# 二十三、KNN 已经尝试过

之前尝试：

```text
KNN
GridSearchCV
```

最佳参数曾经得到：

```text
k = 16
```

但是由于类别严重不平衡，KNN 对正类识别效果很差。

因此当前模型已经切换为：

```text
Logistic Regression
```

**后续不要再回头重复调 KNN。**

------

# 二十四、当前模型效果

当前 Logistic Regression：

```text
ROC-AUC ≈ 0.85068
PR-AUC ≈ 0.34362
```

模型目前已经具备一定区分成功/失败交换的能力。

由于数据中成功交换相对较少：

> PR-AUC 比 ROC-AUC 更值得关注。

------

# 二十五、分类阈值

模型概率默认阈值不是项目最终要求。

当前已经尝试：

```python
threshold = 0.6
```

预测：

```python
y_prob = lr_model.predict_proba(x_test)[:, 1]

lr_pred = (
    y_prob >= threshold
).astype(int)
```

因此当前模型可以根据概率阈值判断：

```text
预测成功
预测失败
```

------

# 二十六、模型解释

已经完成 Logistic Regression 系数分析：

```python
lr_model.coef_[0]
```

并计算：

```python
acs_coefficient
```

用于观察特征影响大小。

之前得到的影响较大的特征包括：

```text
user_accepted_count
user_swap_count
price_diff_abs
category_success_rate
category_swap_count
```

注意：

> 系数表示模型中的统计影响，不等于现实世界中的绝对因果关系。

------

# 二十七、模型保存

已经完成：

```python
joblib.dump(lr_model, 'lr_model.pkl')
joblib.dump(transformer, 'scaler.pkl')
joblib.dump(feature_columns, 'feature_columns.pkl')
```

目前已经有：

```text
lr_model.pkl
scaler.pkl
feature_columns.pkl
```

------

# 二十八、模型加载验证

已经完成保存模型和重新加载模型的验证。

验证结果：

```text
模型预测概率是否一致： True
Scaler mean 是否一致： True
Scaler scale 是否一致： True
```

说明：

> 保存后的模型、Scaler 可以正确重新加载。

**这个验证已经完成，后续不要再重复做。**

------

# 二十九、当前 ML 项目真正进行到哪里

当前已经完成：

```text
数据构造
    ↓
用户行为特征
    ↓
价格特征
    ↓
类别特征
    ↓
历史特征防数据泄漏
    ↓
One-Hot
    ↓
训练/测试集
    ↓
StandardScaler
    ↓
KNN 尝试
    ↓
Logistic Regression
    ↓
类别不平衡处理
    ↓
阈值
    ↓
ROC-AUC / PR-AUC
    ↓
特征重要性
    ↓
模型封装
    ↓
模型保存
    ↓
模型加载
    ↓
保存模型验证
```

**已经完成。**

------

# 三十、当前真正的下一阶段

现在不要再做：

```text
模型训练
模型保存
模型验证
重新测试历史数据
重新画已经画过的图
```

真正下一阶段是：

# 新交换预测

目标：

```text
用户发起一笔新的交换
        ↓
系统读取：
requester_id
target_item_id
offered_item_id
        ↓
根据历史数据计算12个模型特征
        ↓
One-Hot
        ↓
按照 feature_columns 对齐22列
        ↓
Scaler
        ↓
lr_model.predict_proba()
        ↓
得到成功概率
```

最终希望做到：

```text
用户：
我要用物品A交换物品B

        ↓

AI：
预测交换成功概率：73.2%
```

然后再接入 FastAPI。

------

# 三十一、预测代码当前状态

目前已经准备了：

```python
import joblib

model = joblib.load('lr_model.pkl')
scaler = joblib.load('scaler.pkl')
feature_columns = joblib.load('feature_columns.pkl')
```

并准备封装：

```python
def predict_swap(x):
    ...
```

但是当前代码有两个需要修正的问题。

原代码：

```python
def predict_swap(x):

    x = x.reindex(
        columns=feature_columns,
        fil_value=0
    )

    x = scaler.transform(x)

    probability = model.predict(x)

    return probability
```

应该修改为：

```python
def predict_swap(x):

    x = x.reindex(
        columns=feature_columns,
        fill_value=0
    )

    x = scaler.transform(x)

    probability = model.predict_proba(x)[:, 1]

    return probability
```

原因：

### 1. `fil_value` 是拼写错误

正确：

```python
fill_value
```

### 2. `predict()` 返回类别

```python
model.predict(x)
```

返回：

```text
0
1
```

但项目需要的是：

```text
成功概率
```

因此必须：

```python
model.predict_proba(x)[:, 1]
```

------

# 三十二、当前代码设计原则

后续不要把所有东西继续塞进 `analysis.py`。

目前应该逐步形成：

```text
特征工程
    ↓
模型
    ↓
预测
    ↓
FastAPI
```

但：

> **不要为了目录结构漂亮而大规模移动现有文件。**

如果移动文件导致：

```text
ModuleNotFoundError
```

优先按照当前实际目录解决 import。

------

# 三十三、关于 Python import

如果项目结构是：

```text
swap_platform/
└── backend/
    ├── database.py
    ├── models.py
    ├── main.py
```

项目内部如果以 `backend` 作为包运行，可以使用：

```python
from backend.models import User, Items, Swap
from backend.database import SessionLocal
```

但运行方式必须和包结构匹配。

不要一会儿：

```text
python xxx.py
```

一会儿：

```text
python -m backend.xxx
```

导致导入路径不断变化。

**后续如果决定把 ML 文件全部放到项目根目录，则统一按根目录结构处理，不再反复移动。**

------

# 三十四、非常重要：后续开发方式

用户明确要求：

## 每次只做一个完整的小功能

例如：

```text
完成“模型预测函数”
```

而不是一次做：

```text
预测函数
+
FastAPI
+
数据库
+
Redis
+
RabbitMQ
```

------

## 不要重复已经完成的东西

以下内容已经完成：

- JWT
- 用户认证
- 交换接受/拒绝
- 数据分析
- 类别交换分析
- ML 特征构造
- One-Hot
- Logistic Regression
- 模型评估
- ROC-AUC
- PR-AUC
- 特征重要性
- 模型保存
- 模型加载
- 保存/加载验证

后续直接建立在这些基础上。

------

# 三十五、禁止无意义的“测试循环”

以后不要为了：

> “确认代码没问题”

而让用户不断：

```text
运行
↓
打印
↓
看 True
↓
再运行
↓
再打印
```

如果功能本身已经实现并且之前已经验证：

> **直接进入下一个实际功能。**

只有遇到：

```text
真正的报错
真正的数据错误
真正的逻辑问题
```

才进行针对性调试。

------

# 三十六、当前最正确的开发顺序

接下来严格按照：

```text
① 完成 predict_swap()
        ↓
② 让预测模块能够读取已有模型
        ↓
③ 复用已有特征工程构造“新交换”的12个特征
        ↓
④ One-Hot + 22列对齐
        ↓
⑤ Scaler
        ↓
⑥ predict_proba()
        ↓
⑦ 得到交换成功概率
        ↓
⑧ FastAPI 新增预测接口
        ↓
⑨ Swagger 测试一次完整流程
```

完成后再考虑：

```text
Redis
RabbitMQ
推荐系统
NLP
LLM
LangChain
LangGraph
```

------

# 三十七、当前项目最终 AI 方向

第一阶段：

```text
交换成功概率预测
```

第二阶段可以扩展：

```text
相似物品推荐
```

第三阶段：

```text
相似用户推荐
```

第四阶段：

```text
NLP / LLM
```

例如：

```text
用户自然语言描述：
“我有一个用了两年的索尼耳机，
想换一个适合学习的平板”

        ↓

LLM / NLP
        ↓

提取：
物品
类别
价格
需求
        ↓

推荐交换对象
```

最终再结合：

```text
LangChain
LangGraph
```

形成 AI Agent 能力。

------

# 三十八、项目当前一句话状态

> **基础物换物后端已经完成，数据分析已经完成，机器学习交换成功预测模型已经训练、评估、保存并验证完成，现在正在把模型真正封装成“用户发起新交换 → AI 返回成功概率”的可调用功能，下一步应直接完成 `predict_swap()` 并接入新交换特征，而不是继续做重复测试。**

------

# 三十九、下次继续开发时

直接告诉 AI：

> **继续 AI 智能以物换物平台项目。读取 `PROJECT_CONTEXT.md`，不要重新设计，不要重复已经完成的测试和功能。按照当前进度，从“新交换预测”继续，每次只推进一个完整的小功能。**

当前起点就是：

```text
模型文件：
lr_model.pkl
scaler.pkl
feature_columns.pkl

已有：
build_ml_features()
build_xy()

正在做：
predict_swap()

下一目标：
新交换 → 12个特征 → 22列 → scaler → predict_proba → 成功概率
```