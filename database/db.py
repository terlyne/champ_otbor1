from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, joinedload

from models.models import Base, Product, User, OrderProduct, PickupPoint, Order

engine = create_engine("sqlite:///./app.db")
Session = sessionmaker(bind=engine, expire_on_commit=False)

def create_db():
    Base.metadata.create_all(engine)


def read_all_products():
    with Session() as session:
        stmt = select(Product)
        products = session.execute(stmt).scalars().all()

        return products

def read_user(username, password):
    with Session() as session:
        stmt = select(User).where(User.username == username, User.password == password)
        user = session.execute(stmt).scalar_one_or_none()

        return user


def create_order(user_id):
    with Session() as session:
        order = Order(
            total_price = 0,
            total_discount = None,
            pickup_point_id = 1,
            user_id = user_id,
        )
        session.add(order)

        session.commit()

        return order

def create_order_product(order_id, product_id, quantity):
    with Session() as session:
        order_product = OrderProduct(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
        )

        session.add(order_product)
        session.commit()

        return order_product

def update_order_product(order_product, order_id, pickup_point_id, quantity):
    with Session() as session:
        order_product.order_id = order_id
        order_product.pickup_point_id = pickup_point_id
        order_product.quantity = quantity

        session.commit()

        return order_product

def read_all_order_products():
    with Session() as session:
        stmt = select(OrderProduct).options(joinedload(OrderProduct.product))
        products = session.execute(stmt).scalars().all()

        return products




def read_all_pickup_points():
    with Session() as session:
        stmt = select(PickupPoint)
        pickup_points = session.execute(stmt).scalars().all()

        return pickup_points









# Функции для чтения изображения и создания продукта с этим изображением

def image_to_blob(image_path):
    """Фунцкия для перевода изображения в BLOB-формат"""
    with open(image_path, 'rb') as file:
        byte_data = file.read()  # Читаем файл в байтовый формат
    return byte_data


def create_product(name, description, maker, price, image_path, quantity, discount=None):
    with Session() as session:
        product = Product(
            name = name,
            description = description,
            maker = maker,
            price = price,
            discount = discount,
            quantity = quantity,
            photo = image_to_blob(image_path),
        )

        session.add(product)
        session.commit()