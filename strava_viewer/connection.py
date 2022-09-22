from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from json import dump, load
import operator as op


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


class Json(Connection):
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
        _df = pd.read_json(self.ACT_FILE, orient='records')
        return _df

    def is_data_present(self):
        return self.ACT_FILE.exists()


class Redis(Connection):
    ACT_REDIS = '...'

    def get_activities(self):
        pass

    def save_data(self, acts, mode):
        pass

    def is_data_present(self):
        pass


if __name__ == '__main__':
    b = Redis()
    a = Json()
