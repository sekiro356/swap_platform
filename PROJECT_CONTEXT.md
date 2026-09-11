对，你这个疑问是对的：**`class_weight='balanced'` 确实已经在处理类别不平衡了。**
但关键是：

> **类别不平衡只是问题之一，`class_weight='balanced'` 并不能让模型“变准确”。**

你现在的模型效果不理想，**不一定主要是因为类别不平衡**。更大的问题很可能是：你的测试数据是人工构造的，而且“成功/失败”本身和现有特征之间没有特别强的规律。

我先把这次完整的 `PROJECT_CONTEXT` 给你。

# AI 智能以物换物平台 - PROJECT_CONTEXT

## 1. 项目基本信息

**项目名称：** AI 智能以物换物平台 `swap_platform`

**GitHub：**
`https://github.com/sekiro356/swap_platform.git`

**项目目标：**

开发一个可以用于简历、面试展示的 AI 智能以物换物平台。

第一阶段以 FastAPI + MySQL 为基础，实现完整的物品交换业务；随后加入数据分析、机器学习、推荐、LLM、LangChain / LangGraph 等 AI 能力。

项目周期目标约 **1～2个月完成一个可以运行和演示的版本**。

------

# 2. 当前技术栈

### 后端

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- MySQL

### 用户认证

- bcrypt
- JWT
- PyJWT
- HTTPBearer

### 数据分析

- Pandas
- NumPy
- Matplotlib
- Seaborn

### 当前机器学习

- scikit-learn
- train_test_split
- StandardScaler
- One-Hot Encoding
- KNN
- Logistic Regression
- GridSearchCV
- Precision / Recall / F1
- ROC-AUC
- PR-AUC

### 后续计划

- Redis
- RabbitMQ
- Docker
- Linux
- Nginx
- LangChain
- LangGraph
- LLM
- 推荐系统
- 更完善的机器学习模型

------

# 3. 当前后端完成情况

目前已经完成：

```text
FastAPI
   ↓
MySQL
   ↓
SQLAlchemy
   ↓
用户
   ↓
物品
   ↓
交换
```

主要文件：

```text
backend/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── routers/
└── analysis.py
```

数据库：

### users

```text
id
username
password
```

密码已经使用 bcrypt 哈希。

### items

```text
id
name
description
category
price
user_id
status
```

### swaps

```text
id
requester_id
target_item_id
offered_item_id
status
```

------

# 4. 用户认证已经完成

已经完成：

```text
/register
/login
/me
```

JWT 登录认证已经完成。

之前 JWT 完成后的 Git commit：

```text
ad3ccf7
```

Swagger `/docs` 中已经测试 `/me`。

------

# 5. 交换业务已经完成

已经完成交换接受 / 拒绝相关逻辑。

例如：

```text
PUT /swaps/{swap_id}/accept
```

可以处理交换接受。

交换状态包括：

```text
pending
accepted
rejected
```

------

# 6. 数据分析阶段已经完成

已经完成：

```text
MySQL
 ↓
SQLAlchemy
 ↓
Pandas DataFrame
 ↓
数据分析
 ↓
Matplotlib 可视化
```

分析过：

- 用户数量
- 物品数量
- 交换数量
- 每个用户发布物品数量
- 每个用户交换次数
- 用户交换成功次数
- 用户交换成功率
- 物品类别分布
- Top 用户
- 交换成功率
- 类别交换情况
- 类别组合交换情况

目前 `analysis.py` 同时承担数据分析和机器学习数据构造，不急着拆文件。

------

# 7. 当前机器学习真正目标

机器学习的核心目标已经确定：

> **预测一笔具体交换最终成功的概率。**

例如：

```text
用户A

目标物品：
耳机
价格：500

提供物品：
图书
价格：50

用户历史成功率：30%
该类别组合历史成功率：20%

        ↓

机器学习模型

        ↓

预测成功概率：18%
```

最终希望把这个模型接入平台。

------

# 8. 当前机器学习数据

目前构造了约：

```text
1500条交换数据
```

目标：

```python
y = ml_data['label']
```

其中：

```text
label = 1 → accepted
label = 0 → rejected
```

也就是说：

```text
X = 交换的各种特征
y = 最终交换是否成功
```

------

# 9. 当前机器学习特征

目前主要特征：

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

其中：

### 价格特征

