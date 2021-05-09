from sourse.parse_input import parse_movies
import sourse.printing as p


def movie(movie_prefix):
    movie_list = ternary_search_tree.query(movie_prefix)
    if len(movie_list) == 0:
        print(f'> Nenhum filme com prefixo {movie_prefix} encontrado.\n')
        return
    p.print_movie_header()
    for movie_id in movie_list:
        movie = movies_hash.query_hash_movie(movie_id)
        movie_rating = movie.total_rating / movie.rating_count if movie.rating_count else '0.0'
        p.print_movie(movie.id, movie.title, movie.genres, movie_rating, movie.rating_count)

def user(user_id):
    user = users_hash.query_hash_user(user_id)
    if user == None:
        print(f'> Usuário com ID {user_id} não encontrado.\n')
        return
    p.print_user_rating_header()
    for rating in user.ratings:
        user_rating, movie_id = rating
        movie = movies_hash.query_hash_movie(movie_id)
        movie_rating = movie.total_rating / movie.rating_count if movie.rating_count else '0.0'
        p.print_user_rating(user_rating, movie.title, movie_rating, movie.rating_count)
         


# Genarate structures
movies_hash, genres_hash, users_hash, tags_hash, ternary_search_tree = parse_movies('movie_clean.csv', 'minirating.csv', 'tag_clean.csv')





    

