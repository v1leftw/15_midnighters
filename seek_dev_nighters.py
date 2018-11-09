import requests
import pytz
from datetime import datetime


def get_api_data(url, parameters=None):
    error = None
    api_data = None
    try:
        api_data = requests.get(
            url, params=parameters,
            timeout=10).json()
    except requests.exceptions.Timeout:
        error = "Connection timed out"
    except requests.exceptions.HTTPError:
        error = "Status code - {} received".format(api_data.status_code)
    except requests.exceptions.ConnectionError:
        error = "Could not connect to API"
    except ValueError:
        error = "Can not decode JSON-data"
    return api_data, error


def load_users_from_pages():
    base_url = "https://devman.org/api/challenges/solution_attempts/"
    page = 1
    while True:
        api_data, error = get_api_data(base_url, {"page": page})
        if error is not None:
            print("Error: '{}' occurred on page {}".format(error, page))
            break
        for record in api_data.get("records"):
            yield record
        page += 1
        if page > api_data.get("number_of_pages"):
            break


def get_midnighters(users):
    midnighters = []
    for user in users:
        if check_user(user):
            midnighters.append(user["username"])
    return set(midnighters)


def check_user(user):
    user_tz = pytz.timezone(user["timezone"])
    dt = datetime.fromtimestamp(user["timestamp"], user_tz)
    if is_midnighter(dt.hour):
        return user


def is_midnighter(user_time):
    night_start_hour = 0
    night_end_hour = 7
    if night_start_hour <= user_time < night_end_hour:
        return True
    return False


if __name__ == "__main__":
    print("Searching midnighters...")
    is_any_midnighter_exist = False
    for midnighter in get_midnighters(load_users_from_pages()):
        is_any_midnighter_exist = True
        print("got midnighter: {}".format(midnighter))
    if not is_any_midnighter_exist:
        print("No midnighters found")
