from calendar_fetcher import CalendarFetcher 
from canvas import Canvas

calendar_fetcher = CalendarFetcher()
canvas = Canvas()

canvas.print_text(calendar_fetcher.time_remaining())
