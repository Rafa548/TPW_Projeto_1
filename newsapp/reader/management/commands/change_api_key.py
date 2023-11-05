from django.core.management.base import BaseCommand
from newsapp.api_key import API_KEY
from django.conf import settings
import os
import requests

API_KEYS = [
   "fde47eb1fd3c4768964eb3d3bd9eaae2",
   "7dfa405963a9460693136651c8006b36",
   "dbb12ae7153a417b85f1b3ea8f8bfe6e",
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = settings.BASE_DIR  

API_KEY_FILE = os.path.join(BASE_DIR, 'newsapp', 'api_key.py')


class Command(BaseCommand):
    help = 'Rotate the API key'

    def handle(self, *args, **options):
        global API_KEY  # Declare API_KEY as a global variable
        new_api_key = select_new_api_key()  
        if new_api_key:
            API_KEY = new_api_key
            with open(API_KEY_FILE, 'w') as api_key_file:
                api_key_file.write(f"API_KEY = '{new_api_key}'\n")
            self.stdout.write(self.style.SUCCESS('API key change complete.'))
            self.stdout.write(self.style.SUCCESS(f'New API key: {new_api_key}'))
        else:
            self.stdout.write(self.style.WARNING('No unused API keys available.'))

    
def select_new_api_key():
    global API_KEY  
    current_key_index = API_KEYS.index(API_KEY)
    if is_rate_limited(API_KEY):
        next_key_index = (current_key_index + 1) % len(API_KEYS)
    else:
        return API_KEY

    for _ in range(len(API_KEYS)):
        next_key = API_KEYS[next_key_index]
        if not is_rate_limited(next_key):
            return next_key
        next_key_index = (next_key_index + 1) % len(API_KEYS)

    return None

def is_rate_limited(api_key):
    url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us",1,api_key
            )
    response = requests.get(url)
    if response.status_code == 429:  # HTTP 429 indicates rate limiting
        print(f"API key {api_key} is rate limited.")
        return True
    return False
