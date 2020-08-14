from datetime import datetime
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
    for char in line:
        if char.isdigit():
            index_of_first_num = line.find(char)
            datetime_str = line[index_of_first_num:]
            datetime_str = datetime_str.replace('T', ' ')
            converted_datetime_str = datetime.strptime(
                datetime_str, '%Y-%m-%d %H:%M:%S')
            return converted_datetime_str

    """TODO 1:
       Extract timestamp from logline and convert it to a datetime object.
       For example calling the function with:
       INFO 2014-07-03T23:27:51 supybot Shutdown complete.
       returns:
       datetime(2014, 7, 3, 23, 27, 51)
    """


def time_between_shutdowns(loglines):
    """TODO 2:
       Extract shutdown events ("Shutdown initiated") from loglines and
       calculate the timedelta between the first and last one.
       Return this datetime.timedelta object.
    """


with open(logfile) as f:
    loglines = f.readlines()
    for line in loglines:
        stripped_line = line.split('supybot')[0].strip()
        convert_to_datetime(stripped_line)
