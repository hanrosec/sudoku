# Skrypt generujący planszę sudoku

from random import sample, choice
import copy

BASE = 3
MAX_EMPTY = (BASE**4) - 17
DIFFICULTIES = [0, 1, 2, 3] # easy do very hard

def generate_whole_plane():
    """Funkcja do generowania uzupełnionej planszy sudoku
    Ta funkcja to magia
    (https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python)
    """
    side = BASE**2
    
    pattern = lambda rows,columns: (BASE*(rows%BASE)+rows//BASE+columns)%side    
    shuffle = lambda s: sample(s, len(s))
    
    row_base = range(BASE)
    rows  = [g*BASE + row for g in shuffle(row_base) for row in shuffle(row_base)] 
    cols  = [g*BASE + column for g in shuffle(row_base) for column in shuffle(row_base)]
    nums  = shuffle(range(1,BASE*BASE+1))
    
    plane = [[nums[pattern(r,c)] for c in cols] for r in rows]
    # print_pretty_board(plane)
    return plane.copy()

def remove_elements(plane:list, n_items_to_remove):
    assert n_items_to_remove <= MAX_EMPTY
    side = BASE**2
    squares = side**2
    for p in sample(range(squares), n_items_to_remove):
        plane[p//side][p%side] = 0
    return plane
    
def generate_puzzle(difficulty):
    assert difficulty in DIFFICULTIES
    
    all_numbers = list(range(1,(3**4)-17))
    split_to_n = len(all_numbers) // len(DIFFICULTIES)
    chunks = [all_numbers[i:i+split_to_n] for i in range(0, len(all_numbers), split_to_n)]
    # numery do usuniecia na podstawie poziomu trudnosci
    n_to_del = chunks[difficulty]
    solution = generate_whole_plane()
    return solution, remove_elements(copy.deepcopy(solution), choice(n_to_del))

def print_pretty_board(board):
    def expandLine(line):
        return line[0]+line[5:9].join([line[1:5]*(BASE-1)]*BASE)+line[9:13]
    line0  = expandLine("╔═══╤═══╦═══╗")
    line1  = expandLine("║ . │ . ║ . ║")
    line2  = expandLine("╟───┼───╫───╢")
    line3  = expandLine("╠═══╪═══╬═══╣")
    line4  = expandLine("╚═══╧═══╩═══╝")

    symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums   = [ [""]+[symbol[n] for n in row] for row in board ]
    print(line0)
    for r in range(1,(BASE**2)+1):
        print( "".join(n+s for n,s in zip(nums[r-1],line1.split("."))) )
        print([line2,line3,line4][(r%(BASE**2)==0)+(r%BASE==0)])

def parse_board(board):
    parsed = ""
    for x in board:
        for y in x:
            parsed += str(y)
    
    return parsed