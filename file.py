import random

def vectordistance(deck):
    return (sum((v - c) ** 2 for c, v in enumerate(deck))) ** 0.5

def flatten(l):
    return [item for sublist in l for item in sublist]

def riffle(deck):
    splitoffset = random.randint(0, 10)
    half =[0, deck[:26 + splitoffset], deck[26 + splitoffset:]]
    i = 1
    out = []

    while len(out) < len(deck):
        i *= -1
        r = random.choice([1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5])

        if len(half[i]) <= r:
            r = len(half[i]) 

        for _ in range(r):
            out.append(half[i].pop())

    return out


unshuffled = [i for i in range(52)]

