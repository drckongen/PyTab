import sys
from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex


class LargeTableModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        super(LargeTableModel, self).__init__(parent)
        self._data = data
        self._headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return self._data[row][col]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section)
        return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Large Data Table")
        self.setGeometry(100, 100, 800, 600)

        # Sample data: 10,000 rows by 100 columns
        data = [[f"R{row}C{col}" for col in range(100)] for row in range(10000)]
        headers = [f"Column {i}" for i in range(100)]

        # Set up the model
        model = LargeTableModel(data, headers)

        # Set up the view
        table_view = QTableView()
        table_view.setModel(model)
        table_view.setAlternatingRowColors(True)
        table_view.setSortingEnabled(True)

        # Only show the first 10 columns for simplicity
        for col in range(10, 100):
            table_view.setColumnHidden(col, True)

        self.setCentralWidget(table_view)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
