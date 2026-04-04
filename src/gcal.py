# Google Calendar API setup, get events

import os
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Ignore if only pulling from your primary Google calendar
CALENDAR_IDS = [
    "primary",
    os.getenv("ANNALIVIA_CALENDAR_ID")
]

# If you change these scopes, delete token.json and re-authenticate
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json" # generated after first OAuth2 flow init

"""
get_calendar_service()
Authenticates with Google Calendar API and returns a service client.
On first run, opens a browser for OAuth2 login and saves token.json.
On subsequent runs, loads token.json directly (no browser needed).
"""
def get_calendar_service():
    log = logging.getLogger(__name__)
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        log.debug("Loaded credentials from token.json")

    # If no valid credentials, prompt login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            log.debug("Refreshing expired token")
            creds.refresh(Request())
        else:
            log.info("No valid token found — opening browser for authentication")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        log.debug("Saved new token to token.json")

    return build("calendar", "v3", credentials=creds)

"""
fetch_events(month: int, year:  int)
Fetches all Google Calendar events for the given month and year.
Returns a list of events with their summary and start date.
"""
def fetch_events(month: int, year: int):
    log = logging.getLogger(__name__)

    service = get_calendar_service()

    # Build time range for the given month
    time_min = datetime(year, month, 1, tzinfo=timezone.utc).isoformat()
    if month == 12:
        time_max = datetime(year + 1, 1, 1, tzinfo=timezone.utc).isoformat()
    else:
        time_max = datetime(year, month + 1, 1, tzinfo=timezone.utc).isoformat()

    log.info(f"Fetching events for {month}/{year}")

    all_events = []
    for cal_id in CALENDAR_IDS:
        result = service.events().list(
            calendarId=cal_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = result.get("items", [])
        log.debug(f"  {cal_id}: {len(events)} events")
        for event in events:
            summary = event.get("summary", "(no title)")
            start = event["start"].get("date") or event["start"].get("dateTime", "")
            all_events.append({"summary": summary, "start": start})

    all_events.sort(key=lambda e: e["start"])
    log.info(f"Found {len(all_events)} total events across {len(CALENDAR_IDS)} calendars")

    for event in all_events:
        log.debug(f"  {event['start']}: {event['summary']}")

    return all_events

"""
list_calendars()
Prints all calendars accessible to the authenticated account.
Run once to find calendar IDs. Use if including multiple/shared calendars. 
Default sync_cal() just pulls primary Google calendar.
"""
def list_calendars():
    log = logging.getLogger(__name__)
    service = get_calendar_service()
    calendars = service.calendarList().list().execute()
    for cal in calendars.get("items", []):
        log.info(f"  {cal['summary']}: {cal['id']}")