import random
board=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
score=0

def print_board(board):
    for row in board:
        print(*row)
        
def print_ui():
    print_board(board)

def roll_dice():
    dice_num = random.randint(1,6)
    print("Dice rolled", dice_num)
    return dice_num

def place_dice(num):
    global board
    try:
        r=int(input("enter row number (0-4):"))
        c=int(input("enter column number (0-4):"))
    except:
        print("Invalid Input! please enter numbers only")
        return 
    
    if r < 0 or r > 4 or c < 0 or c > 4:
        print("invalid position, choose between (0-4):")
        return 

    if board[r][c]==0:
        board[r][c]=num
        return r, c
    else:
        print("cells already filled choose another position")
        return
        
def if_board_full():
    for row in board:
        if 0 in row:
            return True
    return False

def restart_game():
    global board, score 
    board=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    score=0 

def save_game():
    with open("save_game.txt","w")as file:
        file.write("score:" +str(score)+"\n")
        file.write("Board:\n")
        for row in board:
            file.write("".join(str(x)for x in row)+"\n")

def read_save_game():
    global board, score
    score=0
    board=[]
    try:
        with open("save_game.txt","r") as file:
            lines=file.readlines()
            score=int(lines[0].split(":")[1].strip())
            for line in lines[2:7]:
                val=[int(x) if x.isdigit() else "O" for x in line.strip()]
                board.append(val)
        return True
                #should ignore int (x) if x is not a number  
    except:
        return False
loaded=read_save_game()
if not loaded:
    restart_game()

def check_dice(r,c):
    global score
    value = board[r][c]

    up=r-1>=0 and board[r-1][c]==value 
    down=r+1<5  and board[r+1][c]==value 
    left =c-1>=0 and board[r][c-1]==value 
    right=c+1<5  and board[r][c+1]==value 

    merged=False
    if up:
        print("same value on UP",up)
        board[r-1][c]=0
        merged=True

    if down:
        print("same value on DOWN",down)
        board[r+1][c] =0
        merged=True

    if left:
        print("same value on LEFT",left)
        board[r][c-1]= 0
        merged =True

    if right:
        print("same value on RIGHT",right)
        board[r][c+1] =0
        merged =True
    return merged, r, c

def auto_merge(merged,r,c):
    global score
    if merged:
        if board[r][c]=="O":
            return 
        if board[r][c]<6:
            board[r][c] +=1
        else:
            board[r][c]="O"
        score += 10
        print("current score:", score)

    changed =True
    while changed:
        changed=False
        if board[r][c]=="O":
            break
        value=board[r][c]
        up=r-1>=0 and board[r-1][c]==value
        down=r+1<5  and board[r+1][c]==value
        left=c-1>=0 and board[r][c-1]==value
        right =c+1<5  and board[r][c+1]== value

        if up:
            board[r-1][c]=0
            changed =True
        if down:
            board[r+1][c]=0
            changed = True
        if left:
            board[r][c-1]=0
            changed = True
        if right:
            board[r][c+1]=0
            changed = True

        if changed:
            if board[r][c]<6:
                board[r][c]+=1
            else:
                board[r][c]="O"
            score+=10
            print("current score:", score)

def clearing_3X3(board,row,col):
    rows=len(board)
    cols=len(board[0])
    for r in range(row-1, row+2):
        for c in range(col-1,col+2): 
            if 0<= r<rows and 0<=c<cols:
                board[r][c]=0

def check_horizontal(board):
    rows=len(board)
    cols=len(board[0])
    
    for r in range(rows):
        for c in range(cols-2):
            if board[r][c]==0:
                continue
            if board[r][c]=="O" and board[r][c+1]=="O" and board[r][c+2]=="O":
                print(f"horizontal find at :{r},{c+1}")
                print(clearing_3X3(board,r,c+1))

def check_vertical(board):
    rows=len(board)
    cols=len(board[0])
    for r in range(rows-2):
        for c in range(cols):
            if board[r][c]==0:
                continue
            if board[r][c]== "O" and board[r+1][c]== "O" and board[r+2][c]=="O":
                print(f"vertical find at :{r+1},{c}")
                print(clearing_3X3(board,r,c+1))
def clear_save_game():
    with open("save_game.txt","w") as file:
        file.write("")

while True:
    print_ui()
    if not if_board_full():
        print("GAME OVER")
        choice=input("To restart: click (Y/N)" )
        if choice=="Y":
                restart_game()
                clear_save_game()

                continue
        if choice=="N":
            clear_save_game()
            print("Thanks for playing!")
            break
        

            
    
    num=roll_dice()
    placed =False
    while not placed: 
        result = place_dice(num)
        if result:   
            merged,r,c=check_dice(*result)
            auto_merge(merged, r, c)
            check_horizontal(board)
            check_vertical(board)
            save_game()
            placed = True
# have to breakdown larger code into smaller function  