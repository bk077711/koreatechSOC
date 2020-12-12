import pymysql

class Database() :
    def __init__(self) :
        self.db = pymysql.connect(
            user='root',
            passwd='qwer1234',
            host='boysfishing.c7kxm4cffbqv.ap-northeast-2.rds.amazonaws.com',
            db='boysfishing',
            charset='utf8')

        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}) :
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()

        return row

    def create(self, query, args={}) :
        self.cursor.execute(query, args)
        self.db.commit()

    def truncate(self) :
        query ='truncate table fish'
        self.cursor.execute(query)

    def commit(self) :
        self.db.commit()