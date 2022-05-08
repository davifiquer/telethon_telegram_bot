import asyncio

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtWidgets
from PyQt6.QtCore import *
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUiType
import sys
from os import path
from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession
import main_view
import pickle

# FORM_CLASS, _ = loadUiType(path.join(path.dirname('__file__'), 'main_view.ui'))

class Main(QMainWindow, main_view.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.DEFAULT_CONFIGS()

    def DEFAULT_CONFIGS(self):
        self.txtlogs.setReadOnly(True)
        try:
            with open('user_list.pkl', 'rb') as f:
                userlist = pickle.load(f)
                for user in userlist:
                    rowcount = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(rowcount)
                    self.tableWidget.setItem(rowcount, 0, QTableWidgetItem(user['name']))
                    self.tableWidget.setItem(rowcount, 1, QTableWidgetItem(user['user']))
                self.txtlogs.appendPlainText('Default user list loaded!')
        except FileNotFoundError:
            self.txtlogs.appendPlainText('Default user list not found!')

    def Handel_Buttons(self):
        self.btnadduser.clicked.connect(self.ADD_USER)
        self.btnsend.clicked.connect(self.SEND_MESSAGE)
        self.btnremoveuser.clicked.connect(self.REMOVE_USER)
        self.btnsavelist.clicked.connect(self.SAVE_LIST)

    # Save user list
    def SAVE_LIST(self):
        list_data = []
        rowcount = self.tableWidget.rowCount()
        if rowcount > 0:
            for i in range(rowcount):
                name = self.tableWidget.item(i, 0).text()
                user = self.tableWidget.item(i, 1).text()
                data = {'name': name, 'user': user}
                list_data.append(data)
        with open('user_list.pkl', 'wb') as f:
            pickle.dump(list_data, f)
        self.txtlogs.appendPlainText('User list saved successfully')
        self.txtname.setFocus()

    # Removing the selected user on the table
    def REMOVE_USER(self):
        rowselected = self.tableWidget.currentRow()
        model = self.tableWidget.model()
        model.removeRow(rowselected)

    # Sending message
    def SEND_MESSAGE(self):
        api_id = int(self.txtAppId.text())
        api_hash = str(self.txthashcode.text())
        with open('auth_user.txt', 'r') as f:
            session = f.readlines()
            session = str(session[0])
        client = TelegramClient(StringSession(session), api_id, api_hash)
        client.start()
        for i in range(self.tableWidget.rowCount()):
            try:
                user = self.tableWidget.item(i, 1).text()
                client.send_message(user, self.txtmessage.toPlainText())
                self.txtlogs.appendPlainText('Message sent to user ' + user)
            except ValueError as err:
                self.txtlogs.appendPlainText('Error sending message to user ' + user +
                                             '\nError: ' + str(err))

    # Adding a new user
    def ADD_USER(self):
        if (self.txtname.text() == '') or (self.txttelegramid.text() == ''):
            self.txtlogs.appendPlainText('User or Telegram ID is blank')
        else:
            res = self.CHECK_USER()
            if res:
                rowcount = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowcount)
                self.tableWidget.setItem(rowcount, 0, QTableWidgetItem(self.txtname.text()))
                self.tableWidget.setItem(rowcount, 1, QTableWidgetItem(self.txttelegramid.text()))
                self.txtlogs.appendPlainText('User @' + self.txttelegramid.text() + ' has been added!')
                self.txtname.setText('')
                self.txttelegramid.setText('')
            else:
                self.txtlogs.appendPlainText('User @' + self.txttelegramid.text() + ' has already been added!')

    # checking if the user already exists in the list
    def CHECK_USER(self):
        result = True
        rowcount = self.tableWidget.rowCount()
        if rowcount > 0:
            for row in range(rowcount):
                if self.tableWidget.item(row, 1).text() == self.txttelegramid.text():
                    result = False
                    break
        return result

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
