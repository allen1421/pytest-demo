import yaml


class ENV:
    with open(r"C:\Project\pytest-demo\config\config-dev.yaml") as file:
        try:
            dict = yaml.load(file, yaml.FullLoader)
            print(dict)
            user1 = dict["user1"]
            username = user1["username"]
            password = user1["password"]
            url = dict['url']
        except yaml.YAMLError as e:
            print(e)
