# 负责怎么连接数据库
import os
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv

load_dotenv()
# 构建数据库变量
host = os.getenv('DB_HOST','127.0.0.1')
port = os.getenv('DB_PORT','3306')
user = os.getenv('DB_USER','root')
pwd = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME','swap_platform')

db_url = f'mysql+pymysql://{user}:{pwd}@{host}:{port}/{database}'

# 创建数据库引擎
engine = create_engine(db_url,
                       echo=True) # echo=True:将 sqlalchemy 执行的 seq 语句展示在后端

# 数据库连接/操作会话的生产工厂
# 它自己不是一个数据库连接，而是：生产Session -> Session -> 操作Mysql
SessionLocal = sessionmaker(
    bind=engine,
    autocommit = False, # 不要每执行一个操作就自动提交，什么时候提交由我自己控制
    autoflush= False # 不要在执行某些查询前，自动把当前还没提交的数据先刷到数据库
)

Base = declarative_base() # 所有数据库的父模板


