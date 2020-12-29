# CS 580 Assignment 3

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

| Argument       | Crossword File         | Word List Used
| :------------: | :--------------------: | :-------------:
| `easy`         | `easy_crossword.txt`   | Easy
| `medium`       | `medium_crossword.txt` | Hard
| `hard`         | `hard_crossword.txt`   | Hard

## Analysis

### Easy Crossword

The easy crossword puzzle contains only eight possible wordspaces, making it quick to obtain a solution. Backtracking alone was used in this implementation, but a solution was found quickly.

```
HOSES
##A#T
#HIKE
A#LEE
LASER
E##L#


-- Puzzle solved after 0.0012776851654052734 seconds --

Number of backtracks: 12
```

### Medium Crossword

The medium puzzle had slightly more wordspaces, with a much larger wordlist of ~21,000 words. A combination of backtracking, degree heuristic, and forward checking were used in order to solve the puzzle. At first, I simply ran the board with only backtrackingand got this result:

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

I then added a degree heuristic that sorted attributes by their number of constraints as well as forward checking. Forward checking made the most notable impact, as before words were placed onto the board, the current wordspace would be checked for any letters. If a word in the current domain did not satisfy the constraints, it was removed. This resulted in absolutely no backtracking, but the additional checks made the runtime longer:

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


-- Puzzle solved after 0.44267749786376953 seconds --

Number of backtracks: 0
```

### Hard Crossword

```
##***###***###
#*___*#*___*##
#*____#*____##
*__#*_*__#*_*#
*__*#*__#*___#
*___#*__#*___#
#*__*###*___##
##*__*#*___###
###*__*___####
####*____#####
#####NTH######
######_#######
```

The hard crossword contains over 40 possible variables, making it take much longer to obtain a solution. Through my testing I was unable to obtain a solution, as I was running out of time to complete the assignment. I used the same degree heuristic and forward checking method; however, only a few words were placed before the program backtracked continuously.