import sys
from PyQt6.QtWidgets import QApplication, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVC A B C")
        self.resize(600, 300)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())