from __future__ import print_function

import datetime
import os.path
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser
from event import Event

class CalendarFetcher:
    """
    Retrieves the current event from the calendar
    """

    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None

    def __init__(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file(
                'token.json', self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def current_event(self):
        """
        Retrieves the current event, if any

        Returns an Event()
        """
        try:
            logging.info("Fetching calendar")

            service = build('calendar', 'v3', credentials=self.creds)
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])
            events = map(lambda e: Event(e), events)
            events = filter(lambda e: e.in_progress(), events)
            event  = next(events, None)

            if event:
                logging.info("Found event: %s", event.title())
            
            return event

        except HttpError as error:
            logging.error('An error occurred: %s', error)
            return []
