from PyQt5.QtCore import pyqtSignal, QObject

class SharedData(QObject):
    data_changed = pyqtSignal(str)

    def __init__(self, initial_value="Initial Value"):
        super().__init__()
        self._data = initial_value

    def get_data(self):
        return self._data

    def set_data(self, value):
        self._data = value
        self.data_changed.emit(self._data)
