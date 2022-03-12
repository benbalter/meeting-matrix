from dateutil import parser
import datetime
import math

class Event:
  """
  Represents a single calendar event
  """

  def __init__(self, data):
    self.data = data

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
    return parser.parse(self.data[time].get('dateTime'))

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

  def percent_remaining(self):
    """
    Returns the percent of the event remaining
    """
    return float(self.time_remaining().total_seconds()) / float(self.durration().total_seconds())

  def in_progress(self):
    """
    Returns true if the current event is in progress 
    """

    return self.start() <= datetime.datetime.now(datetime.timezone.utc) and self.end() >= datetime.datetime.now(datetime.timezone.utc)

  def minutes_remaining(self):
    """
    Returns the number of minutes remaining in the event as an integer
    """

    return math.ceil(float(self.time_remaining().total_seconds()) / 60.0)