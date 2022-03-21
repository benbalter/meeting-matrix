from codecs import strict_errors
from calendar_fetcher import CalendarFetcher 
from canvas import Canvas
import time
import logging
import sched
import inflect

logging.basicConfig(level=logging.DEBUG)

calendar_fetcher = CalendarFetcher()
canvas = Canvas()
scheduler = sched.scheduler(time.time, time.sleep)
inflect_engine = inflect.engine()

def seconds_until_next_minute():
  return 60 - time.time() % 60

def clear_and_schedule():
  """
  Clears the canvas and schedules a `run()` for the top of the next minute
  """
  logging.info("Clearing canvas")
  canvas.clear()
  logging.info("Waiting %d seconds until next minute", seconds_until_next_minute())
  scheduler.enter(seconds_until_next_minute(), 1, run)

def time_to_display(event):
  """
  Given an event, returns what time to display, if any

  Conditions where the time remaining is displayed:

  1. Less than or equal to 50% of the event
  2. Every ten minutes if more than twenty minutes remaining
  3. Every five minutes if more than five minutes remaning
  4. Every minute if less than five minutes remain 
  """
  if not event:
    return

  if not event.in_progress():
    logging.info("Event is not in progress")
    return
  
  if event.percent_remaining() > .5:
    logging.info("%f of event remaining", event.percent_remaining())
    return

  minutes_remaining = event.minutes_remaining()
  minute = inflect_engine.plural("minute", minutes_remaining)
  logging.info("%d %s remaining", minutes_remaining, minute)

  if minutes_remaining > 20 and minutes_remaining % 10 == 0:
    return f'{minutes_remaining} {minute}'

  if minutes_remaining < 5 or minutes_remaining % 5 == 0:
    return f'{minutes_remaining} {minute}'


def run():
  """
  Checks for the current event and updates the matrix
  """
  logging.info("Starting Run!")
  event = calendar_fetcher.current_event()
  str = time_to_display(event)

  clear_and_schedule()

  if str:
    canvas.print_text(str)

run()
scheduler.run()
