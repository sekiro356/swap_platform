# MySQL -> sqlalchemy -> Python -> pandas DataFrame
# # 将用户转化为 DataFrame 方便后续画图

import pandas as pd
from matplotlib.ticker import PercentFormatter
from models import User,Items,Swap
from database import SessionLocal
import matplotlib.pyplot as plt
import joblib

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# 连接数据库
db = SessionLocal()

# 先将数据库中的表转化为 dataframe 形式，方便画图

users = db.query(User).all()
# 将用户转化为 DateFrame 形式
df_user = pd.DataFrame([
    {
        'id':user.id,
        'username':user.username
    }
    for user in users
])

# df_user : id,username

items = db.query(Items).all()
df_items = pd.DataFrame([
    {
        'id':item.id,
        'name':item.name,
        'category':item.category,
        'price':item.price,
        'user_id': item.user_id,
        'status':item.status
    }
    for item in items
])
# df_items : id , name , category , price , user_id , status

swaps = db.query(Swap).all()
df_swaps = pd.DataFrame([
    {
        'id':swap.id,
        'requester_id':swap.requester_id,
        'target_item_id':swap.target_item_id,
        'offered_item_id':swap.offered_item_id,
        'status':swap.status
    }
    for swap in swaps
])
# df_swaps : id , requester_id , target_item_id , offered_item_id , status


print('\n用户表:\n',df_user)
print('\n物品表:\n',df_items)
print('\n交换申请表:\n',df_swaps)

print('\n用户数量: ',len(df_user))
print('\n物品数量: ',len(df_items))
print('\n交换记录数量: ',len(df_swaps))

# 查看每种物品的数量
print('\n每种物品的数量:\n')
print(df_items['category'].value_counts())

# 查看交换物品状态数量
print('\n交换物品状态数量:\n')
print(df_swaps['status'].value_counts())

# 看谁发布了多少件商品
print('\n每个用户发布的物品数量：')
print(df_items.groupby('user_id').size())

# 给未命名的列重命名
item_count = df_items.groupby('user_id').size().reset_index(name='item_count')
print('\n每个用户发布的物品数量：\n')
print(item_count)

# 关联 物品表和用户表，显示出用户名
df_user_analysis = df_user.merge(
    item_count,
    left_on='id',
    right_on='user_id',     # df_user.id = item_count.user_id
    how='left'      # 以左边为准，左边所有用户都保留
)

# 将 Nan 填充为0
df_user_analysis['item_count'] = df_user_analysis['item_count'].fillna(0)

# 将 item_count 转换为整数
df_user_analysis['item_count'] = df_user_analysis['item_count'].astype(int)
# df_user_analysis : id | username | user_id | item_count
print(df_user_analysis)

# 交换成功率
accept_count = (df_swaps['status'] == 'accepted').sum()
total_count = len(df_swaps)
success_rate = accept_count / total_count

print('\n交换成功率：',success_rate)

# 给交换记录加上类别
swap_analysis = df_swaps.merge(
    df_items[['category','id']], # 只插入 'category','id' 即可，
    left_on='target_item_id',  # id_x 是 df_swaps 的 id, # id_y 是 df_items 的 id
    right_on='id',
    how = 'left'
)
print('\n得出targeted_id 的类别\n',swap_analysis)
print('\n每种物品的数量\n',swap_analysis['category'].value_counts())

# 不同种类交换
swap_analysis = swap_analysis.merge(
    df_items[['category', 'id']],  # 只插入 'category','id' 即可，
    left_on='offered_item_id',
    right_on='id',
    how='left',
    suffixes=('_target','_offered') # 两边都有 category，只会在联合名字相同的列后面加后缀
    # 合并会变成 category_x和 category_y 经过 suffixes 后变成 category_target 和category_offered
)
print('\n得出offered_id 的类别\n',swap_analysis)
print(
    swap_analysis[
        ['target_item_id', 'offered_item_id',
         'category_target', 'category_offered', 'status']
    ]
)

# 统计交换方向
swap_reaction = (
    swap_analysis.groupby(['category_target','category_offered']).size().reset_index(name='swap_count')
)
print('\n物品交换方向的数量\n',swap_reaction)

# 计算每种交换类别占总交换类别的比例(百分比)
swap_reaction['ratio'] = swap_reaction['swap_count'] / swap_reaction['swap_count'].sum() * 100
print('\n物品交换方向所占的百分比\n',swap_reaction)


