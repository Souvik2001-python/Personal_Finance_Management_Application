import sqlite3

class Database :
    # create the database and intializing it
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS expense_record(item_name text,item_price float,purchase_date date)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS salary(amount float,credit_date date)")
        self.conn.commit()
    
    #function to fetch all the records from salary table
    def fetchSalary(self,query):
        self.cur.execute(query)
        total = self.cur.fetchone()[0]
        return total if total is not None else 0

    #function to fetch all the records from expense record table
    def fetchRecord(self,query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows
    
    # function to insert the records into salary table
    def insertSalary(self,amount,credit_date):
        self.cur.execute("INSERT INTO salary (amount, credit_date) VALUES (?, ?)", (amount, credit_date))
        self.conn.commit()


     # function to insert the records into expense record table

    def insertRecord(self,item_name,item_price,purchase_date):
        self.cur.execute("INSERT INTO expense_record VALUES(?,?,?)",(item_name,item_price,purchase_date))
        self.conn.commit()
    
    # function to remove the records
    def removeRecord(self,rwid):
        self.cur.execute("DELETE FROM expense_record WHERE rowid=?",(rwid,))
        self.conn.commit()
    
    # function to update the records
    def updateRecord(self,item_name,item_price,purchase_date,rid):
        self.cur.execute("UPDATE expense_record SET item_name=?,item_price=?,purchase_date=? WHERE rowid =?",(item_name,item_price,purchase_date,rid))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()