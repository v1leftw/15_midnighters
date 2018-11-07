import requests
import json
import pytz
from datetime import datetime, time


INIT_URL = "https://devman.org/api/challenges/solution_attempts/"


def get_json_data(url, parameters=None):
    error = None
    init_page_json_data = None
    init_page_data = None
    try:
        init_page_data = requests.get(
            url, params=parameters,
            timeout=10).content.decode("utf-8")
    except requests.exceptions.Timeout:
        error = "Connection timed out"
    except requests.exceptions.HTTPError:
        error = "Status code - " + init_page_data.status_code + " recieved"
    except requests.exceptions.ConnectionError:
        error = "Could not connect to API"

    if error is not None:
        return None, error

    try:
        init_page_json_data = json.loads(init_page_data)
    except json.decoder.JSONDecodeError:
        error = "Can not load JSON"
    return init_page_json_data, error


def load_users_from_pages():
    json_data, error = get_json_data(INIT_URL)
    if error is not None:
        raise ValueError(error)
    page_count = json_data["number_of_pages"]
    for page in range(1, page_count+1):
        json_data, error = get_json_data(INIT_URL, {"page": page})
        if error is not None:
            print("Error: \"{}\" occured on page {}".format(error, page))
            continue
        for record in json_data["records"]:
            yield record
    return None


def get_midnighters():
    midnighters = []
    for user in load_users_from_pages():
        user_tz = pytz.timezone(user["timezone"])
        dt = datetime.fromtimestamp(user["timestamp"], user_tz)
        if is_midnighter(dt.time()):
            midnighters.append(user["username"])
    if not midnighters:
        return None
    return set(midnighters)


def is_midnighter(user_time):
    night_start = time(0, 0, 0, 0)
    night_end = time(7, 0, 0, 0)
    if night_start < user_time < night_end:
        return True
    return False


if __name__ == "__main__":
    print("Searching midnighters...")
    if get_midnighters() is not None:
        print("Midnighters:")
        for midnighter in get_midnighters():
            print(midnighter)
    else:
        print("Could not get midnighters")
