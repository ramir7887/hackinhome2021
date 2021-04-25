import json


class Config:

    @staticmethod
    def get_config(path='config.json'):
        with open(path, "r") as config_file:
            config = json.load(config_file)
        return config

    #config = get_config()
    print('Use Config class')