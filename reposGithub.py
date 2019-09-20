import requests
from pprint import pprint
import json
head = {'User-agent': 'Chrome/77.0.3865.7'}
main_link = 'https://api.github.com'
user = 'JuliaDav'
repos = 'repos'

req = requests.get(f'{main_link}/users/{user}/{repos}',headers=head)

if req.ok:
    data = json.loads(req.text)
    print(f'Список репозиториев пользователя {user}:')
    i = 0
    while i < len(data):
        pprint(data[i]['url'])
        i += 1


