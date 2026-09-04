# 定义数据库中的表长什么样

from sqlalchemy import Column,Integer,String
from database import Base

# 直接在 python 让 sqlalchemy 帮忙直接生成 SQL 表，本质和直接在 mysql 中编写一样

# 创建用户表
class User(Base):  # User 类 -> User表
    __tablename__ = 'users'
    # Integer ： int
    # index : 给字段创建索引
    id = Column(Integer,primary_key=True,index=True)
    # unique=True ： 用户名不能重名
    # nullable=False ： 字段不为空
    username = Column(String(50),unique=True,nullable=False)
    password = Column(String(255),nullable=False)

# 创建商品表
class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(200),nullable=False)               # 物品名
    description = Column(String(1000),nullable=False)       # 物品描述
    category = Column(String(50),nullable=False)            # 物品分类
    price = Column(Integer,nullable=False)                  # 物品价格

    user_id = Column(Integer,nullable=False)                # 物品发布者

    status = Column(String(20),nullable=False,default='available')      # 设置物品是否存在，防止已经交换出去了结果还显示物品存在


# 交换申请表
class Swap(Base):
    __tablename__ = 'swaps'

    id = Column(Integer,primary_key=True,index=True)

    # 发起交换的人
    requester_id = Column(Integer,nullable=False)

    # 想要交换的物品
    target_item_id = Column(Integer,nullable=False)

    # 用什么东西交换
    offered_item_id = Column(Integer,nullable=False)

    # 交换状态
    status = Column(String(20),default='pending',nullable=False)

































