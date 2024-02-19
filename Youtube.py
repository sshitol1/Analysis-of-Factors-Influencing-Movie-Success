import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError 
from pymongo import MongoClient

# YouTube API setup
DEVELOPER_KEY = "AIzaSyCcXkXDkoCIE-3oeSr2QhujldnhyEOWzFc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# MongoDB setup
mongo_uri = "mongodb+srv://mohitzaveri06:socialmedia@cluster0.w6rxspg.mongodb.net/"
client = MongoClient(mongo_uri)
db = client['socialmedia']
collection = db['youtube']

def youtube_search_movie_trailer(movie_name, max_results=10):
    query = f"{movie_name} official trailer"
    search_response = youtube_object.search().list(
        q=query, 
        part="id,snippet",
        maxResults=max_results,
        type='video'
    ).execute()

    results = search_response.get("items", [])
    if results:
        video_ids = [result["id"]["videoId"] for result in results]
        video_response = youtube_object.videos().list(
            id=",".join(video_ids),
            part='snippet,contentDetails,statistics'
        ).execute()

        most_viewed_video = max(
            video_response.get("items", []), 
            key=lambda x: int(x["statistics"]["viewCount"])
        )

        title = most_viewed_video["snippet"]["title"]
        views = most_viewed_video["statistics"]["viewCount"]
        likes = most_viewed_video["statistics"].get("likeCount", "N/A")
        comments = most_viewed_video["statistics"].get("commentCount", "N/A")
        all_comments = get_all_comments(most_viewed_video["id"])


        for comment in all_comments:
            comment_with_movie = comment.copy()
            comment_with_movie["movie_name"] = movie_name
            if not collection.find_one({"text": comment["text"]}):
                collection.insert_one(comment)

        moviedetails = {
            "movie_name": movie_name, 
            "title": title,
            "views": views,
            "likes": likes,
            "comments": comments,
            "all_comments": all_comments
        }

        if not collection.find_one({"title": title}):
            collection.insert_one(moviedetails)
            print(f"Stored the trailer info and top comments of '{movie_name}' in the database.")
        else:
            print(f"'{movie_name}' already exists in the database.")
    else:
        print(f"No trailers found for {movie_name}.")

def get_all_comments(video_id):
    comments = []
    next_page_token = None

    try:
        while True:
            comments_response = youtube_object.commentThreads().list(
                videoId=video_id,
                part="snippet",
                order="relevance",
                maxResults=100,  
                pageToken=next_page_token
            ).execute()

            for item in comments_response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "text": comment["textDisplay"],
                    "likes": comment["likeCount"]
                })

            next_page_token = comments_response.get("nextPageToken")
            if not next_page_token:
                break
    except HttpError as error:
       
        print(f"Error fetching comments for '{movie_name}' (Video ID: {video_id}): {error}")
        return []

    return comments

_name_ = '_main_'
if _name_ == "_main_":
    while True:
        movie_names = [
            "Barbie The Movie",
            "Oppenheimer Movie",
            "Fast X",
            "Avatar",
            "Top Gun Maverick",
            "Tenet",
            "Interstellar",
            "Venom Movie",
            "Parasite Movie",
            "Ferrari Movie",
            "Five Nights at Freddy's",
            "It Movie"
        ]
        for movie_name in movie_names:
            youtube_search_movie_trailer(movie_name)
        print("Sleeping for 1 hour before the next fetch...")
        time.sleep(3600)  # Sleep for 1 hour
