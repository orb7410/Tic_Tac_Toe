N = 3

def creat_matrix():
    """creats a matrix as an board to the game in size of N
        returns the matrix"""
    matrix = []
    for i in range(N):
        matrix.append([" " for x in range(N)])
    return matrix

def show_matrix(matrix):
    """prints the matrix
       returns None"""
    print("\033[96m" + N*"----")
    for row in matrix:
        line = "| "
        for i in row:
            line += i + " | "
        print(line)
        print(N*"----")
    print("\033[0m")
    return None

def check_rows(matrix):
    """checks if in a row there are N same signs
        if found returns the sign, if not returns 1"""
    for row in range(N):
        temp = matrix[row][0]
        counter = 1
        for column in range(1, N):
            if temp == " ":
                break
            if matrix[row][column] != temp:
                break
            else:
                temp = matrix[row][column]
            counter += 1
            if counter == N:
                return temp
    return 1

def check_column(matrix):
    """checks if in a column there are N same signs
        if found returns the sign, if not returns 1"""
    for column in range(N):
        temp = matrix[0][column]
        counter = 1
        for row in range(1, N):
            if temp == " ":
                break
            if matrix[row][column] != temp:
                break
            else:
                temp = matrix[row][column]
                counter += 1
                if counter == N:
                    return temp
    return 1

def check_slant1(matrix):
    """checks if in a slant there are N same signs
        if found returns the sign, if not returns 1"""
    temp = matrix[0][0]
    counter = 1
    for i in range(1,N):
        if temp == " ":
            break
        if matrix[i][i] != temp:
            break
        else:
            temp = matrix[i][i]
            counter += 1
            if counter == N:
                return temp
    return 1

def check_slant2(matrix):
    """checks if in a slant there are N same signs
        if found returns the sign, if not returns 1"""
    temp = matrix[0][N-1]
    counter = 1
    j = N-2
    for i in range(1,N):
        if temp == " ":
            break
        if matrix[i][j] != temp:
            break
        else:
            temp = matrix[i][j]
            counter += 1
            j -= 1
            if counter == N:
                return temp
    return 1

def get_winner(matrix):
    """checks if there is a sign that has N places i a row/column/slant and
        returns the sign of the winner
        if there is no winner it returns 1"""
    result = check_rows(matrix)
    if result == 1:
        result = check_column(matrix)
        if result == 1:
            result = check_slant1(matrix)
            if result == 1:
                result = check_slant2(matrix)
                if result == 1:
                    return 1
    return result

def chose_sign():
    """asks the player to chose sign
        returns yhe sign X/O"""
    while (1):
        sign = input("\033[95m" + "Please enter what you want to be X\O: " + "\033[0m")
        if sign == 'X' or sign == 'x':
            return 'X'
        if sign == 'O' or sign == 'o' or sign == '0':
            return 'O'


