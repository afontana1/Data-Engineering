"""Config class"""

import json


class Config:
    """Config class which contains data, train and model hyperparameters"""

    def __init__(self, data, train, output):
        self.data = data
        # self.datapath = os.path.
        self.train = train
        self.output = output

    @classmethod # using config to define constructor of the class
    def from_json(cls, cfg):
        """Creates config from json"""
        params = json.loads(json.dumps(cfg), object_hook=HelperDict)
        # init all class instance with data and train attributes
        return cls(params.data, params.train, params.output) 


class HelperDict(object):
    """Helper class to convert json into Python object"""
    def __init__(self, dict_):
        self.__dict__.update(dict_)