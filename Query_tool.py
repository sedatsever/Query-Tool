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
        self.server_combo.currentIndexChanged.connect(self.list_db)
        self.connect_button.clicked.connect(self.connect)
        self.generate_button.clicked.connect(self.generate)
        self.run_button.clicked.connect(self.run)

    def list_db(self):
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

        dbcursor.execute("select name from sys.databases")

        dbrows = dbcursor.fetchall()

        databases = [row.name for row in dbrows]

        self.db_combo.addItems(databases)

    def connect(self):
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

        global cursor
        cursor = connection.cursor()

        for i in self.gentables():
            self.table_combo.addItems(i)

        self.columns_combo.addItems([column[0] for column in self.table_combo.currentText.description])

        self.operator_combo.addItems('=','>','<','>=','<=','NOT EQUAL TO','IN','LIKE')

    def generate(self):
        pass

    def run(self):
        pass

    def gentables(self):
        for row in cursor.tables():
            yield row.table_name


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