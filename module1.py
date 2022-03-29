import time
import requests
from pprint import pprint


vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
user_id = '492322841'
version = '5.131'

class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token=vk_token, version=version):
        self.params = {
            'access_token' : token,
            'v' : version
}

    def get_albums_id(self, user_id=user_id):
        get_albums_id_url = self.url + 'photos.getAlbums'
        get_albums_id_url_params = {
            'owner_id' : user_id
}
        albums_id = ['wall', 'profile', 'saved']
        req = requests.get(get_albums_id_url, params={**self.params, **get_albums_id_url_params}).json()['response']['items']

        for id in req:
            albums_id.append(id['id'])

        return albums_id

    def get_photo_url(self):
        albums_list = self.get_albums_id()

        get_photo_url = self.url + 'photos.get'
        for album in albums_list:
            req = requests.get(get_photo_url, params={**self.params, 'owner_id' : user_id, 'album_id':album, 'photo_size':0, 'extended':1}, ).json()
            pprint(req)







Sonya = VkUser()
ids = Sonya.get_photo_url()







"""
sonya_id = '492322841'
yadisk_token = 'AQAAAABdQYihAADLW-kcmghJMEY7lfJZUpFynMA'
vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

url = 'https://api.vk.com/method/users.get'
url = 'https://api.vk.com/method/photos.getAll'
params = {  'user_ids' : sonya_id,
            'access_token' : vk_token,
            'v' : '5.131',
            'fields' : 'education,sex,photo_400_orig'

            }

res = requests.get(url, params=params)
pprint(res.json())


max_size = 'w'
"""

