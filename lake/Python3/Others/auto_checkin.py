# 飞机场的自动签到领取流量(不兼容所有网站)

import requests

base_url = '***************'
login_url = 'https://{}/auth/login'.format(base_url)
checkin_url = 'https://{}/user/checkin'.format(base_url)

email = '**************'
passwd = '**************'

payload = {'email': email,
           'passwd': passwd,
           'code': ''}

login = requests.post(login_url, data=payload)
checkin = requests.post(checkin_url, data={}, cookies=login.cookies)

print(checkin.text)