# 统计每个人发起交换发起了多少次
user_swap_count = (swap_analysis.groupby('requester_id').size().reset_index(name='swap_count'))
print('\n每个人发起了多少次交换\n',user_swap_count)

# 统计每个用户交换成功了多少次
user_accept_count = (swap_analysis[swap_analysis['status'] == 'accepted']
                     .groupby('requester_id').size().reset_index(name='accepted_count'))
print('\n每人成功交换次数\n',user_accept_count)

# 将每个人发起的交换次数与交换成功的表进行融合
user_swap_analysis = user_swap_count.merge(
    user_accept_count,
    on='requester_id',
    how='left'
)

user_swap_analysis['accepted_count'] = user_swap_analysis['accepted_count'].fillna(0).astype(int)
print(user_swap_analysis)

# 后面添加交换成功率
user_swap_analysis['success_rate'] = user_swap_analysis['accepted_count'] / user_swap_analysis['swap_count']
print('\n用户交换分析\n',user_swap_analysis)

# 添加 id 和 用户名，使结果更加直观
user_swap_analysis = user_swap_analysis.merge(
    df_user[['id','username']],
    left_on='requester_id',
    right_on='id',
    how='left'
)

user_swap_analysis = user_swap_analysis.drop(columns='id')
print(user_swap_analysis)

# 把用户拥有多少物品，用户发起过的交换结合起来，形成：
# id , 用户名 , 拥有的物品数 , requester_id , 交换数量 ， 同意数量 ， 交换成功率
user_behavior = df_user_analysis.merge(
    user_swap_analysis[['requester_id','swap_count','accepted_count','success_rate']],
    left_on='id',
    right_on='requester_id',
    how='left'
)

# 填充 Nan
user_behavior['swap_count'] = (user_behavior['swap_count'].fillna(0).astype(int))
user_behavior['accepted_count'] = (user_behavior['accepted_count'].fillna(0).astype(int))
user_behavior['success_rate'] = (user_behavior['success_rate'].fillna(0))

print('\n用户行为表\n',user_behavior)

# 画图
# 用户拥有物品数量图
plt.bar(user_behavior['username'],
        user_behavior['item_count'])
plt.xlabel('用户')
plt.ylabel('物品数量')
plt.title('每个用户的物品数量')
plt.xticks(rotation = 45,ha = 'right')
plt.show()

plt.bar(user_behavior['username'],
        user_behavior['swap_count'])

plt.xlabel('用户')
plt.ylabel('交换次数')
plt.title('用户交换次数')
plt.xticks(rotation = 45,ha = 'right')
plt.show()

# 将两图结合起来，方便查看
# 条件筛选，先以交换数量进行筛选
sort_column = 'swap_count'
top_n = 10 # 查看的数量

top_users = user_behavior.sort_values(
    sort_column, # 以什么进行排序
    ascending=False  # 降序
).head(top_n)

x = range(len(top_users['username'])) # 有多少用户就画几条树状图
plt.bar(
    [i - 0.2 for i in x], # 给每组图向左移动，差开交换次数
    top_users['item_count'],
    width=0.4,
    label = '物品数量'
)

plt.bar(
        [i+0.2 for i in x], # # 给每组图向右移动，差开物品数量
        top_users['swap_count'],
        width=0.4,
        label = '交换次数'
        )

plt.xticks(x,top_users['username']) # 第一个 x 表示刻度放在哪里 ，因为原图已经偏移了,top_users['username']表示每个刻度的名

plt.xlabel('用户')
plt.ylabel('数量')
plt.title('Top 10 用户：物品数量与交换次数')
plt.legend()
plt.xticks(rotation = 45,ha = 'right')
plt.show()

# 画用户交换次数 + 交换成功率的图（2个y轴）
# fig 为整张图，ax1为坐标轴
fig,ax1 = plt.subplots(figsize = (8,5))

# 左 Y 轴：交换次数
ax1.bar(
    user_behavior['username'],
    user_behavior['swap_count'],
    width = 0.5,
    label = '交换次数'
)

ax1.set_xlabel('用户')
ax1.set_ylabel('交换次数')
ax1.set_title('用户交换次数与交换成功率')

ax1.tick_params(axis='x', rotation=45)

