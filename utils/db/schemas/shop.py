from utils.db.db_api_gino import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, sql, Sequence

class Shop(TimedBaseModel):
  __tablename__ = 'shops'
  id = Column(BigInteger, Sequence('shop_id_seq'), primary_key=True, index=True, unique=True, nullable=False)
  name = Column(String(200))
  region = Column(String(100))
  admin_contact = Column(String(20))
  author_id = Column(BigInteger)
  
  query: sql.select