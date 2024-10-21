import requests
from src.get_proper_date import rfc3339_date

def get_boxes():
    """
    Get all boxes from the openSenseMap API
    """
    url = 'https://api.opensensemap.org/boxes'
    params = {
        'date': rfc3339_date,
        'phenomenon': 'temperature',
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        boxes = response.json()
    else:
        print('Error: ', response.status_code)
        print(response.text)
        boxes = None

    return boxes