# 右 Y 轴：交换成功率
ax2 = ax1.twinx() # 创建一个与 ax1 共用 X 轴、但拥有独立 Y 轴的 Axes，并把这个 Y 轴放到右边。
ax2.plot(
    user_behavior['username'],
    user_behavior['success_rate'],
    marker = 'o',
    label = '成功率'
)

ax2.set_ylabel('交换成功率')
ax2.set_ylim(0,1) # 将 y 轴限制在 (0,1)
# 把 1 当作 100%，按百分比格式显示
ax2.yaxis.set_major_formatter(PercentFormatter(1))

# 给每个点添加成功率
for x,y in zip(user_behavior['username'],user_behavior['success_rate']):
    ax2.text(
        # username,success_rate(0.4),0.4 -> f'{y:.0%}' -> 40%   --> 将这个人的成功率0.4显示为40%
        # ha：水平对齐（center:水平居中）
        # va:垂直对齐
        x,y,f'{y:.0%}',ha ='center',va = 'bottom',color = 'red'
    )


# 合并两个坐标轴的图例
# 获取图例图标 + 图例文字
lines1,labels1 = ax1.get_legend_handles_labels()
lines2,labels2 = ax2.get_legend_handles_labels()

# 结合
ax1.legend(
    lines1 + lines2,
    labels1 + labels2
)

plt.tight_layout() # 自动调整图中的各个元素位置，避免文字、标签、标题等互相挤压或者跑出画布。
plt.show()


# 画不同物品类别的数量
category_count = df_items['category'].value_counts()
print(category_count)

plt.figure(figsize=(8,5))

plt.bar(
    category_count.index,
    category_count.values
)

plt.xlabel('物品类别')
plt.ylabel('物品数量')
plt.title('物品类别分布')
plt.xticks(rotation = 45,ha = 'right')
plt.tight_layout()
plt.show()


# 不同物品类别，实际发生了多少次交换
# 把交换记录和物品类别关联起来
target_category = df_items[
    ['id','category']
].rename(
    columns={
        'id':'target_item_id',
        'category':'category_target'
    }
)

# 进行表关联
swap_analysis = df_swaps.merge(
    target_category,
    on='target_item_id',
    how='left'
)
print('\n交换记录和物品类别分类表:\n',swap_analysis)

category_swap_count = (
    swap_analysis['category_target'].value_counts()
)
print('\n不同类别的交换次数:\n',category_swap_count)

# 画图
plt.figure(figsize=(8,5))

plt.bar(
    category_swap_count.index,
    category_swap_count.values
)

plt.xlabel('物品类别')
plt.ylabel('交换次数')
plt.title('不同物品类别的交换次数')
plt.xticks(rotation = 45,ha = 'right')
plt.tight_layout()
plt.show()

# 交换成功率
# 成功次数
category_accept_count = (swap_analysis[swap_analysis['status'] == 'accepted'].groupby('category_target').size())

print('\n不同类别交换成功次数:\n',category_accept_count)

# 成功率
category_success_rate = (category_accept_count / category_swap_count).fillna(0)
print('\n不同类别交换成功概率:\n',category_success_rate)

# 画图
plt.figure(figsize=(8,5))

plt.bar(
    category_success_rate.index,
    category_success_rate.values
)

plt.xlabel('物品类别')
plt.ylabel('交换成功率')
plt.title('不同物品类别的交换成功率')

# Y 轴显示百分比
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xticks(rotation = 45,ha = 'right')
plt.tight_layout()
plt.show()

print('\n========== 业务分析结论 ==========')

print(
    f'交换成功率最高的类别：'
    f'{category_success_rate.idxmax()}，'
    f'成功率为 {category_success_rate.max():.2%}'
)

print(
    f'交换成功率最低的类别：'
    # idxmin: 获取最小值对应的索引
    f'{category_success_rate.idxmin()}，'
    # min() : 获取最小值
    f'成功率为 {category_success_rate.min():.2%}'
)


# =========================================准备机器学习数据===============================================================
# 准备模型预测要使用的数据
# 主要使用的有：用户历史行为（用户过去交换多少次、交换次数、成功率）、价格关系特征（差价、价格比例（判断谁是高价方））、
#             类别关系特征（类别交换次数、类别组合交换成功率）主要从三方面的数据进行训练模型进行预测

