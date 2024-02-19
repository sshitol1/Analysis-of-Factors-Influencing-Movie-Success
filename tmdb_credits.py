import requests
from pymongo import MongoClient

def get_movie_credits(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    params = {
        'api_key': api_key,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        credits_data = response.json()

        # Extract and sort cast and crew by popularity
        if 'cast' in credits_data:
            credits_data['cast'] = sorted(credits_data['cast'], key=lambda x: x.get('popularity', 0), reverse=True)[:30]

        if 'crew' in credits_data:
            credits_data['crew'] = sorted(credits_data['crew'], key=lambda x: x.get('popularity', 0), reverse=True)[:30]

        # MongoDB connection and insertion
        mongo_uri = "mongodb+srv://mohitzaveri06:socialmedia@cluster0.w6rxspg.mongodb.net/"
        client = MongoClient(mongo_uri)
        db = client['socialmedia']  # name of the database
        collection = db['tmdb_credits']  # name of the collection for TMDb movie credits

        # Insert credits data into the collection
        collection.insert_one(credits_data)
        print(f"Stored credits for movie ID {movie_id} in the database.")

        return credits_data
    else:
        return response.status_code, response.json()

# Replace with your actual API key from TMDb
your_api_key = 'dd57359b4df32f6b29ede46ac199c76f'


# Replace with a valid movie ID
movies = [872585,346698,385687,19995,361743,577922,157336,335983,48311,629162,507089,19614]

for movie in movies:
    # Fetch and store movie reviews
    print(get_movie_credits(movie, your_api_key))
