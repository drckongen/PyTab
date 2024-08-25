from PyQt5.QtCore import QObject, pyqtSignal
import xml.etree.ElementTree as ET

class XmlData(QObject):
    data_changed = pyqtSignal()  # Signal to notify when the data has changed

    def __init__(self):
        super().__init__()
        self.headers = []  # To store column headers
        self.data = []     # To store the rows of data

    def load_from_file(self, xml_file):
        """Load data from an XML file and parse it."""
        try:
            namespaces = {'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}
            tree = ET.parse(xml_file)
            root = tree.getroot()

            self.headers = []
            self.data = []

            table = root.find('.//ss:Table', namespaces)
            if table is None:
                raise ValueError("No table found in XML")

            for i, row in enumerate(table.findall('ss:Row', namespaces)):
                row_data = []
                for j, cell in enumerate(row.findall('ss:Cell', namespaces)):
                    data_element = cell.find('ss:Data', namespaces)
                    cell_value = data_element.text if data_element is not None else ""
                    row_data.append(cell_value)

                    if i == 0 or i == 1:
                        if i == 0:
                            self.headers.append(cell_value)  # Row 0 as primary headers
                        else:
                            self.headers[j] = f"{self.headers[j]} ({cell_value})"  # Append Row 1 data to headers

                self.data.append(row_data)

            # Emit a signal to notify that data has changed
            self.data_changed.emit()

        except Exception as e:
            print(f"Error loading XML data: {e}")

    def get_headers(self):
        """Return the headers of the table."""
        return self.headers

    def get_data(self):
        """Return the data of the table."""
        return self.data
