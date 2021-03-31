import sys
from puyadl.scraper import Scraper
from PySide6.QtWidgets import *
from types import SimpleNamespace

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

        self.button.clicked.connect(self.query)

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

    def query(self):
        print("Fine")
        
        args = SimpleNamespace()
        args.quality = self.cb.currentText()
        args.episodes = self.eps.text() if self.epsCheckBox.isChecked() else None
        args.all = False # to be implemented

        scraper = Scraper(args)
        scraper.request(self.title.text())
        titles = scraper.list_titles()
        print(titles)
        scraper.filter(titles[0])
        scraper.downloadFirstItem()
        scraper.download()

def initialize():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())