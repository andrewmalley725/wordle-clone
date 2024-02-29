from termcolor import colored
import requests

class Board:
    LENGTH = 5
    WIDTH = 6

    def __init__(self, word):
        self.word = word.upper()
        self.board = [['_ ' for _ in range(self.LENGTH)] for _ in range(self.WIDTH)]
        self.alphabet_row = [chr(ord('A') + i) for i in range(26)]
        self.game_over = False

    def bold(self, guess):
        final = ''
        the_word = [i for i in self.word]
        guess = [i for i in guess]
        for i in range(len(guess)):
            char = guess[i] + ' '
            if guess[i] in the_word:
                if guess[i] == the_word[i]:
                    char = colored(char, 'green')
                else:
                    char = colored(char, 'yellow')
                the_word[the_word.index(guess[i])] = '_'
            final += char
        return final

    def print_board(self):
        print('\n')
        for i in self.board:
            print(''.join(i))
            print('\n')
        print(' '.join(self.alphabet_row))
        print('\n')

    def check_guess(self, guess, num_guess):
        while len(guess) != self.LENGTH or not check_exists(guess):
            guess = input('\nPlease enter a valid five-letter word: ')
        guess = guess.upper()
        attempt = self.bold(guess)
        self.board[num_guess] = ''.join(attempt)
        for letter in guess:
            if letter in self.alphabet_row:
                if letter in self.word:
                    self.alphabet_row[self.alphabet_row.index(letter)] = colored(letter, 'green')
                else:
                    self.alphabet_row[self.alphabet_row.index(letter)] = colored(letter, 'red')
        self.print_board()
        if guess == self.word:
            print('You won!!\n')
            self.game_over = True

def check_exists(guess):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{guess}'
    try:
        response = requests.get(url).json()
        return not isinstance(response, dict)
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        return False

if __name__ == '__main__':
    url ='https://random-word-api.herokuapp.com/word?length=5&number=1'
    word = requests.get(url).json()[0]

    while not check_exists(word):
        word = requests.get(url).json()[0]

    my_board = Board(word)

    num_guess = 0

    while num_guess < my_board.WIDTH and not my_board.game_over:
        guess = input('Enter a five-letter word: ')
        my_board.check_guess(guess, num_guess)
        num_guess += 1

    if not my_board.game_over:
        print(f'Better luck next time! The word was {colored(my_board.word, "green")}\n')
