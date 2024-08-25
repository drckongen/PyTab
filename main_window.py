from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QFileDialog
from child_window_1 import ChildWindow1
from child_window_2 import ChildWindow2
from xmlData import XmlData

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        self.xml_data = XmlData()
        self.child_windows = []

        self.open_child1_button = QPushButton("Open Child Window 1", self)
        self.open_child2_button = QPushButton("Open Child Window 2", self)
        self.load_xml_button = QPushButton("Load XML Data", self)

        layout = QVBoxLayout()
        layout.addWidget(self.open_child1_button)
        layout.addWidget(self.open_child2_button)
        layout.addWidget(self.load_xml_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.open_child1_button.clicked.connect(self.open_child_window_1)
        self.open_child2_button.clicked.connect(self.open_child_window_2)
        self.load_xml_button.clicked.connect(self.load_xml_data)

    def open_child_window_1(self):
        self.child1 = ChildWindow1(self.xml_data)
        self.child1.show()
        self.child_windows.append(self.child1)

    def open_child_window_2(self):
        if hasattr(self, 'child1'):
            self.child2 = ChildWindow2(self.xml_data)
            self.child2.update_column_info()  # Populate the column data based on xml_data
            self.child2.show()
            self.child_windows.append(self.child2)

    def load_xml_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        xml_file, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml);;All Files (*)", options=options)
        if xml_file:
            self.xml_data.load_from_file(xml_file)