def machine_put_in_middle(matrix, sign):
    """checks if the middle is free to the machine to put there the sign
           returns 0 if the matrix hasnt change or 1 if changed"""
    row = N // 2  # puts in the middle
    column = N // 2
    if matrix[row][column] == " ":
        matrix[row][column] = sign
        return 1
    if N % 2 == 0:
        if matrix[(N // 2) - 1][(N // 2) - 1] == " ":
            matrix[(N // 2) - 1][(N // 2) - 1] = sign
            return 1
        if matrix[(N // 2) - 1][N // 2] == " ":
            matrix[(N // 2) - 1][N // 2] = sign
            return 1
        elif matrix[N // 2][(N // 2) - 1] == " ":
            matrix[N // 2][(N // 2) - 1] = sign
            return 1
    return 0

def machine_put_in_edges(matrix, sign):
    """checks if one of the edges is free to the machine  to put there the sign
        returns 0 if the matrix hasnt change  or 1 if changed"""
    for row in range(N):
        if matrix[row][0] == " ":
            matrix[row][0] = sign
            return 1
        if matrix[row][N - 1] == " ":
            matrix[row][N - 1] = sign
            return 1
    for column in range(N):
        if matrix[0][column] == " ":
            matrix[0][column] = sign
            return 1
        if matrix[N - 1][column] == " ":
            matrix[N - 1][column] = sign
            return 1
    return 0

def machine_check_for_2_winnings(matrix, sign):
    counter = 0
    for row in range(N):
        for column in range(N):
            if matrix[row][column] == " ":
                matrix[row][column] = sign  #checks if the mechine can win
                for r in range(N):
                    for c in range(N):
                        if matrix[r][c] == " ":
                            matrix[r][c] = sign  # checks if the mechine can win again
                            winner = get_winner(matrix)
                            if winner == sign:
                                counter += 1
                            matrix[r][c] = " "
                if counter >= 2:
                    return 1, row, column
                else:
                    counter = 0
                    matrix[row][column] = " "
    return 0, None, None


def player_check_for_2_winnings(matrix, machine_sign, player_sign):
    counter = 0
    for row in range(N):
        for column in range(N):
            if matrix[row][column] == " ":
                matrix[row][column] = player_sign  # checks if the mechine can win
                for r in range(N):
                    for c in range(N):
                        if matrix[r][c] == " ":
                            matrix[r][c] = player_sign  # checks if the mechine can win again
                            winner = get_winner(matrix)
                            if winner == player_sign:
                                counter += 1
                            matrix[r][c] = " "
                if counter >= 2:
                    result, first_row, first_column = machine_check_for_2_winnings(matrix, machine_sign)
                    # and this position is not leading to player to put in place that leads to 2 winning next move for the player
                    # maybe check with this move if player will win and dont forget to reset this spot
                    if result == 1:
                        matrix[first_row][first_column] = machine_sign
                        return 1
                    second_result, second_row, second_column = machine_check_for_2_winnings(matrix, player_sign)
                    if second_result == 1:
                        matrix[row][column] = " "
                        matrix[second_row][second_column] = machine_sign
                        return 1
                    matrix[row][column] = machine_sign
                    return 1
                else:
                    counter = 0
                    matrix[row][column] = " "

    return 0


import random
def mechine_play(matrix, sign):
    """play as the machine, first checks if it can win
       or if player can win and blocks it.
       checks if the machine can do a move that lead to 2 winning next move if not
       check the same thing for the player and block it,
        if not puts in the middle or edges.
        if not free puts randomly
       returns the matrix"""
    if sign == 'X':
        player_sign = 'O'
    else:
        player_sign = 'X'
    for row in range(N):
        for column in range(N):
            if matrix[row][column] == " ":
                matrix[row][column] = sign  #checks if the mechine can win
                winner = get_winner(matrix)
                if winner == sign:
                    return matrix
                else:
                    matrix[row][column] = player_sign #checks if the player can win
                    winner = get_winner(matrix)
                    if winner == player_sign:
                        matrix[row][column] = sign
                        return matrix
                    else:
                        matrix[row][column] = " "
    # check if there is a position that lead to 2 winnings for the player
    result = player_check_for_2_winnings(matrix, sign, player_sign)
    if result == 1:
        return matrix
    # check if there is a position that lead to 2 winnings for the machine
    result, x, y = machine_check_for_2_winnings(matrix, sign)
    if result == 1:
        return matrix
    #check if the middle is free
    result = machine_put_in_middle(matrix, sign)
    if result == 1:
        return matrix
    # check if the edges is free
    result = machine_put_in_edges(matrix, sign)
    if result == 1:
        return matrix
    while 1:
        column = random.randint(0, 2)
        row = random.randint(0, 2)
        if matrix[row][column] == " ":
            matrix[row][column] = sign
            return matrix

def player_play(matrix, sign):
    """asks the player to choose place to implant his sign and returns the matrix"""
    print("\033[92m" + "It's your turn!" + "\033[0m")
    while 1:
        while 1:
            row = int(input("Please enter the row: "))
            if row < 0 or row >= N:
                print("\033[91m" + "This row number is not exist please try again" + "\033[0m")
            else:
                break
        while 1:
            column = int(input("Please enter the column: "))
            if column < 0 or column >= N:
                print("\033[91m" + "This column number is not exist please try again" + "\033[0m")
            else:
                break
        if matrix[row][column] == " ":
            matrix[row][column] = sign
            break
        else:
            print("\033[91m" + "This place is occupied please try again" + "\033[0m")
    return matrix

def is_full_board(matrix):
    """checks if the board is full or not,
        if full returns 1 else returns 0"""
    for row in range(N):
        for column in range(N):
            if matrix[row][column] == " ":
                return 0
    return 1

def announce_winner(winner, sign):
    """gets the winner and announce who won
        returns None"""
    if winner == sign:
        print("\033[96m" + "Congratulations you are the winner! " + "\033[0m")
    else:
        print("\033[96m" + "You lost! no big deal.\nmaybe next time! " + "\033[0m")
    show_matrix(matrix)
    print("\033[91m" + "GAME OVER" + "\033[0m")
    return None

def play_game(matrix):
    """run the game, gets an empty matrix
       returns the matrix"""
    sign = chose_sign()
    if sign == 'O':
        machin_sign = 'X'
    else:
        machin_sign = 'O'
    leader = random.randint(0, 1)
    while 1:
        if is_full_board(matrix) == 1:
            break
        if leader == 1:
            show_matrix(matrix)
            matrix = player_play(matrix, sign)
            winner = get_winner(matrix)
            if winner != 1:
                announce_winner(winner, sign)
                break
            leader = 0
        if leader == 0:
            if is_full_board(matrix) == 1:
                break
            matrix = mechine_play(matrix, machin_sign)
            winner = get_winner(matrix)
            if winner != 1:
                announce_winner(winner, sign)
                break
            leader = 1
    if winner == 1:
        print("\033[96m" + "it's a tie! " + "\033[0m")
        show_matrix(matrix)
        print("\033[91m" + "GAME OVER" + "\033[0m")
    return matrix

print("\033[91m" + "welcome to Tic Tac Toe!" + "\033[0m")
while 1:
    menu_input = int(input("To play enter 1\nTo Exit press 2\n "))
    if menu_input == 1:
        matrix = creat_matrix()
        play_game(matrix)
    else:
        exit(0)