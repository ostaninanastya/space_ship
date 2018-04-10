def filter_by_time(hour, minute, second, item_time):
    return (hour < 0 or item_time.hour == hour) and\
        (minute < 0 or item_time.minute == minute) and\
        (second < 0 or item_time.second == second)