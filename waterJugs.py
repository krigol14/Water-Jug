import collections

"""
2 water jugs initially empty: jugA and jugB
jugA's capacity is 70ml and jugB's capacity is 50ml (the jugs do not have markings on them)
The goal is to fill one of the jugs with 40ml of water
The actions we can take are the following:
    1) Fill the first jug
    2) Fill the second jug
    3) Empty the first jug
    4) Empty the second jug
    5) Pour the first jug into the second jug
    6) Pour the second jug into the first jug

visited{}     --> kleisto synolo
path[]        --> mikroskopio
next_states[] --> katastaseis paidia
searchFront   --> metwpo anazhthshs
"""

def main():
    """
    Main function of the code
    """

    initial_state = [[0, 0]]        # initially both jugs are empty
    jugs_capacities = [70, 50]      # list to store the max capacities of the jugs
    goal_amount = 40                # the wanted amount of water in a jug   
    visited = {}                    # dictionary to store the visited states
    choice = choose()               # choice calls def choose, if the user chooses DFS choice = True, otherwise choice = False
    search(initial_state, jugs_capacities, goal_amount, visited, choice)


def choose():
    """
    Function that gives the user the ability to choose the algorithm he wants to implement in order to solve the problem
    """

    press = input("-----CHOOSE THE ALGORITHM YOU WANT TO USE. ENTER 'B' FOR BFS, 'D' FOR DFS: \n")
    # take only the first letter from the user's input
    press = press[0].lower()
    
    # check for invalid input
    while press != 'b' and press != 'd':
        press = input("INVALID INPUT! CHOOSE THE ALGORITHM YOU WANT TO USE. ENTER 'B' FOR BFS, 'D' FOR DFS: ")
        press = press[0].lower()

    if press == 'd':
        return True
    else: 
        return False


def alreadyVisited(state, visited):
    """
    Function to check whether a state has been visited or not
    """

    # if the state has been visited returns True, otherwise returns False
    return visited.get(str(state), False)


def goalReached(path, goal_amount):
    """
    Function to check whether the goal has been reached or no
    """

    if path[-1][0] == goal_amount or path[-1][1] == goal_amount:
        return True
    else:
        return False


def createChildren(jugs_capacities, path, visited):
    """
    Function that creates the possible next states based on the current state
    """

    possible_paths = []     # list that stores the possible paths followed based on the current state
    next_states = []        # list that stores all the possible next states based on the current state
    state = []

    a_max = 70
    b_max = 50

    a = path[-1][0]     # initial amount of water in the first jug 
    b = path[-1][1]     # initial amount of water in the second jug

    # 1) Gemise to prwto pothri 
    state.append(a_max)
    state.append(b)
    if not alreadyVisited(state, visited):
        next_states.append(state)
    state = []

    # 2) Gemise to deytero pothri 
    state.append(a)
    state.append(b_max)
    if not alreadyVisited(state, visited):
        next_states.append(state)
    state = []

    # 3) Rixe nero apo to ptwto pothri sto deytero 
    state.append(min(a_max, a + b))
    state.append(b - (state[0] - a))
    if not alreadyVisited(state, visited):
        next_states.append(state)
    state = []

    # 4) Rixe nero apo to deytero pothri sto prwto 
    state.append(min(a + b, b_max))
    state.insert(0, a - (state[0] - b))
    if not alreadyVisited(state, visited):
        next_states.append(state)
    state = []

    # 5) Adeiase to prwto pothri 
    state.append(0)
    state.append(b)
    if not alreadyVisited(state, visited):
        next_states.append(state)
    state = []

    # 6) Adeiase to deytero pothri  
    state.append(a)
    state.append(0)
    if not alreadyVisited(state, visited):
        next_states.append(state)

    for i in range(0, len(next_states)):
        temp = list(path)
        temp.append(next_states[i])
        possible_paths.append(temp)
    
    return possible_paths


def search(initial_state, jugs_capacities, goal_amount, visited, choice):
    """
    Function to search using either BFS or DFS for the wanted state and return the followed path
    """
    
    if choice:
        print("-----IMPLEMENTING DFS\n")
    else:
        print("-----IMPLEMENTING BFS\n")

    found = False

    # search_front represents metwpo anazhthshs
    search_front = collections.deque()
    search_front.appendleft(initial_state)

    while len(search_front) != 0:
        # path represents mikroskopio
        path = search_front.popleft()

        # mark the current state as visited
        visited[str(path[-1])] = True

        if goalReached(path, goal_amount):
            found = True
            goal = path
            break

        next_moves = createChildren(jugs_capacities, path, visited)
        for i in next_moves:
            if choice:
                # implementing DFS
                search_front.appendleft(i)
            else:
                # implementing BFS
                search_front.append(i)
    
    if found:
        print("-----THE GOAL HAS BEEN ACHIEVED, PRINTING THE PATH FOLLOWED TO THE GOAL STATE\n")
        for i in range(0, len(goal)):
            print(i, ". ", goal[i])
    else:
        print("-----THE PROBLEM CANNOT BE SOLVED, SORRY\n")


if __name__ == '__main__':
    main()
