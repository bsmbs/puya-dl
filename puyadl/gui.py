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

        self.button = QPushButton("Search")

        self.progress = QProgressBar()

        layout = QVBoxLayout(self)
        layout.addLayout(self.topLayout)
        layout.addWidget(self.epsGroup)

        layout.addStretch(1)
        layout.addWidget(self.button)
        layout.addWidget(self.progress)

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

    def choiceDialog(self, titles):
        dialog = QDialog()
        dialog.resize(260, 260)
        vbox = QVBoxLayout(dialog)

        label = QLabel("Multiple titles have been found. Please select which one to download.")
        btnGroup = QButtonGroup(vbox)

        vbox.addWidget(label)

        buttons = []

        for i, title in enumerate(titles):
            button = QRadioButton(title)
            btnGroup.addButton(button)
            btnGroup.setId(button, i)

            vbox.addWidget(button)
            buttons.append(button)

        buttons[0].setChecked(True)

        hbox = QHBoxLayout()
        cancel = QPushButton("Cancel")
        ok = QPushButton("Confirm")

        hbox.addWidget(cancel)
        hbox.addWidget(ok)

        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        cancel.clicked.connect(lambda: dialog.reject())
        ok.clicked.connect(lambda: self.dialogClose(dialog, btnGroup))
        
        dialog.setWindowTitle("puya-dl")
        dialog.setModal(True)

        return dialog

    def dialogClose(self, dialog, group):
        dialog.done(group.checkedId()+1) # +1 because 0 means no choice at all

    def query(self):
        self.progress.setValue(0)
        
        args = SimpleNamespace()
        quality = self.cb.currentText()
        args.quality = quality if quality != "Unspecified" else ""
        args.episodes = self.eps.text() if self.epsCheckBox.isChecked() else None
        args.all = False # to be implemented

        self.progressTo(0, 25)
        scraper = Scraper(args)
        scraper.request(self.title.text()) # TODO exception handling
        self.progressTo(25, 50)

        titles = scraper.list_titles()
        if len(titles) > 1:
            choice = self.choiceDialog(titles)
            result = choice.exec_()
            if result == 0:
                print("No choice")
                self.progress.setValue(0)
                return
            else:
                index = result - 1
        else:
            index = 0

        self.progressTo(50, 100)
        scraper.filter(titles[index])
        scraper.downloadFirstItem()
        scraper.download()

    def progressTo(self, start, to):
        completed = start
        while completed < to:
            completed += 0.0001
            self.progress.setValue(completed)

def initialize():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())