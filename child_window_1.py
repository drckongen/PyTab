from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

class LargeTableModel(QAbstractTableModel):
    def __init__(self, xml_data, parent=None):
        super(LargeTableModel, self).__init__(parent)
        self.xml_data = xml_data

    def rowCount(self, parent=None):
        return len(self.xml_data.get_data())

    def columnCount(self, parent=None):
        return len(self.xml_data.get_headers())

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return self.xml_data.get_data()[row][col]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.xml_data.get_headers()[section]
            else:
                return str(section)
        return None

class ChildWindow1(QDialog):
    def __init__(self, xml_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Child Window 1 - Table View")
        self.setGeometry(100, 100, 800, 600)
        self.xml_data = xml_data

        self.model = LargeTableModel(xml_data)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        # Connect to the xml_data signal to update the table when data changes
        self.xml_data.data_changed.connect(self.on_data_changed)

    def on_data_changed(self):
        """Update the table view when the data changes."""
        self.model.layoutChanged.emit()
        self.table_view.resizeColumnsToContents()
