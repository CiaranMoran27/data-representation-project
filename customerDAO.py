import mysql.connector
import dbconfig as cfg
import csv

class customerDAO:
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
                item = {'EMAIL':prod[0],'PASSWORD' : prod[1], 'CASH' : prod[2]}
                items.append(item)

        return items

    def create(self, values):

        cursor = self.getCursor()
        sql="insert into Customer (EMAIL, PASSWORD, CASH) values (%s,%s,%s)"
        cursor.execute(sql, values)
        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def delete(self, id):

        cursor = self.getCursor()
        sql="delete from Customer where EMAIL = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll

    def getAll(self):

        cursor = self.getCursor()
        sql="select * from Customer"
        cursor.execute(sql)
        result = cursor.fetchall()
        dictResult = self.convertToDictArray(result)
        self.closeAll()
        return dictResult

    def findById(self, id):

        try:
            cursor = self.getCursor()
            sql="select * from Customer where EMAIL = %s"
            values = (id,)
            cursor.execute(sql, values)

            result = cursor.fetchall()
            result = [{'EMAIL': result[0][0],  'PASSWORD': result[0][1], 'CASH': result[0][2]}]
            self.closeAll()
            return result

        except Exception:
            self.closeAll()
            return False

    def updateCash(self, values):  

        cursor = self.getCursor()
        sql="update Customer set CASH = %s  where EMAIL = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()



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
            sql="CREATE TABLE Customer\
                (\
                    EMAIL VARCHAR(100) PRIMARY KEY,\
                    PASSWORD VARCHAR(100) NOT NULL,\
                    CASH FLOAT\
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
        with open('loadData/customer.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            for row in csv_reader:
                data.append(
                    (
                        row[0].strip(),
                        row[1].strip(), 
                        row[2].strip()
                    )
                )

        cursor = self.getCursor()
        sql="insert into Customer (EMAIL, PASSWORD, CASH) values (%s,%s,%s)"
        cursor.executemany(sql, data)
        self.connection.commit()
        self.closeAll()

    def dropTable(self):
        
        try:
            cursor = self.getCursor()
            sql="DROP TABLE Customer"
            cursor.execute(sql)
            self.connection.commit()
            self.closeAll()

        except mysql.connector.Error as err:
            print("Something went wrong...: {}".format(err))



customerDAO = customerDAO()

if __name__ == "__main__":


    customerDAO.createDatabase()
    #customerDAO.dropTable()
    createTable = customerDAO.createTable()
    if createTable:
        customerDAO.initialCreate()
