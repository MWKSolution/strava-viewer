"""Module for importing data from Strava"""
import requests
from os.path import isfile
from pathlib import Path
from urllib3 import disable_warnings, exceptions
from yaml import safe_load
from json import dump, dumps, load
from datetime import datetime
import pandas as pd
from strava_viewer.activities_options import get_options
from strava_viewer.layouts import get_chart

disable_warnings(exceptions.InsecureRequestWarning)


class StravaData:
    URL_TOKEN = "https://www.strava.com/oauth/token"
    URL_STRAVA = "https://www.strava.com/api/v3/athlete"
    SECRET_TOKEN = Path(__file__).parent / 'secret/token.yaml'
    ACT_FILE = Path(__file__).parent / 'local/activities.json'
    ACT_REDIS = '...'

    def __init__(self, data='local'):
        """'local' - local/activities.json
        'redis' - redis database"""
        self.DATA = data
        self.TOKEN_DATA = None
        self.ACCESS_TOKEN = None
        self.LATEST_ACTIVITY = 0
        # Reading personal data from yaml file - see README.md
        with open(self.SECRET_TOKEN) as yaml_file:
            self.TOKEN_DATA = safe_load(yaml_file)

    def reload_all_dataAPI(self):
        """Reload all data - overwrite existing data"""
        self.request_access_tokenAPI()
        _acts = self.get_all_activitiesAPI()
        self.save_all_data(_acts)

    def refresh_dataAPI(self):
        self.request_access_tokenAPI()
        _acts = self.get_new_activitiesAPI()
        self.save_new_data(_acts)

    def get_new_activitiesAPI(self):
        """Refresh data - load only new data. Check last date in data - load only new entries"""
        act_list = []
        page = 1
        while True:
            header = {'Authorization': 'Bearer ' + self.ACCESS_TOKEN}
            param = {'after': self.LATEST_ACTIVITY, 'per_page': 100, 'page': page}
            activities = requests.get(self.URL_STRAVA + '/activities',
                                      headers=header,
                                      params=param).json()
            if activities:
                act_list.extend(self.get_page_of_activities(activities))
            else:
                break
            page += 1

        self.LATEST_ACTIVITY = max((t['timestamp'] for t in act_list))

        return act_list


    def request_access_tokenAPI(self):
        """Returns access_token for use in other requests. Access_token is expiring, so it needs to be refreshed!"""
        res = requests.post(self.URL_TOKEN,
                            data=self.TOKEN_DATA,
                            verify=False)
        access_token = res.json()['access_token']
        self.ACCESS_TOKEN = access_token

    def check_athleteAPI(self):
        """Check information about athlete and return it as string."""
        header = {'Authorization': 'Bearer ' + self.ACCESS_TOKEN}
        athlete = requests.get(self.URL_STRAVA,
                               headers=header).json()
        return dumps(athlete, indent=True)

    @staticmethod
    def get_page_of_activities(activities):
        partial_act_list = []
        if not activities:
            return []
        for act in activities:
            act_id = act['id']
            act_distance = act['distance'] / 1000  # in km
            act_time = act['elapsed_time'] / 3600  # in h with decimals after '.'  (so it could be summed then)
            act_type = act['type']
            act_gain = act['total_elevation_gain']  # in m
            act_date = act['start_date']  # date is split into year, month and day
            dt_obj = datetime.strptime(act_date, '%Y-%m-%dT%H:%M:%SZ')
            timestamp = int(dt_obj.timestamp())
            partial_act_list.append({'id'       : act_id,
                                     'year'     : dt_obj.year,
                                     'month'    : dt_obj.month,
                                     'day'      : dt_obj.day,
                                     'type'     : act_type,
                                     'time'     : act_time,
                                     'distance' : act_distance,
                                     'gain'     : act_gain,
                                     'timestamp': timestamp})
        return partial_act_list

    def get_all_activitiesAPI(self):
        """Get all activities of athlete page by page using Strava API. Returns data as list of dictionaries (json)
        Only subset of parameters is returned. Format:
        [
         {
          "id": xxxxxxxxxxx,
          "year": xxxx,
          "month": x,
          "day": xx,
          "type": "xxxx",
          "time": xxxxxx,
          "distance": xxxx,
          "gain": xxxx
         }, ... ]"""
        act_list = []
        page = 1
        while True:
            header = {'Authorization': 'Bearer ' + self.ACCESS_TOKEN}
            param = {'per_page': 100, 'page': page}
            activities = requests.get(self.URL_STRAVA + '/activities',
                                      headers=header,
                                      params=param).json()
            if activities:
                act_list.extend(self.get_page_of_activities(activities))
            else:
                break
            page += 1

        self.LATEST_ACTIVITY = max((t['timestamp'] for t in act_list))

        return act_list

    def save_all_data(self, _acts):
        if self.DATA == 'local':
            """Save given activities (json) to file to be used in callbacks."""
            with open(self.ACT_FILE, 'w') as json_file:
                dump(_acts, json_file)
        else:
            pass

    def save_new_data(self, new_acts):
        if self.DATA == 'local':
            """Save given activities (json) to file to be used in callbacks."""
            if self.acts_data_present():
                with open(self.ACT_FILE, 'r') as json_file:
                    _acts = load(json_file)
            else:
                _acts = []
            _acts.extend(new_acts)
            with open(self.ACT_FILE, 'w') as json_file:
                dump(_acts, json_file)
        else:
            pass

    def get_activitiesDATA(self):
        """Get all activities from file or redis and return them as dataframe."""
        if self.DATA == 'local':
            _df = pd.read_json(self.ACT_FILE, orient='records')
        else:
            _df = pd.DataFrame()
        self.LATEST_ACTIVITY = _df['timestamp'].max()
        return _df

    def acts_data_present(self):
        """Check if activities data is present."""
        if self.DATA == 'local':
            return isfile(self.ACT_FILE)
        else:
            pass

    def get_optionsDATA(self):
        df = self.get_activitiesDATA()
        return get_options(df)

    def get_chartDATA(self, metrics, activity, year):
        df = self.get_activitiesDATA()
        if year != 'All':
            df = df[df['year'] == int(year)]
        df = df[df['type'].isin(activity)]
        return get_chart(df, metrics, activity, year)


if __name__ == '__main__':
    # For testing
    data = StravaData()
    data.request_access_tokenAPI()
    # print(data.check_athleteAPI())
    print('Wait...')
    activities = data.get_all_activitiesAPI()
    data.save_all_data(activities)
    data.LATEST_ACTIVITY = 1663230452
    acts = data.get_new_activitiesAPI()
    print(dumps(acts[0:5], indent=5))
    data.save_new_data(acts)
    with open(data.ACT_FILE, 'r') as json_file:
        acts = load(json_file)
    print(dumps(acts[0:5], indent=5))  # print only first record
    print(data.LATEST_ACTIVITY)
