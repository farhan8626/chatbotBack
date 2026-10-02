from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    type = Column(String(50)) # 'product' or 'faq'

    products = relationship("Product", back_populates="category")
    faqs = relationship("FAQ", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(255), index=True)
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    in_stock = Column(Boolean, default=True)

    category = relationship("Category", back_populates="products")

class FAQ(Base):
    __tablename__ = "faq"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    question = Column(String(255))
    answer = Column(Text)

    category = relationship("Category", back_populates="faqs")
