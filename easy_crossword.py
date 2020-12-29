import copy
import time

import utility

class EasyCrossword:

    def __init__(self):

        '''Class implements methods to solve the easy crossword puzzle.'''

        self.backtracking = False
        self.num_backtracks = 0
        self.start_time = time.time()
        self.attributes = []


    def generate_attributes(self):

        '''Generates the attributes for the crossword puzzle.

        Using the crossword puzzle and word list read in, attributes are assigned to
        each word space in the crossword puzzle. Attributes include:

        1. Whether the word space is across or down.

        2. The coordinates of where the word space starts (i.e. the current `i` and `j`).

        3. The words valid for the particular word space (i.e. words that equal the length of
        the word space). Ex:

                len('HOSES') = 5
                utility.getAcrossLength(...) -> return 5
        '''

        # Reading each file and spliting its contents into respective lists
        crossword_file = open('crossword puzzles/easy_crossword.txt', 'r')
        word_file = open('wordlists/easy_wordlist.txt', 'r')

        crossword = crossword_file.read().split()
        words = word_file.read().split()

        for i, row in enumerate(crossword):

            for j, element in enumerate(row):

                # Either across or down. Get the words that satisfy the domain constraints
                if element == '*':

                    if utility.is_across(crossword, i, j):

                        word_length = utility.across_length(crossword, i, j)
                        valid_words = []

                        for word in words:

                            if len(word) == word_length:

                                valid_words.append(word)

                        self.attributes.append(['ACROSS', (i, j), valid_words])

                    if utility.is_down(crossword, i, j):

                        word_length = utility.down_length(crossword, i, j)
                        valid_words = []

                        for word in words:

                            if len(word) == word_length:

                                valid_words.append(word)

                        self.attributes.append(['DOWN', (i, j), valid_words])

        crossword_file.close()
        word_file.close()

        del words

        self.solve(crossword, 0, [])


    def completion_check(self, crossword):

        '''Checks for empty spaces. If there are none, quit.

        :param crossword: The crossword state to be checked for completion
        '''

        if utility.remaining_spaces(crossword) == 0:

            exit(f'''
-- Puzzle solved after {time.time() - self.start_time} seconds --

Number of backtracks: {self.num_backtracks}
''')


    def solve(self, crossword, attr_index, used_words):

        '''Solves the crossword puzzle.

        This function solves the crossword puzzle by using recursion and backtracking. If
        here is a possible move, it will be made and the word used will be appended to the
        `used_words` list, so duplication does not occur.

        If there is no possible move, `BACKTRACK` will be set to true. The last unmodified
        crossword state is then used and the last inserted word is removed via
        `removeWord()`.

        :param crossword: The current crossword state we are on
        :param attr_index: The index of which attribute we are on
        :param used_words: The list of used words
        '''

        utility.print_puzzle(crossword)
        self.completion_check(crossword)

        crossword_copy = copy.deepcopy(crossword)

        for word in self.attributes[attr_index][2]:

            if self.backtracking:

                print('=> Backtracking')
                self.num_backtracks += 1

                # Remove the last used word and the word before that from the board
                used_words.pop()
                crossword = utility.remove_word(crossword, self.attributes[attr_index-1])

                self.backtracking = False

            if word not in used_words:

                # Obtaining the coordinates of the beginning of the wordspace
                row, col = self.attributes[attr_index][1]
                letter_index = 0

                # Flag used to determine whether a word is viable. If false don't add it
                valid = True

                if self.attributes[attr_index][0] == 'ACROSS':

                    # ... start to (start + word length) ...
                    for i in range(col, col + len(word)):

                        # If the word space index we are on is a letter and the same index
                        # in the current word does not match, the current word is invalid
                        if crossword_copy[row][i].isalpha():

                            if not word[letter_index] == crossword_copy[row][i]:

                                valid = False
                                break

                        letter_index += 1

                    # Slice the string in the affected row, leaving unaffected parts alone
                    if valid:

                        new_row = crossword_copy[row][:col], \
                                  word, \
                                  crossword_copy[row][col+len(word):]

                        crossword_copy[row] = ''.join(new_row)

                        # Add word to used list to avoid using a word multiple times
                        used_words.append(word)
                        self.solve(crossword_copy, attr_index+1, used_words)

                if self.attributes[attr_index][0] == 'DOWN':

                    # ... start to (start + word length) ...
                    for i in range(row, row + len(word)):

                        if crossword_copy[i][col].isalpha():

                            if not word[letter_index] == crossword_copy[i][col]:

                                valid = False
                                break

                        # Slice the string by column, leaving the unaffected parts alone
                        if valid:

                            new_column = crossword_copy[i][:col], \
                                         word[letter_index], \
                                         crossword_copy[i][col+1:]

                            crossword_copy[i] = ''.join(new_column)

                        letter_index += 1

                    if valid:

                        used_words.append(word)
                        self.solve(crossword_copy, attr_index+1, used_words)

        self.backtracking = True
