import copy
import time

import utility

BACKTRACK = False

class EasyCrossword:

    def __init__(self):

        '''Class implements methods to solve the easy crossword puzzle.'''

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


    def remove_word(self, crossword, attribute):

        '''Removes the last placed word on the crossword puzzle.

        :param crossword: A crossword puzzle state as a result of backtracking
        :param attribute: The attribute that will have its current word deleted
        :return: The crossword puzzle with the removed word
        '''

        direction = attribute[0]
        row, col = attribute[1]
        word_length = len(attribute[2][1])

        if direction == 'ACROSS':

            new_row = []

            # If a letter has a letter above or below it, leave the current letter alone
            # because removing the letter would then alter other words.
            # Else, replace the letter with '_' (i.e. blank space). Then append new row.
            for i in range(col, col + word_length):

                if row == 0 and crossword[row+1][i].isalpha():

                    new_row.append(crossword[row][i])

                elif 0 < row < word_length and (crossword[row-1][i].isalpha() or
                                                crossword[row+1][i].isalpha()):

                    new_row.append(crossword[row][i])

                elif row == word_length and crossword[row-1][i].isalpha():

                    new_row.append(crossword[row][i])

                else:

                    new_row.append('_')

            new_row = crossword[row][:col], ''.join(new_row), \
                                            crossword[row][col+word_length:]

            crossword[row] = ''.join(new_row)

        if direction == 'DOWN':

            # If a letter has a letter to the left or right, leave the letter alone.
            # Else, replace the letter with a '_'. Then append character by character.
            for i in range(row, row + word_length):

                if col == 0 and crossword[i][col+1].isalpha():

                    continue

                elif 0 < col < word_length-1 and (crossword[i][col-1].isalpha() or
                                                  crossword[i][col+1].isalpha()):

                    continue

                elif col == word_length-1 and crossword[i][col-1].isalpha():

                    continue

                # Will not be executed unless all statements above are false.
                new_column = crossword[i][:col], '_', crossword[i][col+1:]
                crossword[i] = ''.join(new_column)

        return crossword


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

        global BACKTRACK

        utility.print_puzzle(crossword)
        self.completion_check(crossword)

        crossword_copy = copy.deepcopy(crossword)

        for word in self.attributes[attr_index][2]:

            if BACKTRACK:

                print('=> Backtracking')
                self.num_backtracks += 1

                # Remove the last used word and the word before that from the board
                used_words.pop()
                crossword = self.remove_word(crossword, self.attributes[attr_index-1])

                BACKTRACK = False

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

        BACKTRACK = True