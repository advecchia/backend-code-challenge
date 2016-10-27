import requests

url = 'http://127.0.0.1:5000/collect/'
data = {'data':'any String', 'anyData':'another data'}
response = requests.post(url, data=data)

if response.ok:
    response.encoding = response.encoding if response.encoding else 'utf-8'
    content = response.json()['content']

    for key in content:
        print key + ' : ' + content[key]

else:
    response.raise_for_status()