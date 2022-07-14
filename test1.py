from random import randint
from rich import print
import math

possible_guesses = []
possible_answers = []

with open('wordleWords.txt', 'r') as file:
    for line in file:
        for word in line.split():
            possible_guesses.append(word)

for i in range(2315):
    possible_answers.append(possible_guesses[i])


class wordleGame:
    def guess_made(self, inp):
        self.words_guessed.append(inp)
        colors = color_match(inp, self.solution)
        self.words_colors.append(colors)
        self.answers_left = update_answers_left(self.answers_left, inp, colors)
        self.best_word = best_word2(self.answers_left, possible_guesses)

    def win(self):
        print("You Won in %s turns with the word %s!" % (len(self.words_guessed), self.solution))
        self.game_running = False

    def lose(self):
        print("You lost with word %s!" % self.solution)
        self.game_running = False

    def print_data(self):
        for wordsleft in self.answers_left:
            print(wordsleft)
        print(len(self.answers_left))
        print(self.solution)
        for i in range(len(self.words_guessed)):
            print(emoji_string(self.words_guessed[i], self.words_colors[i]))
        print(self.best_word)

    def reset(self):
        self.words_guessed = []
        self.words_colors = []
        self.best_word = 'irate'
        self.answers_left = possible_answers.copy()
        self.solution = possible_answers[randint(0, 2314)]
        self.game_running = True

    words_guessed = []
    words_colors = []
    best_word = 'irate'
    answers_left = possible_answers.copy()
    solution = possible_answers[randint(0, 2314)]
    game_running = True


def color_match(word1, word2):
    colors = ''
    for pos in range(5):
        if word1[pos] == word2[pos]:
            colors += 'g'
        else:
            if word1[pos] in word2:
                colors += 'y'
            else:
                colors += 'b'
    return colors


def emoji_string(word, colors):
    emoji = ''
    for i in range(len(colors)):
        if colors[i] == 'g':
            emoji += "[green]%s[/green]" % word[i]
        if colors[i] == 'y':
            emoji += "[yellow]%s[/yellow]" % word[i]
        if colors[i] == 'b':
            emoji += "[black]%s[/black]" % word[i]
    return emoji


def update_answers_left(answers_left, word, colors):
    tempList = set()
    for pos in range(5):
        if colors[pos] == 'y':
            for answer in answers_left:
                if answer.find(word[pos]) == -1:
                    tempList.add(answer)
                    continue
                if word[pos] == answer[pos]:
                    tempList.add(answer)
    for words in tempList:
        answers_left.remove(words)
    tempList.clear()

    for pos in range(5):
        if colors[pos] == 'g':
            for answer in answers_left:
                if answer[pos] != word[pos]:
                    tempList.add(answer)
    for words in tempList:
        answers_left.remove(words)
    tempList.clear()

    for pos in range(5):
        if colors[pos] == 'b':
            for answer in answers_left:
                if answer.count(word[pos]) == 1:
                    tempList.add(answer)
                else:
                    if answer[pos] == word[pos]:
                        tempList.add(answer)
    for words in tempList:
        answers_left.remove(words)

    return answers_left


def best_word2(answers_left, possible_guesses):
    if len(answers_left) == 1:
        return answers_left[0]
    biggestBit = 0
    biggestBitWord = answers_left[0]
    count = 0
    for guess in possible_guesses:
        # if count % 1000 == 0:
        # print(count)
        # count += 1

        bitSum = 0

        for answer in answers_left:
            p = probability(answers_left, word, color_match(answer, word))
            if p != 0:
                bitSum -= (p * math.log(p, 2))
            # print(answer)
            # print(bitSum)

        if bitSum > biggestBit:
            biggestBit = bitSum
            biggestBitWord = guess
        if bitSum == biggestBit and guess in answers_left:
            biggestBit = bitSum
            biggestBitWord = guess
    return biggestBitWord


def probability(answers_left, word, colors):
    tempVar = update_answers_left(answers_left.copy(), word, colors)
    # print(len(tempVar))
    return len(tempVar) / 2315


print('Welcome to Wordle')
currentSum = 0
currentGames = 0
game = wordleGame()
for i in range(100):
    currentGames += 1

    while game.game_running:

        inp = game.best_word
        # inp = input('Guess: ')
        #print('solution')
        #print(game.solution)
        #print('Word Guessed')
        #print(inp)
        #print(len(game.answers_left))
        while len(inp) != 5 or not inp.isalpha():
            print('\n' * 20)
            inp = input('Error Guess Again: ')

        inp = inp.lower()

        game.guess_made(inp);

        if inp == game.solution:
            game.win()
            break
        if len(game.words_guessed) >= 5:
            game.lose()
            break
    currentSum += len(game.words_guessed)
    game.reset()
    average = currentSum / currentGames
    print('%s Average: %s' % (i, average))
    # game.print_data()
