import requests
import pytz
from datetime import datetime


def get_api_data(url, parameters=None):
    error = None
    init_page_data = None
    try:
        init_page_data = requests.get(
            url, params=parameters,
            timeout=10).json()
    except requests.exceptions.Timeout:
        error = "Connection timed out"
    except requests.exceptions.HTTPError:
        error = "Status code - " + init_page_data.status_code + " received"
    except requests.exceptions.ConnectionError:
        error = "Could not connect to API"
    except ValueError:
        error = "Can not decode JSON-data"
    return init_page_data, error


def load_users_from_pages():
    base_url = "https://devman.org/api/challenges/solution_attempts/"
    json_data, error = get_api_data(base_url)
    if error is not None:
        raise ValueError(error)
    page_count = json_data["number_of_pages"]
    for page in range(1, page_count+1):
        json_data, error = get_api_data(base_url, {"page": page})
        if error is not None:
            print("Error: \"{}\" occurred on page {}".format(error, page))
            continue
        for record in json_data.get("records"):
            yield record
    return None


def get_midnighters(*users):
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
    if load_users_from_pages():
        print("Midnighters:")
        for midnighter in get_midnighters(*load_users_from_pages()):
            print(midnighter)
    else:
        print("Could not get midnighters")
