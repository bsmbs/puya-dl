from PySide6.QtWidgets import QMessageBox

def showSimpleDialog(message, details=""):
    box = QMessageBox()
    box.setIcon(QMessageBox.Question)

    box.setText(message)
    box.setWindowTitle("puya-dl")
    box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
    
    return box.exec_()