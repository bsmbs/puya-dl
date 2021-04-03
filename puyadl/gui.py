import sys
from PySide6.QtWidgets import *
from types import SimpleNamespace

from puyadl.scraper import Scraper
from puyadl.dialog import showSimpleDialog, showErrorDialog


class Form(QWidget):
    
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("puya-dl")
        self.resize(440, 210)

        # TopLayout (Title LineEdit + Quality ComboBox)
        self.title = QLineEdit()

        self.label = QLabel("Quality:")

        self.cb = QComboBox()
        self.cb.addItems(["1080p", "720p", "Unspecified"])

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.cb)

        self.eps = QLineEdit()
        self.eps.setPlaceholderText("Episodes")
        self.eps.setDisabled(True)

        self.epsCheckBox = QCheckBox("Specify episodes to download")
        self.epsCheckBox.stateChanged.connect(self.checkboxEvent)

        self.confirmCheckbox = QCheckBox("Don't ask for confirmation")

        self.epsGroupLayout = QVBoxLayout()

        self.epsLayout = QHBoxLayout()
        self.epsLayout.addWidget(self.epsCheckBox)
        self.epsLayout.addWidget(self.eps)

        self.epsGroupLayout.addLayout(self.epsLayout)
        self.epsGroupLayout.addWidget(self.confirmCheckbox)

        self.epsGroup = QGroupBox()
        self.epsGroup.setLayout(self.epsGroupLayout)

        self.button = QPushButton("Download")

        self.progress = QProgressBar()
        self.progress.setTextVisible(True)

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
        if len(self.title.text()) == 0:
            showErrorDialog("No query specified")
            return

        self.progress.setValue(0)
        
        args = SimpleNamespace()
        quality = self.cb.currentText()
        args.quality = quality if quality != "Unspecified" else ""
        args.episodes = self.eps.text() if self.epsCheckBox.isChecked() else None
        args.all = False # to be implemented

        self.progress.setFormat("Fetching results from nyaa...")
        self.progressTo(0, 25)
        scraper = Scraper(args)
        scraper.request(self.title.text()) # TODO exception handling

        if len(scraper.items) == 0:
            showErrorDialog("No results found")
            self.cancel()
            return

        self.progress.setFormat("Parsing results...")
        self.progressTo(25, 50)

        titles = scraper.list_titles()
        if len(titles) > 1:
            choice = self.choiceDialog(titles)
            result = choice.exec_()
            if result == 0:
                print("No choice")
                self.progress.setValue(0)
                self.cancel()
                return
            else:
                index = result - 1
        else:
            index = 0

        self.progress.setFormat("Opening magnet links...")
        scraper.filter(titles[index])
        scraper.downloadFirstItem()
        if self.confirmCheckbox.isChecked() or showSimpleDialog("Your BitTorrent client should open with the first file. Hit OK to continue.") == QMessageBox.Ok:
            self.progressTo(50, 100)
            scraper.download()
            self.progress.setFormat("Your BitTorrent client should open.")
        else:
            self.cancel()

    def cancel(self):
        self.progress.setFormat("Ready")
        self.progress.setValue(0)

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