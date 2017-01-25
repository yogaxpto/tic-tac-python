import copy
import sys
import time

visited_nodes = 0
time_delta = 0


class Node:
    def __init__(self):
        self.table = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        self.parent = None
        self.utility = 0


def print_board(node: Node):
    print('  0 1 2')
    print('0 ' + str(node.table[0]) + ' ' + str(node.table[1]) + ' ' + str(node.table[2]))
    print('1 ' + str(node.table[3]) + ' ' + str(node.table[4]) + ' ' + str(node.table[5]))
    print('2 ' + str(node.table[6]) + ' ' + str(node.table[7]) + ' ' + str(node.table[8]))


def play_user(no: Node, simbolo: str):
    while True:
        try:
            print_board(no)
            (y, x) = input("Insert coordinates (row column):\n").split(' ')
            (y, x) = (int(y), int(x))
            if [0, 1, 2].count(y) == 1 and [0, 1, 2].count(x) == 1 and no.table[3 * y + x] == '-':
                no.table[3 * y + x] = simbolo
                return
            else:
                print("Invalid move. Insert 2 numbers delimited by a space to represent a move.")
        except:
            print("Invalid move. Insert 2 numbers delimited by a space to represent a move.")


def play_ai(node: Node, simbol: str, algorithm: int):
    if algorithm == 0:
        return maxi(node, simbol)
    return max_ab(node, simbol, -sys.maxsize, sys.maxsize)


def create_child(node: Node, simbol: str) -> [Node]:
    free = [i for i, x in enumerate(node.table) if x == "-"]
    list_child = []
    for i in free:
        temp = copy.deepcopy(node)
        temp.parent = node
        temp.table[i] = simbol
        list_child.append(temp)
    return list_child


def maxi(node, simbol):
    childs = create_child(node, simbol)
    global visited_nodes
    for i in childs:
        visited_nodes += 1
        if check_win(i) == 0:
            if i.estado.count('-') != 0:
                if simbol == 'X':
                    i.utility = mini(i, 'O').utility
                else:
                    i.utility = mini(i, 'X').utility
        elif check_win(i) == simbol:
            i.utility += 1
            break
        else:
            i.utility -= 1
    childs.sort(key=lambda x: x.utility)
    return childs[len(childs) - 1]


def mini(node: Node, simbol: str) -> Node:
    childs = create_child(node, simbol)
    global visited_nodes
    for i in childs:
        visited_nodes += 1
        if check_win(i) == 0:
            if i.estado.count('-') != 0:
                if simbol == 'X':
                    i.utility = maxi(i, 'O').utility
                else:
                    i.utility = maxi(i, 'X').utility
        elif check_win(i) != simbol:
            i.utility += 1
        else:
            i.utility -= 1
            break
    childs.sort(key=lambda x: x.utility)
    return childs[0]


def max_ab(node: Node, simbol: str, alpha: int, beta: int):
    childs = create_child(node, simbol)
    global visited_nodes
    for i in childs:
        visited_nodes += 1
        if check_win(i) == 0:
            if i.estado.count('-') != 0:
                if i.utility >= alpha:
                    if simbol == 'X':
                        i.utility = min_ab(i, 'O', alpha, beta).utility
                    else:
                        i.utility = min_ab(i, 'X', alpha, beta).utility
                    alpha = i.utility
        elif check_win(i) == simbol:
            i.utility += 1
            break
        else:
            i.utility -= 1
    childs.sort(key=lambda x: x.utility)
    return childs[len(childs) - 1]


def min_ab(node: Node, simbol: str, alpha: int, beta: int):
    childs = create_child(node, simbol)
    global visited_nodes
    for i in childs:
        visited_nodes += 1
        if check_win(i) == 0:
            if i.estado.count('-') != 0:
                if i.utility <= beta:
                    if simbol == 'X':
                        i.utility = max_ab(i, 'O', alpha, beta).utility
                    else:
                        i.utility = max_ab(i, 'X', alpha, beta).utility
                    beta = i.utility
        elif check_win(i) != simbol:
            i.utility += 1
        else:
            i.utility -= 1
            break
    childs.sort(key=lambda x: x.utility)
    return childs[0]


def check_win(node: Node) -> str or int:
    if node.table[0] == node.table[1] and node.table[1] == node.table[2] and node.table[2] != '-':
        return node.table[2]
    elif node.table[3] == node.table[4] and node.table[4] == node.table[5] and node.table[5] != '-':
        return node.table[5]
    elif node.table[6] == node.table[7] and node.table[7] == node.table[8] and node.table[8] != '-':
        return node.table[8]
    elif node.table[0] == node.table[3] and node.table[3] == node.table[6] and node.table[6] != '-':
        return node.table[6]
    elif node.table[1] == node.table[4] and node.table[4] == node.table[7] and node.table[7] != '-':
        return node.table[7]
    elif node.table[2] == node.table[5] and node.table[5] == node.table[8] and node.table[8] != '-':
        return node.table[8]
    elif node.table[0] == node.table[4] and node.table[4] == node.table[8] and node.table[8] != '-':
        return node.table[8]
    elif node.table[6] == node.table[4] and node.table[4] == node.table[2] and node.table[2] != '-':
        return node.table[2]
    return 0


def winner(no, winner_symbol):
    print_board(no)
    print(str(winner_symbol) + " is the winner!")
    print(str(visited_nodes) + " visited nodes.")
    print("%.4f seconds used by AI." % time_delta)
    sys.exit()


def main():
    node = Node()
    global visited_nodes
    global time_delta

    algorithm = None
    while algorithm is None:
        temp = int(input("Select witch algorithm to use: \n0-Min-Max\n1-Alfa-Beta\n"))
        if [0, 1].count(temp) == 1:
            algorithm = temp
        else:
            print("Unknown input.")

    simbol = None
    while simbol is None:
        temp = input("Choose your symbol:(X/O)\n")
        if ['X', 'x', 'O', 'o'].count(temp) == 1:
            simbol = temp.upper()
        else:
            print("Unknown input.")

    player = None
    while player is None:
        temp = int(input("Who starts playing? \n0-You\n1-AI\n"))
        if [0, 1].count(temp) == 1:
            player = temp
            if player == 0:
                play_user(node, simbol)
        else:
            print("Unknown input.")

    while node.table.count('-') != 0:
        print("AI turn, please wait...")
        a = visited_nodes
        start_time = time.time()
        if simbol == 'X':
            node = play_ai(node, 'O', algorithm)
        else:
            node = play_ai(node, 'X', algorithm)
        end_time = time.time()
        if check_win(node) != 0:
            winner(node, check_win(node))
        elif node.estado.count('-') == 0:
            break
        delta_time = end_time - start_time
        print(str(visited_nodes - a) + " nodes visited in this iteration.")
        print("%.4f seconds used in this iteration." % delta_time)
        time_delta += delta_time
        play_user(node, simbol)
        if check_win(node) != 0:
            winner(node, check_win(node))
    print_board(node)
    print("Draw!")
    print(str(visited_nodes) + " visited nodes.")
    print("%.4f seconds used by the AI." % time_delta)
    sys.exit()


__author__ = "Diogo"
__date__ = "$5/Abr/2015 17:57:45$"

if __name__ == "__main__":
    main()
