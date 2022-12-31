import mysql.connector
import dbconfig as cfg
import csv

class productDAO:
    host =""
    user = ""
    password =""
    database =""
    connection = ""
    cursor =""

    def __init__(self): 
        self.host = cfg.mysql['host']
        self.user = cfg.mysql['user']
        self.password = cfg.mysql['password']
        self.database = cfg.mysql['database']
    
    def getCursor(self): 
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor
        
    def closeAll(self):
        self.connection.close()
        self.cursor.close()


    @staticmethod
    def convertToDictArray(result):
        '''returns dictArray from tupleArray'''

        items = []
        if result:
            for prod in result:
                item = {'ID':prod[0],'NAME' : prod[1], 'QTY' : prod[2], 'PRICE' : prod[3]}
                items.append(item)

        return items

    def getAll(self):

        cursor = self.getCursor()
        sql="select * from Product"
        cursor.execute(sql)
        result = cursor.fetchall()
        dictResult = self.convertToDictArray(result)
        self.closeAll()
        return dictResult

    def updateQuantity(self, values):

        try:
            print(values)
            cursor = self.getCursor()
            sql="update product set QTY = QTY - %s where ID = %s"
            cursor.execute(sql, values)
            self.connection.commit()
            self.closeAll()
            
        except Exception:
            self.closeAll()
            return False


    def createDatabase(self):
        '''
        Creates database if it does not already exist
        '''      
        try:
            self.connection = mysql.connector.connect(
                host=       self.host,
                user=       self.user,
                password=   self.password   
            )
            self.cursor = self.connection.cursor()
            sql="create database "+ self.database
            self.cursor.execute(sql)

            self.connection.commit()
            self.closeAll()

        except mysql.connector.Error as err:
            if err.errno == 1007:
                print("Database already exists..")
            else:
                print("Something went wrong: {}".format(err))

    def createTable(self):
        '''
        Creates table if it does not exist
        Also returns True or False depending if table creation was successful
        '''
        try:
            cursor = self.getCursor()
            sql="CREATE TABLE Product\
                (\
                    ID VARCHAR(100) PRIMARY KEY,\
                    NAME VARCHAR(100) NOT NULL,\
                    QTY INT NOT NULL,\
                    PRICE FLOAT\
                )"
 
            cursor.execute(sql)
            self.connection.commit()
            self.closeAll()
            return True

        except mysql.connector.Error as err:
            if err.errno == 1050:
                print("Table already exists..")
                return False
            else:
                print("Something went wrong: {}".format(err))
                return False

    def initialCreate(self):
        '''
        Read csv data and create sql table
        '''
        data = []
        with open('loadData/product.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            for row in csv_reader:
                data.append(
                    (
                        row[0].strip(),
                        row[1].strip(), 
                        row[2].strip(), 
                        row[3].strip()
                    )
                )

        cursor = self.getCursor()
        sql="insert into Product (ID, NAME, QTY, PRICE) values (%s,%s,%s,%s)"
        cursor.executemany(sql, data)
        self.connection.commit()
        self.closeAll()

    def dropTable(self):

        try:
            cursor = self.getCursor()
            sql="DROP TABLE Product"
            cursor.execute(sql)
            self.connection.commit()
            self.closeAll()

        except mysql.connector.Error as err:
            print("Something went wrong...: {}".format(err))

productDAO = productDAO()

if __name__ == "__main__":


    productDAO.createDatabase()
    #productDAO.dropTable()
    createTable = productDAO.createTable()
    if createTable:
        productDAO.initialCreate()