from sanic import Sanic, response
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

app = Sanic(__name__)

# Replace with your own Google Sheet ID and range
SPREADSHEET_ID = '1iMxqOcGNqflEmSdOCsubryoH7El7cWKTxvK2wUy5QsM'
RANGE_NAME = 'Sheet1!A2:J'

# Replace with your own Flock App credentials
APP_ID = '9f7486f1-a806-4c8f-a030-d6ca8e49b338'
APP_SECRET = '2e666c4a-aeb5-4c59-b754-0226cb7254ea'
BOT_TOKEN = '<your_bot_token>'

# Load the credentials from the credentials file
creds = None
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = './credentials.json'
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Sheets API client
service = build('sheets', 'v4', credentials=creds)


import requests

def send_message(to, text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BOT_TOKEN}'
    }
    data = {
        'to': to,
        'text': text
    }
    response = requests.post('https://api.flock.com/v1/chat.sendMessage', headers=headers, json=data)
    response.raise_for_status()


# Define a route for the Flock event listener
@app.route('/events', methods=['POST'])
async def events(request):
    data = request.json
    # Check if the event is a Flock App installation event
    if data['name'] == 'app.install':
        # Send a welcome message to the user who installed the App
        user_id = data['userId']
        message = 'Thanks for installing the On-Call Bot! Type /oncall to get the current on-call information or use #oncall Team-CFV to get the on-call information for a specific team.'
        send_message(user_id, message)
    return response.text('')

# Define a route for the /oncall command
@app.route('/oncall', methods=['POST'])
async def oncall(request):
    data = request.form
    team_name = data.get('text', '').strip().lower().replace('#oncall', '')
    # Get the current on-call information from the Google Sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    # Filter the on-call information by team name if specified
    if team_name:
        values = [row for row in values if row[0].lower() == team_name]
    # Format the on-call information as a message
    message = 'Current On-Call:'
    for row in values:
        team = row[0]
        l1_dev = row[1]
        l1_contact = row[2]
        l2_dev = row[3]
        l2_contact = row[4]
        l3_dev = row[5]
        l3_contact = row[6]
        message += f'\n\nTeam: {team}\nL1: {l1_dev} ({l1_contact})\nL2: {l2_dev} ({l2_contact})\nL3: {l3_dev} ({l3_contact})'
    # Send the message to the Flock group
    group_id = data['chat']
    send_message(group_id, message)
    return response.text('')
