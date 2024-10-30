"""
Get all boxes from openSenseMap API for temperature phenomenon after a specific date.
"""
import os
import requests
from dotenv import load_dotenv
from src.get_proper_date import rfc3339_date

def get_boxes():
    """
    Get all boxes from the openSenseMap API
    """
    load_dotenv()
    url = os.getenv('SENSEBOX_API_URL')
    params = {
        'date': rfc3339_date,
        'phenomenon': 'temperature',
    }

    response = requests.get(url, params=params, timeout=60)

    if response.status_code == 200:
        boxes = response.json()
    else:
        print('Error: ', response.status_code)
        print(response.text)
        boxes = None

    return boxes