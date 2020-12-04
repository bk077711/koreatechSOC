import json
from bs4 import BeautifulSoup
import requests
from project import db_connect

class apiCall() :
    def __init__(self) :
        with open('myApi.json', 'r') as f :
            self.myApi = json.load(f)

    def fish(self) :
        db_class = db_connect.Database()

        open_api_key = self.myApi['fish']['key']
        params = '&numOfRows=100&pageNo=1'
        open_url = 'http://api.data.go.kr/openapi/tn_pubr_public_fshlc_api?ServiceKey=' + open_api_key + params
        res = requests.get(open_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        total = soup.find('totalcount').get_text()
        total = int(int(total) / 100 + 1)

        for i in range(1, total+1) :
            params = '&numOfRows=100&pageNo=' + str(i)
            open_url = 'http://api.data.go.kr/openapi/tn_pubr_public_fshlc_api?ServiceKey=' + open_api_key + params
            res = requests.get(open_url)
            soup = BeautifulSoup(res.content, 'html.parser')
            data = soup.find_all('item')

            for item in data:
                fshlcNm = item.find('fshlcnm').get_text()
                fshlcType = item.find('fshlctype').get_text()
                if item.find('rdnmadr') == None :
                    rdnmadr = item.find('lnmadr').get_text()
                else :
                    rdnmadr = item.find('rdnmadr').get_text()

                if item.find('fshlcPhoneNumber') != None :
                    fshlcPhoneNumber = item.find('fshlcphonenumber').get_text()
                else :
                    fshlcPhoneNumber = '-'
                kdfsh = item.find('kdfsh').get_text()
                useCharge = item.find('usecharge').get_text()

                sql = 'select * from fish where flocation=\'' + rdnmadr + '\''
                row = db_class.execute(sql)

                if len(row) == 0 :
                    sql = 'insert into fish (fname, ftype, flocation, fphone, fish, fmoney) values (%s, %s, %s, %s, %s, %s)'
                    val = (fshlcNm, fshlcType, rdnmadr, fshlcPhoneNumber, kdfsh, useCharge)
                    print(val)
                    row = db_class.execute(sql, val)
                    print(row)



fish_class = apiCall()
fish_class.fish()