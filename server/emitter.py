import requests, uuid, random, time

def generate_mock_emission():
    return {'vehicleId': str(uuid.uuid4()), 
            'vehicleType': random.choice(['bus', 'taxi', 'tram', 'train']),
            'latitude':round(random.uniform(-90, 90), 6),
            'longitude':round(random.uniform(-180, 180), 6),
            'timestamp': time.time(),
            'heading': random.randint(0, 359)}

url = 'http://127.0.0.1:5000/api/v1/emissions'
data = generate_mock_emission()
response = requests.post(url, json=data)

if response.ok:
    response.encoding = response.encoding if response.encoding else 'utf-8'
    total = response.json()['total']
    offset = response.json()['offset']
    limit = response.json()['limit']
    content = response.json()['data']

    for key in content:
        print key + ' : ' + content[key]

else:
    response.raise_for_status()