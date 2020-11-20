import json
from bs4 import BeautifulSoup
import requests

class apiCall() :
    def __init__(self) :
        with open('myApi.json', 'r') as f :
            self.myApi = json.load(f)

    def fish(self) :
        open_api_key = self.myApi['fish']['key']
        params = '&numOfRows=100&pageNo=1&fshlcType=평지'

        open_url = 'http://api.data.go.kr/openapi/tn_pubr_public_fshlc_api?ServiceKey=' + open_api_key + params

        res = requests.get(open_url)
        soup = BeautifulSoup(res.content, 'html.parser')

        total = soup.find('totalcount')
        print(total)
        data = soup.find_all('item')

        for item in data:
            fshlcnm = item.find('fshlcnm')
            kdfsh = item.find('kdfsh')
            print(fshlcnm.get_text(), kdfsh.get_text())


fish_class = apiCall()
fish_class.fish()