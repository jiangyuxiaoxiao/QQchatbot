
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random

def rndChar():
    return chr(random.randint(65,90))

def rndColor():
     return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

def rndColor2():
    return (random.randint(32,127),random.randint(32,127),random.randint(32,127))

def image_call(wid,hig,sendmessage):
    if '随机验证码' in sendmessage:
        width = wid * 60
        height = hig * 60
        image = Image.new('RGB',(width,height),(255,255,255))   
        draw = ImageDraw.Draw(image) 
        font = ImageFont.truetype(".\\Bot_data\\TTF\\JetBrainsMono-Bold.ttf",36)
        for x in  range(width):
            for y in range(height):
                draw.point((x,y),fill=rndColor())
        for t in range(wid):
            draw.text((60*t+10,10),rndChar(),font=font,fill=rndColor2())

        image = image.filter(ImageFilter.BLUR)
        image.save('.\\Bot_data\\Image\\code.png')
    else:
        image = Image.new('RGB',(wid*70,hig*40),(47,167,0))   
        draw = ImageDraw.Draw(image) 
        font = ImageFont.truetype(".\\Bot_data\\TTF\\PingFang.ttc",32,encoding="utf-8")
        
        print(type(sendmessage))
        print(sendmessage)
        text = sendmessage
        draw.text((0,0), text, fill=(0,47,167), font=font, spacing=2, align="left")
        image.save('.\\Bot_data\\Image\\news.png')
    
    