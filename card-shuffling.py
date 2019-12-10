import random
import math
import json
import glob
import matplotlib.pyplot as plt
import numpy


def nCr(n, r):
    '''Returns the number of ways of choosing r objects from n.'''
    return math.factorial(n) // math.factorial(r) // math.factorial(n - r)


def riffle(deck):
    '''Returns a Riffle shuffle based on the Gilbert-Shannon-Reeds Model'''
    probs = [nCr(len(deck), r)/(2**len(deck)) for r in range(len(deck))]

    split = numpy.random.choice(list(range(len(deck))), p=probs)
    splitdeck = [A, B] = deck[:split], deck[split:]
    newdeck = []

    while A or B:
        newdeck.append(splitdeck[numpy.random.choice([0, 1], p=[len(A)/len(A+B),
                       len(B)/len(A+B)])].pop(0))

    return newdeck


def rand(deck):
    """A function that completely randomly shuffles a deck.
       Based off python's in built random function which uses
       the Fisher-Yates shuffle."""
    newdeck = deck.copy()
    random.shuffle(newdeck)
    return newdeck


def overhand(deck):
    """A function that shuffles a deck using the Pemantle model using an expected packet size of 2."""
    newdeck = []
    while len(deck) > 1:
        probs = [0.5**n for n in range(1, len(deck))]
        k = numpy.random.choice(list(range(1, len(deck))) + [0], p=probs+[1 - sum(probs)])

        newdeck, deck = newdeck + deck[len(deck) - k:], deck[:len(deck) - k]

    return newdeck + [0]


def RSS(after, before):
    """A function that returns the Root-Sum-Squared value for a given deck."""
    return sum((i - before.index(card))**2 for i, card in enumerate(after))**0.5


def RMS(after, before):
    """A function that returns the Root-Mean-Squared value for a given deck."""
    return RSS(after, before) / (len(after) ** 0.5)


def guessing(after, before):
    """A function that returns the number of cards guessed correctly
       for a given deck using the guessing method."""
    count, guess, lastcard, toguess = 0, 0, 0, before.copy()

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


def getdata(shuffles, measures, decks=1000, iters=1, accuracy=1):
    """A function that uses our previously defined shuffle functions
       and measuring functions to collect and save data on those shuffles."""
    for i, shuff in enumerate(shuffles):
        newdecks, olddecks = [], [list(range(52)) for _ in range(decks)]

        data = [[[] for  in range(iters)] for _ in range(len(measures))]

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
            with open('output/' + '_'.join([shuff.__name_, mesr.__name_, str(decks), str(iters), str(accuracy), 'x.txt']), 'w') as outfile:
                json.dump(xdata[c], outfile)

            with open('output/' + '_'.join([shuff.__name_, mesr.__name_, str(decks), str(iters), str(accuracy), 'y.txt']), 'w') as outfile:
                json.dump(ydata[c], outfile)


def plotdata(xdata, ydata, shuffle, measure, decks):
    """A function that uses data to plot graphs and save them as pdfs."""
    for i, x in enumerate(xdata):
        y = ydata[i]
        f = plt.figure()
        plt.rc('font', family='serif')
        plt.plot(x, y, 'bo')
        plt.axis([min(x) - 2, max(x) + 2, 0, max(y) + 2])

        if len(xdata) == 1:
            title = shuffle + ' measured with ' + measure + ' using ' + str(decks) + ' decks'
        else:
            title = shuffle + ' measured with ' + measure + ' using ' + str(decks) + ' decks Iteration ' + str(i)

        plt.title(title, fontsize=11)
        plt.xlabel(measure + ' Score', fontsize=11)
        plt.ylabel('Frequency', fontsize=11)

        #plt.show()

        f.savefig('output/' + title + '.pdf', bbox_inches='tight')
        plt.close()


def example():
    """A simple example function to show how the rest of
       the code was used to collect and create our graphs"""

    # Gets data for all shuffles for all measures using 1000000
    # decks with all measures rounded to 2 decimal places
    getdata([rand, riffle, overhand], [RSS, guessing], decks=1000000, accuracy=2)

    print('Got data.')

    # Plots all availible data.
    for name in glob.glob('./output/*x.txt'):
        shuffle, measure, decks = name.split('\\')[1].split('_')[:3]
        with open(name) as infile:
            xdata = json.load(infile)

        with open(name[:-5] + 'y.txt') as infile:
            ydata = json.load(infile)

        print('Plotting ' + (shuffle, measure, decks).join(' '))
        plotdata(xdata, ydata, shuffle, measure, decks)