```python
price_diff = offered_price - target_price
price_diff_abs = abs(price_diff)
price_ratio = offered_price / target_price
```

------

# 10. 用户历史特征

为了避免数据泄漏，使用了历史累计特征。

例如：

```python
user_swap_count = groupby(...).cumcount()
```

表示：

> 当前交换发生之前，这个用户已经有多少次交换。

用户成功次数使用：

```python
cumsum().shift()
```

确保：

> **当前交换的结果不会被用于预测当前交换。**

然后：

```python
user_success_rate =
user_accepted_count / user_swap_count
```

------

# 11. 类别历史特征

当前使用：

```text
target_category
+
offered_category
```

形成方向：

```text
目标类别 → 提供类别
```

例如：

```text
数码 → 图书
图书 → 数码
数码 → 数码
```

然后计算历史：

```text
category_swap_count
category_accepted_count
category_success_rate
```

同样避免使用当前交换结果造成数据泄漏。

------

# 12. One-Hot Encoding

当前 `X` 已经不是原始类别字符串。

例如：

```text
target_category
offered_category
```

已经转换成类似：

```text
target_category_数码
target_category_图书
offered_category_数码
offered_category_运动
...
```

所以当前：

```text
X.shape
```

为：

```text
(1500, 22)
```

即：

```text
1500条数据
22个模型特征
```

------

# 13. 第一版机器学习模型

最开始尝试过 KNN。

GridSearchCV：

```python
param_grid = {
    'n_neighbors': range(1, 200)
}
```

最终最佳 K：

```text
16
```

但是 KNN 存在严重问题：

```text
正类 Recall ≈ 0.03
```

也就是说：

> 真正成功的交换，模型几乎都没有找出来。

于是没有继续使用 KNN。

------

# 14. 当前模型：Logistic Regression

现在使用：

```python
lr_model = LogisticRegression(
    class_weight='balanced',
    random_state=22
)
```

其中：

```python
class_weight='balanced'
```

用于处理类别不平衡。

------

# 15. 当前数据划分

当前使用：

```python
x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    random_state=22,
    test_size=0.2
)
```

下一版建议增加：

```python
stratify=y
```

即：

```python
x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    random_state=22,
    test_size=0.2,
    stratify=y
)
```

保证训练集和测试集中的成功/失败比例更加接近。

------

# 16. 当前标准化

当前：

```python
transformer = StandardScaler()

x_train = transformer.fit_transform(x_train)
x_test = transformer.transform(x_test)
```

已经明确：

> One-Hot 特征不需要强行标准化。

后续建议：

```text
数值特征
 ↓
StandardScaler

One-Hot 特征
 ↓
保持 0/1
```

而不是全部 22 个特征无差别标准化。

------

# 17. 当前预测

模型：

```python
lr_model.fit(x_train, y_train)
```

然后：

```python
y_prob = lr_model.predict_proba(x_test)[:, 1]
```

得到：

> 每一笔交换预测为成功的概率。

目前使用：

```python
threshold = 0.6
```

然后：

```python
lr_pred = (y_prob >= threshold).astype(int)
```

即：

```text
预测概率 >= 60%
→ 预测成功

预测概率 < 60%
→ 预测失败
```

------

# 18. 当前模型评价

目前已经计算：

```text
Accuracy
Precision
Recall
F1
Confusion Matrix
ROC-AUC
PR-AUC
```

最近得到：

```text
ROC-AUC ≈ 0.8507
PR-AUC ≈ 0.3436
```

目前不再继续疯狂调参数。

原因：

> 当前数据主要是人工构造数据，而且类别严重不平衡，继续调模型容易陷入“为了指标调指标”，偏离项目真正目标。

------

# 19. 当前模型概率分析

已经绘制：

```text
实际失败交换的预测概率
vs
实际成功交换的预测概率
```

代码：

```python
y_prob[y_test == 0]
```

表示：

> 测试集中真实失败的交换，它们的预测成功概率。

而：

```python
y_prob[y_test == 1]
```

表示：

> 测试集中真实成功的交换，它们的预测成功概率。

用直方图观察：

> 模型是否能够把成功和失败交换的概率分布区分开。

------

# 20. 最近实际预测的一笔交换

测试集中的一笔交换：

```text
id：950

目标类别：服装
目标价格：500

提供类别：数码
提供价格：2070

price_diff：1570

user_swap_count：7

user_success_rate：0.142857

category_success_rate：0.21875

真实 label：0
```

