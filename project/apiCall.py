import json
from bs4 import BeautifulSoup
import requests
from project import db_connect
import datetime
from haversine import haversine

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

    def fishLocation(self) :
        db_class = db_connect.Database()

        sql = 'select flocation from fish'

        row = db_class.execute(sql)

        print(row)
        print(type(row))

    def fishFind(self, addr) :
        db_class = db_connect.Database()

        sql = 'select * from fish where flocation like %s'
        val = '%' + addr + '%'

        row = db_class.execute(sql, val)

        # row 결과가 없으면 예외처리

        la = float(row[0]['flatitude'])
        lo = float(row[0]['flongitude'])
        location = la, lo
        # sea = 동해 001, 서해 002, 남해 003
        sea = self.selectSea(location)
        self.temp = self.getTemp(sea)
        self.fishList = self.getFish(self.temp)

        return row

    def selectSea(self, location) : #좌표 받아서 어느 해인지 반환하는 함수
        seasX = [37.1410, 36.1500, 37.0530, 36.0800, 34.4736, 34.4400, 35.3931, 34.0000, 34.0139, 34.4448, # 0~9 서해
                 34.0005, 33.4737, 34.4600, 34.2330, # 10 ~ 13 남해
                 36.2100, 35.2043, 36.5425, 37.2720, 37.2850] # 14 ~ 동해
        seasY = [126.0108, 125.4500, 125.2544, 124.0325, 125.4637, 126.1430, 125.4850, 123.1545, 125.1253, 125.1444, # 0~9 서해
                 127.3005, 126.0828, 128.5400, 128.1330, # 10 ~ 13 남해
                 129.4700, 129.5029, 129.5228, 131.0652, 129.5700] # 14 ~ 동해

        seas = []
        for i in range(len(seasX)) :
            seas.append((seasX[i], seasY[i]))

        degree = []

        for i in seas :
            degree.append(haversine(location, i))

        minD = min(degree)
        index = degree.index(minD)
        if  index >= 0 and index <= 9 : # 서해
            sea = '002'
        elif index > 9 and index <=13 : # 남해
            sea = '003'
        else :
            sea = '001'

        return sea

    def getTemp(self, sea) : # 해당 바다의 평균 수온 구하는 함수
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

        return round(tt/cnt, 2)

    def getFish(self, temp) : # 수온에 따라 추천 어종 리스트 반환하는 함수
        fishList = []

        '''
                참돔 18~20도// 27도~ 활동불가 
                우럭 15~20도 안팎 // 0~5도, 30~35도 활동불가
                볼락 12~16도 // 3도~8도 , 26 ~ 33도 활동불가
                숭어 14~16도 안팎 // 1~4도, 35~37도 활동 불가
                돔 13~20도
                점성어(민어) // 14~20도 안팎 // 7~12도, 31~35도
                도다리 14~16
                광어13~17도 // 
                문어 15 ~ 25
                감성돔 17~19도 // 2~6도, 31도~37도
        '''

        if temp >= 18 and temp <= 20 :
            fishList.append('참돔')
        if temp >= 15 and temp <= 20:
            fishList.append('우럭')
        if temp >= 12 and temp <= 16:
            fishList.append('볼락')
        if temp >= 14 and temp <= 16 :
            fishList.append('숭어')
        if temp >= 13 and temp <= 20 :
            fishList.append('돔')
        if temp >= 14 and temp <= 20 :
            fishList.append('점성어(민어)')
        if temp >= 14 and temp <= 16 :
            fishList.append('도다리')
        if temp >= 13 and temp <= 17 :
            fishList.append('광어')
        if temp >= 15 and temp <= 25 :
            fishList.append('문어')
        if temp >= 17 and temp <= 19 :
            fishList.append('감성돔')

        return fishList

    def getData(self, keyword) :
        if keyword == 'temp' :
            return self.temp

        elif keyword == 'fishList' :
            return self.fishList