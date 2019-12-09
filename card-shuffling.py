import random, math, json, glob
import matplotlib.pyplot as plt
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


def RSS(after, before):
    list(range(52))
    return sum((after[i] - before[i])**2 for i in range(len(after))) ** 0.5


def RMS(after, before):
    before = list(range(52))
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


def getdata(shuffles=(rand, riffle, overhand), measures=[RSS], decks=1000, iters=1, accuracy=1):
    for i, shuff in enumerate(shuffles):
        newdecks, olddecks = [], [list(range(52)) for _ in range(decks)]

        data = [[[] for _ in range(iters)] for __ in range(len(measures))]

        for j in range(iters):
            print('Shuffling ' + str(decks) + ' decks...')
            newdecks = [shuff(deck) for deck in olddecks]

            for k in range(decks):
                print('Iteration: ' + str(j) + ' Deck: ' + str(k))
                for c, mesr in enumerate(measures):
                    data[c][j].append(round(mesr(newdecks[k], olddecks[k]), accuracy))

        xdata = [[list(dict.fromkeys(iteration)) for iteration in mesr] for mesr in data]
        for mesr in xdata:
            for iteration in mesr:
                iteration.sort()

        ydata = [[[data[j][i].count(x) for x in iteration] for i, iteration in enumerate(mesr)] for j, mesr in enumerate(xdata)]

        for c, mesr in enumerate(measures):
            with open('output/' + '_'.join([shuff.__name__, mesr.__name__, str(decks), str(iters), str(accuracy), 'x.txt']), 'w') as outfile:
                json.dump(xdata[c], outfile)

            with open('output/' + '_'.join([shuff.__name__, mesr.__name__, str(decks), str(iters), str(accuracy), 'y.txt']), 'w') as outfile:
                json.dump(ydata[c], outfile)


def plotdata(xdata, ydata, shuffle, measure, decks):
    for i, x in enumerate(xdata):
        y = ydata[i]
        f = plt.figure()
        plt.rc('font', family='serif')
        plt.plot(x, y, 'bo')
        plt.axis([min(x) - 2, max(x) + 2, 0, max(y) + 2])

        if i == 0:
            title = shuffle + ' measured with ' + measure + ' using ' + str(decks) + ' decks'
        else:
            title = shuffle + ' measured with ' + measure + ' using ' + str(decks) + ' decks Iteration ' + str(i)

        plt.title(title, fontsize=11)
        plt.xlabel(measure + ' Score', fontsize=11)
        plt.ylabel('Frequency', fontsize=11)

        #plt.show()

        f.savefig('output/' + title + '.pdf', bbox_inches='tight')
        plt.close()


getdata(decks=100000, accuracy=1, iters=50)
print('Got long term data')

for name in glob.glob('./output/*x.txt'):
    shuffle, measure, decks = name.split('\\')[1].split('_')[:3]
    with open(name) as infile:
        xdata = json.load(infile)

    with open(name[:-5] + 'y.txt') as infile:
        ydata = json.load(infile)

    plotdata(xdata, ydata, shuffle, measure, decks)
