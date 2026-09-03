# 负责启动 FastAPI

from fastapi import FastAPI
import uvicorn
from database import engine,Base,SessionLocal
from models import User
from schemas import UserCreate

app = FastAPI()

# 每次启动时，如果没有表则创建用户表
Base.metadata.create_all(bind=engine)
@app.get('/')
def root():
    return {'messages':'欢迎来到物换物平台'}
@app.get('/test-db')
def test_db():
    with engine.connect() as connection:
        return {'messages':'MySql连接成功'}

@app.post('/register')
def register(user:UserCreate):
    db = SessionLocal()

    # 查询用户是否已存在
    # .filter 查询条件 相当于 Where
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first() #.first():查询结果中拿第一条

    if existing_user:
        db.close()
        return {'messages':'用户已存在'}

    # 创建用户
    new_user = User(
        username=user.username,
        password=user.password
    )  # 数据库中的一条用户数据

    db.add(new_user) # 把这条数据放到当前数据库 Session（进程）
    db.commit() # 提交给 mysql
    db.refresh(new_user)

    db.close()

    return {'messages':'注册成功',
            'user_id':new_user.id,
            'username':new_user.username}

if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)













