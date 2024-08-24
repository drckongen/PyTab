from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class ChildWindow2(QDialog):
    def __init__(self, shared_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Child Window 2")
        self.setGeometry(100, 100, 300, 200)
        self.shared_data = shared_data

        self.label = QLabel(self.shared_data.get_data(), self)
        self.update_button = QPushButton("Update Value to 'Child 2 Value'", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.update_button)
        self.setLayout(layout)

        self.shared_data.data_changed.connect(self.update_label)
        self.update_button.clicked.connect(self.change_value)

    def update_label(self, new_value):
        self.label.setText(new_value)

    def change_value(self):
        new_value = "Child 2 Value"
        self.shared_data.set_data(new_value)
