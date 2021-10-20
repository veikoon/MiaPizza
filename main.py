# Imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import core


# Init values
datafile = 'data.json'

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)

fen = QWidget()

# on donne un titre à la fenêtre
fen.setWindowTitle("Mia Pizza")

# on fixe la taille de la fenêtre
fen.resize(1280,720)

data = core.load()
headers = ["Ingredients", "Quantités"]
ingredients = list(data['Ingredients'].items())

class TableModel(QAbstractTableModel):
    def rowCount(self, parent):
        return len(ingredients)
    def columnCount(self, parent):
        return len(headers)
    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        return ingredients[index.row()][index.column()]
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return headers[section]

model = TableModel()
view = QTableView()
view.setModel(model)
fen.setCentralWidget(view)
fen.show()
app.exec_()