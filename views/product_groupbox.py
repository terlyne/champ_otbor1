import io

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSpinBox
)


class ProductGroupBox(QGroupBox):
    def __init__(self, parent, product, spin_boxes=False):
        super().__init__(parent)

        self.product = product

        self.main_layout = QHBoxLayout()

        self.info_layout = QVBoxLayout()

        self.name_label = QLabel(f"Название: {self.product.name}")
        self.description_label = QLabel(f"Описание: {self.product.description}")
        self.maker_label = QLabel(f"Производитель: {self.product.maker}")
        self.price_label = QLabel(f"Цена: {self.product.price}")

        image_data = self.product.photo
        image_stream = io.BytesIO(image_data)  # Преобразуем BLOB в поток
        pixmap = QPixmap()
        pixmap.loadFromData(image_stream.read())  # Загружаем изображение из потока
        scaled_pixmap = pixmap.scaled(200, 200, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio) # Это необязательно (Чисто для размера изображения)
        self.photo_label = QLabel()
        self.photo_label.setPixmap(scaled_pixmap)

        self.info_layout.addWidget(self.name_label)
        self.info_layout.addWidget(self.description_label)
        self.info_layout.addWidget(self.maker_label)
        self.info_layout.addWidget(self.price_label)

        if self.product.discount:
            self.discount_label = QLabel(f"Скидка: {self.product.discount}")
            self.info_layout.addWidget(self.discount_label)

        self.main_layout.addLayout(self.info_layout)

        self.main_layout.addWidget(self.photo_label)


        if spin_boxes:
            self.spin_box = QSpinBox()
            self.spin_box.setMaximumWidth(100)
            self.main_layout.addWidget(self.spin_box)


        self.setLayout(self.main_layout)