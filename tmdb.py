import requests
from pymongo import MongoClient

def get_basic_movie_details(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        'api_key': api_key,
        'language': 'en-US'  # Optional language parameter
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        # List of fields you want to remove
        fields_to_remove = ['backdrop_path', 'homepage', 'imdb_id', 'overview', 'poster_path', 'production_countries', 'spoken_languages', 'tagline']
        for field in fields_to_remove:
            data.pop(field, None)  # Remove the field from the dictionary

        # MongoDB connection and insertion
        mongo_uri = "mongodb+srv://mohitzaveri06:socialmedia@cluster0.w6rxspg.mongodb.net/"
        client = MongoClient(mongo_uri)
        db = client['socialmedia']  # name of the database
        collection = db['tmdb_basic']  # name of the collection for TMDb movie details

        # Insert filtered movie data into the collection
        collection.insert_one(data)
        print(f"Stored the movie details of '{data['title']}' in the database.")

        return data
    else:
        return response.status_code, response.json()

# Replace with your actual API key from TMDb
your_api_key = 'dd57359b4df32f6b29ede46ac199c76f'


# Replace with a valid movie ID
movies = [872585,346698,385687,19995,361743,577922,157336,335983,48311,629162,507089,19614]

for movie in movies:
    # Fetch and store movie reviews
    print(get_basic_movie_details(movie, your_api_key))
