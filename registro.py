# from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QLineEdit, QPushButton, QTabWidget, QComboBox, QCalendarWidget, QMessageBox, QTableView, QVBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
import sys
from datetime import date, datetime
from sqlite3 import connect
from PyQt5.QtCore import *
from functools import partial


class Egresos(QWidget):
    def __init__(self, window, database):
        super().__init__()
        self.window = window
        self.mainLayout = QGridLayout()

        self.createLabels(database)
        self.createButtons()
        self.addTable(database)
        self.buttons["REFRESH"].clicked.connect(
            partial(self.addTable, database))
        self.buttons["SAVE"].clicked.connect(partial(self.addItem, database))
        self.buttons["DELETE"].clicked.connect(
            partial(self.deleteRow, database))

    def createLabels(self, database):
        self.labels = {
            "<h2>FECHA</h2>": (1, 0),
            "<h2>CONCEPTO</h2>": (2, 0),
            "<h2>VALOR</h2>": (3, 0),
        }
        for labelName, position in self.labels.items():
            self.label = QLabel(labelName)
            self.label.setStyleSheet("""
                    color: #A8DBC5; 
                    font-family: times;
                    font-weight: bold;""")
            self.mainLayout.addWidget(self.label, position[0], position[1])
        self.titleLabel = QLabel(f"<h2>Datos de {database}</h2>")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("""
                    color: #cac03f; font-family: times;
                    font-weight: bold;
                    border: 5px inset #cac03f;                 
                    font-size: 15px;
                    """)
        self.mainLayout.addWidget(self.titleLabel, 0, 0, 1, 3)
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
                    font-size: 15px;
                    """)
            self.mainLayout.addWidget(self.lineEdit, position[0], position[1])
            self.lineWidgets[lineName] = self.lineEdit

    def createButtons(self):
        buttonsName = {
            "SAVE": (1, 2),
            "DELETE": (2, 2),
            "REFRESH": (3, 2),

        }
        self.buttons = {}
        for widgetName, position in buttonsName.items():
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
            self.mainLayout.addWidget(self.button, position[0], position[1])
            self.buttons[widgetName] = self.button
        # Buttons signals

    def addTable(self, database):
        self.tableWidget = QTableView()
        self.tableWidget.setStyleSheet(
            "font-family: arial; background-color: #F8F8FF;")
        if QSqlDatabase.contains():
            db = QSqlDatabase.database()
            db.setDatabaseName('database.sqlite')
            db.open()
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('database.sqlite')
            db.open()

        model = QSqlQueryModel()
        model.setQuery(f"SELECT id, date, concept, value FROM {database}", db)

        self.tableWidget.setModel(model)
        self.mainLayout.addWidget(self.tableWidget, 4, 0, 1, 3)

    def deleteRow(self, database):
        self.conn = connect("database.sqlite")
        self.cur = self.conn.cursor()
        self.cur.execute(
            f"DELETE FROM {database} WHERE id=(SELECT MAX(id) FROM Compras)")
        self.conn.commit()
        self.cur.close()

    def addItem(self, database):
        try:

            date = self.lineWidgets["FECHA"].text()
            concept = self.lineWidgets["CONCEPTO"].text()
            value = int(self.lineWidgets["VALOR"].text())

            self.conn = connect("database.sqlite")
            self.cur = self.conn.cursor()
            self.cur.execute(
                f'''INSERT INTO {database} (date, concept, value) VALUES
                (?, ?, ?)''', (date, concept, value))
            self.conn.commit()
            self.cur.close()
        except ValueError:
            QMessageBox.critical(
                self, "ERROR", "Put all the fields")


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
        """This function creates all the labels of the tab1 and 
        also creates the layouts used in order to organize the 
        presentation"""
        # Grid layout to organize the widgets
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
        # CREATING THE SPECIAL BILL LABEL
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
        # setting the main layout in order to add the logo at the top
        # and the labels, line Edit widgets and buttons at the bottom
        self.mainLayout = QVBoxLayout()
        self.labelImg = QLabel()
        self.labelImg.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap('kafflogo.png')
        self.labelImg.setPixmap(self.pixmap)
        # Setting the vertical layout as the main Layout of the tab 1
        self.tab1.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.labelImg)
        # Adding the grid layout under the image
        self.mainLayout.addLayout(self.grid)

    def createLinesWidgets(self):
        """Function that create all the Line Edit widgets and 
        set the predefined values of the Date and Hour Line Widgets 
        that I don't want the user to touch"""
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

        # Getting the current date and setting its label
        self.today = str(date.today())
        self.lineEditWidgets["FECHA"].setText(self.today)
        # Using QTimer and its signal to actualize the hour Widget
        timer = QTimer(self.tab1)
        timer.timeout.connect(lambda: self.getHour(self.tab1))
        timer.start(1000)

    def getHour(self, parent):
        """This function calculates the current hour and 
        actualize the line edit widget"""
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

        # Buttons Signals
        self.buttons["CLEAR"].clicked.connect(self.clearAll)
        self.buttons["BROWSE"].clicked.connect(self.calendar)
        self.buttons["CALCULATE"].clicked.connect(self.calculate)
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
        """Function responsible of returning all the Line edit 
        widget values"""
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
    """Class used to realize an action that happens when the
    user clicks a button and the Presentation has to interact
    with the database"""

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
            if self.cur.fetchone()[0] is None:
                idBill = 0
            else:
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
    # lo que sigue entonces es llamar las funciones con parametros al crear la tabla
    # el parametro será el nombre de la tabla de la base de datos
    compras = Egresos(window, "Compras")
    compras.window.tab4.setLayout(compras.mainLayout)
    gastos = Egresos(window, "Gastos")
    gastos.window.tab5.setLayout(gastos.mainLayout)
    controller = Controller(window)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
