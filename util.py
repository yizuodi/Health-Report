import os
import requests
from aip import AipOcr


def get_img(driver):
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    url = "https://cas.sysu.edu.cn/cas/captcha.jsp"
    res = s.get(url)

    client = AipOcr(os.environ['APP_ID'], os.environ['API_KEY'], os.environ['SECRET_KEY'])
    code = client.basicGeneral(res.content)['words_result'][0]['words'].replace(' ', '')

    return code


def tgbot_send(token, chatid, message):
    data = {'chat_id': chatid, 'text': f'健康申报结果：{message}'}
    try:
        r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data = data)
        if r.status_code == 200:
            print('发送通知成功')
        else:
            print('发送通知失败')
    except:
        print('发送通知失败')


def wx_send(wxsend_key, message):
    data = {
        "title": f'健康申报结果：{message}',
        "desp": "如遇身体不适、或居住地址发生变化，请及时更新健康申报信息。"
    }
    try:
        r = requests.post(f'https://sctapi.ftqq.com/{wxsend_key}.send', data = data)
        if r.status_code == 200:
            print('发送通知成功')
        else:
            print('发送通知失败')
    except:
        print('发送通知失败')
