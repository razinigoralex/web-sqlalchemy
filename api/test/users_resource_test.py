from requests import post, delete, get

url = 'http://localhost:5000/api/v2/users'

# Получение всех пользователей
print(get(url).json())

# Некорректный запрос на создание пользователя: недостаточно данных
print(post(url,
           json={
               'id': 999,
               'surname': 'Pupkin',
               'name': 'Vasya'
           }).json())

# Корректный запрос на создание пользователя
print(post(url,
           json={
               'id': 999,
               'surname': 'Pupkin',
               'name': 'Vasya',
               'age': 17,
               'position': 'Biologist',
               'speciality': 'Exo-Biologist',
               'address': 'Colotushkina, Pushkina St, St Petersburg, Russia',
               'email': 'pupkin_vasya@gmail.com'
           }).json())

# Проверка, что пользователь добавился
print(get(url).json())

# Некорректный запрос на получение пользователя: несуществующий id
print(get(url + '/998').json())

# Корректный запрос на получение пользователя
print(get(url + '/999').json())

# Некорректный запрос на удаление пользователя: несуществующий id
print(delete(url + '/998').json())

# Корректный запрос на удаление пользователя
print(delete(url + '/999').json())

# Проверка, что пользователь удалился
print(get(url).json())
