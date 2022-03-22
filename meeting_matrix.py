from codecs import strict_errors
from calendar_fetcher import CalendarFetcher
from canvas import Canvas
import time
from datetime import datetime 
import logging
import sched
import inflect

logging.basicConfig(level=logging.DEBUG)

calendar_fetcher = CalendarFetcher()
canvas = Canvas()
scheduler = sched.scheduler(time.time, time.sleep)
inflect_engine = inflect.engine()


def seconds_until_next_minute(minutes=1):
    """
    Calculates the number of seconds until the next minute that's a multiple of the given minute

    This allows us to schedule a run every 5 minutes until the last 5 minutes of the meeting, 
    when we schedule a run for every minute.
    """
    seconds = minutes * 60
    return seconds - (time.time() % seconds)

def clear_and_schedule(event):
    """
    Clears the canvas and schedules a `run()` for the top of the next minute
    """
    logging.info("Clearing canvas")
    canvas.clear()

    if should_display_time(event):
        minutes = 1 
    else:
        minutes = 5

    logging.info("Waiting %d seconds until next minute",
                 seconds_until_next_minute(minutes))
    scheduler.enter(seconds_until_next_minute(minutes), 1, run)


def should_display_time(event):
    """
    Given an event, determines when to display the time remaining

    Conditions where the time remaining is displayed:

    1. Less than or equal to 50% of the event
    2. Every ten minutes if more than twenty minutes remaining
    3. Every five minutes if more than five minutes remaning
    4. Every minute if less than five minutes remain 
    """
    if not event:
        logging.info("No event found")
        return False

    if not event.in_progress():
        logging.info("Event is not in progress")
        return False

    if event.percent_remaining() > .5:
        logging.info("%f of event remaining", event.percent_remaining())
        return False

    minutes_remaining = event.minutes_remaining()
    minute = inflect_engine.plural("minute", minutes_remaining)
    logging.info("%d %s remaining", minutes_remaining, minute)

    if minutes_remaining > 20 and minutes_remaining % 10 == 0:
        return True

    if minutes_remaining < 5 or minutes_remaining % 5 == 0:
        return True

    return False


def run():
    """
    Checks for the current event and updates the matrix
    """
    logging.info("Starting Run!")

    event = calendar_fetcher.current_event()
    clear_and_schedule(event)

    if should_display_time(event):
        canvas.print_minutes_remaining(event)


canvas.print_centered("Meeting")
canvas.print_centered("Matrix", y=25)
canvas.swap_canvas()
time.sleep(1)

run()
scheduler.run()
