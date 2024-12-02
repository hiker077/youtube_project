import re

def get_publishing_period(x):
    ##define date period in which channel published movie
    x = int(x.strftime("%H"))
    if 5 <= x < 12:
        return "Morning"
    elif 12 <= x < 18:
        return "Afternoon"
    else:
        return "Evening"
    

def get_minutes(x):
    ##function to extact time (in minutes)

    hour = re.search(r'(\d{1,2})H', x) 
    minute = re.search(r'(\d{1,2})M', x)
    second = re.search(r'(\d{1,2})S', x)

    hour = 0 if hour is None else int(hour.group(1))
    minute = 0 if minute is None else int(minute.group(1))
    second = 0 if second is None else int(second.group(1))
    minutes = round(hour*60+ minute+ second/60,2)

    return minutes