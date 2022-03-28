from dateutil import parser
import datetime
import math
import logging
import inflect

logger = logging.getLogger('meeting_matrix')


class Event:
    """
    Represents a single calendar event
    """

    def __init__(self, data):
        self.data = data
        self.inflect_engine = inflect.engine()

    def title(self):
        """
        Returns the title of the event
        """
        return self.data['summary']

    def start(self):
        """
        Return the start time as a DateTime
        """
        return self.get_time("start")

    def end(self):
        """
        Return the end time as a DateTime
        """
        return self.get_time("end")

    def get_time(self, time):
        """
        Returns the parsed start or end time as a DateTime
        """
        time = self.data[time].get('dateTime')

        if time:
            return parser.parse(time)

    def time_remaining(self):
        """
        Returns the time remaining within the event
        """
        return self.end() - datetime.datetime.now(datetime.timezone.utc)

    def durration(self):
        """
        Returns the duration of the event
        """
        return self.end() - self.start()

    def perceived_durration(self):
        """
        If the event is a "speedy" meeting (five minutes less than 30 or 60), conceptually
        Treat it as the full 30 or 60 minute meeting for purposes of calculating the halfway point
        """

        if self.durration().total_seconds() in [25 * 60, 50 * 60, 55 * 60]:
            seconds = 30 * 60
            ratio = self.durration() / seconds
            perceived_durration = seconds * round(ratio.total_seconds())
            return datetime.timedelta(seconds=perceived_durration)

        return self.durration()

    def percent_remaining(self):
        """
        Returns the percent of the event remaining
        """
        return float(self.time_remaining().total_seconds()) / \
            float(self.perceived_durration().total_seconds())

    def in_progress(self):
        """
        Returns true if the current event is in progress
        """

        if not self.start() or not self.end():
            return False

        if self.start() >= datetime.datetime.now(datetime.timezone.utc):
            return False

        return self.end() >= datetime.datetime.now(datetime.timezone.utc)

    def is_self(self, attendee):
        """
        Determins if the attendee is the authorized user
        """
        
        return attendee.get('self', False)

    def is_attending(self):
        """
        Returns true if the authorized user is attending the event
        """
        if self.data['organizer'].get('self') or self.data['creator'].get('self'):
            return True

        if not self.data.get('attendees'):
            return False

        attendees = self.data["attendees"]
        authorized_user = filter(self.is_self, attendees)
        authorized_user = next(authorized_user, None)

        if not authorized_user:
            return False

        return authorized_user["responseStatus"] == "accepted"

    def minutes_remaining(self):
        """
        Returns the number of minutes remaining in the event as an integer
        """

        return round(float(self.time_remaining().total_seconds()) / 60.0)

    def should_display_time(self):
        """
        Determines when to display the time remaining

        Conditions where the time remaining is displayed:

        1. Less than or equal to 50% of the event
        2. Every ten minutes if more than twenty minutes remaining
        3. Every five minutes if more than five minutes remaning
        4. Every minute if less than five minutes remain
        """
        if not self.in_progress():
            logger.info("Event is not in progress")
            return False

        minutes_remaining = self.minutes_remaining()
        minute = self.inflect_engine.plural("minute", minutes_remaining)
        logger.info("%d %s remaining", minutes_remaining, minute)

        if minutes_remaining > 30 or self.percent_remaining() > (2/3):
            logger.info("%f of event remaining", self.percent_remaining())
            return False

        if minutes_remaining > 20 and minutes_remaining % 10 == 0:
            return True

        if minutes_remaining < 20 and minutes_remaining % 5 == 0:
            return True

        if minutes_remaining < 5:
            return True

        return False
