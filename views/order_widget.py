from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QComboBox, QPushButton
)

from views.product_groupbox import ProductGroupBox
from database.db import read_all_pickup_points, read_all_order_products


class OrderWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.order_products = read_all_order_products()

        self.setMinimumSize(600, 400)

        self.setWindowTitle("Редактировать заказ")

        # Все пункты выдачи
        self.pickup_points = read_all_pickup_points()

        # Здесь мы сохраним значение выбранного пункта выдачи
        self.pickup_point = None

        self.main_layout = QVBoxLayout()

        self.products_layout = QVBoxLayout()
        self.products_widget = QWidget()
        self.products_scroll = QScrollArea()


        for order_product in self.order_products:
            product_groupbox = ProductGroupBox(self, order_product.product, spin_boxes=True)
            product_groupbox.spin_box.setValue(order_product.quantity)
            self.products_layout.addWidget(product_groupbox)

        self.products_widget.setLayout(self.products_layout)
        self.products_scroll.setWidget(self.products_widget)
        self.products_scroll.setWidgetResizable(True)

        self.main_layout.addWidget(self.products_scroll)

        self.pickup_points_combobox = QComboBox()

        self.pickup_points_addresses = [pickup_point.address for pickup_point in self.pickup_points]

        self.pickup_points_combobox.addItems(self.pickup_points_addresses)

        self.main_layout.addWidget(self.pickup_points_combobox)

        self.accept_button = QPushButton("Сохранить изменения")
        self.accept_button.clicked.connect(self.accept)
        self.main_layout.addWidget(self.accept_button)



        self.setLayout(self.main_layout)

    def accept(self):
        self.pickup_point = self.pickup_points_combobox.currentText()
        self.close()
