from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


def on_button_clicked():
    alert = QMessageBox()
    alert.setText('Has pulsado un botón, INSENSATO!')
    alert.exec_()


qApp = QApplication([])

dark_palette = QPalette()

dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
dark_palette.setColor(QPalette.WindowText, Qt.white)
dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
dark_palette.setColor(QPalette.ToolTipText, Qt.white)
dark_palette.setColor(QPalette.Text, Qt.white)
dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ButtonText, Qt.white)
dark_palette.setColor(QPalette.BrightText, Qt.red)
dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
dark_palette.setColor(QPalette.HighlightedText, Qt.black)

qApp.setPalette(dark_palette)

qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

window = QWidget()
buttonTop = QPushButton('Top')
buttonBottom = QPushButton('Bottom')
buttonTop.clicked.connect(on_button_clicked)
buttonBottom.clicked.connect(on_button_clicked)
layout = QVBoxLayout()
layout.addWidget(buttonTop)
layout.addWidget(buttonBottom)
window.setLayout(layout)
window.show()
qApp.exec_()
