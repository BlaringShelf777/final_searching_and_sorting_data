from sourse.primes import isPrime, makeItPrime, primeList

# Types

MOVIE = 'movie'
USER = 'user'
TAG = 'tag'
GENRE = 'genre'

class Hash:
    # Initializes a Hash
    def __init__(self, n, hash_type):
        self.N = n                                                      # Size of the data set      (Int)                                                                                                                                             # Hash Map
        self.M = makeItPrime(n * 2)                                     # Size of the Hash Map      (Int)
        self.type = hash_type                                           # The type of the hash map  (Str)
        if   self.type == MOVIE: self.hash_map = [Movie()] * self.M     # Hash Map                  (Hash Item)
        elif self.type == USER: self.hash_map = [User()] * self.M     
        elif self.type == TAG: self.hash_map = [Tag()] * self.M
        elif self.type == GENRE: 
            self.hash_map = [Genre()] * self.M
            self.N_aux = 0
        else: return None
        self.prime_list = primeList(makeItPrime(self.M))                # List of prime Numbers     (List) 
    
    # Add Hash items
    # Adds a movie to the HashMap
    def add_movie(self, movie_id, movie_title, movie_genres):
        if self.type == MOVIE:
            hash_key = self.hash_function_number(movie_id)
            index = 0
            while self.hash_map[hash_key].ocuppied and index < self.N:
                index += 1
                hash_key = self.hash_function_number(movie_id, index)
            if self.hash_map[hash_key].ocuppied:
                return False
            self.hash_map[hash_key] = Movie(movie_id, movie_title, movie_genres, True)
            return True
        return None
    
    # Adds an user to the HashMap
    def add_user(self, user_id, user_rating, movie_id):
        if self.type == USER:
            hash_key = self.hash_function_number(user_id)
            index = 0
            while self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].id != user_id and index < self.N:
                index += 1
                hash_key = self.hash_function_number(user_id, index)
            if not self.hash_map[hash_key].ocuppied:
                self.hash_map[hash_key] = User(user_id, True)
            if user_id == self.hash_map[hash_key].id:
                self.hash_map[hash_key].insert_rating(user_rating, movie_id)
            else:
                return False
            return True
        return None

    # Adds a tag to the HashMap
    def add_tag(self, tag, movie_id):
        if self.type == TAG:
            hash_key = self.hash_function_str(tag)
            index = 0
            while self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].tag != tag and index < self.N:
                index += 1
                hash_key = self.hash_function_str(tag, index)
            if not self.hash_map[hash_key].ocuppied: self.hash_map[hash_key] = Tag(tag, True)
            if tag == self.hash_map[hash_key].tag: self.hash_map[hash_key].insert_movie_id(movie_id)
            else: return False
            return True
        return None

    # Adds a genre to the Hash map
    def add_genre(self, genre, movie_id, rebuild_hash=False):
        if self.type == GENRE:
            hash_key = self.hash_function_str(genre)
            index = 0
            while self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].genre != genre and index < self.N:
                index += 1
                hash_key = self.hash_function_str(genre, index)
            if not self.hash_map[hash_key].ocuppied: 
                self.hash_map[hash_key] = Genre(genre, True)
                self.N_aux += 1
            if genre == self.hash_map[hash_key].genre and rebuild_hash: self.hash_map[hash_key].movies = movie_id
            elif genre == self.hash_map[hash_key].genre: self.hash_map[hash_key].insert_movie_id(movie_id)
            else: return False
            if self.N_aux / self.M > 1.5:
                self.rebuild_hash()
            return True
        return None
    
    def rebuild_hash(self):
        genres = list()
        # Stores the genres
        for genre in self.hash_map:
            if genre.genre != None:
                genres.append(genre)
        # Updates the Hash info
        self.N *= 2
        self.M = makeItPrime(self.N * 2)
        self.prime_list = primeList(makeItPrime(self.M))
        self.hash_map = [Genre()] * self.M
        self.N_aux = 0
        # Insert the genres again
        for genre in genres:
            self.add_genre(genre.genre, genre.movies, True)


        

    ## Query:
    # Queries for a movie in the hash map
    def query_hash_movie(self, movie_id):
        if self.type == MOVIE:
            index = 0
            hash_key = self.hash_function_number(movie_id) 
            while self.hash_map[hash_key].id != movie_id and index < self.N:
                index += 1
                hash_key = self.hash_function_number(movie_id, index)
            return self.hash_map[hash_key] if self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].id == movie_id else None                          
        return None

    # Queries for an user in the hash map
    def query_hash_user(self, user_id):
        if self.type == USER:
            index = 0
            hash_key = self.hash_function_number(user_id) 
            while self.hash_map[hash_key].id != user_id and index < self.N:
                index += 1
                hash_key = self.hash_function_number(user_id, index)
            return self.hash_map[hash_key] if self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].id == user_id else None                          
        return None
    
    # Queries for a tag in the hash map
    def query_hash_tag(self, tag):
        if self.type == TAG:
            index = 0
            hash_key = self.hash_function_str(tag) 
            while self.hash_map[hash_key].tag != tag and index < self.N:
                index += 1
                hash_key = self.hash_function_str(tag)
            return self.hash_map[hash_key] if self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].tag == tag else None                          
        return None

    # Queries for a genre in the Hash
    def query_hash_genre(self, genre):
        if self.type == GENRE:
            index = 0
            hash_key = self.hash_function_str(genre) 
            while self.hash_map[hash_key].genre != genre and index < self.N:
                index += 1
                hash_key = self.hash_function_str(genre)
            return self.hash_map[hash_key] if self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].genre == genre else None                          
        return None
    
    ## Hash Funtion:
    # Aux funtion to the hashing function
    def hashFuncAux(self, number, index=0):
        return (number * self.prime_list[index % len(self.prime_list)]) % self.M

    # Hashing Funtion for movie_id and user_id
    def hash_function_number(self, number, index=0):
        number -= 1
        return (number + index * self.prime_list[index % len(self.prime_list)] * self.hashFuncAux(number, index)) % self.M

    # Hashing Functions for tags (strings)
    def hash_function_str(self, tag, index=0):
        key = 0
        for letter in tag:
            key += self.hash_function_number(ord(letter), index)
        return key % self.M


