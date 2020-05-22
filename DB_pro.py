#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import requests
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import QtSql
import sqlite3
import os
import datetime

sqliteConnection = sqlite3.connect('products.sqlite', timeout=300)

class MagnitParser():
    URL = 'https://magnit.ru/promo/'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63',
              'accept': '*/*'
              }
    def __init__(self):
        pass
    def get_html(self, url, params=None):
        r = requests.get(url, headers=MagnitParser.HEADERS, params=params)
        return r
    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('a', class_='card-sale')
        products = []
        date = datetime.datetime.now()
        date = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
        for item in items:
            prod_name = item.find('div', class_='card-sale__title')
            prod_price_int = item.find('span', class_='label__price-integer')
            prod_price_dec = item.find('span', class_='label__price-decimal')
            if ((prod_name is not None) and (prod_price_int is not None) and (prod_price_dec is not None)):
                products.append({
                    'title': prod_name.get_text(),
                    'price_int': prod_price_int.get_text(),
                    'price_dec': prod_price_dec.get_text(),
                    'shop_name': "Магнит",
                    'time': date
                })
        return products
    def parse(self):
        html = self.get_html(MagnitParser.URL)
        if (html.status_code == 200):
            prods = self.get_content(html.text)
            return prods

class AuchanParser():
    URL1 = 'https://www.auchan.ru/pokupki/eda/rasprodazha.html'
    URL2 = 'https://www.auchan.ru/pokupki/kosmetika/akcii-i-skidki.html'
    URL3 = 'https://www.auchan.ru/pokupki/hoztovary/akcii-i-skidki.html'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63',
              'accept': '*/*'
              }
    def __init__(self):
        pass
    def get_html(self, url, params=None):
        r = requests.get(url, headers=AuchanParser.HEADERS, params=params)
        return r
    def get_pages_count(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find('ul', class_ ='pagination__list pagination__list_hidden')
        a = a.find_all('a')
        a = a[-1]
        a = a.get_text()
        a = a.replace(' ','')
        count = int(a)
        return count
    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='products__item-inner')
        products = []
        date = datetime.datetime.now()
        date = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
        for item in items:
            prod_name = item.find('a', class_='products__item-link')
            prod_price_int = item.find('span', class_='price-val')
            if ((prod_name is not None) and (prod_price_int is not None) and (prod_name.get_text()[0] == '\n')):
                products.append({
                    'title': prod_name.get_text()[1:],
                    'price_int': prod_price_int.get_text(),
                    'price_dec': '00',
                    'shop_name': "Ашан",
                    'time': date
                })
        return products
    def parse(self):
        html = self.get_html(AuchanParser.URL1)
        if (html.status_code == 200):
            l = self.get_pages_count(html.text)
            prods = []
            for i in range(l):
                page = i + 1
                html = self.get_html(AuchanParser.URL1, params = {'p': page })
                prods.extend(self.get_content(html.text))
            html = self.get_html(AuchanParser.URL2)
            l = self.get_pages_count(html.text)
            for i in range(l):
                page = i + 1
                html = self.get_html(AuchanParser.URL2, params = {'p': page })
                prods.extend(self.get_content(html.text))
            html = self.get_html(AuchanParser.URL3)
            l = self.get_pages_count(html.text)
            for i in range(l):
                page = i + 1
                html = self.get_html(AuchanParser.URL3, params = {'p': page })
                prods.extend(self.get_content(html.text))
            return prods
class MetroParser():
    URL = 'https://msk.metro-cc.ru/virtual/regular'
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63',
              'accept': '*/*'
              }
    def __init__(self):
        pass
    def get_html(self, url, params=None):
        r = requests.get(url, headers=MetroParser.HEADERS, params=params)
        return r
    def get_pages_count(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        page = soup.find('div', class_ = 'pagination')
        page = page.find_all('li')[-2]
        page = page.find('a').get_text()
        count = int(page)
        return count
    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='catalog-i_w')
        products = []
        date = datetime.datetime.now()
        date = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
        for item in items:
            prod_name = item.find('span', class_='title')
            prod = item.find('div', class_ = 'price_cnt catalog-i_router-item')
            if (prod is None):
                prod = item
            prod_price_int = prod.find('span', class_='int')
            prod_price_dec = prod.find('span', class_='float')
            if ((prod_name is not None) and (prod_price_int is not None) and (prod_price_dec is not None)):
                products.append({
                    'title': prod_name.get_text(),
                    'price_int': prod_price_int.get_text(),
                    'price_dec': prod_price_dec.get_text(),
                    'shop_name': "Metro",
                    'time': date
                })
        return products
    def parse(self):
        html = self.get_html(MetroParser.URL, params = {'limit': 72, 'in_stock': 1 })
        if (html.status_code == 200):
            l = self.get_pages_count(html.text)
            prods = []
            for i in range(l):
                page = i + 1
                html = self.get_html(MetroParser.URL, params = {'page': page, 'limit': 72, 'in_stock': 1 })
                prods.extend(self.get_content(html.text))
            return prods
class AddWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AddWindow, self).__init__()
        self.setObjectName("AddWindow")
        self.setGeometry(0, 0, 830, 700)
        self.setMinimumSize(750, 400)
  
        ### horizontal box with the buttons
        self.groupBox = QtWidgets.QHBoxLayout()

        
        """
        self.insertButton = QtWidgets.QPushButton()
        self.insertButton.setFixedWidth(90)
        self.insertButton.setObjectName("insertButton")
        self.insertButton.setText("Load data")
        """
        
        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setFixedWidth(90)
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setText("Delete")
                

        #and_additional
        self.refreshButton = QtWidgets.QPushButton()
        self.refreshButton.setFixedWidth(90)
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.setText("refresh")
        #self.refreshButton.clicked.connect(self.refresh)

  
        self.clearButton = QtWidgets.QPushButton()
        self.clearButton.setFixedWidth(90)
        self.clearButton.setText("Clear")
        self.clearButton.setObjectName("clearButton")
  
        
        self.saveButton = QtWidgets.QPushButton()
        self.saveButton.setFixedWidth(90)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setText("Save")
        
        #self.groupBox.addWidget(self.insertButton, 0, QtCore.Qt.AlignLeft)
        self.groupBox.addWidget(self.deleteButton, 1, QtCore.Qt.AlignLeft)
        #and_additional
        self.groupBox.addWidget(self.refreshButton, 2, QtCore.Qt.AlignLeft)
        self.groupBox.addWidget(self.clearButton, 0, QtCore.Qt.AlignRight)
        self.groupBox.addWidget(self.saveButton, 0, QtCore.Qt.AlignRight)
        
        #self.refreshButton.clicked.connect(self.refresh) 
        self.deleteButton.clicked.connect(self.delete_product)     
        self.clearButton.clicked.connect(self.clear)     
        #self.insertButton.clicked.connect(self.insert_in_table)


        ### horizontal box with the comboboxes and lineedits
        self.combogroup = QtWidgets.QHBoxLayout()
        #and_add
        """
        self.shop_name_box = QtWidgets.QComboBox()
        self.shop_name_box.setFixedWidth(180)
        self.shop_name_box.setObjectName("shop_name_box")
        self.shop_name_box.setEditable(True)
        self.shop_name_box.lineEdit().setPlaceholderText("Shop's Name")
        """
        self.product_id_box = QtWidgets.QComboBox()
        self.product_id_box.setFixedWidth(100)
        self.product_id_box.setObjectName("product_id_box")
        self.product_id_box.setEditable(True)
        self.product_id_box.lineEdit().setPlaceholderText("Product ID")
        
        

  
        self.product_name_box = QtWidgets.QComboBox()
        self.product_name_box.setFixedWidth(150)
        self.product_name_box.setObjectName("product_name_box")
        self.product_name_box.setEditable(True)
        self.product_name_box.lineEdit().setPlaceholderText("Product Name")
        
        """
        self.product_value_box = QtWidgets.QComboBox()
        self.product_value_box.setFixedWidth(130)
        self.product_value_box.setObjectName("product_value_box")
        self.product_value_box.setEditable(True)
        self.product_value_box.lineEdit().setPlaceholderText("Product Value")
        """
  
        self.lineEdit_price = QtWidgets.QLineEdit()
        self.lineEdit_price.setFixedWidth(80)
        self.lineEdit_price.setObjectName("lineEdit_price")
        self.lineEdit_price.setPlaceholderText("price")
        self.lineEdit_price.addAction(QtGui.QIcon.fromTheme("gnucash") , 0)
        """
        self.lineEdit_quantity = QtWidgets.QLineEdit()
        self.lineEdit_quantity.setFixedWidth(80)
        self.lineEdit_quantity.setObjectName("lineEdit_quantity")
        self.lineEdit_quantity.setPlaceholderText("quantity")
        """
        self.lineEditFind = QtWidgets.QLineEdit()
        self.lineEditFind.setFixedWidth(150)
        self.lineEditFind.setObjectName("lineEdit_find")
        self.lineEditFind.setPlaceholderText("find (RETURN)")
        self.lineEditFind.setClearButtonEnabled(True)
        self.lineEditFind.addAction(QtGui.QIcon.fromTheme("edit-find") , 0)
        self.lineEditFind.returnPressed.connect(self.find_in_table)
         
        #and_add располагаем вторую линию
        #self.combogroup.addWidget(self.shop_name_box, 0, QtCore.Qt.AlignLeft)
        self.combogroup.addWidget(self.product_id_box)
        self.combogroup.addWidget(self.product_name_box)
        self.combogroup.addWidget(self.lineEdit_price)
        
        #self.init_comboBoxforShop() #выбор магазинов

        
        
        ########self.combogroup.addWidget(self.lineEdit_quantity)
        ########self.combogroup.addWidget(self.product_value_box, 1, QtCore.Qt.AlignLeft)
        self.combogroup.addWidget(self.lineEditFind, 1, QtCore.Qt.AlignRight)

        ### set comboboxes to change index by other boxes
        self.product_name_box.currentIndexChanged.connect(self.sync_comboboxes)
        self.product_id_box.currentIndexChanged.connect(self.sync_comboboxes)
        ###############################################
 
        self.lblgroup = QtWidgets.QHBoxLayout()
 
        self.product_id_lbl = QtWidgets.QLabel()
        self.product_id_lbl.setFixedWidth(100)
        self.product_id_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_id_lbl.setObjectName("label")
        self.product_id_lbl.setText("Product ID")
  
        self.product_name_lbl = QtWidgets.QLabel()
        self.product_name_lbl.setFixedWidth(180)
        self.product_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_name_lbl.setObjectName("product_name_lbl")
        self.product_name_lbl.setText("Product Name")
  
        self.product_price_lbl = QtWidgets.QLabel()
        self.product_price_lbl.setFixedWidth(80)
        self.product_price_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_price_lbl.setObjectName("product_price_lbl")
        self.product_price_lbl.setText("Price")
        """
        self.product_quantity_lbl = QtWidgets.QLabel()
        self.product_quantity_lbl.setFixedWidth(80)
        self.product_quantity_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_quantity_lbl.setObjectName("product_quantity_lbl")
        self.product_quantity_lbl.setText("Quantity")
        """
        """
        self.product_value_lbl = QtWidgets.QLabel()
        self.product_value_lbl.setFixedWidth(130)
        self.product_value_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_value_lbl.setObjectName("product_value_lbl")
        self.product_value_lbl.setText("Value")
        """
        """
        self.lblgroup.addWidget(self.product_id_lbl, 0, QtCore.Qt.AlignLeft)
        self.lblgroup.addWidget(self.product_name_lbl)
        self.lblgroup.addWidget(self.product_price_lbl)
        """
        ##########self.lblgroup.addWidget(self.product_quantity_lbl)
        ##########self.lblgroup.addWidget(self.product_value_lbl, 1, QtCore.Qt.AlignLeft)
  
        ##########################################
        self.tableWidget = QtWidgets.QTableView()
        self.tableWidget.horizontalHeader().setStyleSheet("::section{background-color:#d3d7cf;color: #2e3436; border: 1px solid darkgray;font: bold}")
        self.tableWidget.verticalHeader().setStyleSheet("::section{background-color:#d3d7cf;color: #2e3436; border: 1px solid darkgray;font: bold; padding-right: 4px;padding-top: 5px;}")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignRight)

        #### Main Window Layout
        self.vertWidget = QtWidgets.QVBoxLayout()
        self.vertWidget.setSpacing(10)
 
        self.vertWidget.addLayout(self.groupBox)
        self.vertWidget.addLayout(self.lblgroup)
        self.vertWidget.addLayout(self.combogroup)
 
        self.vertWidget.setStretch(0, 1)
        self.vertWidget.setStretch(1, 0)
 
        self.vertWidget.addWidget(self.tableWidget)
 
        self.mainWidget = QtWidgets.QWidget()
 
        self.mainWidget.setLayout(self.vertWidget)
 
        self.setCentralWidget(self.mainWidget)
  
        QtCore.QMetaObject.connectSlotsByName(self)
        
        
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.model = QtSql.QSqlTableModel()
        self.dbfile = ""
        

        self.price_list = []

        self.tableWidget.setModel(self.model)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.selectionModel().selectionChanged.connect(self.sync_comboboxes)
        
        self.setWindowTitle("Products")
        self.statusBar().showMessage("Ready")
        
        self.openDB()
        self.product_name_box.setFocus()
    '''
    def delete(self, query):
        conn = sqlite3.connect('products_list.sqlite')
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
    '''

        
    #def getSelectedRowId(self):
        #return self.tableWidget.currentRow()
        
    #def getSelectedProductId(self):
        #return self.tableWidget.item(getSelectedRowId(),0).text()
    
    def selectedRow(self):
        if self.tableWidget.selectionModel().hasSelection():
            myrow = self.tableWidget.selectionModel().selectedRows()[0]
            row = myrow.row()
            return row
        
    def delete_product(self):
        pass

        



    
    
    def delete_products(self):
        conn = sqlite3.connect('products_list.sqlite')
        c = conn.cursor()
        id_delete = self.selectedRow()
        c.execute("DELETE FROM products_list WHERE product_id = ?", (id_delete, ))
        conn.commit()
        conn.close()
        self.clear()
        self.initializeModel()
    
    

    def clear(self):
        conn = sqlite3.connect('products_list.sqlite')
        c = conn.cursor()
        c.execute('DELETE FROM products_list;',);
        conn.commit()
        conn.close()
        self.initializeModel()


    def find_in_table(self):
        self.msg("find test")
        row = self.product_name_box.findText(self.lineEditFind.text(), QtCore.Qt.MatchContains)
        print(row)
        if row > 0:
            self.product_name_box.setFocus()
            self.product_name_box.setCurrentIndex(row)
        else:
            row = self.product_id_box.findText(self.lineEditFind.text(), QtCore.Qt.MatchContains)
            if row > 0:
                self.product_id_box.setFocus()
                self.product_id_box.setCurrentIndex(row)
          
    def sync_comboboxes(self):
