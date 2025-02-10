import random
from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Float, Integer, LargeBinary
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"
    id: Mapped[int] = mapped_column(primary_key=True)

class User(Base):
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(30))

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")

class Product(Base):
    photo: Mapped[bytes] = mapped_column(LargeBinary)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(120))
    maker: Mapped[str] = mapped_column(String(40))
    price: Mapped[float] = mapped_column(Float(2))
    discount: Mapped[float] = mapped_column(Float(2), nullable=True)
    quantity: Mapped[int]

    order_products: Mapped[list["OrderProduct"]] = relationship("OrderProduct", back_populates="product")

class OrderProduct(Base):
    __tablename__ = "order_products"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]

    product: Mapped["Product"] = relationship("Product", back_populates="order_products")
    order: Mapped["Order"] = relationship("Order", back_populates="order_products")

class Order(Base):
    date: Mapped[datetime] = mapped_column(default=datetime.now())
    total_price: Mapped[float] = mapped_column(Float(2))
    total_discount: Mapped[float] = mapped_column(Float(2), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="Новый")
    pickup_point_id: Mapped[int] = mapped_column(ForeignKey("pickup_points.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


    user: Mapped["User"] = relationship("User", back_populates="orders")
    order_products: Mapped[list["OrderProduct"]] = relationship("OrderProduct", back_populates="order")
    pickup_point: Mapped["PickupPoint"] = relationship("PickupPoint", back_populates="orders")
    receipt: Mapped["Receipt"] = relationship("Receipt", back_populates="order")

class PickupPoint(Base):
    __tablename__ = "pickup_points"
    address: Mapped[str] = mapped_column(String(40))

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="pickup_point")
    receipts: Mapped[list["Receipt"]] = relationship("Receipt", back_populates="pickup_point")

class Receipt(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    pickup_point_id: Mapped[int] = mapped_column(ForeignKey("pickup_points.id"))
    code: Mapped[int] = mapped_column(default=random.randint(100, 999))
    delivery_time: Mapped[str] = mapped_column(default="3 дня")

    order: Mapped["Order"] = relationship("Order", back_populates="receipt")
    pickup_point: Mapped["PickupPoint"] = relationship("PickupPoint", back_populates="receipts")