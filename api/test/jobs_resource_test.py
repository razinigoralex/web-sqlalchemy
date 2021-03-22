from requests import get, post, delete

url = 'http://localhost:5000/api/v2/jobs'

# Получение всех работ
print(get(url).json())

# Некорректный запрос на создание работы: недостаточно данных
print(post(url,
           json={
               'id': 999,
               'team_leader': 1,
               'job': 'just testing'
           }).json())

# Корректный запрос на создание работы
print(post(url,
           json={
               'id': 999,
               'team_leader': 1,
               'job': 'just testing',
               'work_size': 120,
               'collaborators': '(2, 3)',
               'start_date': '30.02.2022 00:00',
               'end_date': '31.02.2022 00:00',
               'is_finished': False
           }).json())

# Проверка, что работа добавилась
print(get(url).json())

# Некорректный запрос на получение работы: несуществующий id
print(get(url + '/998').json())

# Корректный запрос на получение работы
print(get(url + '/999').json())

# Некорректный запрос на удаление работы: несуществующий id
print(delete(url + '/998').json())

# Корректный запрос на удаление работы
print(delete(url + '/999').json())

# Проверка, что работа удалилась
print(get(url).json())
