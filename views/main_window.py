from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QScrollArea,
)
from PyQt6.QtCore import Qt

from database.db import read_all_products, create_order_product, create_order, update_order_product
from views.product_groupbox import ProductGroupBox
from views.login_dialog import LoginDialog
from views.order_widget import OrderWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(700, 500)

        self.setWindowTitle("Продукты")

        self.welcome_label = QLabel("Привет, гость!")

        # Заказ
        self.order = None

        self.user = None

        # Окно редактирования заказа
        self.order_widget = None

        # Кнопка для редактирования заказа
        self.edit_order_button = None


        # Список товаров в заказе
        self.order_products = []

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.show_login_dialog)

        self.main_layout = QVBoxLayout()

        self.upper_layout = QHBoxLayout()

        self.upper_layout.addWidget(self.welcome_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.upper_layout.addWidget(self.login_button)

        self.main_layout.addLayout(self.upper_layout)

        # Экземпляр диалогового окна авторизации
        self.login_dialog = LoginDialog()
        self.login_dialog.authorized.connect(self.show_all_after_login)


        self.products_scroll = QScrollArea()
        self.products_layout = QVBoxLayout()
        self.products_widget = QWidget()

        self.main_layout.addWidget(self.products_scroll)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.products = read_all_products()
        self.show_products()

    def show_products(self, spin_boxes=False):
        if self.products_layout.count() != 0:
            for i in range(self.products_layout.count()):
                product_groupbox = self.products_layout.itemAt(i).widget()
                product_groupbox.deleteLater()
        if spin_boxes:
            for product in self.products:
                product_groupbox = ProductGroupBox(self, product, spin_boxes=True)
                self.products_layout.addWidget(product_groupbox)
        else:
            for product in self.products:
                product_groupbox = ProductGroupBox(self, product)
                self.products_layout.addWidget(product_groupbox)

        self.products_widget.setLayout(self.products_layout)
        self.products_scroll.setWidget(self.products_widget)

        self.products_scroll.setWidgetResizable(True)


    def show_login_dialog(self):
        self.login_dialog.show()


    def show_all_after_login(self):
        self.user = self.login_dialog.user
        # Создаем наш заказ после получения пользователя
        self.order = create_order(self.user.id)

        self.welcome_label.setText(f"Привет, {self.user.username}!")
        self.show_products(spin_boxes=True)
        self.login_button.hide()

        self.edit_order_button = QPushButton("Редактировать заказ")
        self.edit_order_button.clicked.connect(self.show_order_widget)
        self.upper_layout.addWidget(self.edit_order_button)

    def show_order_widget(self):
        for i in range(self.products_layout.count()):
            product_groupbox = self.products_layout.itemAt(i).widget()
            quantity = product_groupbox.spin_box.value()

            # Проверяем, что количество больше 0
            if quantity > 0:
                # Проверяем, существует ли уже OrderProduct с таким product_id и order_id
                exists = any(
                    order_product.product_id == product_groupbox.product.id and order_product.order_id == self.order.id
                    for order_product in self.order_products
                )

                if not exists:  # Если OrderProduct не существует, создаем новый
                    print(self.order)
                    order_product = create_order_product(self.order.id, product_groupbox.product.id, quantity)
                    self.order_products.append(order_product)


        self.order_widget = OrderWidget()
        self.order_widget.show()
