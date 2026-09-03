# 注册接口

from pydantic import BaseModel

# 规定注册接口要求用户传递什么数据(规定前端传什么)
class UserCreate(BaseModel):
    username:str
    password:str

# 登录
class UserLogin(BaseModel):
    username:str
    password:str











