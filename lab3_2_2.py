import sys
import json
import os
from PyQt6.QtWidgets import QApplication, QWidget


class Model:
    MIN_VALUE = 0
    MAX_VALUE = 100

    def __init__(self):
        self.a = 0
        self.b = 50
        self.c = 100
        self.listeners = []

        self.load()  

    def subscribe(self, callback):
        self.listeners.append(callback)
        callback(self.a, self.b, self.c)  

    def notify(self):
        for cb in self.listeners:
            cb(self.a, self.b, self.c)

    def _clamp(self, value):
        return max(self.MIN_VALUE, min(self.MAX_VALUE, value))

 
    def set_a(self, value):
        value = self._clamp(value)
        old = (self.a, self.b, self.c)

        self.a = value
        if self.a > self.b:
            self.b = self.a
        if self.b > self.c:
            self.c = self.b

        if (self.a, self.b, self.c) != old:
            self.notify()

    def set_b(self, value):
        value = self._clamp(value)
        old = (self.a, self.b, self.c)

        if value < self.a:
            value = self.a
        if value > self.c:
            value = self.c

        self.b = value

        if (self.a, self.b, self.c) != old:
            self.notify()

    def set_c(self, value):
        value = self._clamp(value)
        old = (self.a, self.b, self.c)

        self.c = value
        if self.c < self.b:
            self.b = self.c
        if self.b < self.a:
            self.a = self.b

        if (self.a, self.b, self.c) != old:
            self.notify()

    def save(self):
        path = os.path.join(os.path.dirname(__file__), "data.json")
        with open(path, "w") as f:
            json.dump({"a": self.a, "c": self.c}, f)
 
    def load(self):
        path = os.path.join(os.path.dirname(__file__), "data.json")
        try:
            with open(path, "r") as f:
                data = json.load(f)
                self.a = self._clamp(data.get("a", 0))
                self.c = self._clamp(data.get("c", 100))

                self.b = max(self.a, min(50, self.c))
        except:
            self.a = 0
            self.c = 100
            self.b = 50


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVC A B C")
        self.resize(600, 300)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())