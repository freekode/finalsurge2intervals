from ast import parse
import requests
from bs4 import BeautifulSoup
import dateutil.parser as parser

HOST = 'https://log.finalsurge.com'
USERNAME = 'API_KEY'

FORM_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

class FinalSurgeApi:
    session = None
    username = None
    password = None
    logged_in = False

    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        self.password = password

    def login(self):
        if self.logged_in:
            print('already logged in')
            return
        login_data = {
            'login_name': self.username,
            'login_password': self.password,
            'SubmitType': 'lg'
        }

        resp = self.session.post(f'{HOST}/login.cshtml', headers=FORM_HEADERS, data=login_data, allow_redirects=False)
        if resp.status_code != 302:
            raise Exception('cannot login')
        self.logged_in = True

    def get_wellness(self, past_days):
        post_data = {
            'PastDays': past_days
        }
        resp = self.session.post(f'{HOST}/DailyVitals.cshtml', headers=FORM_HEADERS, data=post_data)
        soup = BeautifulSoup(resp.text, 'html.parser')
        table = soup.find(class_ = "table table-striped table-condensed")
        table_header = [cell.text for cell in table('tr')[0]('th')]
        table_content = [[cell.text.strip() for cell in row("td")] for row in table('tr')[1:]]

        daily_data = self._parse_daily_vitals(table_header, table_content)
        daily_data = self._update_date_format(daily_data)
        return daily_data

    def _parse_daily_vitals(self, table_header, table_content):
        out = []
        for row in table_content:
            day = {}
            j = 0
            while j < len(table_header):
                value = row[j]
                day[table_header[j]] = value if value else None
                j += 1

            out.append(day)
        return out[:-1]

    def _update_date_format(self, data):
        for entity in data:
            date_to_parse = entity['Date']
            parsed_data = parser.parse(date_to_parse)
            entity['Date'] = str(parsed_data.date())
        return data