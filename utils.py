import time
import re
import json


def get_current_time_millis():
    return time.time_ns() // 1000000


def validate_json(string: str):
    return bool(re.match(r'\{.+\}', string))


def load_json_safe(string: str):
    if validate_json(string):
        try:
            return json.loads(string)
        except json.decoder.JSONDecodeError:
            pass
    return {}


def debug_log(*args, **kwargs):
    print('Debug:', *args, **kwargs)
