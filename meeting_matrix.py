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
  canvas.clear()
  logging.info("Waiting %d seconds until next minute", seconds_until_next_minute())
  scheduler.enter(seconds_until_next_minute(), 1, run)

def run():
  """
  Checks for the current event and updates the matrix

  Conditions where the time remaining is displayed:

  1. Less than or equal to 50% of the event
  2. Every five minutes if more than five minutes remaning
  3. Every minute if less than five minutes remain 
  """
  logging.info("Starting Run!")
  event = calendar_fetcher.current_event()

  if not event.in_progress():
    logging.info("Event is not in progress")
    return clear_and_schedule()
  
  if event.percent_remaining() > .5:
    logging.info("%f of event remaining", event.percent_remaining())
    return clear_and_schedule()

  minutes_remaining = event.minutes_remaining()
  minute = inflect_engine.plural("minute", minutes_remaining)
  logging.info("%s %s remaining", minutes_remaining, minute)

  if not minutes_remaining <= 5 or minutes_remaining % 5 == 0 or minutes_remaining > 20:
    return clear_and_schedule()

  str = f'{minutes_remaining} {minute}'
  clear_and_schedule()
  canvas.print_text(str)

run()
scheduler.run()