模型预测：

```text
success_probability：

0.3479689526387992
```

即：

```text
≈ 34.8%
```

因为：

```text
34.8% < 60%
```

所以：

```text
predicted_label = 0
```

即模型预测：

> 这笔交换成功概率较低，并预测为失败。

而实际结果：

```text
label = 0
```

确实失败。

------

# 21. 当前阶段真正完成到哪里

目前已经完成：

```text
数据分析
   ↓
特征工程
   ↓
X / y
   ↓
One-Hot
   ↓
训练集 / 测试集
   ↓
Logistic Regression
   ↓
预测概率
   ↓
模型评价
   ↓
单笔交换预测
```

所以：

> **第一版机器学习模型已经跑通。**

下一阶段不是继续堆模型指标。

而是：

```text
训练好的模型
      ↓
封装预测函数
      ↓
输入一笔交换
      ↓
自动构造特征
      ↓
返回 success_probability
      ↓
接入 FastAPI
```

最终成为平台真正的 AI 功能。

------

# 22. 为什么 `class_weight='balanced'` 了，还是“不准”？

这个问题非常重要。

你说：

> “数量少的权重已经更高了，按理来说应该没问题啊？”

**不完全是。**

`class_weight='balanced'` 做的事情是：

> **告诉模型：别因为成功样本少，就完全忽略成功样本。**

它不是：

> **把成功样本变得更多。**

更不是：

> **让原本没有规律的数据突然产生规律。**

举个极端例子。

假设：

```text
1000笔交换
```

其中：

```text
失败：900
成功：100
```

而且我们发现：

```text
成功/失败
```

跟目前这些特征几乎没有关系。

例如：

```text
价格差
用户历史成功率
类别组合
```

成功和失败都乱七八糟。

那么 Logistic Regression 就算给成功样本更高权重：

```text
成功样本权重 ↑
```

它也没有什么可靠规律可以学习。

它只能：

> **更加认真地寻找规律。**

但如果数据本身没有明显规律，它还是找不到。

------

## 这就是你现在最可能的问题

你现在的数据是我们自己构造出来的。

所以真正值得怀疑的是：

```text
成功/失败
     ↑
到底是根据什么规则产生的？
```

如果你的测试数据大概是：

```text
随机生成用户
随机生成物品
随机生成交换
随机决定 accepted / rejected
```

那么模型很难学好。

因为：

```text
输入 X
   ↓
没有稳定规律
   ↓
label
```

模型当然预测不好。

------

## 还有一个很关键的问题：`class_weight` 不等于概率变准

这一点你现在正好需要知道。

你最终想要的是：

```text
成功概率 = 73%
```

但是：

```python
class_weight='balanced'
```

主要是为了让模型在**分类任务**里更加重视少数类。

它改变的是训练时的损失权重。

所以：

> **用了 `balanced` 后，模型的分类能力可能改善，但 `predict_proba()` 得到的概率不一定就是现实世界中经过良好校准的“真实概率”。**

也就是说：

```text
模型输出：
0.73
```

不能简单理解成：

> “现实中恰好有 73% 的概率成功。”

这也是为什么我们现在先把它叫：

> **模型预测成功概率**

而不是说：

> **绝对准确的真实成功概率。**

------

# 23. 所以现在不要因为指标不好就否定这个模型

你现在这个阶段最重要的是：

> **证明机器学习链路跑通。**

而你现在已经证明了：

```text
一笔交换
 ↓
特征
 ↓
模型
 ↓
0~1之间的预测概率
```

这个闭环已经建立。

以后如果换成真实平台积累的：

```text
10万笔交换
100万笔交换
```

并且真实用户行为产生真实的：

```text
价格
类别
用户历史
交换结果
响应时间
用户活跃度
物品热度
……
```

模型才有更多真实规律可以学习。

------

## 下一步

所以我建议我们现在**不要再改 Logistic Regression**。

下一步正式进入：

> **“把训练好的模型封装成一个预测函数”**

让它从：

```python
y_prob = lr_model.predict_proba(x_test)[:, 1]
```

这种只能对测试集预测的代码，

变成：

```python
predict_swap(...)
```

能够对**一笔新的交换**进行预测。

然后再接到 FastAPI。

这才是从“我做了一个机器学习实验”变成：

> **“我的物换物平台里真的有一个 AI 交换成功率预测功能。”**