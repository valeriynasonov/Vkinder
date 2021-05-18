import requests
token = input("Введите токен")
yours_id = input("Введите Ваш id")
def send_data_yourself(token, id):
    response = requests.get("https://api.vk.com/method/users.get/",
                            params={"user_ids": id, "access_token": token, "fields": "sex, bdate, city, relation, personal",
                                    "v": "5.130"}).json()
    print(response)
    return response

def send_data_users(token, yours_id):
    response_sex = []
    sex = input("Введите пол пользователя")
    numbers = [177, 440]
    for n in numbers:
        response1 = requests.get("https://api.vk.com/method/users.get/",
                                    params={"user_ids": n, "access_token": token,
                                            "fields": "sex, bdate, city, relation, personal", "v": "5.130"}).json()
        print(response1)
        for params1 in response1["response"]:
            for name_of_param1, value_of_param1 in params1.items():
                if name_of_param1 == "sex" and "жен" in sex:
                    if value_of_param1 == 1:
                        response_sex.append(response1)
                elif name_of_param1 == "sex" and "муж" in sex:
                    if value_of_param1 == 2:
                        response_sex.append(response1)
    return response_sex

def send_data_bdate(token, yours_id):
    response = send_data_yourself(token, yours_id)
    response_sex = send_data_users(token, yours_id)
    response_sex_bdate = [ ]
    bdate1 = " "
    bdate2 = " "
    bdate_user = " "
    for datas in response["response"]:
        for name_data, value_data in datas.items():
            if name_data == "bdate":
                bdate1 = value_data.split(".")
                if len(bdate1) == 3:
                    bdate_user = int(bdate1[2])
                else:
                    return "Невозможно определить дату рождения"
    for character in response_sex:
        for list_of_params in character["response"]:
            for title_param, value_param in list_of_params.items():
                if title_param == "bdate":
                    bdate2 = value_param.split(".")
                    if len(bdate2) == 3:
                        bdate_friend = int(bdate2[2])
                        if bdate_user < bdate_friend:
                            delt = bdate_friend - bdate_user
                        elif bdate_user > bdate_friend:
                            delt = bdate_user - bdate_friend
                            if delt < 5 or bdate_user == bdate_friend:
                                list_of_params["delt"] = delt
                                response_sex_bdate.append(character)
                            elif delt > 5:
                                continue
    print(response_sex_bdate)
    if len(response_sex_bdate) != 0:
        return response_sex_bdate
    else:
        return "Невозможно определить дату рождения потенциальных друзей"

def send_users_relation(token, yours_id):
    response_sex_bdate = send_data_bdate(token, yours_id)
    print(response_sex_bdate)
    if "Невозможно определить дату рождения" in response_sex_bdate:
        response_sex = send_data_users(token, yours_id)
        response_sex_relation = []
        for character in response_sex:
            for list_of_params in character["response"]:
                for title_param, value_param in list_of_params.items():
                    if title_param == "relation":
                        if value_param == 0:
                            response_sex_relation.append(character)
        return response_sex_relation
    else:
        response_sex_relation = []
        print(response_sex_bdate)
        for character in response_sex_bdate:
            for list_of_params in character["response"]:
                for title_param, value_param in list_of_params.items():
                    if title_param == "relation":
                        if value_param == 0:
                            response_sex_relation.append(character)
    return response_sex_relation


def send_users_city(token, yours_id):
    response = send_data_yourself(token, yours_id)
    response_sex_relation = send_users_relation(token, yours_id)
    response_city = [ ]
    for character in response_sex_relation:
        for list_of_params in character["response"]:
            for params in response["response"]:
                for title_param, value_param in list_of_params.items():
                    for name_of_param, value_of_param in params.items():
                        if name_of_param == "city" and title_param == "city":
                            if value_of_param == value_param:
                                response_city.append(character)
    return response_city

def send_personal_value(token, yours_id):
    response = send_data_yourself(token, yours_id)
    response_city = send_users_city(token, yours_id)
    users_personal = [ ]
    #personal_value = [ ]
    for character in response_city:
        for params1 in character["response"]:
            for params in response["response"]:
                personal_value = [ ]
                for title_param, value_param1 in params1.items():
                    for name_param, value_param in params.items():
                        if title_param == "personal" and name_param == "personal":
                            for name_personal, value_personal1 in value_param1.items():
                                for title_personal, value_personal in value_param.items():
                                    if name_personal == title_personal:
                                        if value_personal1 == value_personal:
                                            personals_data = {"id": params1["id"], "personal": personal_value}
                                            personal_value.append(name_personal)
                                            print(personals_data)
                                            if len(personal_value) >= 3:
                                                inform_user = {"first_name": params1["first_name"], "last_name": params1["last_name"], "id": params1["id"]}
                                                users_personal.append(inform_user)
    print(personals_data)
    for position in users_personal:
        while users_personal.count(position) > 1:
            users_personal.remove(position)
    return users_personal

print(send_personal_value(token, yours_id))









