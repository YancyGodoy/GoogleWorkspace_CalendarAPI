import pprint
from googleapiclient.discovery import build
from google.oauth2 import credentials, service_account

# Scopes required by this endpoint -> https://developers.google.com/calendar/api/v3/reference/events/insert
SCOPES = ["https://www.googleapis.com/auth/calendar",
          "https://www.googleapis.com/auth/calendar.events"]


# Service Account Credentials to be used. How to create at https://developers.google.com/workspace/guides/create-credentials#service-account
SERVICE_ACCOUNT_FILE = 'serviceAccountCredentials.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

#The below email address will be from a Super Admin Account
delegated_creds = credentials.with_subject('adminaccount@yourdomain.com')

#CalendarID (from the user) to insert event into
calId= 'calendarID' 

service = build('calendar', 'v3', credentials = delegated_creds)

event = {
  'summary': 'Your Calendar Event Title',
  'location': '1600 Amphitheatre Pkwy, Mountain View, CA 94043',
  'description': 'A brief description of your meet goes here',
  'start': {
    'dateTime': '2022-02-16T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2022-02-17T17:00:00-08:00',
    'timeZone': 'America/Los_Angeles',
  },
  #This below adds a Google Meet Link to the event
  #The below can be affected by: https://support.google.com/a/answer/9898950
  'conferenceData': {
    'createRequest': {
      'conferenceSolutionKey':{
        'type': 'hangoutsMeet'
      }
    }
  },
  #'recurrence': [
   # 'RRULE:FREQ=DAILY;COUNT=1'
  #],
  'attendees': [
    {'email': 'user1@example.com'},
    {'email': 'user2@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
eventInsert = service.events().insert(calendarId=calId, body=event).execute()
pprint.pprint(eventInsert)
