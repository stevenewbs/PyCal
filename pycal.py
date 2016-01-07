#!/usr/bin/env python
from __future__ import print_function
import httplib2
import os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

PYCAL_DIR = os.path.join(os.path.expanduser('~'), ".pycal")
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'secrets.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
    Credentials, the obtained credential.
    """
    if not os.path.exists(PYCAL_DIR):
        os.makedirs(PYCAL_DIR)
    credential_path = os.path.join(PYCAL_DIR, 'pycal-creds.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        if not os.path.exists(os.path.join(PYCAL_DIR, CLIENT_SECRET_FILE)):
            print("Please review the installation, especially the bit about the secrets file!")
            return None
        flow = client.flow_from_clientsecrets(os.path.join(PYCAL_DIR, CLIENT_SECRET_FILE), SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    if credentials == None :
    	print("No credentials - quitting")
    	return
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.now().isoformat() + "Z"
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
    	d = event['start'].get('date')
    	if d == None :
            d = event['start'].get('dateTime')
            ds = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ")
            s = ds.strftime("%Y/%m/%d %H:%M")
        else :
            ds = datetime.datetime.strptime(d, "%Y-%m-%d")
            s = ds.strftime("%Y/%m/%d")
        print(s, event['summary'])

if __name__ == '__main__':
    main()
