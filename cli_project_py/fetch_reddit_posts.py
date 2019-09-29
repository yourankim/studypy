import requests
import requests.auth
import json
from datetime import datetime
import reddit_client as client


#1. reddit 내 subreddit의 hot 게시물 가져오기

## client 정보
project_name = client.project_name
username = client.username
user_password = client.user_password
client_id = client.client_id
client_secret = client.client_secret
client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)


## access token을 얻기 위한 oauth api 호출
post_data = {"grant_type":"password", "username": username, "password":user_password}
headers = {"User-Agent":project_name+"/0.1 by "+ username}
auth_url = "https://www.reddit.com/api/v1/access_token"
response = requests.post(auth_url, auth=client_auth, data=post_data, headers=headers)
content = response.json()

## 인증 성공(정상 응답)시 원하는 api 호출
posts = []
subreddit = "programming"
if response.status_code == 200:
    headers = {"Authorization":"bearer "+content["access_token"], "User-Agent": project_name+"/0.1 by "+username}
    params = { "limit": 10 } 
    url = "https://oauth.reddit.com/r/"+subreddit+"/hot"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        content = response.json() # response.json()은 dict를 반환
        children = content.get("data").get("children")
        for child in children:
            post = child.get("data")
            title = post.get("title")
            author = post.get("author")
            dt = datetime.fromtimestamp(int(post.get("created")))
            created = dt.strftime('%Y-%m-%d %I:%M%p')
            text = post.get("selftext")
            url = child.get("permalink")
            row = {"title":title, "author":author, "created":created, "text":text, "url":url}
            posts.append(row)

        print(json.dumps(posts, indent=2))    
        