def build_ml_features(df_swaps,df_items):
    # 预测用户交换物品成功率
    # 将目标物品信息加入交换记录
    ml_data = df_swaps.merge(
        df_items[['id','category','price']],
        left_on='target_item_id',
        right_on='id',
        how='left'
    )

    # 重命名目标物品信息
    ml_data = ml_data.rename(
        columns={
            'category':'target_category',
            'price':'target_price'
        }
    )

    # 删除多余的 id
    ml_data = ml_data.drop(columns='id_y')
    print('\n目标物品关联后的机器学习数据：\n')
    print(ml_data.head(10))

    # 将提供物品信息加入交换记录
    ml_data = ml_data.merge(
        df_items[['id','price','category']],
        left_on='offered_item_id',
        right_on='id',
        how='left'
    )

    ml_data = ml_data.rename(
        columns={
            'category':'offered_category',
            'price':'offered_price'
        }
    )

    # 删除多余 id
    ml_data = ml_data.drop(columns='id')
    ml_data = ml_data.rename(columns={'id_x':'id'})
    print('\n目标物品 + 提供物品信息：')
    print(ml_data)

    # ml_data: id | requester_id | target_item_id | offered_item_id | target_price |target_category | offered_price | offered_category

    # 计算价格关系特征
    # 有方向
    ml_data['price_diff'] = (ml_data['offered_price'] - ml_data['target_price'])

    ml_data['price_diff_abs'] = ml_data['price_diff'].abs()

    # 价格比例
    ml_data['price_ratio'] = ml_data['offered_price'] / ml_data['target_price']
    print('\n加入价格关系特征后：')
    print(
        ml_data[
            [
                'target_price',
                'offered_price',
                'price_diff',
                'price_diff_abs',
                'price_ratio'
            ]
        ]
    )

    # 计算用户历史行为特征
    # 只能使用当前之前交换的数据

    # 按交换 id 排序，模拟交换发生的先后顺序
    # drop=True：不要把旧的行号保留下来作为新的一列。
    ml_data = ml_data.sort_values('id').reset_index(drop=True) # reset_index(drop=True)：使重新排列后行号不会变还是从0开始

    # 当前交换之前，该用户已经发生了多少次交换
    ml_data['user_swap_count'] = ml_data.groupby('requester_id').cumcount()
    print('\n加入用户历史交换次数：')
    print(
        ml_data[
            [
                'id',
                'requester_id',
                'status',
                'user_swap_count'
            ]
        ]
    )

    # 当前交换之前，已经成功进行了多少次交换：
    # 按用户分组，然后取每个用户的 status 经过 x:(x.eq('accepted')) 会变成 True/False
    # 再.cumsum()会累次成功次数
    # .shift(fill_value = 0) ： 将 x 的计算结果向下移动
    """
    1     rejected    0
    2     accepted    1
    3     accepted    2
    4     rejected    2
    预测 id = 2 时 成功次数应该为 0 不应该用这次的1，让上面补0，然后下移，就不会让函数提前知道这次会成功，从而进行预测
    id    shift后
    1     0
    2     0
    3     1
    4     2
    """

    # .transform ：将用户分为一组一组的
    # lambda x: x + 10 等价于 def func(x):
    #                           return x + 10
    ml_data['user_accepted_count'] = (ml_data.groupby('requester_id')['status']
                                      .transform(lambda x:(x.eq('accepted')).cumsum().shift(fill_value = 0)))

    print('\n加入用户历史成功次数：')
    print(
        ml_data[
            [
                'id',
                'requester_id',
                'status',
                'user_swap_count',
                'user_accepted_count'
            ]
        ]
    )

    # 计算用户交换成功率
    # 当前交换之前，用户历史成功率
    ml_data['user_success_rate'] = ml_data['user_accepted_count'] / ml_data['user_swap_count']

    # 第一次交换没有历史数据，成功概率为0
    ml_data['user_success_rate'] = ml_data['user_success_rate'].fillna(0)
    print('\n用户历史行为特征：')
    print(
        ml_data[
            [
                'id',
                'requester_id',
                'status',
                'user_swap_count',
                'user_accepted_count',
                'user_success_rate'
            ]
        ]
    )

    # 计算类别交换方向的历史次数
    ml_data['category_swap_count'] = ml_data.groupby(['target_category','offered_category']).cumcount()
    print('\n加入类别方向历史交换次数：')
    print(
        ml_data[
            [
                'id',
                'target_category',
                'offered_category',
                'status',
                'category_swap_count'
            ]
        ]
    )

    # 计算类别交换方向的历史成功次数
    ml_data['category_accepted_count'] = ml_data.groupby(['target_category','offered_category'])['status'].transform(
        lambda x:x.eq('accepted').cumsum().shift(fill_value = 0)
    )

    # 计算交换成功率
    ml_data['category_success_rate'] = ml_data['category_accepted_count'] / ml_data['category_swap_count']

    # 第一次出现交换方向时没有历史数据
    ml_data['category_success_rate'] = ml_data['category_success_rate'].fillna(0)
    print('\n类别方向历史特征：')
    print(
        ml_data[
            [
                'id',
                'target_category',
                'offered_category',
                'status',
                'category_swap_count',
                'category_accepted_count',
                'category_success_rate'
            ]
        ]
    )

    # 将交换结果转换为机器学习标签(目标)
    # accepted = 1，表示交换成功
    # 其他状态 = 0，表示交换失败

    # astype(int): 会将 bool 值转化为 0/1
    ml_data['label'] = (ml_data['status'] == 'accepted').astype(int)
    print('\n加入机器学习标签后：')
    print(
        ml_data[
            [
                'id',
                'status',
                'label'
            ]
        ]
    )

    return ml_data

