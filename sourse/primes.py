
def isPrime(n):
    i = 2
    while i < n and n % i and n / i > i:
        i += 1
    return n >= 2 and (n % i != 0 or n == i)

def makeItPrime(n):
    while not isPrime(n):
        n += 1
    return n


def primeList(n):
    primes = []
    prime = 2
    while prime < n:
        primes.append(prime)
        prime = makeItPrime(prime + 1)
    return primes



