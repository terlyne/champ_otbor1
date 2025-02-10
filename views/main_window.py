from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QScrollArea,
)
from PyQt6.QtCore import Qt

from database.db import read_all_products, create_order, read_pickup_point_by_address
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

        # Пользователь
        self.user = None

        # Пункт выдачи
        self.pickup_point = None

        # Окно редактирования заказа
        self.order_widget = None

        # Кнопка для редактирования заказа
        self.edit_order_button = None


        # Словарь продуктов и их кол-ва в заказе
        self.order_products = {}

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


        self.do_order_button = QPushButton("Сделать заказ")
        self.do_order_button.clicked.connect(self.do_order)

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
                if product in self.order_products:
                    product_groupbox.spin_box.setValue(self.order_products[product])
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

        self.welcome_label.setText(f"Привет, {self.user.username}!")
        self.show_products(spin_boxes=True)
        self.login_button.hide()

        self.edit_order_button = QPushButton("Редактировать заказ")
        self.edit_order_button.clicked.connect(self.show_order_widget)
        self.upper_layout.addWidget(self.edit_order_button)

        self.main_layout.addWidget(self.do_order_button)

    def show_order_widget(self):
        # Обновляем order_products перед открытием OrderWidget
        self.order_products.clear()  # Очищаем предыдущие данные
        for i in range(self.products_layout.count()):
            product_groupbox = self.products_layout.itemAt(i).widget()
            if product_groupbox.spin_box.value() > 0:
                product = product_groupbox.product
                self.order_products[product] = product_groupbox.spin_box.value()

        self.order_widget = OrderWidget(self.order_products, self)
        self.order_widget.closed.connect(self.on_order_updated)
        self.order_widget.show()

    def on_order_updated(self):
        self.pickup_point = read_pickup_point_by_address(self.order_widget.pickup_point)
        print(self.pickup_point)

        self.show_products(spin_boxes=True)

    def do_order(self):
        print("Товары в заказе:", self.order_products)
        print("Пункт выдачи:", self.pickup_point)
        create_order(self.order_products, self.user.id, self.pickup_point.id)
