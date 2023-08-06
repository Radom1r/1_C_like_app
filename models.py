import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Sex(Base):
    __tablename__ = 'Sex'
    sex_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    sex_name = sq.Column(sq.String(length=1), nullable=False, unique=True)

class Brand(Base):
    __tablename__ = 'Brand'
    brand_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    brand_name = sq.Column(sq.String(length=100), nullable=False, unique=True)

class Size(Base):
    __tablename__ = 'Size'
    size_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    size_name = sq.Column(sq.String(length=10), nullable=False, unique=True)

class Category(Base):
    __tablename__ = 'Category'
    category_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    category_name = sq.Column(sq.String(length=100), nullable=False, unique=True)
    sex_id = sq.Column(sq.Integer, sq.ForeignKey('Sex.sex_id'))
    marginality_percent = sq.Column(sq.Integer, nullable=False)
    sexes = relationship('Sex', backref='Category')

class Storage(Base):
    __tablename__ = 'Storage'
    item_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    item_name = sq.Column(sq.String(length=100), nullable=False)
    brand_id = sq.Column(sq.Integer, sq.ForeignKey('Brand.brand_id'))
    category_id = sq.Column(sq.Integer, sq.ForeignKey('Category.category_id'))
    size_id = sq.Column(sq.Integer, sq.ForeignKey('Size.size_id'))
    receive_datetime = sq.Column(sq.DateTime)
    receive_price = sq.Column(sq.Integer)
    sale_price = sq.Column(sq.Integer, nullable=False)
    pottential_revenue = sq.Column(sq.Integer, nullable=False)
    amount_left = sq.Column(sq.Integer)
    fact_marginality_percent = sq.Column(sq.Integer, nullable=False)
    brands = relationship('Brand', backref='Storage')
    Categories = relationship('Category', backref='Storage')
    sizes = relationship('Size', backref='Storage')

class Sells(Base):
    __tablename__ = 'Sell'
    sell_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    item_id = sq.Column(sq.Integer, sq.ForeignKey('Sold_items.item_id'))
    selling_datetime = sq.Column(sq.DateTime)
    amount_sold = sq.Column(sq.Integer)
    rel = relationship('Sold_items', backref='Sells')

class Sold_items(Base):
    __tablename__ = 'Sold_items'
    item_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    item_name = sq.Column(sq.String(length=100), nullable=False)
    brand_id = sq.Column(sq.Integer, sq.ForeignKey('Brand.brand_id'))
    category_id = sq.Column(sq.Integer, sq.ForeignKey('Category.category_id'))
    size_id = sq.Column(sq.Integer, sq.ForeignKey('Size.size_id'))
    receive_datetime = sq.Column(sq.DateTime)
    receive_price = sq.Column(sq.Integer)
    sale_price = sq.Column(sq.Integer, nullable=False)
    pottential_revenue = sq.Column(sq.Integer, nullable=False)
    fact_marginality_percent = sq.Column(sq.Integer, nullable=False)
    brands = relationship('Brand', backref='Sold_items')
    Categories = relationship('Category', backref='Sold_items')
    sizes = relationship('Size', backref='Sold_items')
    
def create_tables(eng):
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)
