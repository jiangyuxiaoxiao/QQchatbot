import json
import urllib.request


def news_():
    url = 'https://api.vvhan.com/api/60s?type=json'
    f = urllib.request.urlopen('%s' % url)
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call)
    msg = ''
    for time in a_result['time']:
        msg += time
        msg += '  '
    data_num = 1
    for data in a_result['data']:
        msg = msg + '\n' + str(data_num) + '. ' + data
        data_num += 1
    return msg
