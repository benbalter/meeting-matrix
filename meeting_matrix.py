from calendar_fetcher import CalendarFetcher 
from canvas import Canvas
import time
import logging

logging.basicConfig(level=logging.DEBUG)

calendar_fetcher = CalendarFetcher()
canvas = Canvas()
event = calendar_fetcher.current_event()

if not event.in_progress():
  logging.info("Event is not in progress")
  exit()
  
#if event.percent_remaining() > .5:
#  logging.info("%f of event remaining", event.percent_remaining())
#  exit()

logging.info(event.percent_remaining())

time_remaining = event.time_remaining()
logging.info("%s remaining", time_remaining)

minutes_remaining = event.minutes_remaining()
str = f'{minutes_remaining} minutes'

canvas.print_text(str)

time.sleep(10)
