# 注册接口
from typing import Literal
from pydantic import BaseModel

# 规定注册接口要求用户传递什么数据(规定前端传什么)
# 注册
class UserCreate(BaseModel):
    username:str
    password:str

# 登录
class UserLogin(BaseModel):
    username:str
    password:str

# 商品发布
class ItemCreate(BaseModel):
    name : str
    description : str
    category : Literal['数码','书籍','服饰','鞋靴','家电','家居生活','美妆个护','运动户外','玩具','乐器','办公用品','其他']
    price : int


# 请求交换
class SwapCreat(BaseModel):
    target_item_id : str
    offered_item_id : str









