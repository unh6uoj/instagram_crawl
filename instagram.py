import requests
from datetime import datetime
import json

class Instagram:
    def __init__(self):
        self.csrf_token = ""
        self.session_id = ""
        self.headers = {}
        self.cookies = {}

        self.sess = None
    
    def login(self, username, password):
        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        self.sess = requests.session()

        time = int(datetime.now().timestamp())
        response = self.sess.get(link)
        csrf = response.cookies['csrftoken']

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        self.headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf
        }

        login_response = self.sess.post(login_url, data=payload, headers=self.headers)
        json_data = json.loads(login_response.text)

        print(login_response.status_code, login_response.text)

        if json_data["authenticated"]:
            self.cookies = login_response.cookies
            # cookie_jar = self.cookies.get_dict()
            # csrf_token = cookie_jar['csrftoken']
            # session_id = cookie_jar['sessionid']
        else:
            print("login failed ", login_response.text)

    def get_search_data_tag_name(self, tag_name):
        url = "https://i.instagram.com/api/v1/tags/web_info"

        print(self.headers)
        print(self.cookies)

        r = self.sess.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            params={
                "tag_name": tag_name
            }
        )

        print(r.text)


username = ""
password = ""

instagram = Instagram()
instagram.login(username, password)
instagram.get_search_data_tag_name("캠핑")