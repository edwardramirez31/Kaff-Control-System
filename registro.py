from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QFormLayout, QLineEdit, QVBoxLayout, QPushButton
import sys


class Registro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bolsa Kaff')
        # crea el objeto layout
        self.mainLayout = QVBoxLayout()
        self.layoutOne = QFormLayout()
        # manipula el layout
        self.layoutOne.addRow('Fecha', QLineEdit())
        self.layoutOne.addRow('NOMBRE', QLineEdit())
        self.layoutOne.addRow('CUMPLEAÑOS', QLineEdit())
        self.layoutOne.addRow('CELULAR', QLineEdit())
        self.layoutOne.addRow('DIRECCIÓN', QLineEdit())
        self.layoutOne.addRow('CIUDAD', QLineEdit())
        self.layoutOne.addRow('MÉTODO DE PAGO', QLineEdit())
        self.mainLayout.addLayout(self.layoutOne)
        # establece o lo agrega a la ventana donde deba ir
        self.setLayout(self.mainLayout)
        self.label = QLabel('PEDIDO', parent=self)
        self.mainLayout.addWidget(self.label)

        # Layout de las empanadas
        self.layoutTwo = QFormLayout()
        self.layoutTwo.addRow('POLLO', QLineEdit())
        self.layoutTwo.addRow('CARNE', QLineEdit())
        self.layoutTwo.addRow('EMPANACHOS', QLineEdit())
        self.layoutTwo.addRow('CANTIDAD EMPANADAS', QLineEdit())
        self.layoutTwo.addRow('VALOR', QLineEdit())
        self.mainLayout.addLayout(self.layoutTwo)
        self.button = QPushButton('LIMPIAR')
        self.button2 = QPushButton('GUARDAR')
        self.button3 = QPushButton('ELIMINAR')
        self.mainLayout.addWidget(self.button)
        self.mainLayout.addWidget(self.button2)
        self.mainLayout.addWidget(self.button3)


app = QApplication(sys.argv)
window = Registro()
window.show()
sys.exit(app.exec_())
