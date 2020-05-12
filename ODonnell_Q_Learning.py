# Kyle O'Donnell
# CISC 481
# HW 4 - Q-Learning
import random


# Class for a square on the board, contains useful information on rewards, Q-values, and type of square
class Square:
    def __init__(self, loc, s_type, reward):
        self.loc = loc
        self.s_type = s_type
        self.north = 0
        self.south = 0
        self.east = 0
        self.west = 0
        self.reward = reward


# Gets user input and formats it for later use
def start():
    print('Type the input string for the desired grid.')
    print('Input:')
    start_str = input()

    init = start_str.split(' ')

    s_goal_1 = int(init[0])
    s_goal_2 = int(init[1])
    s_forbidden = int(init[2])
    s_wall = int(init[3])
    s_output = init[4]
    s_index = -1
    if s_output == 'q':
        s_index = int(init[5])

    return s_goal_1, s_goal_2, s_forbidden, s_wall, s_output, s_index


# Using the current state and action, returns the name of the square that will be moved to, accounting for walls and
# boundaries of the game board
def get_square(s_space, current_sq, action):
    next_sq = current_sq.loc
    if action == 'n':
        if current_sq.loc < 13:
            next_sq += 4
    elif action == 's':
        if current_sq.loc > 4:
            next_sq -= 4
    elif action == 'e':
        if (current_sq.loc % 4) != 0:
            next_sq += 1
    elif action == 'w':
        if ((current_sq.loc+3) % 4) != 0:
            next_sq -= 1

    if s_space[next_sq-1].s_type == 'wall':
        next_sq = current_sq.loc

    return next_sq


# initialization of non-standard squares and output type
goal_1, goal_2, forbidden, wall, output, index = start()

# parameters of this specific q-learning problem
alpha = 0.1
gamma = 0.2
epsilon = 0.1
l_reward = -0.1

# generating game board
state_space = []
for i in range(16):
    sq = Square(i+1, 'empty', l_reward)
    state_space += [sq]

# setting non standard squares
state_space[goal_1 - 1].s_type = 'goal'
state_space[goal_1 - 1].reward = 100
state_space[goal_2 - 1].s_type = 'goal'
state_space[goal_2 - 1].reward = 100
state_space[forbidden - 1].s_type = 'goal'
state_space[forbidden - 1].reward = -100
state_space[wall - 1].s_type = 'wall'

sq_index = 1
random.seed()

# runs 10000 iterations
for i in range(10000):
    # print('Iteration:' + str(i+1))
    sq_index = 1

    # loop that "solves" the q-learning problem
    while True:
        # print('     '+'Index=' + str(sq_index+1))
        # check for exit square
        if state_space[sq_index].s_type == 'goal' or state_space[sq_index].s_type == 'forbidden':
            break
        n, s, e, w = state_space[sq_index].north, state_space[sq_index].south, state_space[sq_index].east, state_space[
            sq_index].west
        actions = [n, s, e, w]
        choices = ['n', 's', 'e', 'w']
        direction = ''
        q_old = 0
        x = -1
        # implementation of epsilon-greedy method for traversal
        if random.random() <= epsilon:
            x = random.randint(0, 3)
            direction = choices[x]
            q_old = actions[x]
        else:
            x = actions.index(max(actions))
            direction = choices[x]
            q_old = actions[x]

        next_square = get_square(state_space, state_space[sq_index], direction)
        next_index = next_square - 1
        next_qs = [state_space[next_index].north, state_space[next_index].south, state_space[next_index].east,
                   state_space[next_index].west]

        # generating new q-value
        q_new = (1-alpha)*q_old + alpha*(state_space[next_index].reward + gamma*max(next_qs))
        if x == 0:
            state_space[sq_index].north = q_new
        elif x == 1:
            state_space[sq_index].south = q_new
        elif x == 2:
            state_space[sq_index].east = q_new
        elif x == 3:
            state_space[sq_index].west = q_new

        # moving to next square
        sq_index = next_index

# printing pi* as the output
if output == 'p':
    print('Below are the best actions to reach the goal from the start state:')
    sq_index = 1
    while state_space[sq_index].s_type == 'empty':
        n, s, e, w = state_space[sq_index].north, state_space[sq_index].south, state_space[sq_index].east, state_space[
            sq_index].west
        actions = [n, s, e, w]
        move = actions.index(max(actions))
        moves = ['North', 'South', 'East', 'West']
        next_move = ['n', 's', 'e', 'w']
        next_square = get_square(state_space, state_space[sq_index], next_move[move])
        next_index = next_square - 1
        print('    ' + str(sq_index+1) + ' : ' + moves[move])
        sq_index = next_index

# printing the q-values of the possible actions for the given state
elif output == 'q':
    print('Below are the Q values associated with the actions in the state with given index:')
    print('     North: ' + str(round(state_space[index-1].north, 5)))
    print('      East: ' + str(round(state_space[index-1].east, 5)))
    print('     South: ' + str(round(state_space[index-1].south, 5)))
    print('      West: ' + str(round(state_space[index-1].west, 5)))
