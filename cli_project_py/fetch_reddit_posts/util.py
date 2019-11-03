import requests
import requests.auth
import json
from pprint import pprint
from datetime import datetime

def fetch_posts(token, user_agent, subreddit, limit):
    posts = []
    sort_type = "best"
    headers = {"Authorization":f"bearer {token}", "User-Agent": user_agent}
    params = { "limit": limit } 
    url = f"https://oauth.reddit.com/r/{subreddit}/{sort_type}"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
       print(response.status_code)
       return None 

    #pprint(response.json())
    content = response.json() # response.json()은 dict를 반환
    children = content.get("data").get("children")
    for child in children:
        row = []
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
        posts.append(row)

    return posts



def convert_posts_to_html(posts_text):
    posts_html = []
    if posts_text is None:
        print("The posts list is None.")
        return None

    if len(posts_text) < 1 :
        print("length of posts is zero.") 
        return None
    
    for key in posts_text:
        posts = posts_text[key]
        if posts is None:
            continue
        posts_html.append(f"<h2>{key}</h2>")
        for post in posts:
            if post is None:
                continue
            if type(post) is not dict:
                continue
            posts_html.append(f"""\
                    <p><a href="https://www.reddit.com{post.get('link')}">
                    {post.get('title')}({post.get('num_comments')})</a><p>
                    {post.get('author')} | {post.get('created')}<br>
                    {post.get('text')}...<br><br>  
                    """)  
        posts_html.append("<hr>")            

    return posts_html          