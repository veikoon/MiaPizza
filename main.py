# Import
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from os.path import exists
import sys
# Initialize PyQt
app = QApplication([])


# Import database
if not exists("data.sql"):
    print("File data.sql does not exist. Please run initdb.py.")
    sys.exit()

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("data.sql")
db.open()

model = QSqlTableModel(None, db)
model.setTable("Pizzas")
model.select()
view = QTableView()
view.setModel(model)
view.show()

# Start application
app.exec_()