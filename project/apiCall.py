import json
from bs4 import BeautifulSoup
import requests
from project import db_connect
import datetime

class apiCall() :
    def __init__(self) :
        with open('myApi.json', 'r') as f :
            self.myApi = json.load(f)

    def fishCreate(self) :
        db_class = db_connect.Database()
        db_class.truncate()

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

    def fishFind(self, addr) :
        db_class = db_connect.Database()

        sql = 'select * from fish where flocation like %s'
        val = '%' + addr + '%'

        row = db_class.execute(sql, val)

        for i in row :
            print(i)

    def fishLocation(self) :
        db_class = db_connect.Database()

        sql = 'select flocation from fish'

        row = db_class.execute(sql)

        print(row)
        print(type(row))

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
#apiCall.fishCreate()
apiCall.fishLocation()
#apiCall.fishFind('태안')
#apiCall.temp('001') # sea = 동해 001, 서해 002, 남해 003

'''
해수어류 ??
해면어류 ??
참돔 18~20도// 27도~ 활동불가 
우럭 15~20도 안팎 // 0~5도, 30~35도 활동불가
볼락 12~16도 // 3도~8도 , 26 ~ 33도 활동불가
숭어 14~16도 안팎 // 1~4도, 35~37도 활동 불가
돔 13~20도
점성어(민어) // 14~20도 안팎 // 7~12도, 31~35도
붕어 삭제
도다리 14~16
광어13~17도 // 
문어 15 ~ 25
감성돔 17~19도 // 2~6도, 31도~37도

35.48630, 129.42927(방어진항) - 일본 이즈모시 지점 밑으로 남해
34.419005,126.078643진도 바다 - 기준 왼쪽은 서해
'''