INF = 0xffffff

def is_game_over(node):
    winning_indexes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    for indexes in winning_indexes:
        hit_count = 0
        chosen_symbol = node[indexes[0]]

        for index in indexes:
            if node[index] is not None and node[index] == chosen_symbol:
                hit_count = hit_count + 1

        if hit_count == 3:
            return True, chosen_symbol

    if node.count(None) == 0:
        return True, None

    return False, None

def generate_children(node, chosen_symbol):
    result = []
    temp = node.copy()
    for i in range(9):
        if(node[i] is None):
            temp[i] = chosen_symbol
            result.append(temp.copy())
            temp[i] = node[i]

    return result

def alternate_symbol(symbol):
    return 'o' if symbol == 'x' else 'x'

def mini_max_ab(node, is_maximizing_player_turn, chosen_symbol, alpha, beta): # TODO: Modify this minimax in order to turn it into an alpha-beta pruning version with depth cutting
    game_result = is_game_over(node)

    if game_result[0]:
        if game_result[1] is None:
            return 0, node # tie

        return (-1, node) if is_maximizing_player_turn else (1, node) #-1 lose, 1 win

    children_results = generate_children(node, chosen_symbol)

    if is_maximizing_player_turn:
        maxvalue = -INF
        child_result = None
        for child in children_results:
            val = mini_max_ab(child, 0, alternate_symbol(chosen_symbol), alpha, beta)
            # maxvalue = max(maxvalue, val[0])
            if val[0] > maxvalue:
                maxvalue = val[0]
                child_result = child.copy()
            alpha = max(alpha, val[0])
            if(beta <= alpha):
                break
        return maxvalue, child_result
    else:
        minvalue = INF
        child_result = None
        for child in children_results:
            val = mini_max_ab(child, 1, alternate_symbol(chosen_symbol), alpha, beta)
            # minvalue = min(minvalue, val[0])
            if val[0] < minvalue:
                minvalue = val[0]
                child_result = child.copy()
            beta = min(beta, val[0])
            if(beta <= alpha):
                break
        return minvalue, child_result

def mini_max(node, is_maximizing_player_turn, chosen_symbol):
    game_result = is_game_over(node)

    if game_result[0]:
        if game_result[1] is None:
            return 0, node

        return (-1, node) if is_maximizing_player_turn else (1, node)
 
    children = generate_children(node, chosen_symbol)
    children_results = list(map(
        lambda child: [
            mini_max(child, not is_maximizing_player_turn, alternate_symbol(chosen_symbol))[0],
            child
        ],
        children
    ))

    return max(children_results, key=str) if is_maximizing_player_turn else min(children_results, key=str)

# node = [None] * 9
# node[0] = 'x'
# node[1] = 'o'
# node[2] = 'x'
# node[3] = 'o'
# node[4] = 'o'
# node[5] = 'x'
# # node[6] = 'o'
# node[7] = 'x'
# # node[8] = 'o'
# r = mini_max_ab(node, 1, 'o', -INF, INF)
# print(r)
# generate_children(node, 'o')