
import datetime
import requests
import time
from pprint import pprint
import json
import os

token_y =     # Введите токен Яндекс
token_vk =    # Введите токен ВК
vk_id =       # Введите ID Вконтакте

             #Запустите программу для загрузки фото


URL_VK = 'https://api.vk.com/method/photos.get'
directory = 'https://cloud-api.yandex.net/v1/disk/resources'
headers = {'Authorization': token_y}
url_ya = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
URL_VKP = 'https://api.vk.com/method/photos.getAlbums'
get_albums_params = {
    'owner_id': vk_id,
    'album_ids': 'all',
    'v': '5.131',
    'access_token': token_vk,
}
res_alb = requests.get(URL_VKP, params=get_albums_params)

album = {'Фото профиля': 'profile'}
for alb in res_alb.json()['response']['items']:
    album.update({alb['title']: alb['id']})

print('У вас есть несколько альбомов:\n', album.keys())
album_id = album[input('Наберите в строке название нужного, и нажмите Enter:', )]

direc = (list(album.keys())[list(album.values()).index(album_id)])


#
def get_photo(vk_id, album_id):
    params_vk = {
        'owner_id': f'{vk_id}',
        'access_token': token_vk,
        'v': '5.131',
        'album_id': f'{album_id}',
        'extended': 'likes'}

    res = requests.get(URL_VK, params=params_vk)
    photo_url = {}
    for photo in res.json()['response']['items']:
        likes = photo['likes']['count']
        date = photo['date']
        max_size = 0
        tre = {}
        for ph in photo['sizes']:
            pix = int(ph['height']) * int(ph['width'])
            ph_url = ph['url']
            size = ph['type']

            if pix >= max_size:
                if likes not in photo_url:

                    tre = {likes: [ph_url, datetime.datetime.fromtimestamp(date).date(), size, likes]}
                else:
                    tre = ({
                        datetime.datetime.fromtimestamp(date).date(): [ph_url,
                                                                       datetime.datetime.fromtimestamp(date).date(),
                                                                       size, likes]})
                max_size = pix
        photo_url.update(tre)
    sort_url = dict(sorted(photo_url.items(), key=lambda x: x[1][1], reverse=True)[0:5])
    return sort_url


#
def file_inf():
    for n, info in get_photo(vk_id, album_id).items():
        name = str(n) + '.json'
        file_info = ({'file name': str(n),
                      'size': info[2]})
        with open(f'photo info {name}', 'w') as file:
            json.dump(file_info, file)


def direct(direc):
    params_directory = {'path': f'{direc}'}
    requests.put(directory, params=params_directory, headers=headers)


def extreme_upload():
    for lik, phot in get_photo(vk_id, album_id).items():
        photo_url = (phot[0])
        name = f'{lik}.jpg'
        params_y = {'path': f'{direc}/{name}',
                    'url': photo_url}
        requests.post(url_ya, params=params_y, headers=headers)


def photo_saver():
    get_photo(vk_id, album_id)
    file_inf()
    direct(direc)
    extreme_upload()


photo_saver()