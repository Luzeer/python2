import json
import urllib.request


def choose_user(user_list):
    print(*user_list, sep=', ', end='\n\n')
    while True:
        print('please enter user-name from list above')
        user_name = input()
        if user_name in user_list:
            return user_name


def get_repos(profile, token):
    data = None
    url = 'https://api.github.com/users/%s/repos?access_token=%s' % (profile, token)
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    data = json.loads(text)
    repo_name_descr = []
    for repo_info in data:
        repo_name_descr.append((repo_info['name'], repo_info['description']))
    return repo_name_descr


def print_repos(repos):
    for rep in repos:
        if (rep[1] == 'None'):
            rep[1] = ''
        print(rep[0], ':', rep[1])

def count_lang(profile, token):
    data = None
    url = 'https://api.github.com/users/%s/repos?access_token=%s' % (profile, token)
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    data = json.loads(text)
    lang_dict = {}
    for rep in data:
        lang_dict[rep['language']] = lang_dict.get(rep['language'], 0) + 1
    return lang_dict

def get_biggest(user_list, token):
    max_amount = 0
    profile = None
    for user_name in user_list:
        url = 'https://api.github.com/users/%s/repos?access_token=%s' % (user_name, token)
        response = urllib.request.urlopen(url)
        text = response.read().decode('utf-8')
        data = json.loads(text)
        if (len(data) > max_amount):
            max_amount = len(data)
            profile = user_name
    return profile, max_amount

import operator

def get_popular_lang(user_list, token):
    res_dict = {}
    for user in user_list:
        temp_dict = count_lang(user, token)
        for key, value in temp_dict.items():
            res_dict[key] = res_dict.get(key, 0) + value
    popular_lang = max(res_dict, key=res_dict.get)
    return popular_lang

def get_followers(user_list, token):
    max_followers = 0
    profile = None
    for user in user_list:
        url = 'https://api.github.com/users/%s/followers?access_token=%s' % (user, token)
        response = urllib.request.urlopen(url)
        text = response.read().decode('utf-8')
        data = json.loads(text)
        if (len(data) > max_followers):
            max_followers = len(data)
            profile = user
    return user

def main():
    profile = choose_user(user_list)
    print('\nВы выбрали пользователя', profile)

    print_repos(get_repos(profile, '130ec820a0c84b277b2d9e3b3becb13cdb5df9e1'))  # 1

    print('\nЯзыки в репозиториях пользователя', profile, '\n',
          count_lang(profile, '130ec820a0c84b277b2d9e3b3becb13cdb5df9e1'))  # 2

    print('\n Больше всего репозиториев из списка у пользователя',
          get_biggest(user_list, '130ec820a0c84b277b2d9e3b3becb13cdb5df9e1')[0])  # 3

    print('\n Самый популярный язык среди пользователей это',
          get_popular_lang(user_list, '130ec820a0c84b277b2d9e3b3becb13cdb5df9e1'))  # 4

    print('\n Больше всего подписчиков у пользователя',
          get_followers(user_list, '130ec820a0c84b277b2d9e3b3becb13cdb5df9e1'))  # 5