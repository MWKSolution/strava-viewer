"""Module for handling data in activities.json file."""
import os.path
import pandas as pd

# default activities file name
ACT_FILE = 'activities.json'


def acts_file_present():
    """Check if activities file is present."""
    return os.path.isfile(ACT_FILE)


def get_acts_from_file():
    """Get all activities from file and return them as dataframe."""
    _df = pd.read_json(ACT_FILE, orient='records')
    return _df


def get_types(_df):
    """Get all unique types of activities present in given dataframe and return them as a list."""
    _types = _df['type'].unique()
    return list(_types)


def get_options(_types):
    """Prepare options list as a parameter for dash dbc.Checklist options.Returns list of dictionaries."""
    _opts = []
    for _t in _types:
        _ts = str(_t)
        _opts.append({'label': _ts.capitalize(), 'value': _ts})
    return _opts

def get_years(_df):
    _ALL = ['All']
    _years = _df['year'].unique()
    _ALL.extend(_years)
    return _ALL

if __name__ == '__main__':
    # for testing
    if acts_file_present():
        df = get_acts_from_file()
        print(df.head())
        types = get_types(df)
        print(types)
        print(get_options(types))
        print(get_years(df))
    else:
        print(f'No "{ACT_FILE}" file!')

