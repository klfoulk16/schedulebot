# See readme.md for instructions on running this code.

from typing import Any, Dict
from zulip_bots.lib import BotHandler
import dotenv
import zulip_bots.bots.schedule.helpers as helpers

dotenv.load_dotenv()

class ScheduleBotHandler:

    def usage(self) -> str:
        return '''
        Let me tell you what events are going on today!

        Usage: 
        @schedulebot all-events
        I'll send you a list of all the events in the next 24 hours.

        @schedulebot my-events
        I'll send you a list of only the events you've RSVP'd for.
        <time> : <event name> <link to join>
        '''

    def handle_message(self, message: Dict[str, Any], bot_handler: BotHandler) -> None:
        req = message['content'].strip().split()

        if req == []:
            bot_handler.send_reply(message, 'No Command Specified')
            return

        req[0] = req[0].lower()

        response = ''

        if req == ['my-events']:
            response = helpers.get_my_events(message['sender_id'])

        if req == ['all-events']:
            response = helpers.get_all_events()

        if response:
            bot_handler.send_reply(message, response)

        return

handler_class = ScheduleBotHandler