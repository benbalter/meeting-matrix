from dateutil import parser
import datetime
import math
import logging
import inflect


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

        if self.data['status'] != 'confirmed':
            return False

        if self.start() >= datetime.datetime.now(datetime.timezone.utc):
            return False

        return self.end() >= datetime.datetime.now(datetime.timezone.utc)

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
            logging.info("Event is not in progress")
            return False

        if self.percent_remaining() > .5:
            logging.info("%f of event remaining", self.percent_remaining())
            return False

        minutes_remaining = self.minutes_remaining()
        minute = self.inflect_engine.plural("minute", minutes_remaining)
        logging.info("%d %s remaining", minutes_remaining, minute)

        if minutes_remaining > 20 and minutes_remaining % 10 == 0:
            return True

        if minutes_remaining < 20 and minutes_remaining % 5 == 0:
            return True

        if minutes_remaining < 5:
            return True

        return False
