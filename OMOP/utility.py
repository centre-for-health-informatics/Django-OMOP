import pytz
from datetime import datetime, date
import re


def getDateTimeFromString(timeStr, timezone="Canada/Mountain"):
    '''Check a string and see if it matches Python time format, returns datetime object.'''

    if not timeStr:
        return None

    timeZone = pytz.timezone(timezone)
    timestamp = None

    if re.match('\d{4}-\d{1,2}-\d{1,2} [0-2]\d*:[0-5]\d*:[0-5]\d*', timeStr):
        try:
            timestamp = timeZone.localize(datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S'))
        except:
            return None

    elif re.match('\d{4}-\d{1,2}-\d{1,2}', timeStr):
        try:
            timestamp = timeZone.localize(datetime.strptime(timeStr, '%Y-%m-%d'))
        except:
            return None

    return timestamp
