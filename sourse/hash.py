from primes import isPrime, makeItPrime, primeList

# Types

MOVIE = 'movie'
USER = 'user'
TAG = 'tag'

class Hash:
    # Initializes a Hash
    def __init__(self, n, hash_type):
        self.N = n                                                      # Size of the data set      (Int)                                                                                                                                             # Hash Map
        self.M = makeItPrime(n * 2)                                     # Size of the Hash Map      (Int)
        self.type = hash_type                                           # The type of the hash map  (Str)
        self.prime_list = primeList(makeItPrime(self.M))                # List of prime Numbers     (List) 
        if hash_type == MOVIE: self.hash_map = [Movie()] * self.M       # Hash Map                  (Hash Item)
        elif hash_type == USER: self.hash_map = [User()] * self.M                             

    # Adds a movie to the HashMap
    def add_movie(self, movie_id, movie_title, movie_genres):
        if self.type == MOVIE:
            hash_key = self.hashFunc(movie_id)
            index = 0
            while self.hash_map[hash_key].ocuppied and index < self.N:
                index += 1
                hash_key = self.hashFunc(movie_id, index)
            if self.hash_map[hash_key].ocuppied:
                return False
            self.hash_map[hash_key] = Movie(movie_id, movie_title, movie_genres, True)
            return True
        return None
    
    # Adds an user to the HashMap
    def add_user(self, user_id, user_rating, movie_id):
        if self.type == USER:
            hash_key = self.hashFunc(user_id)
            index = 0
            while self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].id != user_id and index < self.N:
                index += 1
                hash_key = self.hashFunc(user_id, index)
            if not self.hash_map[hash_key].ocuppied:
                self.hash_map[hash_key] = User(user_id, True)
            if user_id == self.hash_map[hash_key].id:
                self.hash_map[hash_key].insert_rating(user_rating, movie_id)
            else:
                return False
            return True
        return None

    # Queries for a movie in the hash map
    def query_hash_movie(self, movie_id):
        if self.type == MOVIE:
            index = 0
            hash_key = self.hashFunc(movie_id) 
            while self.hash_map[hash_key].id != movie_id and index < self.N:
                index += 1
                hash_key = self.hashFunc(movie_id, index)
            return self.hash_map[hash_key] if self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].id == movie_id else None                          
        return None

    # Queries for an user in the hash map
    def query_hash_user(self, user_id):
        if self.type == USER:
            index = 0
            hash_key = self.hashFunc(user_id) 
            while self.hash_map[hash_key].id != user_id and index < self.N:
                index += 1
                hash_key = self.hashFunc(user_id, index)
            return self.hash_map[hash_key] if self.hash_map[hash_key].ocuppied and self.hash_map[hash_key].id == user_id else None                          
        return None

    # Aux funtion to the hashing function
    def hashFuncAux(self, movie_id, index=0):
        return (movie_id * self.prime_list[index % len(self.prime_list)]) % self.M

    # Hashing Funtion
    def hashFunc(self, movie_id, index=0):
        return (movie_id + index * self.prime_list[index % len(self.prime_list)] * self.hashFuncAux(movie_id, index)) % self.M

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
    