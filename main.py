import io
import json
import os

import pytesseract
import requests
from PIL import Image

# Usage:
# Define 2 strings in userdata.py:
# e.g. username="学号" password="缴费平台密码（非智慧理工大密码）"
# Define your dorm code as a dict:
# e.g. dormdata = {"roomno": "xxxx", "factorycode": "xxxx", "area": "xxxx"}
# This can be found in analyzing JSON responds from the website

# TODO:Create a Dorm-Data table
from serverpush import push

'''
try:
    from userdata import username,password,dormdata
except ImportError:
    print("请检查根目录下是否有userdata.py用户信息文件！")
    quit(-1)
'''

# Const urls
loginurl = "http://cwsf.whut.edu.cn/innerUserLogin"
codeurl = "http://cwsf.whut.edu.cn/authImage"
sydlapi = "http://cwsf.whut.edu.cn/querySydl"


# Image Process Func
def imageProc(im):
    gray = im.convert('L')
    threshold = 120
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = gray.point(table, '1')
    final_image = out.crop((1, 1, 68, 18))
    return final_image


if __name__ == '__main__':
    apptoken = os.environ["apptoken"]
    uid = os.environ["uid"]
    username = os.environ["web_username"]
    password = os.environ["web_password"]
    dormdata = os.environ["dormdata"]


    s = requests.Session()

    s.get(loginurl)

    r_code = s.get(codeurl)

    image_code = Image.open(io.BytesIO(r_code.content))
    final = imageProc(image_code)

    rawCode = pytesseract.image_to_string(final, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789 -l num')
    intCode = rawCode[0:4]
    print("验证码识别：" + intCode)

    login_payload = {'logintype': 'PLATFORM', 'nickName': username, 'password': password, 'checkCode': str(intCode)}

    p = s.post(loginurl, data=login_payload)
    push(p.text,apptoken,uid) # debug push
    r = requests.post(sydlapi, data=dormdata,
                      cookies=dict(JSESSIONID=s.cookies['JSESSIONID']))
    push(r.text,apptoken,uid) # debug push
    if r.text[0] == '<':
        print("ERROR:Login Failed")
        quit()

    json_data = json.loads(r.text)
    print(json_data)
    str = ""
    # print("电量查询：") # TODO:Print room-based response including room number, etc.
    str+="电量查询：\n"
    # print("剩余电量：" + json_data['roomlist']['remainPower'])
    str+=("剩余电量：" + json_data['roomlist']['remainPower']+"\n")
    # print("检测时间：" + json_data['roomlist']['readTime'])
    str+=("检测时间：" + json_data['roomlist']['readTime']+"\n")
    timestamp = json_data['roomlist']['resultInfo']['timeStamp']
    # print("更新时间：" + timestamp.split('T')[0].replace('-','/')+" "+timestamp.split('T')[1].split('.')[0])
    str+=("更新时间：" + timestamp.split('T')[0].replace('-','/')+" "+timestamp.split('T')[1].split('.')[0]+"\n")
    print(str)
    push(str,apptoken,uid)
