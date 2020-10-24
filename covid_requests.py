import requests

endpoint = 'https://covid-19-greece.herokuapp.com/'


def get_covid19_data(resource):
    r = requests.get(endpoint + resource)
    return r


def get_total_tests():
    r = get_covid19_data('total-tests')
    if r.status_code != 200:
        data = []
    else:
        data = r.json()['total_tests']
    return data


def get_confirmed_cases():
    r = get_covid19_data('confirmed')
    if r.status_code != 200:
        data = []
    else:
        data = r.json()['cases']
    return data