# Hash items
class Movie:
    def __init__(self, movie_id=None, movie_title=None, movie_genres=None, ocuppied=False):
        self.id = movie_id                  # Movie Id      (Int)
        self.title = movie_title            # Movie Title   (Str)
        self.genres = movie_genres          # Movie Genres  (List of Str's or None)
        self.total_rating = 0               # Total Rating  (Int)
        self.rating_count = 0               # Rating Count  (Int)
        self.ocuppied = ocuppied            # Ocuppied Flag (Bool)
    
    def __str__(self):
        if self.ocuppied:
            return f'<{self.id}, {self.title}, {self.genres}, {self.total_rating / self.rating_count if self.rating_count else self.rating_count}, {self.rating_count}>'
        return None

    def __repr__(self):
        return self.__str__()

    def increase_rating(self, rating):
        self.total_rating += rating
        self.rating_count += 1
    
    def calc_rating(self):
        return self.total_rating / self.rating_count if self.rating_count else 0

class User:
    def __init__(self, user_id=None, ocuppied=False):
        self.id = user_id           # User ID               (Int)
        self.ratings = list()       # List of rated movies  (List)
        self.ocuppied = ocuppied    # Ocuppied flag         (Bool)
    
    def __str__(self):
        return f'<({self.id}, {self.ratings})>'
    
    def __repr__(self):
        return self.__str__(self)

    def insert_rating(self, rating, movie_id):
        self.ratings.append((rating, movie_id))
    
class Tag:
    def __init__(self, tag=None, ocuppied=False):
        self.tag = tag              # Tag
        self.movies = list()        # list of movie ID's
        self.ocuppied = ocuppied    # Flag
    
    def insert_movie_id(self, movie_id):
        if not movie_id in self.movies: self.movies.append(movie_id)

class Genre:
    def __init__(self, genre=None, ocuppied=False):
        self.genre = genre          # Genre (str)
        self.movies = list()        # List of movie ID's (list)
        self.ocuppied = ocuppied    # Flag (bool)
    
    def insert_movie_id(self, movie_id):
        self.movies.append(movie_id)
    