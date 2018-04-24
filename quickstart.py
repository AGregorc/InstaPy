# -*- coding: utf-8 -*-

import traceback
import time
import math
from random import shuffle
from random import uniform
import schedule

from instapy import InstaPy
from insta_users import *


sleep_minutes = 30
SESSION_DURATION = 6 * 60 * 60 # hours * minutes * seconds

# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'


tags = ['natgeo','amazing', 'view', 'Bled', 'Slovenia', 'winter', 'travelling']
other_tags = ['first',  'eye', 'lake', 'nature', 'wildlife', 'ig_today', 'tree', 'forests', 'love', 'green', 'sky', 'tbt', 'pretty', 'selfie']
last_picture_tags = ['fun', 'time', 'sun', 'sunglasses', 'dog', 'lemonade', 'dogstagram', 'lovedogs', 'dogsofinstagram', 'selfie', 'chill', 'weekend', 'weekendvibes', 'sunny', 'sunshine', 'summer']
all_tags = tags+other_tags+last_picture_tags
shuffle(all_tags)
all_tags = all_tags[0:int(len(all_tags)*uniform(0.7,1))]

locations = [
                '214473716/centralna-postaja-ljubljana/', '314668210/center-ljubljana/', 
                '220764453/ljubljanski-grad-ljubljana-castle/', '220764453/ljubljanski-grad-ljubljana-castle/',
                '213783784/neboticnik-skyscraper/', '217264051/cirkus/', '216382022/bled-slovenia/',
                '219907852/portoroz/', '250609403/zale/', '28108257/bled-castle/', '3914101/hotel-grand-metropol-portoroz/',
                '235518406/metelkova/', '253581293/triglav-national-park/', '570516765/lucija-piran/',
                '16011059/vrhnika/', '240101335/kavarna-rog/', '248355601/beograd-serbia/',
                '828831498/troja-lounge-bar-club/', '264003924/ljubljana-botanical-garden/',
                '281344734/ljubljana-railway-station/', '215729531/kino-siska/'
                ]


def init_new_session():
    return InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False,
                  nogui=True,
                  multi_logs=True)


def start_session():
    try:
        session = init_new_session()
        session.login()

        while True:

            # settings
            session.set_upper_follower_count(limit=2000)
            #session.set_do_follow(enabled=True, percentage=20)
            session.set_dont_unfollow_active_users(enabled=True, posts=3)
            #session.set_do_like(enabled=True, percentage=90)
            session.set_comments([u"👌👍", u"Cool 👌👍", "<3", u"😍", u"😏👍😀"])
            session.set_do_comment(enabled=True, percentage=20)
            
            # actions
            session.unfollow_users(amount=10, onlyNotFollowMe=True, sleep_delay=60)
            #session.follow_by_tags(tags, amount=20)
            session.like_by_locations(locations, amount=math.floor(30/len(locations)))
            session.like_by_tags(all_tags, amount=math.floor(50/len(all_tags)))
            session.unfollow_users(amount=10, onlyNotFollowMe=True, sleep_delay=60)
            session.like_by_feed(amount=70, randomize=True, interact=True)

            #if (datetime.datetime.now() - start).total_seconds() > SESSION_DURATION:
            #    return None
            #time.sleep(sleep_minutes*60)

    except Exception as exc:
        # full stacktrace when raising Github issue
        traceback.print_exc(exc)
        #time.sleep(sleep_minutes*60)
        #start_session(start)

    finally:
        # end the bot 
        if session is not None:
            session.end()

start_session()

schedule.every().day.at("6:35").do(start_session)
schedule.every().day.at("8:13").do(start_session)
schedule.every().day.at("16:28").do(start_session)
schedule.every().day.at("21:47").do(start_session)

while True:
    schedule.run_pending()
    time.sleep(1)
