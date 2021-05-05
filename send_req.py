import json
import requests

URL_PATH = "http://localhost:8000/add_post_ex/"

DATA = { 
    "title": "kiedy jaranie"
    , "author": 'j"a'
    , "content": "test exempt tralalala, piszemy;" 
}
data_json = json.dumps(DATA) # json obj is created

data_json_raw = '{"title": "kiedy jaranie", "author": "ja", "post": "test exempt tralalala, piszemy;"}'

HEADERS = {
    'Content-Type': 'application/json'
    , 'Content-Length': str(len(data_json))
    , 'Accept': 'text/plain'
}

# R = requests.request("POST", URL_PATH, data=payload, headers=HEADERS)  # suggested by Postman
# R = requests.post(URL_PATH, data=data_json, headers=HEADERS)   # json=DATA #data=json.dumps(DATA)
# R = requests.post(URL_PATH, data=DATA)   # json=DATA #data=json.dumps(DATA)
R = requests.post(URL_PATH, data=data_json_raw)

if R.ok:
    print('done')
    print(R.text)
else:
    R.raise_for_status()