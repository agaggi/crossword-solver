import copy
import time

import utility

BACKTRACK = False
NUM_BACKTRACKS = 0
START = time.time()

def generateAttributes():

    '''Generates the attributes for the crossword puzzle.
    
    By using the crossword puzzle and word list read in, attributes are assigned to
    each "number" on the crossword puzzle. Attributes include:
    
    1. A string containing `crossword[i][j]`, the current integer found through 
    `.isdigit()`, and either ACROSS or DOWN depending on the wordspace's 
    characteristics.

    2. The coordinates of where the wordspace starts. This is the `i` and `j` value
    of where a number is found.

    3. The words that are valid for the particular wordspace. These words must equal
    the length of the word space. Ex:
        
            len('HOSES') = 5
            utility.getAcrossLength(...) -> return 5
        
        - Therefore, the word is compatible with the wordspace.
    '''

    # Reading each file and spliting its contents into respective lists
    crossword_file = open('crossword_puzzles/medium_crossword.txt', 'r')
    word_file = open('words/hard_words.txt', 'r')

    crossword = crossword_file.read().split()
    words = word_file.read().split()
    
    attributes = []
    coordinates = []

    # Printing the initial crossword puzzle (unsolved)
    print('Unfilled crossword puzzle: ')
    utility.printPuzzle(crossword)

    for i in range(len(crossword)):

        for j in range(len(crossword[i])):

            # Either across or down. Get the words that satisfy the domain constraints
            if crossword[i][j] == '*':

                if utility.isAcross(crossword, i, j):

                    wordLength = utility.getAcrossLength(crossword, i, j)
                    validWords = []

                    for word in words:

                        if len(word) == wordLength:

                            validWords.append(word)
                    
                    attributes.append(['ACROSS', (i, j), validWords])
                    coordinates.append((i, j))

                if utility.isDown(crossword, i, j):

                    wordLength = utility.getDownLength(crossword, i, j)
                    validWords = []

                    for word in words:

                        if len(word) == wordLength:

                            validWords.append(word)
                    
                    attributes.append(['DOWN', (i, j), validWords])
                    coordinates.append((i, j))
    
    crossword_file.close()
    word_file.close()
    
    del(words)

    # Obtaining the degree of each wordspace
    for attribute in attributes:

        degree = 0
        wordLength = len(attribute[2][0])

        row = attribute[1][0]
        col = attribute[1][1]

        if attribute[0] == 'ACROSS':

            for i in range(col, col + wordLength):
                
                if (row, i) in coordinates:
                    
                    degree += 1

        if attribute[0] == 'DOWN':

            for i in range(row, row + wordLength):

                if (i, col) in coordinates:

                    degree += 1
        
        attribute.append(degree)
    
    del coordinates

    # Sort the attributes based on degree of constraints (most first)
    attributes.sort(reverse=True, key=degree_heuristic)
    solve(crossword, attributes, 0, [])


def degree_heuristic(attribute):

    '''A key function to be used when sorting attributes constraints.

    i.e. *_____* would have a degree value of 2
    
    :param attribute: The current attribute
    :return: The word length with respect to the domain. 
    '''

    return attribute[3]

    



def removeWord(crossword, attribute):

    '''Removes the last placed word on the crossword puzzle.

    :param crossword: A crossword puzzle state as a result of backtracking
    :param attribute: The attribute that will have its current word deleted
    :return: The crossword puzzle with the removed word
    '''

    row, col = attribute[1]
    word_length = len(attribute[2][1])

    if attribute[0] == 'ACROSS':

        to_be_inserted = []
        
        # If a letter has a letter above or below it, leave the letter alone.
        # Otherwise, replace the letter with a '_'. Then append the new row.
        for i in range(col, col + word_length):

            if row == 0 and crossword[row+1][i].isalpha():

                to_be_inserted.append(crossword[row][i])

            elif (0 < row < word_length) and (crossword[row-1][i].isalpha() or 
                                              crossword[row+1][i].isalpha()):
                
                to_be_inserted.append(crossword[row][i])

            elif row == word_length and crossword[row-1][i].isalpha():

                to_be_inserted.append(crossword[row][i])
            
            else:

                to_be_inserted.append('_')
        
        new_row = crossword[row][:col], ''.join(to_be_inserted), \
                                        crossword[row][col+word_length:]

        crossword[row] = ''.join(new_row)

    if attribute[0] == 'DOWN':

        # If a letter has a letter to the left or right, leave the letter alone.
        # Otherwise, replace the letter with a '_'. Then append character by character.
        for i in range(row, row + word_length):

            if col == 0 and crossword[i][col+1].isalpha():

                continue

            elif (0 < col < word_length-1) and (crossword[i][col-1].isalpha() or 
                                                crossword[i][col+1].isalpha()):
                
                continue

            elif col == word_length-1 and crossword[i][col-1].isalpha():

                continue

            else:

                new_column = crossword[i][:col], '_', crossword[i][col+1:]
                crossword[i] = ''.join(new_column)
    
    return crossword


