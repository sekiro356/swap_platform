# 负责启动 FastAPI

from fastapi import FastAPI,Depends,HTTPException
import uvicorn
from database import engine,Base,SessionLocal
from models import User,Items,Swap # 表
from schemas import UserCreate,UserLogin,ItemCreate,SwapCreat # 客户端输入的要求
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
# 执行 /me 之前，先执行 get_current_user()，把得到的用户交给我。
def get_me(current_user:User = Depends(get_current_user)):
    return {
        'user_id':current_user.id,
        'username':current_user.username
    }

# 添加物品
@app.post('/items')
def create_item(
        item:ItemCreate,current_user:User = Depends(get_current_user)
):
    db = SessionLocal()

    new_item = Items(
        name=item.name,
        description=item.description,
        category=item.category,
        price=item.price,
        user_id=current_user.id
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    db.close()

    return {
        'messages':'物品发布成功',
        'item_id':new_item.id,
        'name':new_item.name,
        'user_id':new_item.user_id,
    }

# 查询全部物品
@app.get('/items')
def get_items():
    db = SessionLocal()

    items = db.query(Items).all()

    result = []

    for item in items:
        result.append({
            'item_id':item.id,
            'name':item.name,
            'description':item.description,
            'category':item.category,
            'price':item.price,
            'user_id':item.user_id
        }
        )

    db.close()

    return result

# 查询单个物品
@app.get('/items/{item_id}')
def get_item(item_id:int):
    db = SessionLocal()

    item = db.query(Items).filter(
        Items.id == item_id
    ).first()

    db.close()

    if not item:
        return {'messages':'物品不存在'}


    return {
        'item_id': item.id,
        'name': item.name,
        'description': item.description,
        'category': item.category,
        'price': item.price,
        'user_id': item.user_id
    }



# 添加物品修改接口
@app.put('/items/{item_id}')
def update_item(
        item_id:int,
        item:ItemCreate,
        current_user : User = Depends(get_current_user)
):
    db = SessionLocal()

    db_item = db.query(Items).filter(
        Items.id == item_id
    ).first()

    # 物品不存在
    if not db_item:
        db.close()
        return {'messages':'物品不存在'}

    # 不是自己的商品
    if db_item.user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail='无权限修改此物品'
        )

    # 修改物品
    db_item.name = item.name
    db_item.description = item.description
    db_item.category = item.category
    db_item.price = item.price

    db.commit()
    db.refresh(db_item)
    db.close()

    return {
        'messages':'修改成功',
        'item_id': db_item.id,
        'name': db_item.name,
        'description': db_item.description,
        'category': db_item.category,
        'price': db_item.price,
        'user_id': db_item.user_id
    }


# 删除接口
@app.delete('/items/{item_id}')
def delete_item(item_id:int,current_user:User = Depends(get_current_user)):
    db = SessionLocal()

    db_item = db.query(Items).filter(
        Items.id == item_id
    ).first()

    # 物品不存在
    if not db_item:
        db.close()
        return {'messages': '物品不存在'}

    # 不是自己的商品
    if db_item.user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail='无权限删除此物品'
        )


    db.delete(db_item)
    db.commit()
    db.close()

    return {
        'messages': '删除成功'
    }

# 交换申请接口
@app.post('/swaps')
def create_swap(swap:SwapCreat,current_user:User=Depends(get_current_user)):
    db = SessionLocal()

    # 查询想要交换的物品
    target_item = db.query(Items).filter(
        Items.id == swap.target_item_id
    ).first()

    if not target_item:
        db.close()

        return {'messages':'物品暂时不存在'}

    # 查询自己拿出来交换的物品
    offered_item = db.query(Items).filter(
        Items.id == swap.offered_item_id
    ).first()

    if not offered_item:
        db.close()
        return {'messages':'交换物品不存在'}

    # 不能拿别人的物品进行交换
    if offered_item.user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail='不能拿别人的物品进行交换'
        )

    # 自己没有的物品也不能进行交换
    if offered_item.status != 'available':
        db.close()
        raise HTTPException(
            status_code=400,
            detail='您提供的物品已经无法进行交换'
        )

    # 检查目标物品是否已交换出去了
    if target_item.status != 'available':
        db.close()
        raise HTTPException(
            status_code=400,
            detail='目标物品已无法进行交换'
        )

    # 不能拿自己的物品和自己的物品进行交换
    if target_item.user_id == current_user.id:
        db.close()
        return {'messages':'不能和自己的物品进行交换'}

    # 创建交换申请
    new_swap = Swap(
        requester_id = current_user.id,
        target_item_id= swap.target_item_id,
        offered_item_id=swap.offered_item_id,
        status='pending'
    )
    db.add(new_swap)
    db.commit()
    db.refresh(new_swap)
    db.close()

    return {
        'messages':'交换申请成功!',
        'swap_id':new_swap.id,
        'request_id':new_swap.requester_id,
        'target_item_id':new_swap.target_item_id,
        'offer_item_id':new_swap.offered_item_id,
        'status':new_swap.status
    }

