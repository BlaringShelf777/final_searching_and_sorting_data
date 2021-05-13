from sourse.parse_input import parse_movies
import sourse.printing as p
from sourse.quick_sort import quick_sort
import re

MIN_COUNT = 1000

def movie(movie_prefix):
    movie_list = ternary_search_tree.query(movie_prefix)
    if movie_list == None or len(movie_list) == 0:
        print(f'> Nenhum filme com prefixo {movie_prefix} encontrado.\n')
        return
    p.print_movie_header()
    for movie_id in movie_list:
        movie = movies_hash.query_hash_movie(movie_id)
        movie_rating = movie.total_rating / movie.rating_count if movie.rating_count else '0.0'
        p.print_movie(movie.id, movie.title, movie.genres, movie_rating, movie.rating_count)
    p.screen_clear()

def user(user_id):
    user = users_hash.query_hash_user(user_id)
    if user == None:
        print(f'> Usuário com ID {user_id} não encontrado.\n')
        p.screen_clear()
        return
    p.print_user_rating_header()
    for rating in user.ratings:
        user_rating, movie_id = rating
        movie = movies_hash.query_hash_movie(movie_id)
        movie_rating = movie.total_rating / movie.rating_count if movie.rating_count else '0.0'
        p.print_user_rating(user_rating, movie.title, movie_rating, movie.rating_count)
    p.screen_clear()

def tags(tag_list):
    all_movies = list()
    tagged_movies = list()
    # Create a list of all the movies
    for tag in tag_list:
        tag_obj = tags_hash.query_hash_tag(tag.lower())
        if tag_obj == None: continue
        all_movies += tag_obj.movies
    
    if len(tag_list) > 1:
        for index, movie_id in enumerate(all_movies):
            if (movie_id in all_movies[:index] or movie_id in all_movies[index + 1:]) and not movie_id in tagged_movies:
                tagged_movies.append(movie_id)
        # Prints
        if len(tagged_movies) == 0:
            print(f'> Nenhum filme associado a(s) tag(s) {", ".join([tag for tag in tag_list])}')
            p.screen_clear()
            return
        p.print_movie_header()
        for movie_id in tagged_movies:
            movie = movies_hash.query_hash_movie(movie_id)
            movie_rating = movie.total_rating / movie.rating_count if movie.rating_count else '0.0'
            p.print_movie(movie.id, movie.title, movie.genres, movie_rating, movie.rating_count)
        p.screen_clear()
    else:
        p.print_movie_header()
        for movie_id in all_movies:
            movie = movies_hash.query_hash_movie(movie_id)
            movie_rating = movie.total_rating / movie.rating_count if movie.rating_count else '0.0'
            p.print_movie(movie.id, movie.title, movie.genres, movie_rating, movie.rating_count)
        p.screen_clear()

def top_n(genre, n):
    genre_obj = genres_hash.query_hash_genre(genre)
    if genre == None:
        print(f'> Gênero {genre} não encontrado.\n')
        p.screen_clear()
        return
    movies = genre_obj.movies
    movie_count = 0
    movie_index = len(movies) - 1
    quick_sort(movies, movies_hash, 0, len(movies) - 1)
    p.print_movie_header()
    while movie_count < n and movie_index >= 0:
        movie = movies_hash.query_hash_movie(movies[movie_index])
        if movie.rating_count >= MIN_COUNT:
            p.print_movie(movie.id, movie.title, movie.genres, movie.calc_rating(), movie.rating_count)
            movie_count += 1
        movie_index -= 1
    p.screen_clear()

def crap_n(genre, n):
    genre_obj = genres_hash.query_hash_genre(genre)
    if genre == None:
        print(f'> Gênero {genre} não encontrado.\n')
        p.screen_clear()
        return
    movies = genre_obj.movies
    quick_sort(movies, movies_hash, 0, len(movies) - 1)
    p.print_movie_header()
    movie_index = 0
    movie_count = 0
    while movie_index < len(movies) and  movie_count < n:
        movie = movies_hash.query_hash_movie(movies[movie_index])
        if movie.rating_count >= MIN_COUNT:
            p.print_movie(movie.id, movie.title, movie.genres, movie.calc_rating(), movie.rating_count)
            movie_count += 1
        movie_index += 1
    p.screen_clear()

# Genarate structures
movies_hash, genres_hash, users_hash, tags_hash, ternary_search_tree = parse_movies('movie_clean.csv', 'rating.csv', 'tag_clean.csv')
p.screen_clear()
user_input = ''

while user_input != 'exit':
    p.query_header()
    user_input = str(input('$ ')).lower()
    print('\n')

    if user_input.startswith('movie '):
        movie_prefix = re.findall(r'movie (.*)', user_input)[0]
        movie(movie_prefix)

    elif user_input.startswith('user '):
        try:
            parsed_input = re.findall(r'user ([0-9]*)', user_input)[0]
            user_id = int(parsed_input)
            user(user_id)
        except:
            print('> Função user usada de forma incorreta: user <userID>\n')
            
    elif user_input.startswith('top'):
        try:
            n, genre = re.findall(r'top(.*?) \'(.*?)\'', user_input)[0]
            top_n(genre, int(n))
        except:
            print('> Função top usada de forma incorreta: top<N> \'<genre>\'\n')
    
    elif user_input.startswith('crap'):
        try:
            n, genre = re.findall(r'crap(.*?) \'(.*?)\'', user_input)[0]
            crap_n(genre, int(n))
        except:
            print('> Função crap usada de forma incorreta: crap<N> \'<genre>\'\n')

    elif user_input.startswith('tags '):
        try:
            user_tags = re.split("' '", re.findall(r'tags \'(.*)\'', user_input)[0])
            tags(user_tags)
        except:
            print('> Função tags usada de forma incorreta: tags \'<tag_1>\' \'<tag_2>\' \'<tag_3>\' ...\n')

    elif user_input == 'exit': break

    else: print('> Comando não encontrado.\n')