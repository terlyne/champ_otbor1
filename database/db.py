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

def read_pickup_point_by_address(pickup_point_address):
    with Session() as session:
        stmt = select(PickupPoint).where(PickupPoint.address == pickup_point_address)
        pickup_point = session.execute(stmt).scalar_one_or_none()

        return pickup_point


def create_order(order_products, user_id, pickup_point_id):
    with Session() as session:
        total_discount = None

        # Вычисляем общую цену и общую скидку
        total_price = 0
        for product, quantity in order_products.items():
            total_price += product.price * quantity
            if product.discount:
                total_discount = (total_discount or 0) + (product.discount * quantity)

        # Создаем заказ
        order = Order(
            total_price=total_price,
            total_discount=total_discount,
            user_id=user_id,
            pickup_point_id=pickup_point_id,
        )

        # Создаем записи для каждого продукта в заказе
        for product, quantity in order_products.items():
            order_product_entry = OrderProduct(
                order=order,  # Связываем с текущим заказом
                product_id=product.id,  # Используем id продукта
                quantity=quantity  # Количество
            )
            session.add(order_product_entry)  # Добавляем OrderProduct в сессию

        session.add(order)  # Добавляем сам заказ в сессию
        session.commit()  # Сохраняем изменения в базе данных

        return order








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