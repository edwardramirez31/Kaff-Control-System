# from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QLineEdit, QPushButton, QTabWidget, QComboBox, QCalendarWidget, QMessageBox, QTableView, QVBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
import sys
from datetime import date, datetime
from sqlite3 import connect
from PyQt5.QtCore import *

# arreglar el guardado de datos cuando no hay un campo rellenado
# buscar forma de quitar el 33 de 28333


class Compras(QWidget):
    def __init__(self, window):
        self.mainLayout = QGridLayout()
        self.labels = {
            "<h3>FECHA</h3>": (0, 0),
            "<h3>CONCEPTO</h3>": (2, 0),
            "<h3>VALOR</h3>": (3, 0),
        }
        for labelName, position in self.labels.items():
            self.label = QLabel(labelName)
            self.label.setStyleSheet("""
                    color: #A8DBC5; 
                    font-family: times;
                    font-weight: bold;""")
            self.mainLayout.addWidget(self.label, position[0], position[1])

        self.lineWidgets = {}
        self.lineEdits = {
            "FECHA": (1, 1),
            "CONCEPTO": (2, 1),
            "VALOR": (3, 1),
        }
        for lineName, position in self.lineEdits.items():
            self.lineEdit = QLineEdit()
            self.lineEdit.setStyleSheet("""
                    font-family: times;
                    background-color : #A8DBC5;
                    border: 2px solid white;
                    border-radius: 5px;
                    """)
            self.mainLayout.addWidget(self.lineEdit, position[0], position[1])
            self.lineWidgets[lineName] = self.lineEdit

        window.tab4.setLayout(self.mainLayout)
        self.addTable()

    def addTable(self):

        self.tableWidget = QTableView()
        if QSqlDatabase.contains():
            db = QSqlDatabase.database()
            db.setDatabaseName('database.sqlite')
            db.open()
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('database.sqlite')
            db.open()

        model = QSqlQueryModel()
        model.setQuery("SELECT date, concept, value FROM Compras", db)

        self.tableWidget.setModel(model)
        self.mainLayout.addWidget(self.tableWidget, 4, 1, 1, 2)


class Ingresos(QTableView):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self)
        self.setStyleSheet("font-family: arial; background-color: #F8F8FF;")
        self.refreshButton = QPushButton("REFRESH")
        self.refreshButton.clicked.connect(self.income)
        self.verticalLayout.addWidget(self.refreshButton)
        self.window.tab3.setLayout(self.verticalLayout)
        self.income()

    def income(self):

        if QSqlDatabase.contains():
            db = QSqlDatabase.database()
            db.setDatabaseName('database.sqlite')
            db.open()
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('database.sqlite')
            db.open()

        model = QSqlQueryModel()
        model.setQuery('''
        SELECT Clients.id, Clients.date, Clients.hour, Clients.name, Clients.total, Clients.value FROM Clients''', db)

        self.setModel(model)


class Database(QTableView):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self)
        self.setStyleSheet("font-family: arial; background-color: #F8F8FF;")
        self.showButton = QPushButton("SHOW")
        self.showButton.setStyleSheet("""
                    QPushButton {
                        background-color: #A8DBC5;
                        border-style: outset;
                        border-width: 2px;
                        font-family: arial;
                        font-weight: bold;
                        font-size: 12px;
                        border-color: white;
                    }
                    QPushButton:hover {
                        background-color: #E6E6FA;
                    }
                    QPushButton:pressed {
                        border-style: inset;
                    }
                    """)
        self.showButton.clicked.connect(self.connectDatabase)
        self.verticalLayout.addWidget(self.showButton)
        self.window.tab2.setLayout(self.verticalLayout)
        self.connectDatabase()

    def connectDatabase(self):

        if QSqlDatabase.contains():
            db = QSqlDatabase.database()
            db.setDatabaseName('database.sqlite')
            db.open()
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('database.sqlite')
            db.open()

        model = QSqlQueryModel()
        model.setQuery('''
        SELECT Clients.id, Clients.date, Clients.hour, Clients.name, Clients.birthday, Clients.cellphone,
        Clients.address, City.name, Payment.method, Clients.pollo, Clients.carne,
        Clients.empanachos, Clients.total, Clients.value FROM Clients JOIN City JOIN Payment
        ON Clients.city_id = City.id AND Clients.payment_id = Payment.id''', db)

        self.setModel(model)


