import requests
from send_data_users import send_personal_value

token = input("Введите токен")
yours_id = input("Введите Ваш id")


def send_albums_id(token, yours_id):
    users = send_personal_value(token, yours_id)
    album_ids = [ ]
    value_ids = [ ]
    for character in users:
        for title_key, name_value in character.items():
            if title_key == "id":
                response_albums = requests.get("https://api.vk.com/method/photos.getAlbums/",
                                               params={"owner_id": name_value, "access_token": token,
                                                       "v": "5.130"}).json()
                for title_par_alb, value_par_alb in response_albums["response"].items():
                    if title_par_alb == "items":
                        for pos in value_par_alb:
                            for name_part, value_part in pos.items():
                                if name_part == "id":
                                    value_id = value_part
                                    value_ids.append(value_id)
                                    album = {"id_user": name_value, "album_id": value_ids}
                                    album_ids.append(album)
    return album_ids

def send_photos_data(token, yours_id):
    album_ids = send_albums_id(token, yours_id)
    users = send_personal_value(token, yours_id)
    photos = [ ]
    photos_data = [ ]
    count = []
    lider_photos = [ ]
    users_personal = [ ]
    gen_count = [ ]
    pop_photos = [ ]
    for part in album_ids:
        #for title_pos, id_value in part.items():
        for value_id in part["album_id"]:
            #if title_pos == "id_user":
                    response_photos = requests.get("https://api.vk.com/method/photos.get/",
                                           params={"owner_id": part["id_user"], "access_token": token, "album_id": value_id,
                                                   "extended": 1, "v": "5.130"}).json()
                    if "error" in response_photos:
                        continue
                    for element in response_photos["response"]["items"]:
                        data_photos = {"id_user": part["id_user"], "data_photos": photos}
                        for position_key, position_value in element.items():
                            if position_key == "sizes":
                                for ranger in position_value:
                                    for el_key, el_value in ranger.items():
                                        if el_key == "url":
                                            url = el_value
                            if position_key == "likes":
                                for el_key, el_value in position_value.items():
                                    if el_key == "count":
                                        like = el_value
                                        url_like = {url: like}
                                        photos.append(url_like)
    for element in data_photos["data_photos"]:
        for title_par, value_par in element.items():
            gen_count.append(value_par)
    gen_count.sort()
    gen_count.reverse()
    print(gen_count[0:4])
    for element in gen_count[0:4]:
        for pos in data_photos["data_photos"]:
            for tit_par, val_par in pos.items():
                if val_par == element:
                    lider_photos.append(pos)
    for position in lider_photos:
        for el in data_photos["data_photos"]:
            for key, value in position.items():
                for title_par, value_par in el.items():
                    if value != value_par:
                        data_photos["data_photos"].remove(el)
    for element in data_photos["data_photos"]:
        while data_photos["data_photos"].count(element) > 1:
            data_photos["data_photos"].remove(element)
    return data_photos







print(send_photos_data(token, yours_id))
