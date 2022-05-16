"""
Програма выполняет сохранение фотографий с профиля в ВКонтакте на Яндекс Диск.
На вход принимает токен Яндекс Диска и id пользователя в ВКонтакте.
Программа собирает id всех альбомов пользователя(в том числе со стены, аватарки и сохраненные),
затем собирает url всех фотографий с доступных альбомов, если альбом защищен настройками приватности
программа пропускает его.
На Яндекс Диске в корне создается каталог с именем и фамилией указанными в профиле ВКонтакте
и загружает в него все фотографии. Если такой каталог был создан ранее программа предварительно
переместит его в корзину. Имена загружаемых фотографий формируются по кол-ву лайков.
К фотографиям с одинаковым кол-вом лайков добавляется префикс(_1, _2 и т.д.)
После загрузки каждой фотографии создается запись в списке с параметрами загруженного файла,
после завершения загрузки список сохраняется в файл upload.json в каталог с программой.
За ходом выполнения программы можно наблюдать по логированию и прогрессбару в командной строке.
Спасибо за внимание.
"""



import time
import requests
from pprint import pprint
from tqdm import tqdm
from datetime import datetime

vk_token = '93ac33a6b560ea3101b544107361a6a34125a5929893e54f84de78378b7bdab2b14b5e3ef7c689ffecd3d'
version = '5.131'


## Класс работы с API ВКонтакте

class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token:str, version:str):
        self.user_id = user_id
        self.token = vk_token
        self.version = version
        self.params = {
            'access_token' : token,
            'v' : version
        }


##  Метод возвращает имя пользователя(необходимо для создания каталога на Яндекс Диске)

    def get_user_name(self):
        get_user_name_url = self.url + 'users.get'
        get_user_name_url_params = {
            'user_ids' : self.user_id
        }
        req = requests.get(get_user_name_url, params={**self.params, **get_user_name_url_params}).json()['response']
        user_name = f'''{req[0]['first_name']} {req[0]['last_name']}'''
        return user_name

##  Метод выбирает все ID альбомов со странички

    def get_albums_id(self):
        get_albums_id_url = self.url + 'photos.getAlbums'
        get_albums_id_url_params = {
            'owner_id' : self.user_id,

        }
        albums_id = ['wall', 'profile', 'saved']
        req = requests.get(get_albums_id_url, params={**self.params, **get_albums_id_url_params}).json()['response']['items']
        for id in tqdm(req, desc="Собираем альбомы", ncols=100):
            albums_id.append(id['id'])
        print(f'''Всего найдено {len(albums_id)} альбомов''')
        return albums_id


##  Метод формирует список словарей с данными по свем фотографиям из всех альбомов(кол-во лайков, размер, URL)
##  Блок можно сократить использую список размеров и сопостовляя его с имеющимися значениями

    def get_photo_url(self):
        albums_list = self.get_albums_id()
        get_photo_url = self.url + 'photos.get'
        photo_size = ['w', 'z', 'y', 'x', 's', 'r', 'q', 'p', 'o', 'm']
        photos_for_get = []
        for album in albums_list:
            get_photo_url_params = {
                'owner_id' : user_id,
                'album_id':album,
                'photo_size':0,
                'extended':1,
                'count' : 1000  #Для изменения кол-ва загружаемых фотографий из каждого альбома измените этот параметр
                                #Максимальное значение 1000
            }
            req = requests.get(get_photo_url, params={**self.params, **get_photo_url_params}).json()
            pprint(req)
            if 'response' in req.keys():

                for photo in tqdm(req['response']['items'], desc="Собираем фотографии", ncols=100):
                    photo_param = []
                    photo_likes = photo['likes']['count']
                    for size in photo['sizes']:
                        if 'w' in size['type']:
                            photo_param = {
                                'photo likes' : str(photo_likes),
                                'size' : size['type'],
                                'url' : size['url']
                            }
                        elif 'z' in size['type']:
                            photo_param = {
                                'photo likes' : str(photo_likes),
                                'size' : size['type'],
                                'url' : size['url']
                            }
                        elif 'y' in size['type']:
                            photo_param = {
                                'photo likes' : str(photo_likes),
                                'size' : size['type'],
                                'url' : size['url']
                            }
                        elif 'x' in size['type']:
                            photo_param = {
                                'photo likes' : str(photo_likes),
                                'size' : size['type'],
                                'url' : size['url']
                            }
                        elif 's' in size['type']:
                            photo_param = {
                                'photo likes' : str(photo_likes),
                                'size' : size['type'],
                                'url' : size['url']
                            }
                    if photo_param == []:
                        pass
                    else:
                        photos_for_get.append(photo_param)
            else:
                pass

        return photos_for_get


##  Метод заплатка, для исправления имен файлов с одинаковым кол-вом лайков

    def repeat_name(self):
        user_name = self.get_user_name()
        photo_list = self.get_photo_url()
        for photo in tqdm(photo_list, desc="Формируем названия файлов", ncols=100):
            prefix = 1
            for next_photo in photo_list[photo_list.index(photo)+1::]:
                if photo['photo likes'] == next_photo['photo likes']:
                    next_photo['photo likes'] = f'''{next_photo['photo likes']}_{prefix}'''
                    prefix += 1
        print(f'''Всего найдено {len(photo_list)} фотографий''')
        return photo_list, user_name


##  Класс работы с API Яндекс Диска

class YaUser:
    def __init__(self, token:str, user_name):
        self.token = yadisk_token
        self.path = user_name


##  Метод получения заголовков

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }


##  Метод создания каталога для загрузки фотографий, название каталога формируется из имени пользователя
##  Если такая папка уже существует, она предварительно будет удалена

    def create_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        params = {
            'path': self.path
        }
        headers = self.get_headers()
        req = requests.put(url, params=params, headers=headers).json()
        if 'href' in req.keys():
            print(f'''Папка {self.path} создана!''')
        else:
            print(req['message'])
            req = requests.delete(url, params=params, headers=headers)
            time.sleep(5)  ## Задержка для выполнения операции удаления на Яндекс Диске
            self.create_folder()  ## Рекурсия)


##  Метод загрузки фотографий на Яндекс Диск и формирования json файла

    def upload_photos(self, photo_list):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload/'
        headers = self.get_headers()
        photo_qnt = 0
        json_answer = []
        for photo in tqdm(photo_list, desc="Зугружаем фотографии", ncols=100):
            params = {
            'path' : f'''{self.path}/{photo['photo likes']}''',
            'url' : f'''{photo['url']}'''
            }

            req = requests.post(url, params=params, headers=headers).json()
            photo_qnt += 1
            file_info = {
                'file_name' : photo['photo likes'],
                'size' : photo['size']
            }

            json_answer.append(file_info)
        print(f'''Загружено {photo_qnt} фотографий''')
        return json_answer


##  Метод сохраняет результат программы в json файл

    def save_json(self,json_answer):

        with open('upload.json', 'w') as fw:
            fw.write(str(json_answer))




def main():

    User = VkUser(vk_token, version)
    file_list, user_name = User.repeat_name()
    UserUpl = YaUser(yadisk_token, user_name)
    UserUpl.create_folder()
    json = UserUpl.upload_photos(file_list)
    UserUpl.save_json(json)


if __name__ == '__main__':
    yadisk_token = input('Введите токен Яндекс Диска\n')
    user_id = input('Введите id пользователя Вконтакте\n')
    main()