# 查询交换
@app.get('/swaps')
def get_swaps(current_user:User=Depends(get_current_user)):
    db = SessionLocal()

    # 查询
    #   我发起的交换
    #   别人向我的物品发起的交换
    swaps = db.query(Swap).join(
        Items,
        Swap.target_item_id == Items.id
    ).filter(
        (Swap.requester_id == current_user.id) |
        (Items.user_id == current_user.id)
    ).all()

    result = []

    for swap in swaps:
        result.append({
            'swap_id':swap.id,
            'requester_id':swap.requester_id,
            'target_item_id':swap.target_item_id,
            'offered_item_id':swap.offered_item_id,
            'status':swap.status
        })

    db.close()

    return result


# 添加接受窗口
@app.put('/swaps/{swap_id}/accept')
def accept_swap(swap_id:int,current_user:User=Depends(get_current_user)):
    db = SessionLocal()

    # 查询交换申请
    swap = db.query(Swap).filter(
        Swap.id == swap_id
    ).first()

    # 交换申请不存在
    if not swap:
        db.close()
        return {'messages':'交换申请不存在'}

    # 只有 pending 状态才能接受
    if swap.status != 'pending':
        db.close()
        raise HTTPException(
            status_code=400,
            detail='该交换申请已经处理过了'
        )

    # 查询目标物品
    target_item = db.query(Items).filter(
        Items.id == swap.target_item_id
    ).first()

    # 查询对方想要交换物品
    offered_item = db.query(Items).filter(
        Items.id == swap.offered_item_id
    ).first()

    # 检查对方想要交换的物品是否还存在
    if not offered_item:
        db.close()
        return {'messages': '对方想要交换的物品不存在'}

    # 目标物品不存在
    if not target_item:
        db.close()
        return {'messages':'目标物品不存在'}

    # 只有目标物品的主人才能接受
    if target_item.user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail='无权接受此交换'
        )

    # 修改交换状态
    swap.status = 'accepted'

    target_item.status = 'unavailable'
    offered_item.status = 'unavailable'

    db.commit()
    db.refresh(swap)
    db.close()

    return {
        'messages':'交换申请已接受',
        'swap_id':swap.id,
        'status':swap.status
    }


# 添加拒绝窗口
@app.put('/swaps/{swap_id}/reject')
def reject_swap(swap_id:int,current_user:User=Depends(get_current_user)):
    db = SessionLocal()

    # 查询交换申请
    swap = db.query(Swap).filter(
        Swap.id == swap_id
    ).first()

    # 交换申请不存在
    if not swap:
        db.close()
        return {'messages':'交换申请不存在'}

    # 只有 pending 状态才能拒绝
    if swap.status != 'pending':
        db.close()
        raise HTTPException(
            status_code=400,
            detail='该交换申请已经处理过了'
        )

    # 查询对方想要的物品
    target_item = db.query(Items).filter(
        Items.id == swap.target_item_id
    ).first()

    # 查询对方想要交换物品
    offered_item = db.query(Items).filter(
        Items.id == swap.offered_item_id
    ).first()

    # 检查对方想要交换的物品是否还存在
    if not offered_item:
        db.close()
        return {'messages':'对方想要交换的物品不存在'}

    # 目标物品不存在
    if not target_item:
        db.close()
        return {'messages':'目标物品不存在'}

    # 只有目标物品的主人才能接受
    if target_item.user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail='无权拒绝此交换'
        )

    # 修改交换状态
    swap.status = 'rejected'

    db.commit()
    db.refresh(swap)
    db.close()

    return {
        'messages':'交换申请已拒绝',
        'swap_id':swap.id,
        'status':swap.status
    }

if __name__ == '__main__':
    uvicorn.run('main:app')