ml_data = build_ml_features(df_swaps,df_items)

def build_xy(ml_data):
    # 划分特质 X 和 目标 y

    X = ml_data[
        [
            'user_swap_count',
            'user_accepted_count',
            'user_success_rate',

            'target_price',
            'offered_price',
            'price_diff',
            'price_diff_abs',
            'price_ratio',

            'target_category',
            'offered_category',

            'category_swap_count',
            'category_success_rate',
        ]
    ]

    # y : 模型预测的目标值
    y = ml_data['label']

    print('\n机器学习特征 X：')
    print(X.info())

    print('\n目标 y：')
    print(y)

    # one-hot 处理
    X = pd.get_dummies(X,columns=['target_category','offered_category'],dtype=int)
    print(X.info())

    return X,y

X,y = build_xy(ml_data)
feature_columns = X.columns.tolist()
print('\n模型最终使用的特征：')
print(feature_columns)
joblib.dump(feature_columns, 'feature_columns.pkl')

loaded_feature_columns = joblib.load('feature_columns.pkl')

print('\n特征列是否一致：')
print(feature_columns == loaded_feature_columns)



from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,roc_auc_score,average_precision_score
from sklearn.linear_model import LogisticRegression

import joblib

# 将模型训练封装成函数，方便 FastAPI 调用
def train_model(X,y):

    x_train,x_test,y_train,y_test = train_test_split(X,y,random_state=22,test_size=0.2,stratify=y)

    # 标准化
    transformer = StandardScaler()
    x_train = transformer.fit_transform(x_train)
    x_test = transformer.transform(x_test)

    # KNN模型
    # 为啥不用KNN：数据存在明显的不平衡，逻辑回归可以提高少数样本的权重
    # （刚开始确实用 KNN ，并通过交叉验证得到最佳 K 值为 16 ， 但是正类的召回率只有 0.03，模型几乎吧所有样本都预测成了负类。
    #   进一步分析发现数据极度不平衡,用逻辑回归可以提高少数样本的权重，可以改善模型对成功交换样本的识别能力）
    # model = KNeighborsClassifier(n_neighbors=16)

    # 逻辑回归
    # class_weight='balanced':让模型自动给样本少的更高的权重
    lr_model = LogisticRegression(class_weight='balanced',random_state=22)

    lr_model.fit(x_train,y_train)
    # lr_pred = lr_model.predict(x_test)

    return lr_model,transformer,x_train,x_test,y_train,y_test

lr_model,transformer,x_train,x_test,y_train,y_test = train_model(X,y)

# =========================保存模型和标准化器，以便FastAPI调用时不用每次都重新训练模型===========================================

# 保存训练好的模型
joblib.dump(lr_model, 'lr_model.pkl')

# 保存模型训练时使用的标准化器
joblib.dump(transformer, 'scaler.pkl')

# ======================================================================================================================

# 加载保存的模型和标准化器
loaded_model = joblib.load('lr_model.pkl')
loaded_scaler = joblib.load('scaler.pkl')

# 对比加载的模型和实际模型看看保存的模型是否正确

import numpy as np
# 获取预测为 1 的概率
# 问模型对于测试集中的每一条交换，成功率是多少
y_prob = lr_model.predict_proba(x_test)[:,1]


