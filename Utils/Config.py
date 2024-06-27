import json
import random


class Config:

    def get_api_key(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        # randomly generate a number 0 to 100
        return data['api_keys'][random.randint(0, len(data['api_keys']) - 1)]

    def get_proxy_url(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        return data['proxy']['url']

    def is_proxy_on(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        return data['proxy']['on']

    def is_api_proxy_on(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        return data['api_proxy']['on']

    def get_api_proxy_url(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        return data['api_proxy']['url']
    
    def get_access_key_id(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        return data['ACCESS_KEY_ID']
    
    def get_access_key_secret(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        return data['ACCESS_KEY_SECRET']
    
    def get_app_id(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        return data['APP_ID']
    
    def get_room_owner_auth_code(self):
        with open("config.json", "r") as f:
            data = json.loads(f.read())
        return data['ROOM_OWNER_AUTH_CODE']
