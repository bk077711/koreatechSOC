import pymysql

class Database() :
    def __init__(self) :
        self.db = pymysql.connect(
            user='root',
            passwd='0000',
            host='127.0.0.1',
            db='trinity',
            charset='utf8')

        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}) :
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()

        return row

    def commit(self) :
        self.db.commit()