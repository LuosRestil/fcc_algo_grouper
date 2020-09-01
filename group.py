from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import random
from group_by_level import group_by_level
import os
from dotenv import load_dotenv

load_dotenv()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
READ_SPREADSHEET_ID = os.environ.get('READ_SPREADSHEET_ID')
WRITE_SPREADSHEET_ID = os.environ.get('WRITE_SPREADSHEET_ID')
READ_RANGE_NAME = "'Form Responses 1'!A:H"
WRITE_RANGE_NAME = "'Sheet1'!A:I"

def main():
    # ##############################################################################
    # GOOGLE SHEETS SETUP AND READ INPUT SHEET
    # ##############################################################################

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=READ_SPREADSHEET_ID,
                                range=READ_RANGE_NAME).execute()
    values = result.get('values', [])

    # ##############################################################################
    # SORTING ALGORITHM
    # ##############################################################################

    class Attendee:
        def __init__(self, name, level, algos_completed, lang1, lang2, lang3, lang_other):
            self.name = name
            self.level = level
            self.algos_completed = algos_completed
            self.lang1 = lang1
            self.lang2 = lang2
            self.lang3 = lang3
            self.lang_other = lang_other
            self.can_pair = True

        def __str__(self):
            return f'<Attendee> {self.name}, {self.lang1}, {self.lang2}, {self.lang3}, {self.lang_other}, {self.can_pair}'


    # INITIAL GROUPING BY LANGUAGE AND LEVEL
    beginners = []
    nonbeginners = []

    seen = []

    if not values:
        print('No data found.')
    else:
        values = values[1:]
        for row in values:
            if row != []:
                row = row[1:]
                if len(row) < 7:
                    row.append('')
                for i in range(len(row)):
                    row[i] = row[i].lower()
                    if row[i] == 'other, state below':
                        row[i] = 'other'
                    elif row[i] == 'not beginner':
                        row[i] = 'nonbeginner'
                if row not in seen:
                    attendee = Attendee(name=row[0], level=row[1], algos_completed=row[2], lang1=row[3], lang2=row[4], lang3=row[5], lang_other=row[6])
                    if attendee.level == 'beginner':
                        beginners.append(attendee)
                    else:
                        nonbeginners.append(attendee)
                    seen.append(row)

    print("***** BEGINNERS PRE-GROUPING *****")
    for beginner in beginners:
        print(f'\t{beginner}')
    print("***** NONBEGINNERS PRE-GROUPING *****")
    for non in nonbeginners:
        print(f'\t{non}')

    print("######################################################")
    print("######################################################")
    print("######################################################")
    print("######################################################")
    print("######################################################")

    print('group by level, beginner')
    beginner_groups = group_by_level(beginners)
    print('group by level, nonbeginner')
    nonbeginner_groups = group_by_level(nonbeginners)

    final_groups = beginner_groups + nonbeginner_groups

    print("***** BEGINNERS *****")
    for group in beginner_groups:
        print("##################################################")
        for attendee in group:
            print(attendee)
    print("***** NONBEGINNERS *****")
    for group in nonbeginner_groups:
        print("##################################################")
        for attendee in group:
            print(attendee)
    print("***** FINAL GROUPS *****")
    for group in final_groups:
        print("##################################################")
        for attendee in group:
            print(attendee)

    # ##############################################################################
    # GOOGLE SHEETS WRITE TO OUTPUT SHEET
    # ##############################################################################

    values = []
    for group in final_groups:
        for attendee in group:
            row = [attendee.name, attendee.level, attendee.algos_completed, attendee.lang1, attendee.lang2, attendee.lang3, attendee.lang_other, attendee.can_pair]
            values.append(row)
        values.append(['', '', '', '', '', '', '', ''])
    values.append(['END', 'END', 'END', 'END', 'END', 'END', 'END', 'END'])
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=WRITE_SPREADSHEET_ID, range=WRITE_RANGE_NAME,
        valueInputOption='RAW', body=body).execute()



if __name__ == '__main__':
    main()