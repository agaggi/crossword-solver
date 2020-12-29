'''Helper module for crossword puzzle files.'''

def print_puzzle(crossword):

    '''Prints a crossword puzzle state.

    :param crossword: The crossword puzzle to be printed
    '''

    print()

    for row in crossword:

        print(row)

    print()


def remaining_spaces(crossword):

    '''Returns the number of empty spaces in a crossword puzzle.

    :param crossword: A puzzle state to have its remaining spaces counted
    :return: The number of empty spaces left
    '''

    amount = 0

    for row in crossword:

        for element in row:

            if element == '_':

                amount += 1

    return amount


def is_across(crossword, row, col):

    '''Determines whether the word space is across or not.

    :param crossword: The unfilled crossword puzzle
    :param row: The current row
    :param col: The current column
    :return: True/False, whether the word space is across or not
    '''

    if col == 0:

        return crossword[row][col+1] != '#'

    elif 0 < col < len(crossword[row]):

        return crossword[row][col-1] == '#' and crossword[row][col+1] != '#'

    # If we're at the last column in the row
    return False


def is_down(crossword, row, col):

    '''Determines whether the word space is down or not.

    :param crossword: The unfilled crossword puzzle
    :param row: The current row
    :param col: The current column
    :return: True/False, whether the word space is down or not
    '''

    if row == 0:

        return crossword[row+1][col] != '#'

    elif 0 < row < len(crossword):

        return crossword[row-1][col] == '#' and crossword[row+1][col] != '#'

    # If we're at the last row in the column
    return False


def across_length(crossword, i, j):

    '''Obtains the length of a word space considered across.

    :param crossword: The unfilled crossword puzzle
    :param i: THe current row
    :param j: The current column
    :return: The length of the word space across
    '''

    word_length = 0

    while j < len(crossword[i]):

        if crossword[i][j] != '#':

            word_length += 1

        else:

            break

        j += 1

    return word_length


def down_length(crossword, i, j):

    '''Obtains the length of a word space considered down.

    :param crossword: The unfilled crossword puzzle
    :param i: THe current row
    :param j: The current column
    :return: The length of the word space down
    '''

    word_length = 0

    while i < len(crossword):

        if crossword[i][j] != '#':

            word_length += 1

        else:

            break

        i += 1

    return word_length


def remove_word(crossword, attribute):

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
