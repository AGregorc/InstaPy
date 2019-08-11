# -*- coding: utf-8 -*-

import traceback
import time
import math
from random import shuffle
from random import uniform
import schedule
import datetime

from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace
from insta_users import *

min_sleep_minutes = 2
max_sleep_minutes = 15
SESSION_DURATION = 1 * 60 * 60  # hours * minutes * seconds

# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'


tags = ['natgeo', 'amazing', 'view', 'Bled', 'Slovenia', 'winter', 'travelling']
other_tags = ['first', 'eye', 'lake', 'nature', 'wildlife', 'ig_today', 'tree', 'forests', 'love', 'green', 'sky',
              'tbt', 'pretty', 'selfie']
last_picture_tags = ['fun', 'time', 'sun', 'sunglasses', 'dog', 'lemonade', 'dogstagram', 'lovedogs', 'dogsofinstagram',
                     'selfie', 'chill', 'weekend', 'weekendvibes', 'sunny', 'sunshine', 'summer']

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


def get_shuffled_tags():
    all_tags = tags + other_tags + last_picture_tags
    shuffle(all_tags)
    all_tags = all_tags[0:int(len(all_tags) * uniform(0.7, 1))]
    return all_tags


def init_new_session():
    return InstaPy(username=insta_username,
                   password=insta_password,
                   headless_browser=False,
                   nogui=no_gui,
                   multi_logs=True,
                   bypass_with_mobile=True)


# set workspace folder at desired location (default is at your home folder)
set_workspace(path=workspace_path)


def start_session():
    session = init_new_session()
    all_tags = get_shuffled_tags()

    with smart_run(session):
        # start = datetime.datetime.now()
        #
        # while True:
        #     if (datetime.datetime.now() - start).total_seconds() > SESSION_DURATION:
        #         return None

        # settings
        session.set_relationship_bounds(enabled=True,
                                        potency_ratio=None,
                                        delimit_by_numbers=None,
                                        max_followers=8500,
                                        max_following=4490,
                                        min_followers=20,
                                        min_following=15,
                                        min_posts=1,
                                        max_posts=1000)

        session.set_quota_supervisor(enabled=True,
                                     sleep_after=["likes", "comments_d", "follows", "unfollows"],
                                     sleepyhead=True, stochastic_flow=True, notify_me=True,
                                     peak_likes=(62, 552),
                                     peak_comments=(22, 134),
                                     peak_follows=(31, 84),
                                     peak_unfollows=(35, 402),
                                     peak_server_calls=(None, 4700))

        session.set_skip_users(skip_private=False,
                               skip_no_profile_pic=True,
                               skip_business=True,
                               business_percentage=84)

        # session.set_do_follow(enabled=True, percentage=20)
        session.set_dont_unfollow_active_users(enabled=True, posts=5)
        # session.set_do_like(enabled=True, percentage=90)
        session.set_comments([u"@{} 👌👍", u"Cool 👌👍", "@{} <3", u"😍", u"😏👍😀", "<3", u"👌👍"])
        session.set_do_comment(enabled=True, percentage=18)
        session.set_do_like(enabled=True, percentage=67)
        session.set_do_story(enabled=True, percentage=23, simulate=False)
        session.set_smart_location_hashtags(locations, radius=25, limit=7)
        session.join_pods()

        # interactions
        session.set_user_interact(amount=3, randomize=True, percentage=43, media='Photo')

        # actions
        session.unfollow_users(amount=10, nonFollowers=True, unfollow_after=42 * 60 * 60)
        # session.follow_by_tags(tags, amount=20)
        # session.like_by_locations(locations, amount=math.floor(30 / len(locations)))
        session.like_by_tags(all_tags, amount=math.floor(50 / len(all_tags)))
        session.like_by_tags(amount=4, use_smart_location_hashtags=True)
        session.unfollow_users(amount=10, nonFollowers=True, unfollow_after=42 * 60 * 60)
        session.like_by_feed(amount=15, randomize=True, interact=True)

        # if (datetime.datetime.now() - start).total_seconds() > SESSION_DURATION:
        #     return None
        # time.sleep(uniform(min_sleep_minutes * 60, max_sleep_minutes * 60))


debug = False
if not debug:
    now = input("Do you want to start now? (Y/N)")
    if now == "Y":
        print("Session is starting.")
        start_session()
    else:
        print("Session will start on schedule.")
else:
    start_session()

# schedule.every().day.at("06:35").do(start_session)
schedule.every().day.at("08:13").do(start_session)
schedule.every().day.at("16:28").do(start_session)
schedule.every().day.at("21:47").do(start_session)

while True:
    schedule.run_pending()
    time.sleep(1)
