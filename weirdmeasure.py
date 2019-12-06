import time, random
import matplotlib.pyplot as plt

def vectordistance(deck):
    return (sum((v - c) ** 2 for c, v in enumerate(deck))) ** 0.5

def plot_data(trials):
    unshuffled, data = [i for i in range(52)], []
    start_time = time.time()

    for _ in range(trials):
        deck = unshuffled.copy()
        random.shuffle(deck)
        data.append(vectordistance(deck))

    time_taken = time.time() - start_time
    print('Took ' + str(time_taken))

    data = [round(d) for d in data]
    print(max(data))

    unique_data_points = list(dict.fromkeys(data))
    unique_data_points.sort()

    histogram = [(i, data.count(i)) for i in unique_data_points]
    x = [i[0] for i in histogram]
    y = [i[1] for i in histogram]

    print(x, y)

    probs = [i/sum(y) for i in y]

    exp = sum(x[i]*probs[i] for i in range(len(x)))
    print('Expectation: ' + str(exp))



    deviation = 0

    for c, v in enumerate(x):
        deviation += (v ** 2) * y[c]

    deviation = deviation / sum(y)
    deviation -= exp ** 2
    deviation = deviation ** 0.5

    print('Deviation: ' + str(deviation))


    # get the figure
    f = plt.figure()

    # use LaTeX fonts in the plot
    #plt.rc('text', usetex=True)

    print('setfont')


    plt.rc('font', family='serif')
 
    # plot
    plt.plot(x, y)
    plt.axis([min(x) - 2, max(x) + 2, 0, max(y) + 2])
 
    # set labels (LaTeX can be used)
    plt.title(r'\textbf{Total vector distance}', fontsize=11)
    plt.xlabel(r'\textbf{Distance}', fontsize=11)
    plt.ylabel(r'\textbf{Frequency}', fontsize=11)
    plt.show()
 

    # save as PDF
    #f.savefig('Total_Vector_Distance_{}.pdf'.format(trials), bbox_inches='tight')

plot_data(1000000)