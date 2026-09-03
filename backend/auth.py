import jwt
import os
from datetime import datetime,timedelta
from dotenv import load_dotenv
from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from database import SessionLocal
from models import User

load_dotenv()
# JWT 密钥
SECRET_KEY = os.getenv('SECRET_KEY')

# 加密算法
ALGORITHM = 'HS256'

def create_access_token(user_id:int):
    # Token 中保存数据
    payload = {
        'user_id':user_id,
        'exp':datetime.utcnow() + timedelta(hours=2) # 设置 token 的过期时间：2小时后
    }

    # 生成 JWT
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

security = HTTPBearer() # 负责从请求中拿出 token

def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    print('收到 Token:',token)
    print('当前SECRET_KEY:',SECRET_KEY)

    try:
        # 解码 JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # 从 JWT 中取出 user_id
        user_id = payload.get('user_id')

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail='Token 无效'
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail='Token 已过期'
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail='Token 无效'
        )

    # 根据用户的 user_id 查询用户
    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    db.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail='用户不存在'
        )

    return user





























