import json
from bs4 import BeautifulSoup
import requests
from project import db_connect
import datetime

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

                kdfsh = item.find('kdfsh').get_text()
                useCharge = item.find('usecharge').get_text()

                latitude = item.find('latitude').get_text()
                longitude = item.find('longitude').get_text()

                sql = 'select * from fish where flocation=\'' + rdnmadr + '\''
                row = db_class.execute(sql)

                if len(row) == 0 and fshlcType == '바다' and fshlcNm != '35.065079' and latitude != '11.11111111':
                    sql = 'insert into fish (fname, flocation, fish, fmoney, flatitude, flongitude) values (%s, %s, %s, %s, %s, %s)'
                    val = (fshlcNm, rdnmadr, kdfsh, useCharge, latitude, longitude)
                    db_class.create(sql, val)

    def temp(self, sea) :
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y%m%d')

        open_api_key = self.myApi['weather']['key']
        params = '&pageNo=1&GRU_NAM=' + sea + '&SDATE=' + nowDate + '&EDATE=' + nowDate
        open_url = 'http://apis.data.go.kr/1520635/OceanMensurationService/getOceanMesurationListrisa?ServiceKey=' + open_api_key + params

        res = requests.get(open_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        data = soup.find_all('item')

        cnt = 0
        tt = 0
        for item in data :
            if item.find('wtrtmp_1') == None :
                pass

            else :
                tt += float(item.find('wtrtmp_1').get_text())
                cnt += 1
        print(round(tt/cnt, 2))

apiCall = apiCall()
#apiCall.fish()
apiCall.temp('001')
# sea = 동해 001, 서해 002, 남해 003