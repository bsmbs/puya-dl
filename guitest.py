import sys
from main import req, list_titles, filter, download
from PySide6.QtWidgets import *

class Form(QWidget):
    
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("puya-dl")
        self.resize(330, 330)

        # TopLayout (Title LineEdit + Quality ComboBox)
        self.title = QLineEdit("Jujutsu Kaisen")

        self.label = QLabel("Quality:")

        self.cb = QComboBox()
        self.cb.addItems(["1080p", "720p", "Unspecified"])
        self.cb.currentIndexChanged.connect(self.change)

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.cb)

        self.button = QPushButton("Download")

        self.eps = QLineEdit()
        self.eps.setPlaceholderText("Episodes")
        self.eps.setDisabled(True)

        self.epsCheckBox = QCheckBox("Specify episodes to download")
        self.epsCheckBox.stateChanged.connect(self.checkboxEvent)

        self.epsLayout = QHBoxLayout()
        self.epsLayout.addWidget(self.epsCheckBox)
        self.epsLayout.addWidget(self.eps)

        self.epsGroup = QGroupBox()
        self.epsGroup.setLayout(self.epsLayout)

        layout = QVBoxLayout(self)
        layout.addLayout(self.topLayout)
        layout.addWidget(self.epsGroup)

        layout.addStretch(1) ######
        layout.addWidget(self.button)

        self.button.clicked.connect(self.request)

    def checkboxEvent(self, state):
        if state == 0:
            self.eps.setDisabled(True)
        else:
            self.eps.setDisabled(False)

    def change(self, i):
        print("Current index is", self.cb.currentText())

    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        
        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # msg.buttonClicked.connect(msgbtn)

        retval = msg.exec_()

    def request(self):
        items = req(self.title.text(), False, self.cb.currentText())
        titles = list_titles(items)

        if self.epsCheckBox.isChecked():
            filtered = filter(items, titles[0], self.eps.text())
        else:
            filtered = filter(items, titles[0], False)
        download(filtered, False)
        print(titles)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())