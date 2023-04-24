from __future__ import print_function

import os.path

from sanic import Sanic, response
from sanic.log import logger
import json
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1iMxqOcGNqflEmSdOCsubryoH7El7cWKTxvK2wUy5QsM'
SAMPLE_RANGE_NAME = 'Sheet1!A2:J'

app = Sanic("Oncall")


async def main_func(team_name=None):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            return 'No data found.'

        logger.info(f'ok"{team_name}"')
        logger.info(values)

        if team_name:
            if team_name.casefold()!='all':
                values = [row for row in values if row[0].casefold() == team_name.casefold()]
                if not values:
                    return 'Invalid Team Name! Please check from https://docs.google.com/spreadsheets/d/1iMxqOcGNqflEmSdOCsubryoH7El7cWKTxvK2wUy5QsM/edit?usp=sharing'

            # Format the on-call information as a message
            message = 'Current On-Call:'
            for row in values:
                team = row[0]
                l1_dev = row[1]
                l1_contact = row[2] + ', ' + row[3]
                l2_dev = row[4]
                l2_contact = row[5] + ', ' + row[6]
                l3_dev = row[7]
                l3_contact = row[8] + ', ' + row[9]
                message += f'\n\nTeam: {team}\nL1: {l1_dev} ({l1_contact})\nL2: {l2_dev} ({l2_contact})\nL3: {l3_dev} ({l3_contact})'
                message += '\n\n For discrepancies, please edit here: https://docs.google.com/spreadsheets/d/1iMxqOcGNqflEmSdOCsubryoH7El7cWKTxvK2wUy5QsM/edit?usp=sharing'

        else:
            message = ''

        logger.info(f'message: {message}')
        return message

    except HttpError as err:
        print(err)

async def send_message(to, text, user):
    payload = {
    'text': text,
    }

    headers = {
        'Content-Type': 'application/json',}

    response = requests.post('https://api.flock.com/hooks/sendMessage/31436eeb-8e01-4f50-bcd4-9b5f958a60d1', data=json.dumps(payload), headers=headers)



@app.route('/')
def home(request):
    return response.text('Thanks for installing the On-Call Bot! Type /oncall to get the current on-call information for all teams or use /oncall team-name to get the on-call information for a specific team.')
# Define a route for the Flock event listener
@app.route('/events', methods=['POST'])
async def events(request):
    data = request.json
    logger.info(data)
    # Check if the event is a Flock App installation event
    # if data['name'] == 'app.install':
    #     # Send a welcome message to the user who installed the App
    #     user_id = data['userId']
    #     message = 'Thanks for installing the On-Call Bot! Type /oncall to get the current on-call information or use #oncall Team-Name to get the on-call information for a specific team.'
    #     send_message(user_id, message)
    return response.json(data, status=200)

@app.route('/webhook', methods=['POST'])
async def oncall(request):
    data = request.json
    logger.info(f"data incoming: {data}")
    if not data.get('text', '').strip().lower().startswith('!oncall'):
        return response.text('')

    team_name = data.get('text', '').strip().lower().replace('!oncall', '').strip()
    # Get the current on-call information from the Google Sheet

    message = await main_func(team_name=team_name)
    # Send the message to the Flock group
    group_id = data['to']
    user_id = data['from']
    await send_message(group_id, message, user_id)
    return response.text('')


if __name__ == '__main__':
    app.run(port=8000, debug=True)

