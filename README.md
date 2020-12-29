# Crossword Puzzle Solver

## Program Requirements

- Python 3.7 or newer

## Compilation and Execution

The `main.py` file is the file specified to be run; attempting to run any other file will result in no output. The program should be run following this format:

```bash
# Linux
python3 main.py [crossword difficulty]

# Windows
py .\main.py [crossword difficulty]
```

### Arguments

The following arguments are valid:

| Argument       | Crossword File         | Word List Used
| :------------: | :--------------------: | :-------------:
| `easy`         | `easy_crossword.txt`   | Easy
| `hard`         | `hard_crossword.txt`   | Hard

## Analysis

### Easy Crossword

The easy crossword puzzle contains **8** possible wordspaces with few constraints, making it easier to find a solution state. The word list used with this puzzle contained **15** words. Backtracking alone was used in this implementation, but a solution was found quickly.

```
HOSES
##A#T
#HIKE
A#LEE
LASER
E##L#


-- Puzzle solved after 0.0007722377777099609 seconds --

Number of backtracks: 12
```

### Hard Crossword

The hard puzzle had slightly more wordspaces (**11**), with a much larger wordlist of ~**21,000** words. A combination of backtracking, degree heuristic, and forward checking were used in order to solve the puzzle. At first, I simply ran the board with **only backtracking** and obtained this result:

```
##abalone####
##b#####a##a#
##a#####c##b#
##c##aloha#a#
##k####c###c#
####a##coypu#
####b##u#a#s#
#a#babel#m###
#b##t##t#m###
obtain###e###
#e##s####r###


-- Puzzle solved after 0.05314517021179199 seconds --

Number of backtracks: 14
```

We, however, wanted to find a solution that minimized the use of backtracking. I added a degree heuristic that sorted attributes by their number of constraints, as well as forward checking. Forward checking made the most notable impact, as before words were placed onto the board, the current wordspace would be checked for any letters. If a word in the current domain did not satisfy the constraints, it was removed. This resulted in absolutely no backtracking, but the additional checks made the runtime longer:

```
##abalone####
##b#####p##a#
##a#####i##b#
##s##aback#l#
##e####b###a#
####a##abaft#
####b##c#b#e#
#a#bayou#b###
#b##t##s#a###
obtain###c###
#e##s####y###


-- Puzzle solved after 0.4260573387145996 seconds --

Number of backtracks: 0
```