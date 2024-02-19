#!/usr/bin/env python3
from dotenv import load_dotenv
import os
import requests
import pymongo
import datetime

# Loading environment variables
load_dotenv()

user_agent = 'python:subreddit_post_fetcher:v1.0 (by u/mzaveri1)'

# Reddit credentials from .env
client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_SECRET_KEY')
username = os.getenv('REDDIT_USERNAME')
password = os.getenv('REDDIT_PASSWORD')

# MongoDB connection details from .env
mongo_uri = os.getenv('MONGO_URI')

# Connecting to MongoDB
try:
    client = pymongo.MongoClient(mongo_uri)
    db = client['socialmedia']
    collection = db['reddit']
except pymongo.errors.ConnectionFailure as e:
    print(f"MongoDB Connection Error: {e}")
    exit(1)

# Reddit URLs
auth_url = 'https://www.reddit.com/api/v1/access_token'
api_url = 'https://oauth.reddit.com'

def get_reddit_auth():
    try:
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        data = {'grant_type': 'password', 'username': username, 'password': password}
        headers = {'User-Agent': user_agent}
        res = requests.post(auth_url, auth=auth, data=data, headers=headers)

        if res.status_code != 200:
            raise Exception("Error in obtaining the token:", res.status_code, res.text)

        TOKEN = res.json()['access_token']
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
        return headers
    except requests.RequestException as e:
        print(f"Error fetching Reddit auth token: {e}")
        exit(1)

def fetch_comments_for_post(post_id, limit, headers):
    try:
        url = f"{api_url}/comments/{post_id}?limit={limit}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve comments for post {post_id}. Status code: {response.status_code}")
            return []

        comments_data = response.json()
        comments = []
        for comment in comments_data[1]['data']['children']:
            if 'body' in comment['data']:
                comments.append({
                    "body": comment['data'].get('body'),
                    "upvotes": comment['data'].get('ups'),
                    "timestamp": datetime.datetime.fromtimestamp(comment['data'].get('created_utc'))
                })
        return comments
    except requests.RequestException as e:
        print(f"Error fetching comments: {e}")
        return []

def fetch_posts(subreddit, category, time_filter, headers):
    post_limit = 50 if category == "top" and time_filter == "all" else 30
    comment_limit = 45 if category == "top" and time_filter == "all" else 20

    try:
        url = f"{api_url}/r/{subreddit}/{category}.json?limit={post_limit}&t={time_filter}" if category == "top" else f"{api_url}/r/{subreddit}/{category}.json?limit={post_limit}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve {category} posts for subreddit {subreddit}. Status code: {response.status_code}")
            return []

        posts_data = response.json()['data']['children']
        posts = []
        for post_data in posts_data:
            post = post_data['data']
            comments = fetch_comments_for_post(post['id'], comment_limit, headers)
            posts.append({
                "title": post.get('title'),
                "likes": post.get('ups'),
                "total_comments": post.get('num_comments'),
                "timestamp": datetime.datetime.fromtimestamp(post.get('created_utc')),
                "top_comments": comments
            })
        return posts
    except requests.RequestException as e:
        print(f"Error fetching posts: {e}")
        return []

def fetch_and_store_subreddits_data(subreddit_list):
    headers = get_reddit_auth()
    categories = ['top', 'new', 'hot', 'controversial', 'rising']
    time_filters = ['all', 'year', 'month', 'day']

    for subreddit in subreddit_list:
        # Checking if data already exists for the subreddit
        existing_data = collection.find_one({"subreddit": subreddit})
        
        if existing_data:
            print(f"Data already exists for subreddit {subreddit}. Skipping...")
            continue

        all_posts_data = []
        for category in categories:
            time_filter = time_filters if category == 'top' else ['']
            for tf in time_filter:
                posts = fetch_posts(subreddit, category, tf, headers)
                all_posts_data.extend(posts)

        subreddit_info = {
            "subreddit": subreddit,
            "posts_data": all_posts_data
        }

        try:
            collection.update_one({"subreddit": subreddit}, {"$set": subreddit_info}, upsert=True)
            print(f"Data stored for subreddit {subreddit}")
        except pymongo.errors.PyMongoError as e:
            print(f"Error storing data in MongoDB for subreddit {subreddit}: {e}")


def fetch_general_movie_data():
    general_subreddits = ['movies', 'boxoffice', 'filmmakers']
    categories = ['hot', 'new', 'rising'] 
    post_limit = 10
    comment_limit = 10
    headers = get_reddit_auth()

    for subreddit in general_subreddits:
        all_posts_data = []
        for category in categories:
            posts = fetch_posts(subreddit, category, '', headers)  
            all_posts_data.extend(posts)

        subreddit_info = {
            "subreddit": subreddit,
            "posts_data": all_posts_data
        }

        try:
            collection.update_one({"subreddit": subreddit}, {"$set": subreddit_info}, upsert=True)
            print(f"Data stored for general subreddit {subreddit}")
        except pymongo.errors.PyMongoError as e:
            print(f"Error storing data in MongoDB for subreddit {subreddit}: {e}")

if __name__ == "__main__":
    subreddits = ['BarbieTheMovie', 'OppenheimerMovie', 'FastX', 'Avatar', 'topGunMaverick', 'tenet', 'interstellar', 'VenomMovie', 'ParasiteMovie', 'FerrariMovie', 'ItTheMovie', 'fivenightsatfreddys', 'MovieSuggestions', 'moviecritic', 'entertainment', 'TrueFilm', 'classicfilms', 'MovieDetails', 'horror', 'ForeignMovies' ]
    fetch_and_store_subreddits_data(subreddits)
    print(f"Data fetched and stored at {datetime.datetime.now()}")
