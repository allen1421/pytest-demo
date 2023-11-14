import yaml
import os


class ENV:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(BASE_DIR + r'\config\config-dev.yaml') as file:
        try:
            dict = yaml.load(file, yaml.FullLoader)
            print(dict)
            user1 = dict["user1"]
            username = user1["username"]
            password = user1["password"]
            url = dict['url']
        except yaml.YAMLError as e:
            print(e)
