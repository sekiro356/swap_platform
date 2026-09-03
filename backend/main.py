# 负责启动 FastAPI

from fastapi import FastAPI,Depends
import uvicorn
from database import engine,Base,SessionLocal
from models import User # 表
from schemas import UserCreate,UserLogin # 客户端输入的要求
from auth import create_access_token
import bcrypt

from auth import create_access_token,get_current_user
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

    # 对密码进行 bcrypt 哈希
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf8'), # 编码：将密码转换为二进制 bytes
        bcrypt.gensalt() # 生成一段随机东西加进去
    ).decode('utf8') # 解码：将二进制重新解码为普通字符串

    # 创建用户
    new_user = User(
        username=user.username,
        password=hashed_password
    )  # 数据库中的一条用户数据

    db.add(new_user) # 把这条数据放到当前数据库 Session（进程）
    db.commit() # 提交给 mysql
    db.refresh(new_user)

    db.close()

    return {'messages':'注册成功',
            'user_id':new_user.id,
            'username':new_user.username}

@app.post('/login')
def login(user:UserLogin):
    db = SessionLocal()

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        db.close()
        return {'messages':'用户不存在'}

    # 验证密码
    is_password_correct = bcrypt.checkpw(
        # 进行最终结果的比较
        user.password.encode('utf8'),
        db_user.password.encode('utf8')
    )

    if not is_password_correct:
        db.close()
        return {'messages':'用户名或密码错误'}

    # 生成 JWT
    access_token = create_access_token(db_user.id)

    db.close()

    return {
        'messages':'登陆成功',
        'user_id':db_user.id,
        'user_name':db_user.username,
        'access_token': access_token,
        'token_type':'bearer',

    }


@app.get('/me')
def get_me(current_user:User = Depends(get_current_user)):
    return {
        'user_id':current_user.id,
        'username':current_user.username
    }




if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)













