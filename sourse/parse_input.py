
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

    print(f'> Movies Ternary Search Tree created, Movies Hash Map created, Genres Hash Map created - {(time.time() - execution_start) / 60} min')
    # Open files
    ratings_file_path, tag_file_path = f'{PATH}{rating_file_name}', f'{PATH}{tag_file_name}'
    ratings, tags = open(ratings_file_path, encoding='utf8'), open(tag_file_path, encoding='utf8')
    # Reads Header
    rating_line, tag_line = ratings.readline(), tags.readline()
    # Data structures
    users_hash = Hash(USERS, 'user')
    tags_hash = Hash(TAGS, 'tag')
    
    # Flags 
    ratings_flag, tags_flag = True, True
    execution_start = time.time()
    for i in range(RATINGS):
        if rating_line != '':
            rating_line = ratings.readline()
            if rating_line != '':
                # Parse CSV line: User Id - Movie Id - User Rating
                user_id, movie_id, user_rating = re.findall(r'(.*?),(.*?),(.*?),', rating_line)[0]
                user_id, movie_id, user_rating = int(user_id), int(movie_id), float(user_rating)
                # Queries for the movie
                movie = movies_hash.query_hash_movie(movie_id)
                # Updates the rating
                movie.increase_rating(user_rating)
                # Adds the user to the User Ternary Tree
                users_hash.add_user(user_id, user_rating, movie_id)
            else:
                if ratings_flag:
                    print(f'> Users Hash Map: {(time.time() - total_execution_time) / 60} min.')
                    ratings_flag = False 

        if tag_line != '':
            tag_line = tags.readline()
            if tag_line != '':
                # Parse CSV line: Movie id - User tag
                movie_id, user_tag = re.findall(r'.*?,(.*?),"(.*?)",', tag_line)[0]
                # Adds the tag to the hash
                tags_hash.add_tag(user_tag.lower(), int(movie_id))
            else:
                if tags_flag:
                    print(f'> Tags Hash Map: {(time.time() - total_execution_time) / 60} min.')
                    tags_flag = False 
    tags.close()
    ratings.close()
    print(f'> {(time.time() - total_execution_time) / 60} min')
    return movies_hash, genres_hash, users_hash, tags_hash, ternary_search_tree