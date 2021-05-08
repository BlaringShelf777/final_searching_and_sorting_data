
# Ternary Search Tree
class TernarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert_word(self, word, word_id):
        if len(word) <= 0:
            return
        self.root = self.__insert_word(self.root, word.lower(), word_id)
    
    def __insert_word(self, node, word, word_id):
        # First letter of the string
        letter = word[0]
        # None existing node
        if node == None:
            node = Node(letter)
        # Node bigger than letter search/insert left
        elif node.key > letter:
            node.child[0] = self.__insert_word(node.child[0], word, word_id)
            return node
        # Node smaller than letter search/insert right
        elif node.key < letter:
            node.child[2] = self.__insert_word(node.child[2], word, word_id)
            return node            
        # Checks word end
        if len(word) == 1:
            if node.label == None:
                node.label = word_id
            return node
        node.child[1] = self.__insert_word(node.child[1], word[1:], word_id)
        return node

    def query(self, word, prefix=True):
        if word == '':
            return 
        self.__query(word.lower(), self.root, prefix)
    
    def __query(self, word, node, prefix, found=''):
        if node == None:
            return
        if word != '':
            letter = word[0]
            if node.key == letter:
                found += letter
                if len(word) == 1 and node.label != None:
                    print(f'{found}, {node.label}')
                    if not prefix:
                        return
                self.__query(word[1:], node.child[1], prefix, found)
            elif node.key > letter:
                self.__query(word, node.child[0], prefix, found)
            else:
                self.__query(word, node.child[2], prefix, found)
            return
        else:
            if node.label != None:
                print(f'{found}{node.key}, {node.label}')
            if node.child[1] != None:
                self.__query(word, node.child[1], prefix, found + node.key)
            self.__query(word, node.child[0], prefix, found)
            self.__query(word, node.child[2], prefix, found)

class TernarySearchTreeTags:
    def __init__(self):
        self.root = None
    
    def insert_word(self, tag, movie_id):
        word = tag
        if len(word) <= 0:
            return
        self.root = self.__insert_word(self.root, word, tag, movie_id)
    
    def __insert_word(self, node, word, tag, movie_id):
        # First letter of the string
        letter = word[0]
        # None existing node
        if node == None:
            node = Node(letter)
        # Node bigger than letter search/insert left
        elif node.key > letter:
            node.child[0] = self.__insert_word(node.child[0], word, tag, movie_id)
            return node
        # Node smaller than letter search/insert right
        elif node.key < letter:
            node.child[2] = self.__insert_word(node.child[2], word, tag, movie_id)
            return node            
        # Checks word end
        if len(word) == 1:
            if node.label == None:
                node.label = tag
                node.tag = Tag(Tag)
            node.tag.insert_movie(movie_id)
            return node
        node.child[1] = self.__insert_word(node.child[1], word[1:], tag, movie_id)
        return node

    def query(self, tag):
        word = tag
        node = self.root
        while len(word) > 1 and node != None:
            letter = word[0]
            if node.key > letter: node = node.child[0]
            elif node.key < letter: node = node.child[2]
            else:
                node = node.child[1]
                word = word[1:]
        return node.tag if node != None and node.label == tag else None



class Node:
    def __init__(self, key=None, label=None, tag=None):
        self.key = key
        self.label = label
        self.tag = tag
        self.child = [None, None, None]

class Tag:
    def __init__(self, tag=None):
        self.tag = tag             # Tag             (str)
        self.movies = list()       # List of movies  (List)

    def insert_movie(self, movie_id):
        self.movies.append(movie_id)