from requests import get, delete

url = 'http://localhost:5000/api/jobs'
params = ('/999', '/16')

for i, param in enumerate(params):
    print(f'Тест №{i}:')
    print(delete(url + param).json())
    print(get(url).json())
