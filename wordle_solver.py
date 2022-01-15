import numpy as np
from scipy import stats
import time
import wordle

class WordleSolver:
    def __init__(self):
        # The state matrix at (i,a) is True iff the 'a'th alphabet is allowed
        # at the 'i'th position of the answer from available information
        self.state = np.ones((5,26), dtype=bool)

        # The is_viable vector at (n) is True iff the 'n'th dictionary word
        # is currently a viable answer
        self.viability = np.ones(len(wordle.dictionary), dtype=bool)

        # The dict_index matrix at (i,n) contains the alphabetic index (a=0, z=25)
        # of the 'i'th letter of the 'n'th dictionary word.
        # TODO: make this a static or global variable?
        base = ord('a')
        inds = [[ord(let)-base for let in word] for word in wordle.dictionary]
        self.dict_index = np.transpose(np.array(inds, dtype=int))

        self.dict = np.array(wordle.dictionary)
        self.allowed_words = self.dict

    def update(self, word, result):
        # Update the game state and viable answers from new (word, result) info
        self.update_state(word, result)
        self.update_viability()

    def update_state(self, word, result):
        for i, (let, res) in enumerate(zip(word, result)):
            a = ord(let) - ord('a')
            if res == 'B':      # Blue
                self.state[:,a] = False
            elif res == 'G':    # Green
                self.state[i,:] = False
                self.state[i,a] = True
            else:   # Yellow
                self.state[i,a] = False
        # TODO: add logical deductions? (e.g. 5 distinct yellows -> anagram)

    def update_viability(self):
        self.viability = np.all([self.state[i,self.dict_index[i,:]]
                                 for i in range(5)], axis=0)
        self.allowed_words = self.dict[self.viability]

    def solve(self, game=None):
        # Solve wordle. Inherited classes should override this function
        if game is None:
            game = wordle.Game()

        while not game.finished:
            word = np.random.choice(self.allowed_words)
            res = game.attempt(word)
            self.update(word, res)

            #print(len(self.allowed_words))
            #if len(self.allowed_words) < 100: print(self.allowed_words)

        #print(game.summary())
        self.reset()
        return game

    def reset(self):
        self.state = np.ones((5, 26), dtype=bool)
        self.viability = np.ones(len(wordle.dictionary), dtype=bool)
        self.allowed_words = self.dict
        #self.allowed_words = np.array(wordle.dictionary)

    def evaluate(self):
        # Test the performance of the wordle solver
        n_tries_vec = np.zeros(len(wordle.dictionary), dtype=int)
        worst_game = self.solve(wordle.Game("tests"))

        t_start = time.time()
        for i, word in enumerate(wordle.dictionary):
            game = self.solve(wordle.Game(word))
            if game.n_tries > worst_game.n_tries:
                worst_game = game
            n_tries_vec[i] = game.n_tries
        t_end = time.time()

        avg_time = (t_end - t_start) / len(wordle.dictionary)
        print("Average time spent solving a game:", avg_time, "seconds")
        #print("Average number of tries:", np.mean(n_tries_vec))
        print("Statistics for the number of tries to solve:")
        print(stats.describe(n_tries_vec))


if __name__ == "__main__":
    basic_solver = WordleSolver()
    #basic_solver.solve()
    basic_solver.evaluate()