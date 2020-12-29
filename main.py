import sys

from easy_crossword import EasyCrossword
from hard_crossword import HardCrossword

def main():

    '''The main function for the Crossword Solver program.

    Arguments will be taken in from the command-line and will determine the difficulty the
    program will run on.
    '''

    #try:

    if sys.argv[1].lower() == 'easy':

        easy = EasyCrossword()
        easy.generate_attributes()

    elif sys.argv[1].lower() == 'hard':

        hard = HardCrossword()
        hard.generate_attributes()
    # except IndexError:

    #     print('\n -- Invalid argument entered, see README file for valid arguments --\n')


if __name__ == '__main__':

    main()
