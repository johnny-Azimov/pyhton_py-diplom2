import requests
import time
from datetime import date, datetime
import sorting as s
from urllib.parse import urlencode

# ID моего приложения = 7361055
APP_ID = int(input('Введите ID приложения: '))
AUTH_URL = 'https://oauth.vk.com/authorize'
AUTH_DATA = {'client_id': APP_ID, 'display': 'page', 'scope': 'friends', 'response_type': 'token'}
print('Перейдите по ссылке ниже, скопируйте token и вставьте: ')
print('?'.join((AUTH_URL, urlencode(AUTH_DATA))))


TOKEN = input("Введите токен: ")


params = {
    'access_token': TOKEN,
    'v': 5.101
}

def get_user_friends():
    response = requests.get('https://api.vk.com/method/friends.get', params)
    print('-')
    friends_list = response.json()['response']['items']
    return friends_list


def get_user_groups():
    response = requests.get('https://api.vk.com/method/groups.get', params)
    print('-')
    groups_list = response.json()['response']['items']
    return groups_list


def get_user_info():
    params['fields'] = ['sex, city, bdate, music, books, interests']
    response = requests.get('https://api.vk.com/method/users.get', params)
    print('-')
    info = response.json()
    return info


def calculate_age(bdate):
    today = date.today()
    age = today.year - bdate.year
    if today.month < bdate.month:
        age -= 1
    elif today.month == bdate.month and today.day < bdate.day:
        age -= 1
    return age


def search_users(user_info):
    city_id = user_info['response'][0]['city']['id']
    sex = 2 if user_info['response'][0]['sex'] == 1 else 1
    bdate_str = user_info['response'][0]['bdate']
    try:
        bdate = datetime.strptime(bdate_str, "%d.%m.%Y")
        age = calculate_age(bdate)
        age_from = age - 2
        age_to = age + 2
    except ValueError:
        print("У подьзователя не указан год рождения")
        age = int(input('Введите ваш возраст'))
        age_from = age - 2
        age_to = age + 2
    params['age_from'] = [age_from]
    params['age_to'] = [age_to]
    params['count'] = [100]
    params['city'] = [city_id]
    params['sex'] = [sex]
    params['status'] = [1, 6]
    response = requests.get('https://api.vk.com/method/users.search', params)
    print('-')
    info = response.json()['response']['items']
    return info


def compare_friends_groups(users_list):
    result = []
    user_groups = get_user_groups()
    errors = 0
    for user in users_list:
        try:
            params['user_id'] = user['id']
            groups_list = get_user_groups()
            user_coincidences = {
                'id': user['id'],
                'matching_groups': [],
                'number_matching_groups': 0
            }
            for group in groups_list:
                if group in user_groups:
                    user_coincidences['matching_groups'].append(group)
                user_coincidences['number_matching_groups'] = len(user_coincidences['matching_groups'])
            result.append(user_coincidences)
        except KeyError:
            errors += 1
            continue
        finally:
            print('-')
            time.sleep(0.5)
    return result


def find_top3_photos(top10_users):
    for user in top10_users:
        params['user_id'] = user['id']
        params['album_id'] = ['profile']
        params['extended'] = [1]
        response = requests.get('https://api.vk.com/method/photos.get', params)
        profile_photos = response.json()['response']['items']
        top3 = s.find_top3(profile_photos)
        user['top3_photos'] = top3
        time.sleep(0.5)
    return top10_users

