#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import argparse
import re
from sys import stderr


class HTTPGeneralException(Exception):
    """
    Exception для обработки ошибок обращения к API
    """
    pass


def GitHubAPIRequest(url, creds=''):
    """
    Функция отправляет GET запрос к api.github.com и в случае успеха
    возвращает разобранный json в ввиде списка словарей.

    Аргументы:
    url - URI запроса без '/' в начале
    creds - (Необязательный) учётные данные для авторизованного доступа
            к GitHub API в виде логин:пароль. Позволяют делать больше запросов.
    """

    # Учётку будем подставлять прямо в uri, а не передавать через auth=
    if creds != '':
        creds = creds + '@'

    # Отправляем наш запрос
    response = requests.get(f'https://{creds}api.github.com/{url}')

    # Если сервер ответил статус 200 OK, возвращаем спрасенный JSON
    if response.status_code == 200:
        return json.loads(response.content)
    # Во всех остальных случаях выкидывам Exception
    else:
        message = json.loads(response.content)['message']
        raise HTTPGeneralException(
                f"(GET /{url} HTTP response code: {response.status_code})\n" +
                message)


def GetReposByUser(user, creds=''):
    """
    Получаем генератор списка репозиториев пользователя user.
    Если указанный пользователь не существует,
    функция GitHubAPIRequest выкинет Exception.

    Можно задать учётные данные через аргумент creds.
    """
    repos = GitHubAPIRequest(f'users/{user}/repos', creds)
    for repo in repos:
        yield repo['name']


def GetIssuesByUserRepo(user, repo, creds=''):
    """
    Получаем issues из репозитория repo пользователя user.
    Если указанный пользователь, или репозиторий не существует,
    функция GitHubAPIRequest выкинет Exception.
    Функция возвращает генератор списка кортежей вида (number, title)

    Можно задать учётные данные через аргумент creds.
    """

    issues = GitHubAPIRequest(f"repos/{user}/{repo}/issues", creds)
    for iss in issues:
        yield (iss['number'], iss['title'])


def GithubCredsType(arg_value,
                    pat=re.compile(r"^[a-zA-Z0-9\-]{0,39}\:[a-f0-9]{40}$")):
    """
    Функция для проверки аргумента --creds.
    Если формат соответствует валидной паре логин:токен, возвращаем аргумент,
    иначе выкидываем Exception.

    Передача пароля через командную строку
    создает предпосылки для его компрометации.
    """

    if not pat.match(arg_value) and arg_value != '':
        raise argparse.ArgumentTypeError
    return arg_value


def main():
    # конфигурируем ArgumentParser
    parser = argparse.ArgumentParser()
    # по-умолчанию запрашиваем issues у юзера devopshq
    parser.add_argument("-u", "--user", type=str, default='devopshq', help='''
                        You can define github account instead of "devopshq".
                        ''')
    parser.add_argument("-r", "--repo", type=str, default='',
                        help='Also you can specify repository.')
    parser.add_argument("-c", "--creds", type=GithubCredsType, default='',
                        help='Access credentials in format "login:token".')

    args = parser.parse_args()

    try:
        # по-умолчанию проходимся по всем репозиториям пользователя
        if args.repo == '':
            reps = GetReposByUser(args.user, args.creds)
        # если задан конкретный репозиторий, получаем issues с него
        else:
            reps = [args.repo]
        # выводим список issues в соответствии с заданием
        for repo in reps:
            print(f'{repo}:\n')
            for (inumber, ititle) in GetIssuesByUserRepo(args.user,
                                                         repo, args.creds):
                print(f'#{inumber} {ititle}')
            print('')
    # если что-то пошло не так, выводим ошибку
    except HTTPGeneralException as e:
        print('Query failed: {}'.format(str(e)), file=stderr)
        return 2
    else:
        return 0


if __name__ == "__main__":
    main()
