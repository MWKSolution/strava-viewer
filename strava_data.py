"""Module for importing data from Strava"""
import requests
from urllib3 import disable_warnings, exceptions
from yaml import safe_load
from json import dump, dumps, load
from datetime import datetime
from activities import ACT_FILE

disable_warnings(exceptions.InsecureRequestWarning)

URL_TOKEN = "https://www.strava.com/oauth/token"
URL_STRAVA = "https://www.strava.com/api/v3/athlete"

# Reading personal data from yaml file - see README.md
with open('token.yaml') as yaml_file:
    TOKEN_DATA = safe_load(yaml_file)


def request_access_token():
    """Returns access_token for use in other requests. Access_token is expiring, so it needs to be refreshed!"""
    res = requests.post(URL_TOKEN, data=TOKEN_DATA, verify=False)
    access_token = res.json()['access_token']
    return access_token


def check_athlete(_token):
    """Check information about athlete and return it as string"""
    header = {'Authorization': 'Bearer ' + _token}
    athlete = requests.get(URL_STRAVA, headers=header).json()
    return dumps(athlete, indent=True)


def get_activities(_token):
    """Get all activities of athlete page by page using Strava API. Returns data as list of dictionaries (json)
    Only subset of parameters is returned."""
    act_list = []
    page = 1
    while True:
        header = {'Authorization': 'Bearer ' + _token}
        param = {'per_page': 100, 'page': page}
        activities = requests.get(URL_STRAVA + '/activities', headers=header, params=param).json()
        if not activities:
            break
        for act in activities:
            act_id = act['id']
            act_distance = act['distance'] / 1000  # in km
            act_time = act['elapsed_time'] / 3600  # in h with decimals after '.'  (so it could be summed then)
            act_type = act['type']
            act_gain = act['total_elevation_gain']  # in m
            act_date = act['start_date']            # date is split into year, month and day
            dt_obj = datetime.strptime(act_date, '%Y-%m-%dT%H:%M:%SZ')
            act_list.append({'id': act_id,
                             'year': dt_obj.year,
                             'month': dt_obj.month,
                             'day': dt_obj.day,
                             'type': act_type,
                             'time': act_time,
                             'distance': act_distance,
                             'gain': act_gain})
        page += 1
    return act_list


def dump_acts_to_file(acts):
    """Save given activities (json) to file to be used in callbacks."""
    with open(ACT_FILE, 'w') as json_file:
        dump(acts, json_file)


if __name__ == '__main__':
    # For testing
    token = request_access_token()
    print(check_athlete(token))
    print('Wait...')
    activities = get_activities(token)
    dump_acts_to_file(activities)
    with open(ACT_FILE, 'r') as json_file:
        acts = load(json_file)
    print(dumps(acts[0]))  # print only first record
