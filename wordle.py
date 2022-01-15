# Wordle game environment (https://www.powerlanguage.co.uk/wordle/)
# Thank you for making such an interesting game! :D
# Written by Wuhyun Sohn

import random

with open("dictionary.txt") as f:
    raw = f.readlines()
    dictionary = [l.rstrip() for l in raw if l[0] != "#"]
    dictionary.sort()


class Game():

    def __init__(self, answer=None):
        if answer is None:
            self.answer = random.choice(dictionary)
        else:
            self.answer = answer
        self.attempts = []
        self.hints = []
        self.n_tries = 0
        self.finished = False

    def check(self, word):
        res = ""
        for i, c in enumerate(word):
            if c not in self.answer:
                res += "B"  # Black, letter not in WORDLE
            elif c == self.answer[i]:
                res += 'G'  # Green, correct letter and position
            else:
                res += 'Y'  # Yellow, correct letter, wrong position
        return res

    def attempt(self, word):
        res = self.check(word)
        self.attempts.append(word)
        self.hints.append(res)
        self.n_tries += 1
        if res == "GGGGG":
            self.finished = True
        return res

    def summary(self):
        s = "Game Summary:\n"
        if self.finished:
            s += "Wordle: {0}, took {1:d} tries\n".format(self.answer.upper(), self.n_tries)
        for n in range(self.n_tries):
            s += "#{0:d}: {1} -> {2}\n".format(n+1, self.attempts[n], self.hints[n])
        return s

    def play(self):
        print("Welcome to a game of Wordle!")
        while not self.finished:
            print("Attempt #", self.n_tries+1, ": ", end="")
            word = input().lower()
            if len(word) != 5:
                if word == "alohomora":       # cheat
                    print(self.answer)
                print("Please type a five-letter word.")
            elif word not in dictionary:
                print("Sorry, not in my dictinoary.")
            else:
                res = self.attempt(word)
                print(res)

        print("Congratulations!!", end="")
        print("You guessed the word correctly in", self.n_tries, "tries!")
        print(self.summary())


if __name__ == "__main__":
    game = Game()
    game.play()