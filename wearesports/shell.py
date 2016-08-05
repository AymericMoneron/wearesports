import argparse
import datetime
import json
import re
import requests
import time

from bs4 import BeautifulSoup
from prettytable import PrettyTable

from wearesports.utils import env, valid_date

VERSION = 'wearesports.py 0.1'
DESCRIPTION = 'Playing field booking system for www.wearesports.fr'

ACTIVITIES = ['badminton', 'padel', 'foot', 'foot_5', 'squash']
DAYS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
CURRENCY = u"\u20AC"  # €

LOGIN_URL = 'http://www.wearesports.fr/espace-membre'
LOGOUT_URL = 'http://www.wearesports.fr/user/logout'
SCHEDULE_URL = 'http://www.wearesports.fr/views/ajax'

FORM_ID = 'user_login'
VIEW_COURT = 'comptage_des_terrains'
VIEW_AVAILABILITY = 'disponibilite_terrains'
VIEW_SCHEDULE = 'creneaux_terrains'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

def get_args():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION, version=VERSION)
    parser.add_argument('activity', choices=ACTIVITIES, help='Activity')

    subparsers = parser.add_subparsers(help='commands')

    schedule_parser = subparsers.add_parser(
        'schedule',
        help='Show court availability')
    schedule_parser.add_argument(
        'date',
        default=datetime.datetime.today().strftime('%Y-%m-%d'),
        type=valid_date,
        help='Date - format YYYY-MM-DD')

    group = parser.add_argument_group('authentication')
    group.add_argument('-u', '--username', required=False, help='Username')
    group.add_argument('-p', '--password', required=False, help='Password')

    parser.set_defaults(username=env('WAS_USERNAME'))
    parser.set_defaults(password=env('WAS_PASSWORD'))

    return parser.parse_args()


def count_court(args, session, url=SCHEDULE_URL):
    data = {
        'view_name': VIEW_COURT,
        'view_display_id': 'block_1',
        'view_args': args.activity
    }

    response = session.post(url, data)
    return int(json.loads(response.text)[1]['data'])


def get_slots(args, session, url=SCHEDULE_URL):

    view_args = args.activity + "/" + args.date.strftime('%Y-%m-%d')

    data = {
        'view_name': VIEW_AVAILABILITY,
        'view_display_id': 'block',
        'view_args': view_args
    }

    response = session.post(url, data)

    html = json.loads(response.text)[1]['data']
    soup = BeautifulSoup(html, "html.parser")

    slots = {}

    for slot in soup.find_all('div'):
        slots[slot.get('title')] = slot.get('data-dispo')

    return slots


def login(args, url=LOGIN_URL):
    session = requests.session()
    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    form_build_id = soup.find(
        id="user-login").find('input', {'name': 'form_build_id'}).get('value')

    credentials = {
        'name': args.username,
        'pass': args.password,
        'form_build_id': form_build_id,
        'form_id': FORM_ID
    }

    session.post(url, credentials)

    return session


def logout(args, session, url=LOGOUT_URL):
    session.get(url)
    session.close()
    return True


def print_schedule(args, session, url=SCHEDULE_URL):

    t = PrettyTable()
    t.field_names = ['Time', 'Price', 'Booking']
    t.align["Booking"] = "l"

    date = args.date

    view_display_id = 'creneaux_' + DAYS[date.weekday()]
    view_args = args.activity + "/" + str(int(time.mktime(date.timetuple())))

    data = {
        'view_name': VIEW_SCHEDULE,
        'view_display_id': view_display_id,
        'view_args': view_args
    }

    response = session.post(url, data)
    html = json.loads(response.text)[1]['data']

    court_count = count_court(args, session)
    slots = get_slots(args, session)

    soup = BeautifulSoup(html, "html.parser")
    for time_slot in soup.find_all('a'):
        start = time_slot.get('data-hdebut')
        end = time_slot.get('data-hfin')
        price = time_slot.get('data-tarif')
        slot_count = 0

        if(slots.has_key(start)):
            slot_count = slots[start]

        availability = str(slot_count) + '/' + str(court_count)
        if(slot_count >= str(court_count)):
            availability = str(slot_count) + '/' + str(court_count) + ' FULL'

        t.add_row([start + '-' + end, price + ' ' + CURRENCY, availability])

    print t


def main():

    args = get_args()

    session = login(args)
    print_schedule(args, session)
    logout(args, session)

    return 0

if __name__ == "__main__":
    main()
