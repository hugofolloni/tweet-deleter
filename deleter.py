import json
import calendar
from datetime import date, datetime

class Tweet:
    def __init__(self, text, favs, rts, date, id):
        self.id = int(id)
        self.text = text
        self.favs = int(favs)
        self.date = date
        self.rts = int(rts)
        self.ignore = True

def get_datetime(created):
    try:
        a = created.split(' ')
        month = list(calendar.month_abbr).index(a[1])
        year = a[-1]
        day = a[2]
        return date(int(year), int(month), int(day))
    except: 
        return datetime.today()
    
count_rts = 0

def get_info_from_json(path):
    f = open(path, encoding="utf8") 
    data = json.load(f)

    user_tweets = []

    for tweet in data['tweets']:
        try:
            i = tweet['tweet']
            if i['full_text'].split(' ')[0] == "RT":
                count_rts += 1
                continue
            date = get_datetime(i['created_at'])
            user_tweets.append(Tweet(i['full_text'], i['favorite_count'], i['retweet_count'], date, i['id']))
        except:
            continue     
        
    f.close()

    return user_tweets

def print_infos(tweets):
    for i in tweets:
        print('{:^20} | {:^50.50} | {:^4} |  {:^4} | {:^10} | {}'.format(i.id, i.text, i.favs, i.rts, str(i.date), i.ignore))

def print_item(i):
    print('{:^20} | {:^50.50} | {:^4} |  {:^4} | {:^10} | {}'.format(i.id, i.text, i.favs, i.rts, str(i.date), i.ignore))


def handle_filters(tweets, min_date='', max_date='', fav=0, rt=0):
    if min_date == '':
        min_date = '31/12/9999'
    if max_date == '':        
        max_date == '01/01/1900'

    max_date_part = max_date.split('/')
    maximum = date(int(max_date_part[2]), int(max_date_part[1]), int(max_date_part[0]))
    min_date_part = min_date.split('/')
    minimum = date(int(min_date_part[2]), int(min_date_part[1]), int(min_date_part[0]))
    for item in tweets:
        if item.favs < fav and item.rts < rt:
            item.ignore = False
        if maximum > item.date:
            item.ignore = False
        if minimum < item.date:
            item.ignore = False
    return tweets

def get_remaining_tweets(after_filters):
    count = 0
    list_sorted = sorted(after_filters, key=lambda x: x.date)
    for i in list_sorted:
        if i.ignore:
            count += 1
            print_item(i)
    return count

def get_list_to_delete(list):
    to_delete = []
    for item in list:
        if not item.ignore:
            to_delete.append(item.id)
    return to_delete

def __main__():
    tweets = get_info_from_json('tweets.json')
    after_filters = handle_filters(tweets, fav=7, rt=3, max_date = '31/12/2021')
    print(get_list_to_delete(after_filters))
    print(f'Remaining: {get_remaining_tweets(after_filters)}')
    print(f'Deleted: {len(get_list_to_delete(after_filters))}')
    print(f"Total tweets: {len(after_filters)}")
    print(f"Total RTs: {count_rts}")
        
__main__()