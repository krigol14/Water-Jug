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

    starting_node = [[0, 0]]
    jugs_capacities = [70, 50]
    goal_amount = 40
    visited = {}
    choice = choose()
    search(starting_node, jugs_capacities, goal_amount, visited, choice)
    pass


def choose():
    """
    The user can choose whether to solve the problem using BFS or DFS
    Function returns True if the user chooses DFS, False if the user chooses BFS
    """

    press = input("Enter 'b' to use BFS, or 'd' to use DFS: ")
    # in case the user enters b in upper-case
    press = press[0].lower()

    # check for invalid input
    while press != 'd' and press != 'b':
        press = input("Invalid input! Enter 'b' to use BFS, or 'd' to use DFS: ")
        press = press[0].lower()

    if press == 'd':
        return True
    else:
        return False


def goalReached(path, goal_amount):
    """
    Function that checks if the goal state has been reached
    Returns True if the path given terminates at the goal state

    path: list of nodes that represent the path to be checked
    goal_amount: integer representing the desired amount of water in the goal state
    """

    if path[-1][0] == goal_amount or path[-1][1] == goal_amount:
        return True
    else:
        return False
    

def alreadyVisited(node, visited):
    """
    Function that checks if the given node has been already visited during the implementation of the algorithm
    Returns True if the node has been already visited, False otherwise

    node: list of two integers representing the current state of the two jugs
    visited: dictionary that stores visited nodes
    """

    # convert node[] to string because lists are not hashable in python
    node_str = str(node)
    # if the specified key doesn't exist, returns False (2nd parameter), otherwise returns True
    return visited.get(node_str, False)


def createChildren(jugs_capacities, path, visited):
    """
    Function that creates a list of all possible transitions from the current state

    jugs_capacities: list of two integers representing the max volume each jug has
    path: list of nodes that represent the path to be checked 
    visited: dictionary that stores visited nodes
    """

    result = []
    next_children = []
    node = []

    a_max = 70
    b_max = 50 

    a = path[-1][0]     # initial amount in the first jug
    b = path[-1][1]     # initial amount in the second jug

    # 1) fill in the first jug
    node.append(a_max)
    node.append(b)
    if not alreadyVisited(node, visited):
        next_children.append(node)
    node = []

    # 2) fill in the second jug
    node.append(a)
    node.append(b_max)
    if not alreadyVisited(node, visited):
        next_children.append(node)
    node = []

    # 3) pour water from the second jug to the first jug
    node.append(min(a_max, a + b))
    node.append(b - (node[0] - a))
    if not alreadyVisited(node, visited):
        next_children.append(node)
    node = []

    # 4) pour water from the first jug to the second jug
    node.append(min(a + b, b_max))
    node.insert(0, a - (node[0] - b))
    if not alreadyVisited(node, visited):
        next_children.append(node)
    node = []

    # 5) empty the first jug
    node.append(0)
    node.append(b)
    if not alreadyVisited(node, visited):
        next_children.append(node)
    node = []

    # 6) empty the second jug  
    node.append(a)
    node.append(0)
    if not alreadyVisited(node, visited):
        next_children.append(node)

    # create a list of next paths
    for i in range(0, len(next_children)):
        temp = list(path)
        temp.append(next_children[i])
        result.append(temp)
    
    return result


def action(old_state, new_state, jugs_capacities):
    """
    Function that explains the action taken to move from the old state to the new state

    old: list storing the old state
    new: list storing the new state
    jugs_capacities: list of two integers representing the max volume each jug has
    """

    a = old_state[0]
    b = old_state[1]
    a_new = new_state[0]
    b_new = new_state[1]
    a_max = 70
    b_max = 50

    if a > a_new:
        if b == b_new:
            return "Clear {0}-liter jug:\t\t\t".format(a_max)
        else:
            return "Pour {0}-liter jug into {1}-liter jug:".format(a_max, b_max)
    else:
        if b > b_new:
            if a == a_new:
                return "Clear {0}-liter jug:\t\t\t".format(b_max)
            else: 
                return "Pour {0}-liter jug into {1}-liter jug:".format(b_max, a_max)
        else:
            if a == a_new:
                return "Fill {0}-liter jug:\t\t\t".format(b_max)
            else:
                return "Fill {0}-liter jug:\t\t\t".format(a_max)
 
              
def printActions(path, jugs_capacities):
    """
    Function that prints the path followed to reach the goal state

    path: list of nodes that represent the path to be checked
    jugs_capacities: list of two integers representing the max volume each jug has
    """

    print("Starting from:\t\t\t\t", path[0])
    for i in range(0, len(path) - 1):
        print(i, ".", action(path[i], path[i+1], jugs_capacities), path[i+1])


def search(starting_node, jugs_capacities, goal_amount, visited, choice):
    """
    Function that searches for a path starting from the starting_node and ending at the goal state

    starting_node: list of two integers representing the initial state of the jugs
    jugs_capacities: list of two integers representing the max volume each jug has
    goal_amount: integer representing the desired amount of water in the goal state
    visited: dictionary that stores visited nodes
    choice: represents the choice of the user (implements DFS if True, BFS otherwise)
    """

    if choice:
        print("-----IMPLEMENTING DFS-----")
    else:
        print("-----IMPLEMENTING BFS-----")

    goal = []
    accomplished = False

    q = collections.deque()
    q.appendleft(starting_node)     # q = deque([[[0, 0]]])

    while len(q) != 0:
        # remove the first state from the queue
        path = q.popleft()          # path = [[0, 0]]

        # mark the current state as visited
        # convert path[-1] to string because it is unhashable
        visited_node = str(path[-1])
        visited[visited_node] = True

        # check if the goal state has been achieved
        if goalReached(path, goal_amount):
            accomplished = True
            goal = path
            break
        
        # add states in the queue
        next_moves = createChildren(jugs_capacities, path, visited)
        for i in next_moves:
            if choice:
                # implementing DFS
                q.appendleft(i)
            else:
                # implementing BFS
                q.append(i)
    
    if accomplished:
        print("\n-----THE GOAL IS ACHIEVED, PRINTING THE SEQUENCE OF ACTIONS MADE-----\n")
        printActions(goal, jugs_capacities)
    else:
        print("\n-----PROBLEM CANNOT BE SOLVED-----")


if __name__ == '__main__':
    main()
    

