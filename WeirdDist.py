import random, time
import matplotlib.pyplot as plt

def get_data():
    toguess = [i for i in range(52)]
    deck = [i for i in range(52)]
    random.shuffle(deck)
    guess = 0
    result = 0

    while deck:
        guess = random.choice(toguess)
        if guess == deck[-1]:
            result += 1

        toguess.remove(deck.pop())

    return result


start_time = time.time()
data = [get_data() for _ in range(1000000)]
time_taken = time.time() - start_time
print('Took ' + str(time_taken))

histogram = [(i, data.count(i)) for i in range(max(data) + 1)]
x = [i[0] for i in histogram]
y = [i[1] for i in histogram]

probs = [i/sum(y) for i in y]

exp = sum(x[i]*probs[i] for i in range(len(x)))
print(exp)

plt.plot(x, y)
plt.axis([0, max(x), 0, max(y)])
plt.axvline(x=4.538)
plt.show()


#count how many cards stay in the same place