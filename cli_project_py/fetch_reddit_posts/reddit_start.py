import requests
import requests.auth
import json
from pprint import pprint
from datetime import datetime
import send_email_smtplib as mymail
from util import fetch_posts,convert_posts_to_html
import configparser

#1. reddit 내 subreddit의 hot 게시물 가져오기

## client 정보
section = 'REDDIT_CLIENT'
config = configparser.ConfigParser()
config.read('..\prop.config')
project_name = config.get(section,'ProjectName')
username = config.get(section,'Username')
user_password = config.get(section,'Password')
client_id = config.get(section,'ClientId')
client_secret = config.get(section,'ClientSecret')
client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
# user_agent : <platform>:<app ID>:<version string> (by /u/<reddit username>)
user_agent = config.get(section,'UserAgent')


## access token을 얻기 위한 oauth api 호출
post_data = {"grant_type":"password", "username": username, "password":user_password}
headers = {"User-Agent":user_agent}
auth_url = "https://www.reddit.com/api/v1/access_token"
response = requests.post(auth_url, auth=client_auth, data=post_data, headers=headers)
token = response.json().get("access_token")

## 인증 성공(정상 응답)시 원하는 api 호출
posts_text = {}
posts_html = []
subreddits = ["programming", "learnprogramming","python","javascript","rust"]
limit = 3
print(user_agent)
print(response.status_code)
if response.status_code == 200:

    for subreddit in subreddits:
        posts = fetch_posts(token, user_agent, subreddit, limit)
        # print(f"{subreddit} size : {len(posts)}")
        posts_text[subreddit] = posts
     
    posts_html = convert_posts_to_html(posts_text)            

                     
    text = "Sorry. This content is only readable in html format yet."
    html = "".join(posts_html)
    '''
    send_email: 메일 발송 모듈
    realpython.com(https://realpython.com/python-send-email/) 튜토리얼의 코드 참조
    '''
    mymail.send_email(text, html)   