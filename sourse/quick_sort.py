import random
import time

def hoarePartition(movie_id_list, movie_hash_map, start, end):
    left, pivot_movie_id, i, j = True, movie_id_list[start], start, end
    pivot = movie_hash_map.query_hash_movie(pivot_movie_id)
    pivot_rating = pivot.calc_rating()
    while i != j:
        if left:
            movie = movie_hash_map.query_hash_movie(movie_id_list[j])
            movie_rating = movie.calc_rating()
            if movie_rating > pivot_rating:
                j -=1
            else:
                left = False
                movie_id_list[i] = movie_id_list[j]
                i += 1
        else:
            movie = movie_hash_map.query_hash_movie(movie_id_list[i])
            movie_rating = movie.calc_rating()
            if movie_rating < pivot_rating:
                i += 1
            else:
                left = True
                movie_id_list[j] = movie_id_list[i]
                j -= 1
    movie_id_list[j] = pivot_movie_id
    return j

def quick_sort(movie_id_list, movie_hash_map, start, end):
    if start < end:
        # Random Pivot
        randIndex = random.randint(start, end)
        movie_id_list[start], movie_id_list[randIndex] = movie_id_list[randIndex], movie_id_list[start]
        # Create Partition
        pivotIndex = hoarePartition(movie_id_list, movie_hash_map, start, end)
        # Recursion
        quick_sort(movie_id_list, movie_hash_map, start, pivotIndex - 1)
        quick_sort(movie_id_list, movie_hash_map, pivotIndex + 1, end)
