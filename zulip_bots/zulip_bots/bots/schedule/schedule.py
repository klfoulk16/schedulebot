# See readme.md for instructions on running this code.

from typing import Any, Dict
from zulip_bots.lib import BotHandler
import requests
import dotenv
import os
from requests.auth import HTTPBasicAuth
import pprint

dotenv.load_dotenv()

class ScheduleBotHandler:
    def usage(self) -> str:
        return '''
        Let me tell you what events you've signed up for today!

        Usage: @schedulebot schedule <Optional=timezone>
        I'll send you a list of the events you've RSVP'd for
        in RC's calendar and what time they're at.
        <time> : <event name> <link to join>
        '''

    def handle_message(self, message: Dict[str, Any], bot_handler: BotHandler) -> None:
        content = get_schedule(message['sender_id'])
        bot_handler.send_reply(message, content)

        return

handler_class = ScheduleBotHandler

def get_schedule(person_id):
    """
    return formatted schedule
    """
    response = query_for_events()
    if response.ok:
        events = parse_json(response.json(), person_id)
        return format_content(events)
    else:
        return "Unable to fetch events."

def query_for_events():
    """
    query
    handle errors
    """
    return requests.request(
        'GET',
        'https://www.recurse.com/api/v1/events?include_participants=true&happening_within=P1D',
        auth=HTTPBasicAuth(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))
    )

def parse_json(response, person_id):
    """
    create dict of events user is attending
    in the next 24 hours
    """
    their_events = []
    for event in response:
        if "participants" not in event:
            continue
        else:
            for participant in event['participants']:
                if participant['person']['zulip_id'] == person_id:
                    their_events.append(format_event(event))
    return their_events


def format_event(event):
    """
    Take the massive event dictionary and format it
    """
    return f"{event['title']} {event['start_time']} {event['url']}"


def convert_timezone():
    pass

def format_content(events):
    content = "Your schedule for the day:\n"
    ocean = "🌊 "
    for event in events:
        content = content + ocean + event + '\n'
    return content
        