#        self.tableWidget.clearSelection()
        if self.product_name_box.hasFocus():
            row = self.product_name_box.currentIndex()
            self.product_id_box.setCurrentIndex(row)
            self.tableWidget.selectRow(row)
            self.tableWidget.setFocus()
        elif self.product_id_box.hasFocus():
            row = self.product_id_box.currentIndex()
            self.product_name_box.setCurrentIndex(row)
            self.tableWidget.selectRow(row)
            self.tableWidget.setFocus()
        elif self.tableWidget.hasFocus():
            row = self.tableWidget.selectionModel().selectedRows()[0].row()
            self.product_name_box.setCurrentIndex(row)
            self.product_id_box.setCurrentIndex(row)
        price = self.getPrice()
        self.lineEdit_price.setText(price)
##############################################
    def openDB(self):
        mydir = os.path.abspath(os.path.dirname(sys.argv[0])) #os.path.dirname(sys.argv[0])
        self.dbfile = mydir + "/products_list.sqlite"
        self.tablename = "products_list"
        self.db.setDatabaseName(self.dbfile)
        self.db.open()
        self.initializeModel()

    def initializeModel(self):
        print("Table selected:", self.tablename)
        self.model.setTable(self.tablename)
        self.model.sort(0, 0)
#        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.setAutoWidth()
        self.msg(self.tablename + " loaded *** " + str(self.model.rowCount()) + " records")
        self.fill_products_list_id_combo()
        self.fill_products_list_price_list()
        self.fill_products_list_name_combo()
        conn=sqlite3.connect(self.dbfile)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        c.execute('select * from products_list')
        names = list(map(lambda x: x[0], c.description))
        print(names)
            

    def fill_products_list_id_combo(self):
        conn=sqlite3.connect(self.dbfile)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        data = c.execute('SELECT product_id FROM products_list ORDER BY product_id').fetchall()
        self.product_id_box.insertItems(0, [str(item) for item in data])

    def fill_products_list_name_combo(self):
        conn=sqlite3.connect(self.dbfile)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        data = c.execute('SELECT product_name FROM products_list ORDER BY product_id').fetchall()
        self.product_name_box.insertItems(0, data)
        icon = QtGui.QIcon.fromTheme("computer")
        self.product_name_box.setIconSize(QtCore.QSize(16, 16))
        for x in range(self.product_name_box.count()):
            self.product_name_box.setItemIcon(x, icon)

    def fill_products_list_price_list(self):
        conn=sqlite3.connect(self.dbfile)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        data = c.execute('SELECT product_price FROM products_list ORDER BY product_id').fetchall()
        self.price_list.append(data)

    def setAutoWidth(self):
        self.tableWidget.resizeColumnsToContents()

    def msg(self, message):
        self.statusBar().showMessage(message)

    def selectedColumn(self):
        column =  self.tableWidget.selectionModel().selectedIndexes()[0].column()
        return int(column)

    def getPrice(self):
        if self.tableWidget.selectionModel().hasSelection():
            myrow = self.tableWidget.selectionModel().selectedRows()[0]
            row = myrow.row()
            column = 3
            myitem = myrow.sibling(row, column).data()
            self.msg("Price: " + str(myitem) + " ₽")
            return (str(myitem))
        else:
            self.msg("no selection")






