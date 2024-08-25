from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableView, QCheckBox, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex

class EnableTableModel(QAbstractTableModel):
    def __init__(self, columns_info, parent=None):
        super(EnableTableModel, self).__init__(parent)
        # Ensure columns_info is a list of lists to allow mutation
        self.columns_info = [list(col_info) for col_info in columns_info]

    def rowCount(self, parent=QModelIndex()):
        return len(self.columns_info)

    def columnCount(self, parent=QModelIndex()):
        return 3  # ID, Name, Enable

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()

            if col == 0:  # ID
                return self.columns_info[row][0]
            elif col == 1:  # Name
                return self.columns_info[row][1]
        elif role == Qt.CheckStateRole and index.column() == 2:
            return Qt.Checked if self.columns_info[index.row()][2] else Qt.Unchecked
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole and index.column() == 2:
            self.columns_info[index.row()][2] = (value == Qt.Checked)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if index.column() == 2:  # Enable column
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class ChildWindow2(QDialog):
    def __init__(self, xml_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Child Window 2 - Enable/Disable Columns")
        self.setGeometry(100, 100, 400, 300)
        self.xml_data = xml_data

        # Placeholder for column data: [(ID, Name, Enabled), ...]
        self.columns_info = []

        self.model = EnableTableModel(self.columns_info)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        # Connect to the xml_data signal to update the table when data changes
        self.xml_data.data_changed.connect(self.update_column_info)

    def update_column_info(self):
        # Populate columns_info based on the headers from xml_data
        headers = self.xml_data.get_headers()
        self.columns_info = [(i + 1, headers[i], True) for i in range(len(headers))]  # All columns enabled by default
        self.model.columns_info = self.columns_info  # Update model data
        self.model.layoutChanged.emit()

    def apply_column_visibility(self, child_window1):
        # Apply the visibility settings based on the state of the checkboxes
        for i, (col_id, col_name, enabled) in enumerate(self.columns_info):
            child_window1.table_view.setColumnHidden(i, not enabled)
