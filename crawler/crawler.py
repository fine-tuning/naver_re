import requests
import json
import logging
import time
import pandas as pd
import random
from datetime import datetime
from datetime import timedelta

URL = "https://m.land.naver.com/complex/getComplexArticleList"

param = {
    #'hscpNo': '112054',
    'hscpNo': '111515',
    'tradTpCd': 'A1',
    'order': 'date_',
    'showR0': 'N',
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
    'Referer': 'https://m.land.naver.com/'
}

page = 0
resultset = pd.DataFrame()

while True:
    page += 1
    param['page'] = page

    resp = requests.get(URL, params=param, headers=header)
    if resp.status_code != 200:
        logging.error('invalid status: %d' % resp.status_code)
        break

    data = json.loads(resp.text)
    result = data['result']
    if result is None:
        logging.error('no result')
        break
    
    for item in result['list']:
        this_row = item
        this_row = pd.DataFrame(data=[list(this_row.values())],columns=list(this_row.keys()))
                
        if len(resultset) > 0: 
            resultset = pd.concat([resultset, this_row])
        else:
            resultset = this_row
        
    if result['moreDataYn'] == 'N':
        break
        
    time.sleep(random.randrange(100, 120)*0.01)
    
this_filename = (os.getcwd() + '/resultset_' + this_timestamp + ".csv")
resultset.to_csv(this_filename, sep=',', na_rep='', index=False, encoding='euc-kr')
