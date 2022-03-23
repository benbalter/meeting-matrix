from codecs import strict_errors
from calendar_fetcher import CalendarFetcher
from canvas import Canvas
import time
from datetime import datetime
import logging
import sched

logger = logging.getLogger('meeting_matrix')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

calendar_fetcher = CalendarFetcher()
canvas = Canvas()
scheduler = sched.scheduler(time.time, time.sleep)


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
    canvas.clear()

    if event and event.should_display_time():
        minutes = 1
    else:
        minutes = 5

    logger.info("Waiting %d seconds until next minute",
                 seconds_until_next_minute(minutes))
    scheduler.enter(seconds_until_next_minute(minutes), 1, run)


def run():
    """
    Checks for the current event and updates the matrix
    """
    logger.info("Starting Run!")

    event = calendar_fetcher.current_event()
    clear_and_schedule(event)

    if event and event.should_display_time():
        canvas.print_minutes_remaining(event)


canvas.print_centered("Meeting")
canvas.print_centered("Matrix", y=25)
canvas.swap_canvas()
time.sleep(1)

run()
scheduler.run()
