import requests
from urllib3 import disable_warnings, exceptions
from yaml import safe_load
from json import dump, dumps
from datetime import datetime

disable_warnings(exceptions.InsecureRequestWarning)

URL_TOKEN = "https://www.strava.com/oauth/token"
URL_STRAVA = "https://www.strava.com/api/v3/athlete"

with open('token.yaml') as yaml_file:
    token_data = safe_load(yaml_file)


def request_access_token():
    print("Requesting Token...\n")
    res = requests.post(URL_TOKEN, data=token_data, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))
    return access_token


def check_athlete(_token):
    header = {'Authorization': 'Bearer ' + _token}
    athlete = requests.get(URL_STRAVA, headers=header).json()
    print(dumps(athlete, indent=True))


def get_activities(_token):
    act_list = []
    page = 1
    while True:
        print(page)
        header = {'Authorization': 'Bearer ' + _token}
        param = {'per_page': 100, 'page': page}
        activities = requests.get(URL_STRAVA + '/activities', headers=header, params=param).json()
        if not activities: break
        for act in activities:
            act_id = act['id']
            act_distance = act['distance'] / 1000  # in km
            act_time = act['elapsed_time'] / 3600  # in h with decimals after '.'  (not getting mins and secs for now)
            act_type = act['type']
            act_gain = act['total_elevation_gain']  # in m
            act_date = act['start_date']
            dt_obj = datetime.strptime(act_date, '%Y-%m-%dT%H:%M:%SZ')
            act_list.append({'id': act_id,
                             'date': {'year': dt_obj.year, 'month': dt_obj.month, 'day': dt_obj.day},
                             'type': act_type,
                             'time': act_time,
                             'distance': act_distance,
                             'gain': act_gain})
        page += 1
    with open('activities.json', 'w') as json_file:
        dump(act_list, json_file)


if __name__ == '__main__':
    token = request_access_token()
    check_athlete(token)
    get_activities(token)
