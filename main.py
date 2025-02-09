from PyQt6.QtWidgets import QApplication
import sys

from views.main_window import MainWindow


from database.db import create_product


if __name__ == "__main__":
    # create_product("Помидоры", "Помидоры Тест Помидоры Тест", "ООО \"Зеленое Яблоко\"", 10.33, "image.jpg", 3)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    # from database.db import create_db
    # create_db()




