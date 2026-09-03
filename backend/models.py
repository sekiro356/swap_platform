# 定义数据库长什么样

from sqlalchemy import Column,Integer,String
from database import Base

# 直接在 python 让 sqlalchemy 帮忙直接生成 SQL 表，本质和直接在 mysql 中编写一样

class User(Base):  # User 类 -> User表
    __tablename__ = 'users'
    # Integer ： int
    # index : 给字段创建索引
    id = Column(Integer,primary_key=True,index=True)
    # unique=True ： 用户名不能重名
    # nullable=False ： 字段不为空
    username = Column(String(50),unique=True,nullable=False)
    password = Column(String(255),nullable=False)