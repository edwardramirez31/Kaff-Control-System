from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout, QLineEdit, QPushButton, QTabWidget, QComboBox, QCalendarWidget
import sys
# from PyQt5.QtCore import *
from datetime import date
from sqlite3 import connect


class Registro(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bolsa Kaff')
        self.createTabs()
        self.createLabels()
        self.createLinesWidgets()
        self.createButtons()

    def createTabs(self):
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.addTab(self.tab1, "Registro")
        self.addTab(self.tab2, "Base de Datos")

    def createLabels(self):
        # Client Data
        self.grid = QGridLayout()
        self.labelWidgets = {
            "FECHA": (0, 0),
            "NOMBRE": (1, 0),
            "CUMPLEAÑOS": (2, 0),
            "CELULAR": (3, 0),
            "DIRECCIÓN": (4, 0),
            "CIUDAD": (5, 0),
            "MÉTODO DE PAGO": (6, 0),
            "PEDIDO": (7, 0, 1, 3),
            "POLLO": (8, 0),
            "CARNE": (9, 0),
            "EMPANACHOS": (10, 0),
            "CANTIDAD DE EMPA": (11, 0),
            "VALOR": (12, 0)
        }
        for labelName, position in self.labelWidgets.items():
            if len(position) == 4:
                self.label = QLabel(labelName)
                self.label.setStyleSheet(
                    "background-color: gray; color: gray")
                self.grid.addWidget(
                    self.label, position[0], position[1], position[2], position[3])
            else:
                self.label = QLabel(labelName)
                self.grid.addWidget(
                    self.label, position[0], position[1])

    def createLinesWidgets(self):

        lineEditWidgets = {
            "FECHA": (0, 1, 1, 2),
            "NOMBRE": (1, 1, 1, 2),
            "CUMPLEAÑOS": (2, 1),
            "CELULAR": (3, 1, 1, 2),
            "DIRECCIÓN": (4, 1, 1, 2),
            "CIUDAD": (5, 1, 1, 2),
            "POLLO": (8, 1, 1, 2),
            "CARNE": (9, 1, 1, 2),
            "EMPANACHOS": (10, 1, 1, 2),
            "CANTIDAD DE EMPA": (11, 1, 1, 2),
            "VALOR": (12, 1)

        }
        self.lineEditWidgets = {}
        for widgetName, position in lineEditWidgets.items():
            if len(position) == 2:
                self.lineEdit = QLineEdit()
                self.grid.addWidget(self.lineEdit, position[0], position[1])
                self.lineEditWidgets[widgetName] = self.lineEdit
            else:
                self.lineEdit = QLineEdit()
                self.grid.addWidget(
                    self.lineEdit, position[0], position[1], position[2], position[3])
                self.lineEditWidgets[widgetName] = self.lineEdit

        # Getting the current date
        today = str(date.today())
        self.lineEditWidgets["FECHA"].setText(today)

    def createButtons(self):
        buttons = {
            "Browse": (2, 2),
            "CALCULATE": (12, 2),
            "SAVE": (13, 0),
            "CLEAR": (13, 1),
            "DELETE": (13, 2)
        }
        self.buttons = {}
        for widgetName, position in buttons.items():
            self.button = QPushButton(widgetName)
            self.grid.addWidget(self.button, position[0], position[1])
            self.buttons[widgetName] = self.button
        self.tab1.setLayout(self.grid)

        # Buttons Signals
        self.buttons["CLEAR"].clicked.connect(self.clearAll)
        self.buttons["Browse"].clicked.connect(self.calendar)
        self.buttons["CALCULATE"].clicked.connect(self.calculate)

        # Creating the Combo Box Button
        self.combo = QComboBox()
        self.combo.addItems(['Efectivo', 'Nequi'])
        self.grid.addWidget(self.combo, 6, 1, 1, 2)

    def clearAll(self):
        for widgetName, lineWidget in self.lineEditWidgets.items():
            if widgetName == "FECHA":
                pass
            else:
                lineWidget.setText("")

    def calculate(self):
        self.pollo = self.lineEditWidgets["POLLO"].text()
        self.carne = self.lineEditWidgets["CARNE"].text()
        self.empanachos = self.lineEditWidgets["EMPANACHOS"].text()
        self.Total = int(self.pollo) + int(self.carne)+int(self.empanachos)
        self.lineEditWidgets["CANTIDAD DE EMPA"].setText(str(self.Total))
        if self.Total > 5:
            self.value = 2300 * self.Total
        else:
            self.value = 2500 * self.Total
        self.lineEditWidgets["VALOR"].setText(str(self.value))

    def calendar(self):
        self.cal = QCalendarWidget()
        self.cal.setWindowTitle("Get Birthday")
        self.cal.show()
        self.cal.clicked.connect(self.dateB)

    def dateB(self):
        self.date = self.cal.selectedDate()
        self.lineEditWidgets["CUMPLEAÑOS"].setText(
            self.date.toString("yyyy-MM-dd"))

    def save(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = Registro()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
