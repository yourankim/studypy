import requests
import requests.auth
import json
from pprint import pprint
from datetime import datetime
import reddit_client as client
import send_mail_smtplib as mymail

#1. reddit 내 subreddit의 hot 게시물 가져오기

## client 정보
project_name = client.project_name
username = client.username
user_password = client.user_password
client_id = client.client_id
client_secret = client.client_secret
client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
# user_agent : <platform>:<app ID>:<version string> (by /u/<reddit username>)
user_agent = client.user_agent


## access token을 얻기 위한 oauth api 호출
post_data = {"grant_type":"password", "username": username, "password":user_password}
headers = {"User-Agent":client.user_agent}
auth_url = "https://www.reddit.com/api/v1/access_token"
response = requests.post(auth_url, auth=client_auth, data=post_data, headers=headers)
token = response.json().get("access_token")

## 인증 성공(정상 응답)시 원하는 api 호출
posts_text = []
posts_html = []
subreddit = "programming"
sort_type = "hot"
if response.status_code == 200:
    headers = {"Authorization":f"bearer {token}", "User-Agent": user_agent}
    params = { "limit": 5 } 
    url = f"https://oauth.reddit.com/r/{subreddit}/{sort_type}"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        content = response.json() # response.json()은 dict를 반환
        children = content.get("data").get("children")
        for child in children:
            textrow = []
            htmlrow = []
            
            post = child.get("data")
            title = post.get("title")
            author = post.get("author")
            dt = datetime.fromtimestamp(int(post.get("created")))
            created = dt.strftime('%Y-%m-%d %I:%M%p')
            text = post.get("selftext")
            link = post.get("permalink")
            media = post.get("media_embed")
            num_comments = post.get("num_comments")
            row = {"title":title, "author":author, "created":created, "text":text[:140], "num_comments":num_comments, "link":link}
            posts_text.append(json.dumps(row))
            
            posts_html.append(f"""\
                          <p><a href="https://www.reddit.com{link}">{title}({num_comments})</a><p>
                          {author} | {created}<br>
                          {text}...<br><br>  
            """)
                     

        text = "".join(posts_text)
        html = "".join(posts_html)
        '''
        send_email: 메일 발송 모듈
        realpython.com(https://realpython.com/python-send-email/) 튜토리얼의 코드 참조
        '''
        mymail.send_email(text, html)   