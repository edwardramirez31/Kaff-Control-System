from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QFormLayout, QLineEdit, QVBoxLayout, QPushButton, QTabWidget
import sys
from PyQt5.QtCore import *


class Registro(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bolsa Kaff')
        # crea el objeto layout
        # self.mainLayout = QVBoxLayout()
        self.createTabs()
        self.tab1Content()

    def createTabs(self):
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.addTab(self.tab1, "Registro")
        self.addTab(self.tab2, "Base de Datos")
        self.tab1Layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1Layout)

    def tab1Content(self):
        # Client Data
        self.layoutOne = QFormLayout()
        self.layoutOne.addRow('Fecha', QLineEdit())
        self.layoutOne.addRow('NOMBRE', QLineEdit())
        self.layoutOne.addRow('CUMPLEAÑOS', QLineEdit())
        self.layoutOne.addRow('CELULAR', QLineEdit())
        self.layoutOne.addRow('DIRECCIÓN', QLineEdit())
        self.layoutOne.addRow('CIUDAD', QLineEdit())
        self.layoutOne.addRow('MÉTODO DE PAGO', QLineEdit())
        self.tab1Layout.addLayout(self.layoutOne)
        # LABEL
        self.label = QLabel('PEDIDO', parent=self)
        self.label.setStyleSheet(
            "background: black; color: white;")
        self.label.setAlignment(Qt.AlignCenter)
        self.tab1Layout.addWidget(self.label)
        # Layout Cantidad de Empanadas
        self.layoutTwo = QFormLayout()
        self.polloWidget = QLineEdit()
        self.layoutTwo.addRow('POLLO', self.polloWidget)
        self.layoutTwo.addRow('CARNE', QLineEdit())
        self.layoutTwo.addRow('EMPANACHOS', QLineEdit())
        self.layoutTwo.addRow('CANTIDAD EMPA.', QLineEdit())
        self.layoutTwo.addRow('VALOR', QLineEdit())
        self.tab1Layout.addLayout(self.layoutTwo)
        # Buttons
        self.button = QPushButton('GUARDAR')
        self.button2 = QPushButton('LIMPIAR')
        self.button2.clicked.connect(self.tab1Buttons)

        self.button3 = QPushButton('ELIMINAR')
        self.tab1Layout.addWidget(self.button)
        self.tab1Layout.addWidget(self.button2)
        self.tab1Layout.addWidget(self.button3)

    def tab1Buttons(self):
        self.polloWidget.setText("")


app = QApplication(sys.argv)
window = Registro()
window.show()
sys.exit(app.exec_())
