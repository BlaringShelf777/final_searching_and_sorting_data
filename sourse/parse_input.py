
from sourse.ternary_search_tree import TernarySearchTree, TernarySearchTreeTags
from sourse.hash import Hash
import time
import re

MOVIES = 27278
RATINGS = 20000263
RATINGS_MIN = 10000
TAGS = 465564
USERS = 138493
GENRES = 50
PATH = 'data\\'

def parse_movies(movies_file_name, rating_file_name, tag_file_name):
    total_execution_time = time.time()
    # Creates the Ternary Tree and a Hash Map for the movies
    try:
        execution_start = time.time()
        ternary_search_tree = TernarySearchTree()
        movies_hash = Hash(MOVIES, 'movie')
        genres_hash = Hash(GENRES, 'genre')
        movies_file_path = f'{PATH}{movies_file_name}'
        with open(movies_file_path, encoding='utf8') as movies:
            # Eliminates Header
            movies.readline()
            for movie in movies:
                # Parse a csv line - Movie ID, Movie Name, Movie Genres
                movie_id, movie_name, movie_genres = re.findall(r'(.*?),"(.*?)","(.*?)"', movie)[0]
                # parse Movie ID
                movie_id = int(movie_id)
                # Parse Genres
                movie_genres = movie_genres.split('|')
                # Adds the genre to the genre hash
                for genre in movie_genres:
                    genres_hash.add_genre(genre.lower(), movie_id)
                # Adds the movie name to the Ternary Search Tree
                ternary_search_tree.insert_word(movie_name, movie_id)
                # Adds the movie to the Hash Map
                movies_hash.add_movie(movie_id, movie_name, movie_genres)
    except:
        print(f'Error! file {movies_file_name} not found')
        return None
    print(f'> Movies Ternary Search Tree created, Movies Hash Map created, Genres Hash Map created - {(time.time() - execution_start) / 60} min')
    # Calculates rates 
    try:
        execution_start = time.time()
        ratings_file_path = f'{PATH}{rating_file_name}'
        # users_tree = TernarySearchTreeUser()
        users_hash = Hash(USERS, 'user')
        with open(ratings_file_path, encoding='utf8') as ratings:
            # Eliminates Header
            ratings.readline()
            for rate in ratings:
                # Parse CSV line: User Id - Movie Id - User Rating
                user_id, movie_id, user_rating = re.findall(r'(.*?),(.*?),(.*?),', rate)[0]
                user_id, movie_id, user_rating = int(user_id), int(movie_id), float(user_rating)
                # Queries for the movie
                movie = movies_hash.query_hash_movie(movie_id)
                # Updates the rating
                if movie != None: movie.increase_rating(user_rating)
                # Adds the user to the User Ternary Tree
                users_hash.add_user(user_id, user_rating, movie_id)
    except:
        print(f'Error! file {rating_file_name} not found')
        return None
    print(f'> Ratings Hash Map created  - {(time.time() - execution_start) / 60} min')
    # Creates the hash map for the tags
    try:
        execution_start = time.time()
        tag_file_path = f'{PATH}{tag_file_name}'
        tags_hash = Hash(TAGS, 'tag')
        with open(tag_file_path, encoding='utf8') as tags:
            # Eliminates Header
            tags.readline()
            for tag in tags:
                # Parse CSV line: Movie id - User tag
                movie_id, user_tag = re.findall(r'.*?,(.*?),"(.*?)",', tag)[0]
                # Adds the tag to the hash
                tags_hash.add_tag(user_tag.lower(), int(movie_id))
    except:
        print(f'Error! file {tag_file_name} not found')
        return None
    print(f'> Tags Hash Map created - {(time.time() - execution_start) / 60} min\n')
    print(f'> {(time.time() - total_execution_time) / 60} min')

    return movies_hash, genres_hash, users_hash, tags_hash, ternary_search_tree