class Registro(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kaff Bussiness Management')
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: #2b8c84;")
        self.createTabs()
        self.createLabels()
        self.createLinesWidgets()
        self.createButtons()

    def createTabs(self):
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.addTab(self.tab1, "Registro")
        self.addTab(self.tab2, "Base de Datos")
        self.addTab(self.tab3, "Ingresos")
        self.addTab(self.tab4, "Compras")
        self.addTab(self.tab5, "Gastos")

    def createLabels(self):
        # Client Data
        self.grid = QGridLayout()
        self.labelWidgets = {

            "<h2>FECHA</h2>": (0, 0),
            "<h2>BILL AREA</h2>": (0, 3, 1, 1),
            "<h2>HORA</h2>": (1, 0),
            "<h2>NOMBRE</h2>": (2, 0),
            "<h2>CUMPLEAÑOS</h2>": (3, 0),
            "<h2>CELULAR</h2>": (4, 0),
            "<h2>DIRECCIÓN</h2>": (5, 0),
            "<h2>CIUDAD</h2>": (6, 0),
            "<h2>MÉTODO DE PAGO</h2>": (7, 0),
            "<h2>PEDIDO</h2>": (8, 0, 1, 3),
            "<h2>TOTAL POLLO</h2>": (9, 0),
            "<h2>TOTAL CARNE</h2>": (10, 0),
            "<h2>EMPANACHOS</h2>": (11, 0),
            "<h2>TOTAL PRODUCTOS</h2>": (12, 0),
            "<h2>VALOR ($)</h2>": (13, 0)
        }
        for labelName, position in self.labelWidgets.items():
            if len(position) == 4:
                self.label = QLabel(labelName)
                self.label.setAlignment(Qt.AlignCenter)
                self.label.setStyleSheet("""
                    color: #cac03f; font-family: times;
                    font-weight: bold;
                    border: 5px inset #cac03f;                 
                    font-size: 15px;
                    """)
                self.grid.addWidget(
                    self.label, position[0], position[1], position[2], position[3])

            else:
                self.label = QLabel(labelName)
                self.label.setStyleSheet("""
                    color: #A8DBC5; 
                    font-family: times;
                    font-weight: bold;""")
                self.grid.addWidget(self.label, position[0], position[1])

    def createLinesWidgets(self):

        lineEditWidgets = {
            "FECHA": (0, 1, 1, 2),
            "HORA": (1, 1, 1, 2),
            "NOMBRE": (2, 1, 1, 2),
            "CUMPLEAÑOS": (3, 1),
            "CELULAR": (4, 1, 1, 2),
            "DIRECCIÓN": (5, 1, 1, 2),
            "CIUDAD": (6, 1, 1, 2),
            "POLLO": (9, 1, 1, 2),
            "CARNE": (10, 1, 1, 2),
            "EMPANACHOS": (11, 1, 1, 2),
            "CANTIDAD DE EMPA": (12, 1, 1, 2),
            "VALOR": (13, 1),

        }
        self.lineEditWidgets = {}
        for widgetName, position in lineEditWidgets.items():
            if len(position) == 2:
                self.lineEdit = QLineEdit()
                self.lineEdit.setReadOnly(True)

                self.lineEdit.setStyleSheet("""
                    font-family: times;
                    font-size: large;
                    background-color : #A8DBC5;
                    border: 2px solid white;
                    border-radius: 5px;
                    font-size: 15px;
                    """)
                # self.lineEdit.setStyleSheet("border-radius: 1px;")
                self.grid.addWidget(self.lineEdit, position[0], position[1])
                self.lineEditWidgets[widgetName] = self.lineEdit
            else:
                self.lineEdit = QLineEdit()

                self.lineEdit.setStyleSheet("""
                    font-family: times;
                    font-size: large;
                    background-color : #A8DBC5;
                    border: 2px solid white;
                    border-radius: 5px;
                    font-size: 15px;
                    """)
                if widgetName == "CANTIDAD DE EMPA":
                    self.lineEdit.setReadOnly(True)
                self.grid.addWidget(
                    self.lineEdit, position[0], position[1], position[2], position[3])
                self.lineEditWidgets[widgetName] = self.lineEdit

        # Getting the current date
        self.today = str(date.today())
        timer = QTimer(self.tab1)
        timer.timeout.connect(lambda: self.getHour(self.tab1))
        timer.start(1000)
        self.lineEditWidgets["FECHA"].setText(self.today)

        self.bill = QLabel()
        self.bill.setFixedWidth(300)
        self.bill.setStyleSheet("""
                    font-family: times;
                    font-size: large;
                    background-color : white;
                    border: 4px solid #A8DBC5;
                    font-size: 15px;
                    """)
        self.grid.addWidget(self.bill, 1, 3, 13, 1)

    def getHour(self, parent):

        self.now = datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        self.lineEditWidgets["HORA"].setText(self.current_time)

    def createButtons(self):
        buttonsPosition = {
            "BROWSE": (3, 2),
            "CALCULATE": (13, 2),
            "SAVE": (14, 0),
            "CLEAR": (14, 1),
            "DELETE": (14, 2),
            "GENERATE BILL": (14, 3)
        }
        self.buttons = {}
        for widgetName, position in buttonsPosition.items():
            self.button = QPushButton(widgetName)

            self.button.setStyleSheet("""
                    QPushButton {
                        
                        background-color: #A8DBC5;
                        font-family: arial;
                        font-weight: bold;
                        font-size: 12px;
                        border-color: white;
                    }
                    QPushButton:hover {
                        background-color: #DAE0E2;
                    }
                    """)
            self.grid.addWidget(self.button, position[0], position[1])
            self.buttons[widgetName] = self.button
        self.vertical = QVBoxLayout()
        self.labelImg = QLabel()

        self.labelImg.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap('kafflogo.png')
        self.labelImg.setPixmap(self.pixmap)
        self.tab1.setLayout(self.vertical)
        self.vertical.addWidget(self.labelImg)
        self.vertical.addLayout(self.grid)

        # Buttons Signals
        self.buttons["CLEAR"].clicked.connect(self.clearAll)
        self.buttons["BROWSE"].clicked.connect(self.calendar)
        self.buttons["CALCULATE"].clicked.connect(self.calculate)
# DAE0E2
        # Creating the Combo Box Button
        self.combo = QComboBox()
        self.combo.setStyleSheet("""
                    font-family: times;
                    font-size: 15px;
                    background-color : #A8DBC5;
                    border: 1px solid white;
                    
                    """)
        self.combo.addItems(['Efectivo', 'Nequi'])
        self.grid.addWidget(self.combo, 7, 1, 1, 2)

    def clearAll(self):
        for widgetName, lineWidget in self.lineEditWidgets.items():
            if widgetName == "FECHA" or widgetName == "HORA":
                pass
            else:
                lineWidget.setText("")

    def calculate(self):
        self.pollo = self.lineEditWidgets["POLLO"].text()
        self.carne = self.lineEditWidgets["CARNE"].text()
        self.empanachos = self.lineEditWidgets["EMPANACHOS"].text()

        if self.pollo == "":
            self.lineEditWidgets["POLLO"].setText("0")
            self.pollo = 0
        if self.carne == "":
            self.lineEditWidgets["CARNE"].setText("0")
            self.carne = 0
        if self.empanachos == "":
            self.lineEditWidgets["EMPANACHOS"].setText("0")
            self.empanachos = 0

        try:
            self.Total = int(self.pollo) + int(self.carne)
            self.lineEditWidgets["CANTIDAD DE EMPA"].setText(str(self.Total))
            if self.Total > 5:
                self.value = round(7000/3 * self.Total +
                                   2500 * int(self.empanachos))
            else:
                self.value = round(2500 * (self.Total + int(self.empanachos)))
            self.lineEditWidgets["VALOR"].setText(str(self.value))
        except:
            QMessageBox.critical(
                self, "ERROR", "Put only numbers in 'POLLO' and 'CARNE' fields")

    def calendar(self):
        self.cal = QCalendarWidget()
        self.cal.setWindowTitle("Get Birthday")
        self.cal.show()
        self.cal.clicked.connect(self.dateB)

    def dateB(self):
        self.date = self.cal.selectedDate()
        self.lineEditWidgets["CUMPLEAÑOS"].setText(
            self.date.toString("yyyy-MM-dd"))

    def getValues(self):
        self.valuesToSave = list()
        for widgetName, widget in self.lineEditWidgets.items():
            if widgetName == "CIUDAD":
                if widget.text() == "Bucaramanga":
                    self.valuesToSave.append(1)
                else:
                    self.valuesToSave.append(2)
            else:
                self.valuesToSave.append(widget.text())
        if str(self.combo.currentText()) == "Nequi":
            payment_id = 1
        else:
            payment_id = 2

        date, hour, name, birthday, cellphone, address, city_id, pollo, carne, empanachos, total, value = self.valuesToSave

        pollo = int(pollo)
        carne = int(carne)
        empanachos = int(empanachos)
        total = int(total)
        value = int(value)

        return date, hour, name, birthday, cellphone, address, city_id, payment_id, pollo, carne, empanachos, total, value


class Controller:
    def __init__(self, window):
        self.window = window
        self.window.buttons["DELETE"].clicked.connect(self.deleteRow)
        self.window.buttons["SAVE"].clicked.connect(self.saveRow)
        self.window.buttons["GENERATE BILL"].clicked.connect(self.generateBill)

    def deleteRow(self):
        self.conn = connect('database.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('''
        DELETE FROM Clients WHERE id=(SELECT MAX(id) FROM Clients)
        ''')
        self.conn.commit()
        self.cur.close()

    def saveRow(self):
        try:
            # obtener el id con busqueda SQL y lo asigne a una variable
            self.valuesToSave = self.window.getValues()
            self.conn = connect('database.sqlite')
            self.cur = self.conn.cursor()
            self.cur.execute('''INSERT INTO Clients(date, hour, name, birthday,
            cellphone, address,city_id, payment_id, pollo, carne, empanachos, total,
            value) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', self.valuesToSave)
            self.conn.commit()
            self.cur.close()
            self.window.clearAll()
            self.window.bill.setText("")
        except ValueError:
            QMessageBox.critical(
                self.window, "ERROR", "Put all the fields")

    def generateBill(self):
        try:
            today = self.window.today
            hour = self.window.lineEditWidgets["HORA"].text()
            nombre = self.window.lineEditWidgets["NOMBRE"].text()
            price = self.window.lineEditWidgets["VALOR"].text()
            total = int(self.window.lineEditWidgets["CANTIDAD DE EMPA"].text())
            pollo = int(self.window.lineEditWidgets["POLLO"].text())
            carne = int(self.window.lineEditWidgets["CARNE"].text())
            empanachos = int(self.window.lineEditWidgets["EMPANACHOS"].text())

            if total > 5:
                valorEmpanada = 2350
            else:
                valorEmpanada = 2500
            # get bill number
            self.conn = connect('database.sqlite')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT MAX(id) FROM Clients")
            idBill = self.cur.fetchone()[0]
            self.cur.close()

            self.window.bill.setText(f'''
        Welcome to Kaff
        ==============================
        Fecha: {today}   
        Hora: {hour}
        No de Factura: {idBill + 1}
        Nombre: {nombre}        
        ==============================
       
        Descr\t\tCant\tPrecio\n
        Pollo\t\t{pollo}\t{pollo*valorEmpanada}
        Carne\t\t{carne}\t{carne*valorEmpanada}
        Pollo\t\t{empanachos}\t{empanachos*2500}
        ==============================
        TOTAL\t\t{total}\t${price}
        
        ''')
        except ValueError:
            QMessageBox.critical(
                self.window, "ERROR", "Put all the fields")


def main():
    app = QApplication(sys.argv)
    window = Registro()
    window.show()
    tabDatabase = Database(window)
    ingresos = Ingresos(window)
    compras = Compras(window)
    controller = Controller(window)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
