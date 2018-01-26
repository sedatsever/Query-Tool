import sys
import pyodbc
from PyQt5 import QtGui, QtWidgets, QtCore,  uic
import xml.etree.ElementTree as ET

etree = ET.parse(r'C:\Users\tradesoft\PycharmProjects\Query Tool\.idea\environments.xml')

eroot = etree.getroot()

class MyWindow(QtWidgets.QDialog):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('Smart_query_tool.ui', self)

        self.show()

        #Fill server combo
        self.server_combo.addItems([elem.attrib['name'] for elem in eroot])

        #Connect object functions
        self.server_combo.currentTextChanged.connect(self.list_db)
        self.connect_button.clicked.connect(self.connect)
        self.table_combo.activated.connect(self.list_columns)
        self.generate_button.clicked.connect(self.generate)
        self.run_button.clicked.connect(self.run)

    def list_db(self):
        self.db_combo.clear()
        db_connection = pyodbc.connect('Driver=SQL Server;''Server={a};''Database=gtpbrdb;''uid={b};pwd={c};'.format(
                                                                                  a = '{d}'.format(d = eroot.findall(
                                                                                      ".//*[@name='{e}']/connection".format(
                                                                                          e = self.server_combo.currentText()))[0].text),
                                                                                  b = '{f}'.format(f = eroot.findall(
                                                                                      ".//*[@name='{g}']/id".format(
                                                                                          g = self.server_combo.currentText()))[0].text),
                                                                                  c = '{h}'.format(h = eroot.findall(
                                                                                      ".//*[@name='{i}']/pass".format(
                                                                                          i = self.server_combo.currentText()))[0].text)))

        dbcursor = db_connection.cursor()

        dbcursor.execute("select name from sys.databases (NOLOCK)")

        dbrows = dbcursor.fetchall()

        self.db_combo.addItems([row.name for row in dbrows])

        #db_connection.close()

    def connect(self):
        global connection
        connection = pyodbc.connect('Driver=SQL Server;''Server={a};''Database={b};''uid={c};pwd={d};'.format(
                                                                                  a='{e}'.format(e= eroot.findall(
                                                                                      ".//*[@name='{f}']/connection".format(
                                                                                          f=self.server_combo.currentText()))[0].text),
                                                                                  b = self.db_combo.currentText(),
                                                                                  c = '{g}'.format(g = eroot.findall(
                                                                                      ".//*[@name='{h}']/id".format(
                                                                                          h = self.server_combo.currentText()))[0].text),
                                                                                  d = '{i}'.format(i=eroot.findall(
                                                                                      ".//*[@name='{j}']/pass".format(
                                                                                          j = self.server_combo.currentText()))[0].text)))

        cursor = connection.cursor()

        # while True:
        #     row=cursor.fetchone()
        #     if not row:
        #         break
        #     self.table_combo.addItems(i)

        # tables=[row.table_name for row in cursor.tables()]

        # for row in cursor.tables():
        #     tables.append(row.table_name)
        #
        self.table_combo.clear()

        self.table_combo.addItems([row.table_name for row in cursor.tables()])

        # columns=[]




        # for i in self.gentables():
        #     self.table_combo.addItems(i)

        # self.columns_combo.addItems([column[0] for column in self.table_combo.currentText.description])
        #
        # self.operator_combo.addItems('=','>','<','>=','<=','NOT EQUAL TO','IN','LIKE')

    def list_columns(self):
        self.columns_combo.clear()

        tcursor = connection.cursor()

        tcursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS (NOLOCK) WHERE TABLE_NAME = N'{table_name}'".format(table_name=self.table_combo.currentText()))

        tresults = tcursor.fetchall()

        self.columns_combo.addItems([row.COLUMN_NAME for row in tresults])

        self.operator_combo.addItems(['=', '>', '<', '>=', '<=', 'NOT EQUAL', 'IN', 'LIKE'])

    def generate(self):
        self.q_textEdit.clear()
        self.q_textEdit.setText('SELECT')

    def run(self):
        pass

    def gentables(self):
        pass
        #for row in cursor.tables():
         #   yield row.table_name


# class Session:
#
#     def __init__(self, server, db, uid, pwd):
#         self.server=server
#         self.db=db
#         self.uid=uid
#         self.pwd=pwd
#
#     def set_server(self,server):
#         self.server=server
#
#     def set_db(self,db):
#         self.db=db
#
#     def connect(self):
#         return('Driver=SQL Server;''Server={a};''Database={b};''uid={c};pwd={d};'.format(a='212.252.33.21', b='gtpbrdb',
#                                                                                        c='GTPDB', d='GTPDB'))

    #def fill_db(self):


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())