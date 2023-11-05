from django.core.management.base import BaseCommand
from newsapp.api_key import API_KEY
from django.conf import settings
import os

# Sample list of API keys
API_KEYS = [
   "fde47eb1fd3c4768964eb3d3bd9eaae2",
   "7dfa405963a9460693136651c8006b36",
   "dbb12ae7153a417b85f1b3ea8f8bfe6e",
]

# Initialize a variable to keep track of the currently used key
current_key_index = 0
used_keys = set()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = settings.BASE_DIR  # Use the Django project's base directory

# Construct the full file path for the API key file
API_KEY_FILE = os.path.join(BASE_DIR, 'newsapp', 'api_key.py')

# In your custom management command
class Command(BaseCommand):
    help = 'Rotate the API key'

    def handle(self, *args, **options):
        global API_KEY  # Declare API_KEY as a global variable
        new_api_key = select_new_api_key()  # Get a new key from the array
        if new_api_key:
            # Update the global API_KEY variable with the new API key
            API_KEY = new_api_key
            
            # Write the updated API_KEY back to the file
            with open(API_KEY_FILE, 'w') as api_key_file:
                api_key_file.write(f"API_KEY = '{new_api_key}'\n")

            self.stdout.write(self.style.SUCCESS('API key rotation complete.'))
        else:
            self.stdout.write(self.style.WARNING('No unused API keys available.'))


def select_new_api_key():
    global current_key_index  # Access the global index variable
    while current_key_index < len(API_KEYS):
        new_key = API_KEYS[current_key_index]
        # Check if the key has been used already
        if not key_already_used(new_key):
            return new_key
        current_key_index += 1  # Move to the next key
    return None  # No unused keys available

def key_already_used(key):
    # Check if the key is in the set of used keys
    if key in used_keys:
        return True
    else:
        # Mark the key as used by adding it to the set
        used_keys.add(key)
        return False