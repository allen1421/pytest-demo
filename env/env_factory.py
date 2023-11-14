import yaml
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'config', 'config-dev.yaml')


class ENV:
    with open(CONFIG_FILE_PATH) as file:
        try:
            dict = yaml.load(file, yaml.FullLoader)
            print(dict)
            user1 = dict["user1"]
            username = user1["username"]
            password = user1["password"]
            url = dict['url']
        except yaml.YAMLError as e:
            print(e)
