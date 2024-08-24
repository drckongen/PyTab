import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton
from PyQt5.QtCore import QAbstractTableModel, Qt

class LargeTableModel(QAbstractTableModel):
    def __init__(self, data=None, headers=None, parent=None):
        super(LargeTableModel, self).__init__(parent)
        self._data = data if data else []
        self._headers = headers if headers else []

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

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

    def update_data(self, data, headers):
        self.beginResetModel()
        self._data = data
        self._headers = headers
        self.endResetModel()

class ChildWindow1(QDialog):
    def __init__(self, shared_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Child Window 1 - Table View")
        self.setGeometry(100, 100, 800, 600)
        self.shared_data = shared_data

        self.model = LargeTableModel()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)

        self.update_button = QPushButton("Update Shared Data from Table View", self)
        self.update_button.clicked.connect(self.update_shared_data)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addWidget(self.update_button)
        self.setLayout(layout)

    def update_shared_data(self):
        new_value = "Updated from Table View"
        self.shared_data.set_data(new_value)

    def load_data_from_xml(self, xml_file):
        try:
            # Define the namespaces used in the XML file
            namespaces = {
                'ss': 'urn:schemas-microsoft-com:office:spreadsheet'
            }

            # Parse the XML file and extract data
            tree = ET.parse(xml_file)
            root = tree.getroot()

            data = []
            headers = []

            # Find the Table element
            table = root.find('.//ss:Table', namespaces)
            if table is None:
                raise ValueError("No table found in XML")

            # Process the rows in the table
            for i, row in enumerate(table.findall('ss:Row', namespaces)):
                row_data = []
                for j, cell in enumerate(row.findall('ss:Cell', namespaces)):
                    data_element = cell.find('ss:Data', namespaces)
                    cell_value = data_element.text if data_element is not None else ""
                    row_data.append(cell_value)

                    # Use the first row as headers if headers are not already set
                    if i == 0:
                        headers.append(f"Column {j + 1}")

                data.append(row_data)

            # Update the table model with the parsed data
            self.model.update_data(data, headers)
            self.table_view.resizeColumnsToContents()  # Resize columns to fit content

        except Exception as e:
            print(f"Error loading XML data: {e}")  # Print any errors
