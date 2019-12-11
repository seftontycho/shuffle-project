import random
import math
import json
import glob
import matplotlib.pyplot as plt
import numpy


def nCr(n, r):
    '''Returns the number of ways of choosing r objects from n.'''
    return math.factorial(n) // math.factorial(r) // math.factorial(n - r)


def Riffle(deck):
    '''Returns a Riffle shuffle based on the Gilbert-Shannon-Reeds Model'''
    probs = [nCr(len(deck), r)/(2**len(deck)) for r in range(len(deck))]

    split = numpy.random.choice(list(range(len(deck))), p=probs)
    splitdeck = [A, B] = deck[:split], deck[split:]
    newdeck = []

    while A or B:
        choice = numpy.random.choice([0, 1], p=[len(A)/len(A+B),
                                                len(B)/len(A+B)])

        newdeck.append(splitdeck[choice].pop(0))

    return newdeck


def FisherYates(deck):
    """A function that completely randomly shuffles a deck.
       Based off python's in built random function which uses
       the Fisher-Yates shuffle."""
    newdeck = deck.copy()
    random.shuffle(newdeck)
    return newdeck


def Overhand(deck):
    """A function that shuffles a deck using the Pemantle model
       using an expected packet size of 2."""
    newdeck = []
    while len(deck) > 1:
        probs = [0.5**n for n in range(1, len(deck))]
        k = numpy.random.choice(list(range(1, len(deck))) + [0],
                                p=probs+[1 - sum(probs)])

        newdeck, deck = newdeck + deck[len(deck) - k:], deck[:len(deck) - k]

    return newdeck + [0]


def RSS(after, before):
    """A function that returns the Root-Sum-Squared value for a given deck."""
    return sum((i - before.index(c))**2 for i, c in enumerate(after))**0.5


def RMS(after, before):
    """A function that returns the Root-Mean-Squared value for a given deck."""
    return RSS(after, before) / (len(after) ** 0.5)


def Guessing(after, before):
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


def collectdata(shuffles, measures, decks=1000, cycles=1, accuracy=1):
    for _, shuffle in enumerate(shuffles):
        data = [[[] for __ in range(cycles)] for _ in range(len(measures))]
        newdecks, olddecks = [], [list(range(52)) for _ in range(decks)]

        for i in range(cycles):
            print(shuffle.__name__ + ' Shuffling ' + str(decks) + ' decks...')
            newdecks = [shuffle(deck) for deck in olddecks]

            for j, deck in enumerate(newdecks):
                print(shuffle.__name__ + f' Cycle: {i} Deck: {j}')

                for k, measure in enumerate(measures):
                    data[k][i].append(round(measure(deck,
                                            list(range(len(deck))))))

        xdata = [[list(dict.fromkeys(i)) for i in measure] for measure in data]
        ydata = [[[] for cycle in measure] for measure in xdata]

        for measure in xdata:
            for cycle in measure:
                cycle.sort()

        for i, measure in enumerate(xdata):
            for j, cycle in enumerate(measure):
                for datapoint in cycle:
                    ydata[i][j].append(data[i][j].count(datapoint))

        for i, measure in enumerate(measures):
            name = '_'.join([shuffle.__name__, measure.__name__, str(decks),
                             str(cycles), str(accuracy), '.txt'])

            with open(('output/data/' + name), 'w') as outfile:
                json.dump([xdata[i], ydata[i]], outfile)


def graphdata(xdata, ydata, shuffle, measure, decks):
    """A function that uses data to plot graphs and save them as pdfs."""
    plt.rc('font', family='serif')

    for i, (xaxis, yaxis) in enumerate(zip(xdata, ydata)):
        f = plt.figure()
        x_range = max(xaxis) - min(xaxis)

        plt.plot(xaxis, yaxis, 'ko', markersize=4)
        plt.axis([min(xaxis) - x_range * 0.05,
                  max(xaxis) + x_range * 0.05,
                  min(yaxis) * 0.9, max(yaxis) * 1.1])

        template = '{} shuffle measured with {} using {} decks.'
        title = template.format(shuffle, measure, decks)

        if len(xdata) != 1:
            title += f' Cycle: {i}.'

        plt.title(title, fontsize=11)
        plt.xlabel(measure + ' Score', fontsize=11)
        plt.ylabel('Frequency', fontsize=11)

        title = title.replace('.', '').replace(':', '')

        f.savefig('output/graphs/' + title + '.pdf', bbox_inches='tight')
        plt.close()


def example():
    """A simple example function to show how the rest of
       the code was used to collect and create our graphs"""

    # Gets data for all shuffles for all measures using 1000000
    # decks with all measures rounded to 2 decimal places

    collectdata([Overhand], [RSS],
                decks=50000, accuracy=2, cycles=1)

    print('Collected data.')

    # Plot availible data.
    for name in glob.glob('./output/data/*.txt'):
        shuffle, measure, decks = name.split('\\')[1].split('_')[:3]

        with open(name) as infile:
            xdata, ydata = json.load(infile)

        print('Plotting ' + ' '.join([shuffle, measure, decks]))
        graphdata(xdata, ydata, shuffle, measure, decks)


example()
