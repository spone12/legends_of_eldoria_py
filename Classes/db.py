import sqlite3, csv
from Classes.logger import *
from gameSettings import *

class DB():
    """
        DB class
    """

    def __init__(self):
        self.conn = sqlite3.connect('Eldoria.db')
        self.curs = self.conn.cursor()
        self.createTables()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def createTables(self) -> None:
        """
            Create game tables IF NOT EXISTS
        """
        
        if not self.checkIfTableExists('items'):
            self.curs.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    item_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    data json NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        self.importDataToTable('items.csv')


    def checkIfTableExists(self, table):
        listOfTables = self.curs.execute(
        """SELECT name FROM sqlite_master WHERE type='table'
        AND name='""" + table + """'; """).fetchall()
        
        if listOfTables == []:
            return False
        else:
            return True

    def importDataToTable(self, fileName):
        try:

            with open(path.join(IMPORT_FOLDER, fileName), 'r') as file:
                
                # csv.DictReader
                reader = csv.DictReader(file)
                for row in reader:
                    self.curs.execute('''
                        INSERT INTO items (name, type, data)
                        VALUES (:name, :type, :data);
                    ''', row)
                self.conn.commit()

        except Exception as err:
            Logger().log(self.__class__.__name__, f"Import error: {err}")

    def checkTableExists(self, tablename):

        self.curs.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))
        if self.curs.fetchone()[0] == 1:
            return True

        return False

    def get(self, table = 'Items', where = None, values = None):
        """
            Get saved translated rows
        """

        try:
            sql = "SELECT * FROM " + table
            
            if where is not None:
                sql += " WHERE " + where

            self.curs.execute(sql)
            return self.curs.fetchall()
        except Exception as err:
            Logger().log(self.__class__.__name__, f"Select error: {err}")

    def insert(self, table, fields, values) -> None:
        """
            Insert Row
        """

        try:
            self.curs.execute('INSERT INTO ' + table + ' (' + fields + ') VALUES (?, ?, ?, ?, ?, ?)',
                (
                   values
                )
            )
        except Exception as err:
            Logger().log(self.__class__.__name__, f"Insert error: {err}")

    def update(self, table, set, where, update) -> None:
        """
            Update Row
        """

        try:
           self.curs.execute('UPDATE ' + table + ' SET ' + set + ' WHERE ' + + ' ', (update))
        except Exception as err:
            Logger().log(self.__class__.__name__, f"Update error: {err}")

    def deleteTranslate(self, table, id) -> None:
        """
            Delete Row
        """

        try:
           self.curs.execute('DELETE FROM ' + table + ' WHERE id = ?', (id, ))
        except Exception as err:
            Logger().log(self.__class__.__name__, f"Delete error: {err}")        