def forward_check(crossword, attribute, used_words):

    '''Forward checks ahead of time removing unviable words from the domain.

    The function will check whether there are any letters on the current path. If so, the
    words within the current domain will be tested against the current path. The ones that
    do not satisfy the constraints or are already used are removed.

    :param crossword: The current crossword state
    :param attribute: The current attribute we are on
    :param used_words: The currently used words
    :return: The current attribute with its domain modified so only the words that satisfy
    the constraints are left
    '''

    row, col = attribute[1]

    invalid_words = []

    for j, word in enumerate(attribute[2]):

        letter_index = 0

        if attribute[0] == 'ACROSS':

            for k in range(col, col + len(word)):

                if crossword[row][k].isalpha():
                    
                    if word[letter_index] != crossword[row][k] or word in used_words:

                        invalid_words.append(attribute[2][j])
                        break
                
                letter_index += 1

        if attribute[0] == 'DOWN':
            
            for k in range(row, row + len(word)):

                if crossword[k][col].isalpha():

                    if word[letter_index] != crossword[k][col] or word in used_words:

                        invalid_words.append(attribute[2][j])
                        break
                
                letter_index += 1

    attribute[2][:] = [word for word in attribute[2] if word not in invalid_words]

    return attribute   


def solve(crossword, attributes, attr_index, used_words):

    '''Solves the crossword puzzle.

    This function aims to solve the crossword puzzle by using recursion and backtracking.
    If there is a possible move to be made, it will be made and the word used will be
    appended to the `used_words` list, so duplication does not occur.

    If there is not a move to be made, a global variable `BACKTRACK` will be set to true,
    as the for-loop will exit after going through all the words. The last unmodified
    crossword state is then used and the last inserted word is removed via `removeWord()`.

    :param crossword: The current crossword state wee are on
    :param attributes: The list of attributes for the whole crossword puzzle
    :param attr_index: The current wordspace we are on
    :param used_words: The list of used words
    '''

    global BACKTRACK
    global NUM_BACKTRACKS

    crossword_copy = copy.deepcopy(crossword)
    completionCheck(crossword)

    attributes[attr_index] = forward_check(crossword, attributes[attr_index], used_words)

    for word in attributes[attr_index][2]:

        if BACKTRACK:
            
            print('=> Backtracking')
            NUM_BACKTRACKS += 1
    
            # Get rid of the last used word and remove the word before that from the board
            used_words.pop()
            crossword = removeWord(crossword, attributes[attr_index-1])
            
            BACKTRACK = False

        if word not in used_words:

            # Obtaining the coordinates of the beginning of the wordspace
            row, col = attributes[attr_index][1]
            letter_index = 0

            # Flag used to determine whether a word is viable. If not don't add it
            valid = True

            if attributes[attr_index][0] == 'ACROSS':

                # ... start to (start + word length) ...
                for i in range(col, col + len(word)):

                    # If there's a letter in the path, check if it's the same as the 
                    # current index in the word. If they are different, move on
                    if crossword_copy[row][i].isalpha():
                        
                        if not word[letter_index] == crossword_copy[row][i]:
                        
                            valid = False
                            break
                    
                    letter_index += 1
                
                # Slice the string in the affected row, leaving unaffected parts alone
                if valid:

                    new_row = crossword_copy[row][:col], word, crossword_copy[row][col+len(word):]
                    crossword_copy[row] = ''.join(new_row)

                    # Add word to used list to avoid using a word multiple times
                    used_words.append(word)
                    utility.printPuzzle(crossword_copy)
                    
                    solve(crossword_copy, attributes, attr_index+1, used_words)
            
            if attributes[attr_index][0] == 'DOWN':
        
                # ... start to (start + word length) ...
                for i in range(row, row + len(word)):

                    if crossword_copy[i][col].isalpha():

                        if not word[letter_index] == crossword_copy[i][col]:

                            valid = False
                            break
                    
                    # Slice the string by column, leaving the unaffected parts alone
                    if valid:

                        new_column = crossword_copy[i][:col], word[letter_index], \
                                                              crossword_copy[i][col+1:]

                        crossword_copy[i] = ''.join(new_column)

                    letter_index += 1
                
                if valid: 
                    
                    used_words.append(word)
                    utility.printPuzzle(crossword_copy)
                    
                    solve(crossword_copy, attributes, attr_index+1, used_words)
    
    BACKTRACK = True