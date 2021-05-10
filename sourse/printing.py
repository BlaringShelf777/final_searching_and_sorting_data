from math import trunc
import os

# Movie
M_ID_LEN     = 6
M_TITLE_LEN  = 60
M_GENRE_LEN  = 50
M_RATING_LEN = 8
# User
U_RATING_LEN = 8

SYM = '_'

def print_movie_header():
    print(f'ID{" " * (M_ID_LEN + 1)} Title{" " * (M_TITLE_LEN - 2)} Genres{" " * (M_GENRE_LEN - 3)} Rating{" " * (M_RATING_LEN - 3)} Count')
    print(f'{SYM * (M_ID_LEN + M_TITLE_LEN + M_GENRE_LEN + M_RATING_LEN + 25)}')

def print_movie(id, movie_title, gender, rating, rating_count):
    movie_id, movie_genders, movie_rating = str(id), ','.join(gender), str(rating)
    # Adjusts movie id
    if len(movie_id) < M_ID_LEN: movie_id += ' ' * (M_ID_LEN - len(movie_id))
    # Adjusts movie title
    if len(movie_title) < M_TITLE_LEN: movie_title += ' ' * (M_TITLE_LEN - len(movie_title))
    elif len(movie_title) > M_TITLE_LEN: movie_title = movie_title[:M_TITLE_LEN - 3] + '...'
    # Adjusts movie genders
    if len(movie_genders) < M_GENRE_LEN: movie_genders += ' ' * (M_GENRE_LEN - len(movie_genders))
    elif len(movie_genders) > M_GENRE_LEN: movie_genders = movie_genders[:M_GENRE_LEN - 3] + '...'
    # Adjusts movie rating
    if len(movie_rating) < M_RATING_LEN: movie_rating += '0' * (M_RATING_LEN - len(movie_rating))
    if len(movie_rating) > M_RATING_LEN: movie_rating = movie_rating[:M_RATING_LEN]
    # Prints
    print(f'{movie_id}   |{movie_title}   |{movie_genders}   |{movie_rating}   |{rating_count}')

def print_user_rating_header():
    print(f'User Rating    Title{" " * (M_TITLE_LEN + 7)} Global Rating{" " * (M_RATING_LEN - 5)} Count')
    print(f'{SYM * (M_TITLE_LEN + M_GENRE_LEN + M_RATING_LEN)}')

def print_user_rating(user_rating, movie_title, movie_rating, rating_count):
    user_rating = str(user_rating)
    movie_rating = str(movie_rating)
    # Adjusts user rating
    user_rating = ' ' * (U_RATING_LEN - len(user_rating) + 3) + user_rating
    # Adjusts movie title
    if len(movie_title) < M_TITLE_LEN: movie_title += ' ' * (M_TITLE_LEN - len(movie_title))
    elif len(movie_title) > M_TITLE_LEN: movie_title = movie_title[:M_TITLE_LEN - 3] + '...'
    # Adjusts movie rating
    if len(movie_rating) < M_RATING_LEN: movie_rating += '0' * (M_RATING_LEN - len(movie_rating))
    if len(movie_rating) > M_RATING_LEN: movie_rating = movie_rating[:M_RATING_LEN]
    # Prints
    print(f'{user_rating}   |{movie_title}   {" " * 9}|{movie_rating}        |{rating_count}')

# The screen clear function
def screen_clear():
    input('\n> Precione \'Enter\' para continuar...')
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
    # for windows platfrom
      _ = os.system('cls')


def query_header():
    print('''\n
               Operações
    _______________________________

        > movie <movie_prefix>
        > user <user_id>
        > top<N> '<genre>'
        > tags '<list of tags>'
        > exit
    _______________________________
     \n''')