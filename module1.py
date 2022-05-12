import time
import requests
from pprint import pprint
from progress.bar import Bar
from tqdm import tqdm


vk_token = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
user_id = '492322841'
version = '5.131'
yadisk_token = 'AQAAAABdQYihAADLW-kcmghJMEY7lfJZUpFynMA'

"""
class  tqdm ():

    def  __init__(self , iterable = None , desc = None , total = None , leave = True ,
                file = None , ncols = None , mininterval = 0.1 ,
                maxinterval = 10.0 ,miniters = None , ascii = None , disable = False ,
               unit = 'it' ,unit_scale = False , dynamic_ncols = False ,
                smoothing = 0.3 ,bar_format = None , initial = 0 , position = None ,
                postfix = None ,unit_divisor = 1000):
                    pass
"""

class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token=vk_token, version=version):
        self.params = {
            'access_token' : token,
            'v' : version
}


##  Метод выбирает все ID альбомов со странички

    def get_albums_id(self, user_id=user_id):
        get_albums_id_url = self.url + 'photos.getAlbums'
        get_albums_id_url_params = {
            'owner_id' : user_id
}
        albums_id = ['wall', 'profile', 'saved']
        req = requests.get(get_albums_id_url, params={**self.params, **get_albums_id_url_params}).json()['response']['items']
        for id in tqdm(req, desc="Собираем альбомы", ncols=100):
            albums_id.append(id['id'])
        print(f'''Всего найдено {len(albums_id)} альбомов''')
        return albums_id


##  Метод формирует список словарей с данными по свем фотографиям из всех альбомов(кол-во лайков, размер, URL)

    def get_photo_url(self):
        albums_list = self.get_albums_id()
        get_photo_url = self.url + 'photos.get'
        photos_for_get = []
        for album in albums_list:
            req = requests.get(get_photo_url, params={**self.params, 'owner_id' : user_id, 'album_id':album, 'photo_size':0, 'extended':1}, ).json()

            if 'response' in req.keys():

                for photo in tqdm(req['response']['items'], desc="Собираем фотографии", ncols=100):
                    photo_param = []
                    photo_likes = photo['likes']['count']
                    for size in photo['sizes']:
                        if 'w' in size['type']:
                            photo_param = {'photo likes' : photo_likes,
                                           'size' : size['type'],
                                           'url' : size['url']}
                        elif 'z' in size['type']:
                            photo_param = {'photo likes' : photo_likes,
                                           'size' : size['type'],
                                           'url' : size['url']}
                        elif 'y' in size['type']:
                            photo_param = {'photo likes' : photo_likes,
                                           'size' : size['type'],
                                           'url' : size['url']}
                    photos_for_get.append(photo_param)

            else:
                pass

        return photos_for_get

    def repeat_name(self):
        photo_list = self.get_photo_url()
        for photo in tqdm(photo_list, desc="Формируем названия файлов", ncols=100):
            prefix = 1
            for next_photo in photo_list[photo_list.index(photo)+1::]:
                if photo['photo likes'] == next_photo['photo likes']:
                    next_photo['photo likes'] = f'''{next_photo['photo likes']}_{prefix}'''
                    prefix += 1
        print(f'''Всего найдено {len(photo_list)} фотографий''')
        return photo_list


"""
class YaUser:
    url =
"""



#class YaDiskUser:




Sonya = VkUser()
ids = Sonya.repeat_name()
#pprint(ids)












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

