
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random

def rndChar():
    return chr(random.randint(65,90))

def rndColor():
     return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

def rndColor2():
    return (random.randint(32,127),random.randint(32,127),random.randint(32,127))

def image_call(wid,hig,sendmessage):
    # if '随机验证码' in sendmessage:
    #     width = wid * 60
    #     height = hig * 60
    #     image = Image.new('RGB',(width,height),(255,255,255))   
    #     draw = ImageDraw.Draw(image) 
    #     font = ImageFont.truetype("./Bot_data/TTF/JetBrainsMono-Bold.ttf",36)
    #     for x in  range(width):
    #         for y in range(height):
    #             draw.point((x,y),fill=rndColor())
    #     for t in range(wid):
    #         draw.text((60*t+10,10),rndChar(),font=font,fill=rndColor2())

    #     image = image.filter(ImageFilter.BLUR)
    #     image.save('./Bot_data/Image/code.png')
    # else:
    image = Image.new('RGB',(wid*40,(hig+3)*40),(255,255,255))   
    draw = ImageDraw.Draw(image) 
    font = ImageFont.truetype("./Bot_data/TTF/PingFang.ttc",50,encoding="utf-8")
    text = '百度热搜榜'
    draw.text((50*3,10),text, fill=(255,0,0), font= font, spacing=2, align = 'center')
    font = ImageFont.truetype("./Bot_data/TTF/PingFang.ttc",32,encoding="utf-8")
    print(sendmessage)
    

    text = sendmessage
    #计算字体位置
    #w,h = len(sendmessage)*font_size,font_size
    #text_coordinate = int(())
    draw.text((15,90), text, fill=(0,0,0), font=font, spacing=2, align="left")
    image.save('./Bot_data/Image/news.png')
    
    