import random, math, json
import numpy


def nCr(n, r):
    return math.factorial(n) / math.factorial(r) / math.factorial(n - r)


def riffle(deck):
    probs = [nCr(len(deck), r)/(2**len(deck)) for r in range(len(deck))]
    split = numpy.random.choice(list(range(len(deck))), p=probs)
    splitdeck = [A, B] = deck[:split], deck[split:]
    newdeck = []
    while A or B:
        newdeck.append(splitdeck[numpy.random.choice([0, 1], p=[len(A)/len(A+B), len(B)/len(A+B)])].pop(0))

    return newdeck


def rand(deck):
    newdeck = [e for e in deck]
    random.shuffle(newdeck)
    return newdeck


def overhand(deck):
    newdeck = []
    while len(deck) > 1:
        probs = [0.5**n for n in range(1, len(deck))]
        k = numpy.random.choice(list(range(1, len(deck))) + [0], p=probs+[1 - sum(probs)])
        newdeck.append(deck[len(deck) - k:])
        deck = deck[:len(deck) - k]

    return [item for sublist in newdeck for item in sublist] + [0]


def RSS(after, before=list(range(52))):
    return sum((after[i] - before[i])**2 for i in range(len(after))) ** 0.5


def RMS(after, before=list(range(52))):
    return RSS(after, before) / (len(after) ** 0.5)


def guessing(after, before=list(range(52))):
    count, guess, lastcard, toguess = 0, 0, 0, [i for i in before]

    for card in after:
        guess = numpy.random.choice(toguess)

        if lastcard != before[-1]:
            if before[before.index(lastcard) + 1] in toguess:
                guess = before[before.index(lastcard) + 1]
                                

        if card == guess:
            count += 1

        toguess.remove(card)
        lastcard = card
        
    return count


def getdata(shuffle=rand, measure=RSS,  decks=1000, shuffles=1, accuracy=1):
    xdata, ydata, newdecks, olddecks = [], [], [], [list(range(52)) for _ in range(decks)]

    for i in range(shuffles):
        print('Shuffling ' + str(decks) + ' decks...')
        newdecks = [shuffle(deck) for deck in olddecks]
        data = []
        for j in range(decks):
            print('Shuffle: ' + str(i) + ' Deck: ' + str(j))
            data.append(round(measure(newdecks[j], olddecks[j]), accuracy))

        olddecks = newdecks
        currentx = list(dict.fromkeys(data))
        currentx.sort()
        xdata.append(currentx)
        ydata.append([data.count(x) for x in currentx])

    with open('_'.join([shuffle.__name__, measure.__name__, str(decks), str(shuffles), str(accuracy), 'x.txt']), 'w') as outfile:
        json.dump(xdata, outfile)

    with open('_'.join([shuffle.__name__, measure.__name__, str(decks), str(shuffles), str(accuracy), 'y.txt']), 'w') as outfile:
        json.dump(ydata, outfile)


def fastdata(shuffles=(rand, riffle, overhand), measures=(RSS, guessing), decks=1000, iters=1, accuracy=1):
    for i, shuff in enumerate(shuffles):
        newdecks, olddecks = [], [list(range(52)) for _ in range(decks)]

        xdata = [[[] for _ in range(iters)] for __ in range(len(measures))]

        for j in range(iters):
            print('Shuffling ' + str(decks) + ' decks...')
            newdecks = [shuff(deck) for deck in olddecks]

            for k in range(decks):
                print('Deck: ' + str(k))
                for c, mesr in enumerate(measures):
                    xdata[c][j].append(round(mesr(newdecks[k], olddecks[k]), accuracy))

        currentx = [[list(dict.fromkeys(iteration)) for iteration in mesr] for mesr in xdata]
        ydata = [[[xdata.count(data) for data in iteration] for iteration in mesr] for mesr in currentx]

        for c, mesr in enumerate(measures):
            with open('_'.join([shuff.__name__, mesr.__name__, str(decks), str(iters), str(accuracy), 'x.txt']), 'w') as outfile:
                json.dump(xdata[c], outfile)

            with open('_'.join([shuff.__name__, mesr.__name__, str(decks), str(iters), str(accuracy), 'y.txt']), 'w') as outfile:
                json.dump(ydata[c], outfile)


fastdata(decks=1000, accuracy=2)
print('Got nice data')

fastdata(decks=1000, iters=20, accuracy=1)
print('Got long term data')
