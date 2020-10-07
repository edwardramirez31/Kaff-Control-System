from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtCore import *
from datetime import date, datetime
from functools import partial
from sqlite3 import connect
import matplotlib.pyplot as plt
import numpy as np
import sys


class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kaff Bussiness Management')
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: #2b8c84;")
        self.createTabs()
        self.createLabels()
        self.createLinesWidgets()
        self.createButtons()
        self.comboBoxes()

    def createTabs(self):
        """ Function that creates all the tabs and set their name"""
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()
        self.addTab(self.tab1, "Registro")
        self.addTab(self.tab2, "Base de Datos")
        self.addTab(self.tab3, "Ingresos")
        self.addTab(self.tab4, "Compras")
        self.addTab(self.tab5, "Gastos")
        self.addTab(self.tab6, "Res. Diarios")
        self.addTab(self.tab7, "Res. Mensuales")
        self.addTab(self.tab8, "Res. Anuales")

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
        self.bill = QTextEdit()
        self.bill.setFixedWidth(320)
        self.bill.setStyleSheet("""
                    font-family: times;
                    font-size: large;
                    background-color : white;
                    border: 4px solid #A8DBC5;
                    font-size: 15px;
                    """)
        self.grid.addWidget(self.bill, 1, 3, 12, 1)
        # setting the main layout in order to add the logo at the top
        # and the labels, line Edit widgets and buttons at the bottom
        self.mainLayout = QVBoxLayout()
        # Creating the Image Label for the Business logo
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
        """This function aims to create the buttons, 
        set their style, items, save them in a dictionary
        and add them to the grid layout"""
        buttonsPosition = {
            "BROWSE": (3, 2),
            "CALCULATE": (13, 2),
            "SAVE": (14, 0),
            "CLEAR": (14, 1),
            "DELETE": (14, 2),
            "PRINT": (13, 3),
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
        # Setting calendar icon
        self.buttons["BROWSE"].setIcon(QIcon("calendarr.png"))
        # Buttons Signals
        self.buttons["CLEAR"].clicked.connect(self.clearAll)
        self.buttons["BROWSE"].clicked.connect(self.calendar)
        self.buttons["CALCULATE"].clicked.connect(self.calculate)
        self.buttons["PRINT"].clicked.connect(self.printBill)

    def comboBoxes(self):
        """This function aims to create the two QComboBox buttons, 
        set their style, items and add it to the grid layout """
        # Cities Combo Button
        self.comboCities = QComboBox()
        self.comboCities.setStyleSheet("""
                    font-family: times;
                    font-size: 15px;
                    background-color : #A8DBC5;
                    border: 1px solid white;

                    """)
        self.comboCities.addItems(
            ['Girón', 'Piedecuesta', 'Floridablanca', 'Bucaramanga'])
        self.grid.addWidget(self.comboCities, 6, 1, 1, 2)
        self.comboCities.setCurrentText("Bucaramanga")
        # Payment Combo Button
        self.comboPayment = QComboBox()
        self.comboPayment.setStyleSheet("""
                    font-family: times;
                    font-size: 15px;
                    background-color : #A8DBC5;
                    border: 1px solid white;

                    """)
        self.comboPayment.addItems(['Efectivo', 'Nequi'])
        self.grid.addWidget(self.comboPayment, 7, 1, 1, 2)

    def clearAll(self):
        """Function that clears the Line Edit Widgets"""
        for widgetName, lineWidget in self.lineEditWidgets.items():
            if widgetName == "FECHA" or widgetName == "HORA":
                pass
            else:
                lineWidget.setText("")

    def calculate(self):
        """Function that calculates the total price"""

        self.pollo = self.lineEditWidgets["POLLO"].text()
        self.carne = self.lineEditWidgets["CARNE"].text()
        self.empanachos = self.lineEditWidgets["EMPANACHOS"].text()

        # setting variable values and widget text to 0 if
        # there is no number on screen
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
            # Total of main products
            self.Total = int(self.pollo) + int(self.carne)
            self.lineEditWidgets["CANTIDAD DE EMPA"].setText(
                str(self.Total + int(self.empanachos)))
            # Calculate the value in function of the Total
            if self.Total > 5:
                self.value = round(7000/3 * self.Total +
                                   2500 * int(self.empanachos))
            else:
                self.value = round(2500 * (self.Total + int(self.empanachos)))
            # setting value on screen
            self.lineEditWidgets["VALOR"].setText(str(self.value))
        except ValueError:
            QMessageBox.critical(
                self, "ERROR", "Put only numbers in 'POLLO' and 'CARNE' fields")

    def calendar(self):
        """This function creates the Calendar widget and connects its 
        buttons with the function used to get the date"""
        self.cal = QCalendarWidget()
        self.cal.setWindowTitle("Get Birthday")
        self.cal.show()
        self.cal.clicked.connect(self.dateB)

    def dateB(self):
        """Function used to assign the selected date in the 
        calendar to its corresponding Line Edit Widget"""
        self.date = self.cal.selectedDate()
        self.lineEditWidgets["CUMPLEAÑOS"].setText(
            self.date.toString("yyyy-MM-dd"))

    def getValues(self):
        """function whose goal is to return the values of each widget
        displayed on the screen"""
        self.valuesToSave = list()
        # Getting the values that are in the QLineEdit Widgets
        for widgetName, widget in self.lineEditWidgets.items():
            self.valuesToSave.append(widget.text())
        # Unpacking the list
        date, hour, name, birthday, cellphone, address, pollo, carne, \
            empanachos, total, value = self.valuesToSave
        # Getting the city id from the comboCities Widget
        if str(self.comboCities.currentText()) == "Bucaramanga":
            city_id = 1
        elif str(self.comboCities.currentText()) == "Floridablanca":
            city_id = 2
        elif str(self.comboCities.currentText()) == "Piedecuesta":
            city_id = 3
        else:
            city_id = 4

        # Getting the payment id from the comboPayment Widget
        if str(self.comboPayment.currentText()) == "Nequi":
            payment_id = 1
        else:
            payment_id = 2

        # Getting month and year id. If the month is 01, get the
        # second string char
        try:
            month = int(date.split("-")[1])
        except ValueError:
            month = int(date.split("-")[1][1])

        year = int(date.split("-")[0])

        return date, month, year, hour, name, birthday, cellphone, \
            address, city_id, payment_id, int(pollo), int(carne), \
            int(empanachos), int(total), int(value)

    def printBill(self):
        self.printer = QPrinter(QPrinter.HighResolution)
        self.dialog = QPrintDialog(self.printer, self)

        if self.dialog.exec_() == QPrintDialog.Accepted:
            self.bill.print_(self.printer)


class Controller:
    """Class used to perform an action that occurs when 
    the user clicks a button and the presentation has 
    to interact with the database"""

    def __init__(self, window):
        # Connecting buttons with signals
        self.window = window
        self.window.buttons["DELETE"].clicked.connect(self.deleteRow)
        self.window.buttons["SAVE"].clicked.connect(self.saveRow)
        self.window.buttons["GENERATE BILL"].clicked.connect(self.generateBill)

    def deleteRow(self):
        """Function used to delete the last row of the database"""
        self.conn = connect('database.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('''
        DELETE FROM Clients WHERE id=(SELECT MAX(id) FROM Clients)
        ''')
        self.conn.commit()
        self.cur.close()

    def saveRow(self):
        """Function used to get the values displayed on the screen, 
        assign them to a tuple and run SQL to save them to the database"""
        try:
            self.valuesToSave = self.window.getValues()
            self.conn = connect('database.sqlite')
            self.cur = self.conn.cursor()
            self.cur.execute('''INSERT INTO Clients (date, month, 
            year, hour, name, birthday, cellphone, address,city_id, 
            payment_id, pollo, carne, empanachos, total, value) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?)
            ''', self.valuesToSave)
            self.conn.commit()
            self.cur.close()
            self.window.clearAll()
            self.window.bill.setText("")
        except ValueError:
            QMessageBox.critical(
                self.window, "ERROR", "Put all the fields and check the values")

    def generateBill(self):
        try:
            # Getting the current date and hour from screen
            today = self.window.today
            hour = self.window.lineEditWidgets["HORA"].text()
            # Getting the purchase values
            nombre = self.window.lineEditWidgets["NOMBRE"].text()
            direccion = self.window.lineEditWidgets["DIRECCIÓN"].text()
            price = self.window.lineEditWidgets["VALOR"].text()
            total = int(self.window.lineEditWidgets["CANTIDAD DE EMPA"].text())
            pollo = int(self.window.lineEditWidgets["POLLO"].text())
            carne = int(self.window.lineEditWidgets["CARNE"].text())
            empanachos = int(self.window.lineEditWidgets["EMPANACHOS"].text())

            # Setting the actual item price
            if total > 5:
                valorEmpanada = 7000/3
            else:
                valorEmpanada = 2500
            # Get bill number
            self.conn = connect('database.sqlite')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT MAX(id) FROM Clients")
            idBill = self.cur.fetchone()[0]
            self.cur.close()
            # Setting the text of the Bill Widget
            self.window.bill.setText(f'''
        Welcome to Kaff
        ===============================
        Fecha: {today}
        Hora: {hour}
        No de Factura: {idBill + 1}
        Nombre: {nombre}
        Dirección: {direccion}
        ===============================

        Descr\t\tCant\tPrecio\n
        Pollo\t\t{pollo}\t{round(pollo*valorEmpanada)}
        Carne\t\t{carne}\t{round(carne*valorEmpanada)}
        Empanachos\t{empanachos}\t{empanachos*2500}
        ===============================
        TOTAL\t{total}\t${price}

        ''')
            # SAVING THE BILL IN "Facturas" Folder
            with open(f"Facturas/Factura No {idBill + 1}", "w") as fhandle:
                fhandle.write(self.window.bill.toPlainText())

        except ValueError:
            QMessageBox.critical(
                self.window, "ERROR", "Put all the fields")


class Egresos(QWidget):
    def __init__(self, window, database):
        """ The init method create the tab view, use the database
        name as parameter in order to run SQL in the correct db"""
        super().__init__()
        self.window = window
        self.mainLayout = QGridLayout()
        # Creating the Widgets
        self.createLabels(database)
        self.createLineWidgets()
        self.createButtons()
        # Adding the Table widget in function of the database name
        self.addTable(database)
        # Connecting the buttons with their function
        self.buttons["REFRESH TABLE"].clicked.connect(
            partial(self.addTable, database))
        self.buttons["SAVE"].clicked.connect(
            partial(self.addItem, database))
        self.buttons["DELETE"].clicked.connect(
            partial(self.deleteRow, database))
        self.buttons["ADD NULL DAY"].clicked.connect(
            partial(self.addingNull, database))

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
        # Special Label
        self.titleLabel = QLabel(f"<h2>DATOS DE {database.upper()}</h2>")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("""
                    color: #cac03f; font-family: times;
                    font-weight: bold;
                    border: 5px inset #cac03f;
                    font-size: 15px;
                    """)
        self.mainLayout.addWidget(self.titleLabel, 0, 0, 1, 3)

    def createLineWidgets(self):
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
        self.lineWidgets["FECHA"].setPlaceholderText(
            '''Usa el formato de fecha "yyyy-mm-dd" Ej: 2020-12-01 para el 1 de Diciembre''')

    def createButtons(self):
        buttonsName = {
            "SAVE": (1, 2),
            "DELETE": (2, 2),
            "REFRESH TABLE": (4, 1),
            "ADD NULL DAY": (3, 2)
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

    def addTable(self, database):
        """ This function creates the table widget, checks the 
        Database connection and run a SQL Query in function of
        the database name"""
        self.tableWidget = QTableView()
        self.tableWidget.setStyleSheet(
            "font-family: arial; background-color: #F8F8FF;")
        # Checking connection
        if QSqlDatabase.contains():
            db = QSqlDatabase.database()
            db.setDatabaseName('database.sqlite')
            db.open()
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('database.sqlite')
            db.open()
        # Setting the SQL Query
        model = QSqlQueryModel()
        model.setQuery(f'''SELECT id, date, concept, value 
        FROM {database}''', db)
        # Modeling and setting the Widget Position in the grid
        self.tableWidget.setModel(model)
        self.mainLayout.addWidget(self.tableWidget, 5, 0, 1, 3)

    def deleteRow(self, database):
        """Function used to delete the last row of the database"""
        self.conn = connect("database.sqlite")
        self.cur = self.conn.cursor()
        self.cur.execute(
            f"DELETE FROM {database} WHERE id=(SELECT MAX(id) FROM {database})")
        self.conn.commit()
        self.cur.close()

    def addItem(self, database):
        # getting dates
        try:
            date = self.lineWidgets["FECHA"].text()
            try:
                month = int(date.split("-")[1])
            except ValueError:
                month = int(date.split("-")[1][0])
            year = int(date.split("-")[0])

            concept = self.lineWidgets["CONCEPTO"].text()
            value = int(self.lineWidgets["VALOR"].text())

            self.conn = connect("database.sqlite")
            self.cur = self.conn.cursor()
            self.cur.execute(
                f'''INSERT INTO {database} (date, month_id, year, concept, 
                value) VALUES(?, ?, ?, ?, ?)
                ''', (date, month, year, concept, value))
            self.conn.commit()
            self.cur.close()
            # Deleting the widgets content
            for lineWidget in self.lineWidgets.values():
                lineWidget.setText("")
        except (ValueError, IndexError):
            QMessageBox.critical(
                self, "ERROR", '''Put the values in their correct form 
                and field''')

    def addingNull(self, database):
        """if the business doesn't buy anything in a day, a purchase 
        value of zero must be added for that day"""
        try:
            date = self.lineWidgets["FECHA"].text()
            try:
                month = int(date.split("-")[1])
            except ValueError:
                month = int(date.split("-")[1][0])
            year = int(date.split("-")[0])
            self.conn = connect("database.sqlite")
            self.cur = self.conn.cursor()
            self.cur.execute(
                f'''INSERT INTO {database} (date, month_id, year, concept, 
                value) VALUES(?, ?, ?, ?, ?)
                ''', (date, month, year, "NADA", 0))
            self.conn.commit()
            self.cur.close()
        except (ValueError, IndexError):
            QMessageBox.critical(
                self, "ERROR", '''Put the date in its correct form''')


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
                        border-color: gray;
                    }
                    """)
        self.verticalLayout.addWidget(self.showButton)

    def checkingConnection(self):
        """This function aims to check the database connection name
        and use it if exists"""
        if QSqlDatabase.contains():
            self.db = QSqlDatabase.database()
            self.db.setDatabaseName('database.sqlite')
            self.db.open()
        else:
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            self.db.setDatabaseName('database.sqlite')
            self.db.open()

    def connectDatabase(self):
        """This function displays the Main Database with a SQL Query"""
        self.checkingConnection()

        self.model = QSqlQueryModel()
        self.model.setQuery('''
        SELECT Clients.id, Clients.date, Clients.hour, Clients.name, 
        Clients.birthday, Clients.cellphone, Clients.address, City.name, 
        Payment.method, Clients.pollo, Clients.carne, Clients.empanachos, 
        Clients.total, Clients.value FROM Clients JOIN City JOIN Payment
        ON Clients.city_id = City.id AND Clients.payment_id = Payment.id
        ''', self.db)

        self.setModel(self.model)

    def income(self):
        """This function displays the Daily Income results table on its 
        window tab"""
        self.checkingConnection()
        model = QSqlQueryModel()
        model.setQuery('''
        SELECT Clients.id, Clients.date, Clients.hour, Clients.name, 
        (Clients.carne + Clients.pollo) AS empanadas,
        Clients.total, Clients.value FROM Clients''', self.db)
        self.setModel(model)

    def resultadosDiarios(self):
        """This function displays the Daily Results table on its 
        window tab"""
        self.checkingConnection()
        self.model = QSqlQueryModel()
        self.model.setQuery('''SELECT date1, ingresos, compras, gastos,
            (ingresos - compras - gastos) AS Saldo FROM (SELECT date1,
            ingresos, compras, gastos FROM ((SELECT Clients.date AS date1,
            SUM(Clients.value) AS ingresos FROM Clients GROUP BY Clients.date)
            JOIN (SELECT Compras.date AS date2, SUM(Compras.value) AS compras
            FROM Compras GROUP BY Compras.date) JOIN (SELECT Gastos.date AS date3,
            SUM(Gastos.value) AS gastos FROM Gastos GROUP BY Gastos.date)
            ON date1 = date2 AND date2 = date3))''', self.db)
        self.setModel(self.model)

    def resultadosMensuales(self):
        """This function displays the Monthly Results table on its 
        window tab and also gets the table values and save them 
        in a series of lists"""
        self.checkingConnection()
        self.model = QSqlQueryModel()
        self.model.setQuery('''
            SELECT months.name, ingresos, compras, gastos,
            (ingresos - compras - gastos) AS Saldo FROM (
			SELECT month,
            ingresos, compras, gastos FROM ((SELECT Clients.month AS month,
            SUM(Clients.value) AS ingresos FROM Clients GROUP BY Clients.month)
            JOIN (SELECT Compras.month_id AS month2, SUM(Compras.value) AS compras
            FROM Compras GROUP BY Compras.month_id) JOIN (SELECT Gastos.month_id AS month3,
            SUM(Gastos.value) AS gastos FROM Gastos GROUP BY Gastos.month_id)
            ON month = month2 AND month2 = month3)
			) JOIN months ON month=months.id ''', self.db)
        # Set the empty lists
        self.months = []
        self.ingresos = []
        self.compras = []
        self.gastos = []
        self.total = []
        # Save the Query values in each list
        for i in range(self.model.rowCount()):
            # record is the row and value the column
            self.months.append(self.model.record(i).value("name"))
            self.ingresos.append(self.model.record(i).value("ingresos"))
            self.compras.append(self.model.record(i).value("compras"))
            self.gastos.append(self.model.record(i).value("gastos"))
            self.total.append(self.model.record(i).value("Saldo"))

        self.setModel(self.model)
        # Creating the Bar Graph
        self.grafica(self.months)

    def grafica(self, timeList):
        """This function displays the Results Graph 
        in a bar graph with matplotlib and use the
        timeList second parameter as the required 
        timeline in order to set the X axis"""
        n_groups = len(timeList)
        # create plot
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.2
        opacity = 1
        index2 = [x + bar_width for x in index]
        index3 = [x + bar_width for x in index2]
        index4 = [x + bar_width for x in index3]
        rects1 = plt.bar(index, self.ingresos, bar_width,
                         alpha=opacity,
                         color='r',
                         label='Ingresos')

        rects2 = plt.bar(index2, self.compras, bar_width,
                         alpha=opacity,
                         color='yellow',
                         label='Compras')
        rects3 = plt.bar(index3, self.gastos, bar_width,
                         alpha=opacity,
                         color='b',
                         label='Gastos')
        rects4 = plt.bar(index4, self.total, bar_width,
                         alpha=opacity,
                         color='black',
                         label='Saldo')

        plt.xlabel('Línea de tiempo')
        plt.ylabel('Total ($)')
        plt.title('Resultados')
        plt.xticks(index + bar_width, timeList)
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.show()

    def resultadosAnuales(self):
        """This function displays the Annual Results table on its 
        window tab"""
        self.checkingConnection()
        self.model = QSqlQueryModel()
        self.model.setQuery('''SELECT years, ingresos, compras, gastos, 
            (ingresos - compras - gastos) AS Total FROM (
			SELECT years, 
            ingresos, compras, gastos FROM ((SELECT Clients.year AS years, 
            SUM(Clients.value) AS ingresos FROM Clients GROUP BY Clients.year) 
            JOIN (SELECT Compras.year AS year2, SUM(Compras.value) AS compras 
            FROM Compras GROUP BY Compras.year) JOIN (SELECT Gastos.year AS year3, 
            SUM(Gastos.value) AS gastos FROM Gastos GROUP BY Gastos.year) 
            ON years = year2 AND year2 = year3)
			) ''', self.db)
        # Getting the table values
        self.years = []
        self.ingresos = []
        self.compras = []
        self.gastos = []
        self.total = []
        # Save the Query values in each list
        for i in range(self.model.rowCount()):
            # record is the row and value the column
            self.years.append(self.model.record(i).value("years"))
            self.ingresos.append(self.model.record(i).value("ingresos"))
            self.compras.append(self.model.record(i).value("compras"))
            self.gastos.append(self.model.record(i).value("gastos"))
            self.total.append(self.model.record(i).value("Total"))
        self.setModel(self.model)
        # Creating the Bar Graph
        self.grafica(self.years)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Initialize the class with the main window
    tabDatabase = Database(window)
    # Seting the tab where the QTableView is going to be displayed
    tabDatabase.window.tab2.setLayout(tabDatabase.verticalLayout)
    # Showing the Main Database calling its respective function
    tabDatabase.connectDatabase()
    # Connecting the instance button with the desired function
    # in order to refresh the table view
    tabDatabase.showButton.clicked.connect(tabDatabase.connectDatabase)

    revenue = Database(window)
    revenue.window.tab3.setLayout(revenue.verticalLayout)
    revenue.showButton.clicked.connect(revenue.income)
    revenue.income()

    resultados = Database(window)
    resultados.window.tab6.setLayout(resultados.verticalLayout)
    resultados.resultadosDiarios()
    resultados.showButton.clicked.connect(resultados.resultadosDiarios)

    monthlyResults = Database(window)
    monthlyResults.window.tab7.setLayout(monthlyResults.verticalLayout)
    monthlyResults.showButton.clicked.connect(
        monthlyResults.resultadosMensuales)

    annualResults = Database(window)
    annualResults.window.tab8.setLayout(annualResults.verticalLayout)
    annualResults.showButton.clicked.connect(annualResults.resultadosAnuales)

    # Initialize the class with the name of the desired database
    # And also set the tab layout
    compras = Egresos(window, "Compras")
    compras.window.tab4.setLayout(compras.mainLayout)

    gastos = Egresos(window, "Gastos")
    gastos.window.tab5.setLayout(gastos.mainLayout)

    controller = Controller(window)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
