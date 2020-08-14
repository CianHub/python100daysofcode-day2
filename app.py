from datetime import datetime
from datetime import timedelta
from pprint import pprint
import os
import urllib.request

SHUTDOWN_EVENT = 'Shutdown initiated'

# prep: read in the logfile
tmp = os.getenv("TMP", "/tmp")
logfile = os.path.join(tmp, 'log')
urllib.request.urlretrieve(
    'https://bites-data.s3.us-east-2.amazonaws.com/messages.log',
    logfile
)


def convert_to_datetime(line):
    index_of_first_num = -1
    line = line.split('supybot')[0].strip()
    for char in line:
        if char.isdigit():
            index_of_first_num = line.find(char)
            datetime_str = line[index_of_first_num:]
            datetime_str = datetime_str.replace('T', ' ')
            converted_datetime_str = datetime.strptime(
                datetime_str, '%Y-%m-%d %H:%M:%S')
            return converted_datetime_str


def time_between_shutdowns(loglines):
    shutdowns = filter(get_shutdowns, loglines)

    shutdown_list = []

    for x in shutdowns:
        shutdown_list.append(x)

    shutdown_init = get_first_shutdown_init(shutdown_list[:])
    shutdown_complete = get_last_shutdown_complete_event(
        shutdown_list[:])

    return shutdown_complete - shutdown_init


def get_first_shutdown_init(shutdowns):
    shutdown_init_events = filter(get_init_events, shutdowns)

    first_shutdown_init_event = None

    for line in shutdown_init_events:
        if first_shutdown_init_event == None:
            first_shutdown_init_event = convert_to_datetime(line)

        elif convert_to_datetime(line) < first_shutdown_init_event:
            first_shutdown_init_event = convert_to_datetime(line)

    return first_shutdown_init_event


def get_last_shutdown_complete_event(shutdowns):
    shutdown_complete_events = filter(get_complete_events, shutdowns)

    last_shutdown_complete_event = None

    for line in shutdown_complete_events:
        if last_shutdown_complete_event == None:
            last_shutdown_complete_event = convert_to_datetime(line)

        elif convert_to_datetime(line) > last_shutdown_complete_event:
            last_shutdown_complete_event = convert_to_datetime(line)

    return last_shutdown_complete_event


def get_shutdowns(line):
    if 'Shutdown' in line:
        return True
    else:
        return False


def get_complete_events(line):
    if 'complete.' in line:
        return True
    else:
        return False


def get_init_events(line):
    if 'Shutdown initiated' in line:
        return True
    else:
        return False


with open(logfile) as f:
    loglines = f.readlines()
    print(time_between_shutdowns(loglines))
