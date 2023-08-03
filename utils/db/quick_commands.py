from utils.db.schemas.shop import Shop
from utils.db.schemas.user import User
from asyncpg import UniqueViolationError

async def add_user(user_id: int, name: str, username: str, status: str, login: str, password: str):
  try: 
    user = User(user_id=user_id, name=name, username=username, status=status, login=login, password=password )
    await user.create()
  except Exception as e:
        print(f"Ошибка при создании пользователя: {e}")
        raise 

async def select_all_users():
    users = await User.query.gino.all()
    return users
  
async def select_one_user(user_id):
    return await User.query.where(User.user_id == user_id).gino.first()
  
async def create_shop(name: str, region: str, admin_contact: int, author_id: int,):
  try: 
    shop = Shop( name=name, region=region, admin_contact=admin_contact, author_id=author_id)
    await shop.create()
  except Exception as e:
        print(f"Ошибка при создании магазина: {e}")
        raise 
      
async def select_all_shops():
    shops = await Shop.query.gino.all()
    return shops
  
async def select_assorted_shops():
    # Используем метод order_by, чтобы отсортировать магазины по алфавиту
    shops = await Shop.query.gino.all()
    shops = sorted(shops, key=lambda shop: shop.name)
    return shops
  
async def delete_shop_by_id(shop_id):
    shop = await Shop.query.where(Shop.id == shop_id).gino.first()
    if shop:
        await shop.delete()
        return True
    else:
        return False