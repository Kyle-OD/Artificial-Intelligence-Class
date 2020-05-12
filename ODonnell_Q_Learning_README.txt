Kyle O'Donnell
CISC 481
Homework 4 - Q-Learning

This file is fairly straightforward to run, simply type 4 numbers between 1 and 16 (excluding 2), assuming
that all numbers are unique.  Separate them with a space, and at the end, use either the character 'p' or 'q',
depending if you want to see the ideal path to a goal or the Q-Values of each action of given index respectively. If 'q'
is selected, type an additional number, indicating the aforementioned index.

Below are some possible inputs with an explanation:

15 12 8 6 p

    This command will place 'goals' at indices 15 and 12, a 'forbidden' square at index 8, and a 'wall' at index 6.
    The 'p' character signifies that the output will be the optimal found path from start to finish.

15 12 8 6 q 5

    This command will place 'goals' at indices 15 and 12, a 'forbidden' square at index 8, and a 'wall' at index 6.
    The 'q' character signifies that the output will be the four Q-Values of the square at index 5.