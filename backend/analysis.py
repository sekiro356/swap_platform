# MySQL -> sqlalchemy -> Python -> pandas DataFrame
# # 将用户转化为 DataFrame 方便后续画图

import pandas as pd
from matplotlib.ticker import PercentFormatter
from models import User,Items,Swap
from database import SessionLocal
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

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

print(df_user)
print(df_items)
print(df_swaps)

print('\n用户数量: ',len(df_user))
print('\n物品数量: ',len(df_items))
print('\n交换记录数量: ',len(df_swaps))

# 查看每种物品的数量
print(df_items['category'].value_counts())

# 查看交换物品状态数量
print(df_swaps['status'].value_counts())

# 看谁发布了多少件商品
print('\n每个用户发布的物品数量：')
print(df_items.groupby('user_id').size())

# 给未命名的列重命名
item_count = df_items.groupby('user_id').size().reset_index(name='item_count')
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
print(swap_analysis)
print(swap_analysis['category'].value_counts())

# 不同种类交换
swap_analysis = swap_analysis.merge(
    df_items[['category', 'id']],  # 只插入 'category','id' 即可，
    left_on='offered_item_id',
    right_on='id',
    how='left',
    suffixes=('_target','_offered') # 两边都有 category
    # 合并会变成 category_x和 category_y 经过 suffixes 后变成 category_target 和category_offered
)
print(swap_analysis)
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
print(swap_reaction)

# 计算每种交换类别占总交换类别的比例(百分比)
swap_reaction['ratio'] = swap_reaction['swap_count'] / swap_reaction['swap_count'].sum() * 100
print(swap_reaction)


# 统计每个人发起交换发起了多少次
user_swap_count = (df_swaps.groupby('requester_id').size().reset_index(name='swap_count'))
print(user_swap_count)

# 统计每个用户交换成功了多少次
user_accept_count = (df_swaps[df_swaps['status'] == 'accepted']
                     .groupby('requester_id').size().reset_index(name='accepted_count'))
print(user_accept_count)

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
print(user_swap_analysis)

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

print(user_behavior)

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

plt.xticks(x,top_users['username'])

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

db.close()






