# 加载后的模型的预测
loaded_prob = loaded_model.predict_proba(x_test)[:,1]
print("模型预测概率是否一致：", np.allclose(y_prob, loaded_prob))

print("原模型前5个预测概率：")
print(y_prob[:5])

print("加载模型前5个预测概率：")
print(loaded_prob[:5])

print(
    "Scaler mean 是否一致：",
    np.allclose(transformer.mean_, loaded_scaler.mean_)
)

print(
    "Scaler scale 是否一致：",
    np.allclose(transformer.scale_, loaded_scaler.scale_)
)

# 设置分类阈值
# 成功率大于阈值的预测为1，小于阈值的预测为0
threshold = 0.6

# 根据阈值判断最终类别
lr_pred = (y_prob >= threshold).astype(int)


# # 交叉验证
# param_grid = {'n_neighbors':range(1,200)}
# estimator = GridSearchCV(estimator=model,param_grid=param_grid,cv=4)
# estimator.fit(x_train,y_train)
# print(estimator.best_estimator_)

# model.fit(x_train,y_train)
# y_pred = model.predict(x_test)

print('\n阈值:\n',threshold)

print('\n准确率:\n',accuracy_score(y_test,lr_pred))

print('\n混淆矩阵:\n',confusion_matrix(y_test,lr_pred))

print('\n分类报告：\n',classification_report(y_test,lr_pred))


# 获取测试集对应的原始数据索引
test_index = y_test.index  # 找出这些测试数据原本在 ml_data 中对应的行

# 将预测概率保存到测试集数据中
ml_data.loc[test_index,'success_probability'] = y_prob

# 保存最终预测结果
ml_data.loc[test_index,'predicted_label'] = lr_pred

print(ml_data.loc[
    test_index,
    [
        'id','target_category','offered_category',
        'label','success_probability','predicted_label'
    ]
      ].head(10))


# 查看逻辑回归模型的特征权重（查看哪个特征对样本预测成功率影响最大）
feature_names = X.columns

coef_df = pd.DataFrame({
    'feature':feature_names,
    'coefficient':lr_model.coef_[0]
})

# 按权重绝对值从大到小排序
coef_df['acs_coefficient'] = coef_df['coefficient'].abs()

coef_df = coef_df.sort_values(
    'acs_coefficient',
    ascending=False
)

print('\n影响最大的特征：\n')
print(coef_df.head(10))

"""
                  feature  coefficient  acs_coefficient
8     category_swap_count    -1.834602         1.834602
6          price_diff_abs    -1.310446         1.310446
0         user_swap_count    -0.785082         0.785082
4           offered_price     0.743469         0.743469

 coefficient 为负，acs_coefficient越大，则模型认为交换越不会成功
"""

# ROC-AUC
roc_auc = roc_auc_score(y_test,y_prob) # 判断模型的可靠性，auc值越大，模型可靠性越高

# PR-AUC
pr_auc = average_precision_score(y_test,y_prob)
print('\nROC-AUC：', roc_auc) # auc 面积越大，模型性能越好
# 看模型预测出的正类准不准确
print('PR-AUC：', pr_auc) # 主要看模型找出来的"成功交换"到底好不好

import matplotlib.pyplot as plt

# 直方图
plt.hist(
    y_prob[y_test == 0], # 预测概率中，实际是 0（失败），返回 bool
    bins=20, # 把 0-1 分成 20 个区间
    alpha=0.6, # 透明度
    label='实际失败'
)

plt.hist(
    y_prob[y_test == 1],
    bins=20,
    alpha=0.6,
    label='实际成功'
)

plt.xlabel('预测成功概率')
plt.ylabel('数量')
plt.title('预测成功概率分布')
plt.legend()
plt.show()

category_stats = ml_data.groupby(
    ['target_category', 'offered_category']
)['label'].agg(
    ['count', 'sum', 'mean']
)

category_stats = category_stats.sort_values(
    'count',
    ascending=False
)

print(category_stats)


# 查看一笔交易的预测结果
sample_index = test_index[0]
print('\n这笔交换的信息：')

print(
    ml_data.loc[
        sample_index,
        [
            'id',
            'target_category',
            'target_price',
            'offered_category',
            'offered_price',
            'price_diff',
            'user_swap_count',
            'user_success_rate',
            'category_success_rate',
            'label'
        ]
    ]
)

print('\n模型预测成功概率：', y_prob[0])


db.close()





















