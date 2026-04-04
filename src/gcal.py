# Google Calendar API setup, get events

import os
import logging
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone

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

    result = service.events().list(
        calendarId="primary",
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = result.get("items", [])
    log.info(f"Found {len(events)} events")

    parsed = []
    for event in events:
        summary = event.get("summary", "(no title)")
        start = event["start"].get("date") or event["start"].get("dateTime", "")
        log.debug(f"  {start}: {summary}")
        parsed.append({"summary": summary, "start": start})

    return parsed