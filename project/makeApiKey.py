import requests
import json

myApi = dict()
mapApi = dict()
fishApi = dict()
weatherApi = dict()

mapApi['clientId'] = ''
mapApi['clientSecret'] = ''
fishApi['key'] = ''
weatherApi['key'] = ''

myApi['map'] =mapApi
myApi['fish'] = fishApi
myApi['weather'] = weatherApi

with open('myApi.json', 'w') as f :
    json.dump(myApi, f)