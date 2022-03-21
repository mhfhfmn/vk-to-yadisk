import time
import requests
from pprint import pprint







sonya_id = '492322841'
yadisk_token = 'AQAAAABdQYihAADLW-kcmghJMEY7lfJZUpFynMA'
vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

url = 'https://api.vk.com/method/users.get'
params = {  'user_ids' : sonya_id,
            'access_token' : vk_token,
            'v' : '5.131',
            'fields' : 'education,sex,photo_400_orig'

            }

res = requests.get(url, params=params)
pprint(res.json())