import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi
from SSHLogEntry import SSHLogEntry as SSH
from string_to_dict import create_dict_list, create_list_from_file
from get_ipv4s_from_log import get_ipv4s_from_log
from create_SSH_log_journal import create_journal as cre
from HTTPLogEntry import HTTPLogEntry as HTTP
from log_browser import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.listOfLogs.clicked.connect(self.updateLabels)
        self.comboBoxSSHOrHTTP.addItems(["HTTP", "SSH"])
        self.comboBoxSSHOrHTTP.currentIndexChanged.connect(self.updateLabelTypes)
        self.PathButton.clicked.connect(lambda: self.fillList(file_name=self.pathInput.toPlainText()))
    def connectSignalsSlots(self):
        ...

    def fillList(self, file_name):
        self.listOfLogs.clear()
        if file_name == "":
            QMessageBox.warning(self, "Warning", "Please enter a file name")
            return
        for log in cre(file_name):
            self.listOfLogs.addItem(log._raw_desc)
    def updateLabels(self):
        selected_item = self.listOfLogs.currentItem()
        if selected_item is not None:
            log=SSH(selected_item.text())
            self.labelRemoteHost.setText(log.pid)
            self.labelDate.setText(f"{log.month} {log.day}")
            self.labelTime.setText(log.time)
            self.labelTimezone.setText(log.username)
            self.labelStatusCode.setText(log.get_messege_type())
        else:
            self.labelDescription.setText("")
    def updateLabelTypes(self):
        selected_item = self.comboBoxSSHOrHTTP.currentText()
        if selected_item is not None and selected_item == "HTTP":
            self.labelDateRemoteHostL.setText("Remote Host")
            self.labelDateL.setText("Date")
            self.labelTimeL.setText("Time")
            self.labelTimezoneL.setText("Timezone")
            self.labelStatusCodeL.setText("Status Code")
            self.labelMethodL.setText("Method")
            self.labelResourceL.setText("Resource")
            self.labelSizeL.setText("Size")
        else:
            self.labelDateRemoteHostL.setText("Pid")
            self.labelDateL.setText("Date")
            self.labelTimeL.setText("Time")
            self.labelTimezoneL.setText("User")
            self.labelStatusCodeL.setText("Type")
            self.labelMethodL.setText("")
            self.labelResourceL.setText("")
            self.labelSizeL.setText("")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())