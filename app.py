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
    shutdowns = filter(get_init_events, loglines)

    shutdown_list = []

    for x in shutdowns:
        shutdown_list.append(x)

    return convert_to_datetime(shutdown_list[1]) - convert_to_datetime(shutdown_list[0])


def get_init_events(line):
    if 'Shutdown initiated' in line:
        return True
    else:
        return False


with open(logfile) as f:
    loglines = f.readlines()
    print(time_between_shutdowns(loglines))
