import requests
import os


def text_to_sound(wb):
    filesname = os.getcwd()
    print()
    filesname = filesname + '\\Bot_data\\sound_of_text'
    isexists = os.path.exists(filesname)
    if not isexists:
        os.mkdir(filesname)

    url = 'https://api.oick.cn/txt/apiz.php?'

    params = {
        'text': wb,
        'spd': 1
    }

    p = requests.get(url=url, params=params).content
    with open('./Bot_data/sound_of_text/{}.mp3'.format(wb), 'wb') as fp:
        fp.write(p)
    name='./Bot_data/sound_of_text/{}.mp3'.format(wb)
    return name
