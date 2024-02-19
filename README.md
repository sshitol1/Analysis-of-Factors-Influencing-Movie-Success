Social Media Data Integration Project

Project Overview

This project consists of Python scripts designed to fetch and store data from various social media and movie-related APIs into a MongoDB database. The APIs utilized in this project include YouTube, Reddit, and The Movie Database (TMDb). The data fetched includes YouTube movie trailers statistics, Reddit posts and comments from specific subreddits, basic movie details from TMDb, and movie credits including cast and crew information.

Prerequisites

Python 3.x
MongoDB account and a cluster
API keys for YouTube, Reddit, and TMDb
Dependencies

Before running the scripts, install the required Python packages using the following command:

sh
Copy code
pip install google-api-python-client pymongo requests python-dotenv
Setup Instructions

Clone the Repository: Clone this repository to your local machine using git clone.
API Keys and MongoDB URI: Obtain API keys for YouTube, Reddit, and TMDb. Set up a MongoDB database and obtain your MongoDB URI.
Environment Variables: Create a .env file in the root directory of the project and fill in your API keys and MongoDB URI as follows:
makefile
Copy code
YOUTUBE_API_KEY=your_youtube_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_SECRET_KEY=your_reddit_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
MONGO_URI=your_mongodb_uri
TMDB_API_KEY=your_tmdb_api_key
Running the Scripts: Navigate to the project directory in your terminal and run each script individually as needed:
sh
Copy code
python youtube.py
python reddit.py
python tmdb.py
python tmdb_credits.py
Script Descriptions

YouTube API Script (youtube.py)
Fetches and stores YouTube video statistics and comments for movie trailers.
Stores data in a MongoDB collection named youtube.
Reddit API Script (reddit.py)
Fetches and stores posts and comments from specified subreddits.
Supports different post categories and time filters.
Stores data in a MongoDB collection named reddit.
TMDb API Script (tmdb.py)
Fetches and stores basic movie details from The Movie Database (TMDb).
Filters out unnecessary fields before storage.
Stores data in a MongoDB collection named tmdb_basic.
TMDb Credits Script (tmdb_credits.py)
Fetches and stores movie credits including cast and crew information from TMDb.
Sorts cast and crew by popularity before storage.
Stores data in a MongoDB collection named tmdb_credits.
Data Usage

The data fetched and stored by these scripts can be utilized for various applications such as social media analysis, movie recommendation systems, and content aggregation platforms.