class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.setGeometry(0, 0, 830, 700)
        self.setMinimumSize(750, 400)
  
        ### horizontal box with the buttons
        self.groupBox = QtWidgets.QHBoxLayout()

        #addWindow
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setFixedWidth(90)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Purchase")

        self.setCentralWidget(self.pushButton)
        self.dialog = AddWindow(self)
        #########
        
        self.insertButton = QtWidgets.QPushButton()
        self.insertButton.setFixedWidth(90)
        self.insertButton.setObjectName("insertButton")
        self.insertButton.setText("Load data")
  
        
        self.addButton = QtWidgets.QPushButton()
        self.addButton.setFixedWidth(90)
        self.addButton.setObjectName("insertButton")
        self.addButton.setText("Insert")
                

        #and_additional
        self.refreshButton = QtWidgets.QPushButton()
        self.refreshButton.setFixedWidth(90)
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.setText("refresh")
        self.refreshButton.clicked.connect(self.refresh)
        
        

        
  
        self.clearButton = QtWidgets.QPushButton()
        self.clearButton.setFixedWidth(90)
        self.clearButton.setText("Clear")
        self.clearButton.setObjectName("clearButton")
  
        '''
        self.saveButton = QtWidgets.QPushButton()
        self.saveButton.setFixedWidth(90)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setText("Save")
        '''
        self.groupBox.addWidget(self.insertButton, 0, QtCore.Qt.AlignLeft)
        #self.groupBox.addWidget(self.deleteButton, 1, QtCore.Qt.AlignLeft)
        #and_additional
        self.groupBox.addWidget(self.refreshButton, 2, QtCore.Qt.AlignLeft)
        self.groupBox.addWidget(self.addButton, 0, QtCore.Qt.AlignLeft)
        self.groupBox.addWidget(self.clearButton, 0, QtCore.Qt.AlignRight)
        self.groupBox.addWidget(self.pushButton, 0, QtCore.Qt.AlignRight)

        #self.groupBox.addWidget(self.saveButton, 0, QtCore.Qt.AlignRight)
        self.addButton.clicked.connect(self.add) 
        self.refreshButton.clicked.connect(self.refresh) 
        self.clearButton.clicked.connect(self.clear)     
        self.insertButton.clicked.connect(self.insert_in_table)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)


        ### horizontal box with the comboboxes and lineedits
        self.combogroup = QtWidgets.QHBoxLayout()
        #and_add
        self.shop_name_box = QtWidgets.QComboBox()
        self.shop_name_box.setFixedWidth(180)
        self.shop_name_box.setObjectName("shop_name_box")
        self.shop_name_box.setEditable(True)
        self.shop_name_box.lineEdit().setPlaceholderText("Shop's Name")
        
        self.product_id_box = QtWidgets.QComboBox()
        self.product_id_box.setFixedWidth(100)
        self.product_id_box.setObjectName("product_id_box")
        self.product_id_box.setEditable(True)
        self.product_id_box.lineEdit().setPlaceholderText("Product ID")
        
        

  
        self.product_name_box = QtWidgets.QComboBox()
        self.product_name_box.setFixedWidth(150)
        self.product_name_box.setObjectName("product_name_box")
        self.product_name_box.setEditable(True)
        self.product_name_box.lineEdit().setPlaceholderText("Product Name")
        
        """
        self.product_value_box = QtWidgets.QComboBox()
        self.product_value_box.setFixedWidth(130)
        self.product_value_box.setObjectName("product_value_box")
        self.product_value_box.setEditable(True)
        self.product_value_box.lineEdit().setPlaceholderText("Product Value")
        """
  
        self.lineEdit_price = QtWidgets.QLineEdit()
        self.lineEdit_price.setFixedWidth(80)
        self.lineEdit_price.setObjectName("lineEdit_price")
        self.lineEdit_price.setPlaceholderText("price")
        self.lineEdit_price.addAction(QtGui.QIcon.fromTheme("gnucash") , 0)
        """
        self.lineEdit_quantity = QtWidgets.QLineEdit()
        self.lineEdit_quantity.setFixedWidth(80)
        self.lineEdit_quantity.setObjectName("lineEdit_quantity")
        self.lineEdit_quantity.setPlaceholderText("quantity")
        """
        self.lineEditFind = QtWidgets.QLineEdit()
        self.lineEditFind.setFixedWidth(150)
        self.lineEditFind.setObjectName("lineEdit_find")
        self.lineEditFind.setPlaceholderText("find (RETURN)")
        self.lineEditFind.setClearButtonEnabled(True)               #stop
        self.lineEditFind.addAction(QtGui.QIcon.fromTheme("edit-find") , 0)
        self.lineEditFind.returnPressed.connect(self.find_in_table)
         
        #and_add располагаем вторую линию
        self.combogroup.addWidget(self.shop_name_box, 0, QtCore.Qt.AlignLeft)
        self.combogroup.addWidget(self.product_id_box)
        self.combogroup.addWidget(self.product_name_box)
        self.combogroup.addWidget(self.lineEdit_price)
        
        self.init_comboBoxforShop() #выбор магазинов

        
        
        ########self.combogroup.addWidget(self.lineEdit_quantity)
        ########self.combogroup.addWidget(self.product_value_box, 1, QtCore.Qt.AlignLeft)
        self.combogroup.addWidget(self.lineEditFind, 1, QtCore.Qt.AlignRight)

        ### set comboboxes to change index by other boxes
        self.product_name_box.currentIndexChanged.connect(self.sync_comboboxes)
        self.product_id_box.currentIndexChanged.connect(self.sync_comboboxes)
        ###############################################
 
        self.lblgroup = QtWidgets.QHBoxLayout()
 
        self.product_id_lbl = QtWidgets.QLabel()
        self.product_id_lbl.setFixedWidth(100)
        self.product_id_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_id_lbl.setObjectName("label")
        self.product_id_lbl.setText("Product ID")
  
        self.product_name_lbl = QtWidgets.QLabel()
        self.product_name_lbl.setFixedWidth(180)
        self.product_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_name_lbl.setObjectName("product_name_lbl")
        self.product_name_lbl.setText("Product Name")
  
        self.product_price_lbl = QtWidgets.QLabel()
        self.product_price_lbl.setFixedWidth(80)
        self.product_price_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_price_lbl.setObjectName("product_price_lbl")
        self.product_price_lbl.setText("Price")
        """
        self.product_quantity_lbl = QtWidgets.QLabel()
        self.product_quantity_lbl.setFixedWidth(80)
        self.product_quantity_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_quantity_lbl.setObjectName("product_quantity_lbl")
        self.product_quantity_lbl.setText("Quantity")
        """
        """
        self.product_value_lbl = QtWidgets.QLabel()
        self.product_value_lbl.setFixedWidth(130)
        self.product_value_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.product_value_lbl.setObjectName("product_value_lbl")
        self.product_value_lbl.setText("Value")
        """
        """
        self.lblgroup.addWidget(self.product_id_lbl, 0, QtCore.Qt.AlignLeft)
        self.lblgroup.addWidget(self.product_name_lbl)
        self.lblgroup.addWidget(self.product_price_lbl)
        """
        ##########self.lblgroup.addWidget(self.product_quantity_lbl)
        ##########self.lblgroup.addWidget(self.product_value_lbl, 1, QtCore.Qt.AlignLeft)
  
        ##########################################
        self.tableWidget = QtWidgets.QTableView()
        self.tableWidget.horizontalHeader().setStyleSheet("::section{background-color:#d3d7cf;color: #2e3436; border: 1px solid darkgray;font: bold}")
        self.tableWidget.verticalHeader().setStyleSheet("::section{background-color:#d3d7cf;color: #2e3436; border: 1px solid darkgray;font: bold; padding-right: 4px;padding-top: 5px;}")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignRight)

        #### Main Window Layout
        self.vertWidget = QtWidgets.QVBoxLayout()
        self.vertWidget.setSpacing(10)
 
        self.vertWidget.addLayout(self.groupBox)
        self.vertWidget.addLayout(self.lblgroup)
        self.vertWidget.addLayout(self.combogroup)
 
        self.vertWidget.setStretch(0, 1)
        self.vertWidget.setStretch(1, 0)
 
        self.vertWidget.addWidget(self.tableWidget)
 
        self.mainWidget = QtWidgets.QWidget()
 
        self.mainWidget.setLayout(self.vertWidget)
 
        self.setCentralWidget(self.mainWidget)
  
        QtCore.QMetaObject.connectSlotsByName(self)
        
        
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.model = QtSql.QSqlTableModel()
        self.dbfile = ""
        

        self.price_list = []

        self.tableWidget.setModel(self.model)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.selectionModel().selectionChanged.connect(self.sync_comboboxes)
        
        self.setWindowTitle("Products")
        self.statusBar().showMessage("Ready")
        self.openDB()
        self.product_name_box.setFocus()
        
    
    
    def on_pushButton_clicked(self):
        self.dialog.show()    
    
    
    def add(self):
        pass
    
        """
        elif ('Перекресток' == self.shop_name_box.currentText()):
            pars = PerekrestokParser()
            prods = pars.parse()
            self.insert_in_table(prods)
            del pars
        """
    
    def refresh(self):
        self.clear()
        if ('Магнит' == self.shop_name_box.currentText()):
            pars = MagnitParser()
            prods = pars.parse()
            self.insert_in_table(prods)
            del pars

        
        elif ('Ашан' == self.shop_name_box.currentText()):
            pars = AuchanParser()
            prods = pars.parse()
            self.insert_in_table(prods)
            del pars
        elif ('Metro' == self.shop_name_box.currentText()):
            pars = MetroParser()
            prods = pars.parse()
            self.insert_in_table(prods)
            del pars

        self.initializeModel()



    def insert_additional(self, prods):
        l = len(prods)
        conn = sqlite3.connect('products.sqlite')  
        c = conn.cursor() ###
     
        for i in range(l):
            #c = conn.cursor()
            prod_name = prods[i]['title']
            prod_price = prods[i]['price_int'] + '.' + prods[i]['price_dec'] 
            store_name = prods[i]['shop_name']
            time_ = prods[i]['time']
            c.execute("INSERT INTO products(product_id, store_name, product_name,product_price, time) VALUES(?,?,?,?,?)", (i,store_name, prod_name,prod_price, time_));
            #conn.commit()
        conn.commit()    
        conn.close()
        #self.initializeModel()
    
        """
        elif ('Перекресток' == self.shop_name_box.currentText()):
            pars = PerekrestokParser()
            prods = pars.parse()
            self.insert_additional(prods)
        """
    def insert_in_table(self, prods):
        if ('Магнит' == self.shop_name_box.currentText()):
            pars = MagnitParser()
            prods = pars.parse()
            self.insert_additional(prods)

        elif ('Ашан' == self.shop_name_box.currentText()):
            pars = AuchanParser()
            prods = pars.parse()
            self.insert_additional(prods)
        elif ('Metro' == self.shop_name_box.currentText()):
            pars = MetroParser()
            prods = pars.parse()
            self.insert_additional(prods)
        self.initializeModel()



    
    
    
    def clear(self):
        conn = sqlite3.connect('products.sqlite')
        c = conn.cursor()
        c.execute('DELETE FROM products;',);
        conn.commit()
        conn.close()
        self.initializeModel()


    
    
    
    def init_comboBoxforShop(self):
            self.shop_name_box.addItems(['Магнит', 'Перекресток', 'Ашан', 'Metro'])

    def find_in_table(self):
        self.msg("find test")
        row = self.product_name_box.findText(self.lineEditFind.text(), QtCore.Qt.MatchContains)
        print(row)
        if row > 0:
            self.product_name_box.setFocus()
            self.product_name_box.setCurrentIndex(row)
        else:
            row = self.product_id_box.findText(self.lineEditFind.text(), QtCore.Qt.MatchContains)
            if row > 0:
                self.product_id_box.setFocus()
                self.product_id_box.setCurrentIndex(row)
          
    def sync_comboboxes(self):
