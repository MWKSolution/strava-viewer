from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from json import dump, load, loads, dumps
import operator as op
from yaml import safe_load
from redis import Redis
# :todo: requirements.txt !


class NotValidConnection(Exception):
    pass


class Connection(ABC):

    @abstractmethod
    def get_activities(self):
        pass

    @abstractmethod
    def save_data(self, acts, mode):  # mode = 'overwrite', 'append'
        pass

    @abstractmethod
    def is_data_present(self):
        pass


class JsonFile(Connection):
    ACT_FILE = Path(__file__).parent / 'local/activities.json'

    def save_data(self, acts, mode):
        _acts = []
        if mode == 'append':
            if self.is_data_present():
                with open(self.ACT_FILE, 'r') as json_file:
                    _acts = load(json_file)
        _acts.extend(acts)
        _acts.sort(key=op.itemgetter('timestamp'), reverse=True)  # descending order by timestamp
        with open(self.ACT_FILE, 'w') as json_file:
            dump(_acts, json_file)

    def get_activities(self):
        _df = pd.read_json(self.ACT_FILE, orient='columns', convert_dates=False)
        return _df

    def is_data_present(self):
        return self.ACT_FILE.exists()


class RedisDB(Connection):
    REDIS_YAML = Path(__file__).parent / 'secret/redis.yaml'

    def __init__(self):
        with open(self.REDIS_YAML) as yaml_file:
            self.ACCESS = safe_load(yaml_file)
        self.r = Redis(host=self.ACCESS['host'],
                       port=self.ACCESS['port'],
                       username=self.ACCESS['username'],
                       password=self.ACCESS['password'])

    def get_activities(self):
        data = loads(self.r.get('acts'))
        _df = pd.DataFrame.from_dict(data, orient='columns')
        return _df

    def save_data(self, acts, mode):
        _acts = []
        if mode == 'append':
            if self.is_data_present():
                r_acts = self.r.get('acts')
                _acts = loads(r_acts)
        _acts.extend(acts)
        _acts.sort(key=op.itemgetter('timestamp'), reverse=True)  # descending order by timestamp
        self.r.set('acts', dumps(_acts))

    def is_data_present(self):
        return self.r.exists('acts')


if __name__ == '__main__':
    b = RedisDB()
    print(b.r.dbsize(), b.r.keys())
    a = JsonFile()
