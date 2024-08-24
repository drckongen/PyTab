from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QFileDialog
from child_window_1 import ChildWindow1
from child_window_2 import ChildWindow2
from shared_data import SharedData

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        self.shared_data = SharedData()
        self.child_windows = []

        self.open_child1_button = QPushButton("Open Child Window 1", self)
        self.open_child2_button = QPushButton("Open Child Window 2", self)
        self.load_xml_button = QPushButton("Load XML Data into Table", self)
        self.update_label = QLabel(self.shared_data.get_data(), self)

        layout = QVBoxLayout()
        layout.addWidget(self.open_child1_button)
        layout.addWidget(self.open_child2_button)
        layout.addWidget(self.load_xml_button)
        layout.addWidget(self.update_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.open_child1_button.clicked.connect(self.open_child_window_1)
        self.open_child2_button.clicked.connect(self.open_child_window_2)
        self.load_xml_button.clicked.connect(self.load_xml_data)
        self.shared_data.data_changed.connect(self.update_label_from_shared_data)

    def open_child_window_1(self):
        child_window = ChildWindow1(self.shared_data)
        child_window.show()
        self.child_windows.append(child_window)
        self.child1 = child_window  # Keep a reference for later use

    def open_child_window_2(self):
        child_window = ChildWindow2(self.shared_data)
        child_window.show()
        self.child_windows.append(child_window)

    def load_xml_data(self):
        if hasattr(self, 'child1'):
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            xml_file, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml);;All Files (*)", options=options)
            if xml_file:
                self.child1.load_data_from_xml(xml_file)

    def update_label_from_shared_data(self, new_value):
        self.update_label.setText(new_value)
