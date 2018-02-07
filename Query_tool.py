import sys, csv, io
import decimal
import pyodbc
from PyQt5 import QtGui, QtWidgets, QtCore,  uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET

etree = ET.parse(r'config.xml')

eroot = etree.getroot()

class MyWindow(QtWidgets.QDialog):
    def __init__(self, fn=None,parent=None):
        super(MyWindow, self).__init__(parent,\
        flags = Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint )
        uic.loadUi('query_tool_ui.ui', self)

        self.show()

        #Fill server combo
        self.server_combo.addItems([elem.attrib['name'] for elem in eroot])

        self.d_tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)

        self.makepassive()

        self.cnxn_error_label.hide()
        self.qry_error_label.hide()
        self.cnxn_label.hide()

        # self.q_textEdit.setText('Please connect to a server to generate or manually input a query')

        #Connect object functions
        self.server_combo.activated.connect(self.list_db)
        self.connect_button.clicked.connect(self.connect)
        self.table_combo.activated.connect(self.list_columns)
        self.generate_button.clicked.connect(self.generate)
        self.run_button.clicked.connect(self.run)
        self.d_tableWidget.customContextMenuRequested.connect(self.openMenu)

    def list_db(self):
        self.cnxn_error_label.hide()
        self.db_combo.clear()

        try:
            db_connection = pyodbc.connect('Driver=SQL Server;''Server={a};''Database={j};''uid={b};pwd={c};'.format(
                                                                                  a = '{d}'.format(d = eroot.findall(
                                                                                      ".//*[@name='{e}']/server".format(
                                                                                          e = self.server_combo.currentText()))[0].text),
                                                                                  b = '{f}'.format(f = eroot.findall(
                                                                                      ".//*[@name='{g}']/id".format(
                                                                                          g = self.server_combo.currentText()))[0].text),
                                                                                  j = '{k}'.format(k = eroot.findall(
                                                                                      ".//*[@name='{l}']/db".format(
                                                                                          l = self.server_combo.currentText()))[0].text),
                                                                                  c = '{h}'.format(h = eroot.findall(
                                                                                      ".//*[@name='{i}']/pass".format(
                                                                                          i = self.server_combo.currentText()))[0].text)),timeout=3)
        except:
            self.cnxn_error_label.show()
            self.cnxn_label.hide()
            self.makepassive()

        else:
            dbcursor = db_connection.cursor()

            dbcursor.execute("select name from sys.databases (NOLOCK)")

            dbrows = dbcursor.fetchall()

            self.db_combo.addItems([row.name for row in dbrows])

            self.cnxn_error_label.hide()

    def connect(self):
        global connection

        try:
            connection = pyodbc.connect('Driver=SQL Server;''Server={a};''Database={b};''uid={c};pwd={d};'.format(
                                                                                  a='{e}'.format(e= eroot.findall(
                                                                                      ".//*[@name='{f}']/server".format(
                                                                                          f=self.server_combo.currentText()))[0].text),
                                                                                  b = self.db_combo.currentText(),
                                                                                  c = '{g}'.format(g = eroot.findall(
                                                                                      ".//*[@name='{h}']/id".format(
                                                                                          h = self.server_combo.currentText()))[0].text),
                                                                                  d = '{i}'.format(i=eroot.findall(
                                                                                      ".//*[@name='{j}']/pass".format(
                                                                                          j = self.server_combo.currentText()))[0].text)))
        except:
            self.cnxn_error_label.show()
            self.cnxn_label.hide()
            self.makepassive()

        else:
            global cursor
            cursor = connection.cursor()

            self.table_combo.clear()

            self.table_combo.addItems([row.table_name for row in cursor.tables()])

            self.q_textEdit.setEnabled(True)
            self.table_combo.setEnabled(True)
            self.columns_combo.setEnabled(True)
            self.operator_combo.setEnabled(True)
            self.cr_lineEdit.setEnabled(True)
            self.generate_button.setEnabled(True)
            self.run_button.setEnabled(True)

            self.qry_error_label.hide()
            self.cnxn_label.show()
            # self.q_textEdit.clear()

    def list_columns(self):
        self.columns_combo.clear()

        tcursor = connection.cursor()

        tcursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS (NOLOCK) WHERE TABLE_NAME = N'{table_name}'".format(table_name=self.table_combo.currentText()))

        tresults = tcursor.fetchall()

        self.columns_combo.addItems([row.COLUMN_NAME for row in tresults])

        self.operator_combo.addItems(['=', 'LIKE', 'IN', '<>', '>', '<', '>=', '<='])

    def generate(self):
        self.q_textEdit.clear()
        if self.operator_combo.currentText()=='LIKE':
            self.q_textEdit.setText("SELECT * FROM {table} WHERE {column} {operator} '{a}{criteria}{a}'".format(
                table=self.table_combo.currentText(),
                column=self.columns_combo.currentText(),
                operator=self.operator_combo.currentText(),
                a='%',
                criteria=self.cr_lineEdit.text()))
        elif any([self.operator_combo.currentText()=='=' , self.operator_combo.currentText()=='<>']) and self.cr_lineEdit.text().isdigit()==False:
            self.q_textEdit.setText("SELECT * FROM {table} (NOLOCK)  WHERE {column} {operator} '{criteria}'".format(table=self.table_combo.currentText(),
                                                                                                    column=self.columns_combo.currentText(),
                                                                                                    operator=self.operator_combo.currentText(),
                                                                                                    criteria=self.cr_lineEdit.text()))
        else:
            self.q_textEdit.setText("SELECT * FROM {table} (NOLOCK) WHERE {column} {operator} {criteria}".format(table=self.table_combo.currentText(),
                                                                                                    column=self.columns_combo.currentText(),
                                                                                                    operator=self.operator_combo.currentText(),
                                                                                                    criteria=self.cr_lineEdit.text()))

    def run(self):
        try:
            cursor.execute(self.q_textEdit.toPlainText())

        except:
            self.qry_error_label.show()

        else:
            qresults = cursor.fetchall()

            row_count=0

            for rows in iter(qresults):
                row_count+=1

            self.d_tableWidget.setRowCount(row_count)

            column_count = len([column[0] for column in cursor.description])

            self.d_tableWidget.setColumnCount(column_count)

            self.d_tableWidget.setHorizontalHeaderLabels([column[0] for column in cursor.description])

            for row in range(row_count):
                for column in range(column_count):
                    self.d_tableWidget.setItem(row, column, QTableWidgetItem(str(qresults[row][column])))

            self.d_tableWidget.resizeColumnsToContents()
            self.qry_error_label.hide()

    def openMenu(self,position):
        menu = QMenu()
        copydataAction = menu.addAction("Copy Data")
        copyheadersAction = menu.addAction("Copy Headers")
        action = menu.exec_(self.d_tableWidget.mapToGlobal(position))
        if action == copydataAction:
            self.copydata()
        if action == copyheadersAction:
            self.copyheaders()

    def copydata(self):
        selection = self.d_tableWidget.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream).writerows(table)
            QApplication.clipboard().setText(stream.getvalue())

    def copyheaders(self):
        headers_lst=[column[0] for column in cursor.description]
        headers_str=",".join(headers_lst)
        QApplication.clipboard().setText(headers_str)

    def makepassive(self):
        self.q_textEdit.setEnabled(False)
        self.table_combo.setEnabled(False)
        self.columns_combo.setEnabled(False)
        self.operator_combo.setEnabled(False)
        self.cr_lineEdit.setEnabled(False)
        self.generate_button.setEnabled(False)
        self.run_button.setEnabled(False)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
