import os
from requests.auth import HTTPBasicAuth
import requests


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


def get_my_events(person_id):
    """
    return formatted schedule
    """
    response = query_for_events()
    if response.ok:
        my_events = []
        for event in response.json():
            if "participants" not in event:
                continue
            else:
                for participant in event['participants']:
                    if participant['person']['zulip_id'] == person_id:
                        my_events.append(event)
        return format_content("Your schedule for the day:\n", my_events)
    else:
        return "Unable to fetch events."

def get_all_events():
    response = query_for_events()
    if response.ok:
        all_events = response.json()
        return format_content("Here are all the events today:\n", all_events)
    else:
        return "Unable to fetch events."


def format_event(event):
    """
    Take the massive event dictionary and format it
    """
    # format time string
    start_time = event['start_time']
    markdown_time = '<time:' + start_time[0:10] + 'T' + start_time[11:-1] + '+00:00>'
    link = f"[View on Calendar]({event['url']})"

    return f"{event['title']} {markdown_time} {link}"


def format_content(content, events):
    # loop through all events that are passed in and format it, and add it to content
    ocean = "🌊 "
    for event in events:
        content = content + ocean + format_event(event) + '\n'
    return content