#        self.tableWidget.clearSelection()
        if self.product_name_box.hasFocus():
            row = self.product_name_box.currentIndex()
            self.product_id_box.setCurrentIndex(row)
            self.tableWidget.selectRow(row)
            self.tableWidget.setFocus()
        elif self.product_id_box.hasFocus():
            row = self.product_id_box.currentIndex()
            self.product_name_box.setCurrentIndex(row)
            self.tableWidget.selectRow(row)
            self.tableWidget.setFocus()
        elif self.tableWidget.hasFocus():
            row = self.tableWidget.selectionModel().selectedRows()[0].row()
            self.product_name_box.setCurrentIndex(row)
            self.product_id_box.setCurrentIndex(row)
        price = self.getPrice()
        self.lineEdit_price.setText(price)
##############################################
    def openDB(self):
        mydir = os.path.abspath(os.path.dirname(sys.argv[0])) #os.path.dirname(sys.argv[0])
        self.dbfile = mydir + "/products.sqlite"
        self.tablename = "products"
        self.db.setDatabaseName(self.dbfile)
        self.db.open()
        self.initializeModel()

    def initializeModel(self):
        print("Table selected:", self.tablename)
        self.model.setTable(self.tablename)
        self.model.sort(0, 0)
#        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.setAutoWidth()
        self.msg(self.tablename + " loaded *** " + str(self.model.rowCount()) + " records")
        self.fill_products_id_combo()
        self.fill_products_price_list()
        self.fill_products_name_combo()
        conn=sqlite3.connect(self.dbfile)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        c.execute('select * from products')
        names = list(map(lambda x: x[0], c.description))
        print(names)
            

    def fill_products_id_combo(self):
        conn=sqlite3.connect(self.dbfile)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        data = c.execute('SELECT product_id FROM products ORDER BY product_id').fetchall()
        self.product_id_box.insertItems(0, [str(item) for item in data])

    def fill_products_name_combo(self):
        conn=sqlite3.connect(self.dbfile)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        data = c.execute('SELECT product_name FROM products ORDER BY product_id').fetchall()
        self.product_name_box.insertItems(0, data)
        icon = QtGui.QIcon.fromTheme("computer")
        self.product_name_box.setIconSize(QtCore.QSize(16, 16))
        for x in range(self.product_name_box.count()):
            self.product_name_box.setItemIcon(x, icon)

    def fill_products_price_list(self):
        conn=sqlite3.connect(self.dbfile)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        data = c.execute('SELECT product_price FROM products ORDER BY product_id').fetchall()
        self.price_list.append(data)

    def setAutoWidth(self):
        self.tableWidget.resizeColumnsToContents()

    def msg(self, message):
        self.statusBar().showMessage(message)

    def selectedColumn(self):
        column =  self.tableWidget.selectionModel().selectedIndexes()[0].column()
        return int(column)

    def getPrice(self):
        if self.tableWidget.selectionModel().hasSelection():
            myrow = self.tableWidget.selectionModel().selectedRows()[0]
            row = myrow.row()
            column = 3
            myitem = myrow.sibling(row, column).data()
            self.msg("Price: " + str(myitem) + " ₽")
            return (str(myitem))
        else:
            self.msg("no selection")

if __name__ == "__main__":
    #import sys
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    
    



    
    
    
    