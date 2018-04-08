import datetime

def time_to_str(t):
    return ('%02d' % t.hour) + ':' + ('%02d' % t.minute) + ':' + ('%02d' % t.second)

def date_to_str(t):
    return str(t)