import random
import time

def intInput(mi, ma):
    i = input()
    while (not(i.isnumeric()) or int(i) > ma or int(i) < mi):
        print("Not a allowable answer please type in a number between "+str(mi)+" and "+str(ma))
        i = input()
    i = int(i)
    return i

def printTable(data):
    for e in data:
        if e[0] != '%':
            print("/---\/---\/---\ ")
            print("| "+e[0]+" || "+e[1]+" || "+e[2]+" | ")
            print("\---/\---/\---/ ")
        else:
            print("     /---\      ")
            print("     | "+e[1]+" |      ")
            print("     \---/      ")
# end function

def printScore(data):
    print("Player 1: "+str(data[0][0])+" on start   "+str(data[0][1])+" at home")
    print("Player 2: "+str(data[1][0])+" on start   "+str(data[1][1])+" at home")
# end function

def printOptions(player, roll, table, score, ai, dis):
    c = 1
    cmd = []
    col = -1
    if(player==2):
        ismain = lambda a: a.isnumeric()
        isalt = lambda a: a.isalpha()
        col = 2
    else:
        col = 0
        ismain = lambda a: a.isalpha()
        isalt = lambda a: a.isnumeric()

    if score[player-1][0] > 0:
        if table[4-roll][col] == " " or table[4-roll][col] == "*":
            if dis:
                print(str(c)+". move a piece out of start")
            cmd.append(0) # cmd 0 is move piece out of start
            c +=1
    i = -1
   
    for e in table:
        i +=1
        if ismain(e[col]): # check player column
            if i >5:
                if (i-roll) == 5:
                    if dis:
                        print(str(c)+". move "+e[col]+" home")
                    cmd.append(e[col])
                    c +=1
                if ((i-roll) > 5) and not(ismain(table[(i-roll)][col])):
                    if dis:
                        print(str(c)+". move "+e[col])
                    cmd.append(e[col])
                    c +=1   
            else:
                mov = (i-roll)
                x = col
                if mov < 0:
                    mov = abs(mov)-1
                    x = 1
                if not(ismain(table[mov][x]))and not(isalt(table[mov][x]) and (mov == 3 and x == 1)):
                    if dis:
                        print(str(c)+". move "+e[col])
                    cmd.append(e[col])
                    c +=1

        if ismain(e[1]): # check middle column
            mov = i+roll
            x = 1
            if mov > 7:
                x = col
                mov = (7-(mov-7))-1
            
            if not(ismain(table[mov][x]))and not((isalt(table[mov][x]) and (mov == 3 and x == 1)) and not(x == col and mov < 6)):
                if dis:
                    print(str(c)+". move "+e[1])
                cmd.append(e[1])
                c +=1
    if( c ==1):
        return -1
    if(ai == 0):
        i = intInput(1,c-1)
    elif(ai == 1):
        i = 1
    elif(ai == 2):
        if(c > 2):
            i = 2
        else:
            i = 1
    elif(ai == 3):
        i = c-1
    elif(ai == 4):
        i = random.randint(1,c-1)
        while i>(c-1) or i<1:
            i = random.randint(1,c-1)
    return cmd[i-1]
# end function

def roll(dis):
    r = random.randint(0,1)+random.randint(0,1)+random.randint(0,1)+random.randint(0,1)
    if dis:
        print("You rolled a "+str(r))
    return r

def mov(cmd, roll, table, Player, score):
    rollagain = False
    if cmd == 0:
        if Player == 1:
            pieces = ['a','b','c','d','e','f','g']
            x=0
        if Player == 2:
            pieces = ['1','2','3','4','5','6','7']
            x=2

        score[Player-1][0] -= 1
        for p in pieces:
            l=find(table, p)
            if l == [-1,-1]:
                if table[4-roll][x] == '*':
                    rollagain = True
                table[4-roll][x] = p
                break
    else:
        loc = find(table, cmd)
        Newloc = CalcLoc(Player, loc, roll)

        if table[Newloc[0]][Newloc[1]].isnumeric():
            score[1][0] += 1 
        if table[Newloc[0]][Newloc[1]].isalpha():
            score[0][0] += 1 
        if table[Newloc[0]][Newloc[1]] == '*':
            rollagain = True

        table[Newloc[0]][Newloc[1]] = table[loc[0]][loc[1]]
        
        if (loc[0] == 0 and loc[1] == 0)or(loc[0] == 0 and loc[1] == 2)or(loc[0] == 3 and loc[1] == 1)or(loc[0] == 6 and loc[1] == 0)or(loc[0] == 6 and loc[1] == 2):
            table[loc[0]][loc[1]] = "*"# if it was a rose place, replace the rose.
        else:
            table[loc[0]][loc[1]] = " "
        
        if(Newloc == [5,0])or(Newloc == [5,2]): # if you moved off
            table[Newloc[0]][Newloc[1]] = '%'
            score[Player-1][1] +=1
    return rollagain

#end function
def find(table, element):
    n = 0
    m = 0
    for t in table:
        for e in t:
            if e == element:
                return [n,m]
            else:
                m +=1
        m = 0
        n+=1
    
    return [-1,-1]
# end function

def CalcLoc(Player, currLoc, roll):
    if Player == 1:
        col = 0
    else:
        col = 2
    
    if currLoc[1] == 1: # if in the middle 
        ret = currLoc[0]+roll
        x = 1
        if ret > 7:
            ret = 7-(ret-7-1)
            x = col
        return [ret,x]
    else:
        ret = currLoc[0]-roll
        x = col
        if(ret < 0):
            ret = abs(ret)-1
            x=1
        return [ret,x]
#end function
        
def play(t,s,p1,p2, dis):
    winner = 0
    rounds = 0
    ticks = time.perf_counter()

    while winner == 0:
        rounds +=1
        winner = turn(1, t,s, p1, dis)
        if winner != 0:
            break
        winner = turn(2,t,s,p2,dis)
    newticks = time.perf_counter()
    timer = newticks - ticks

    print("WINNER " + str(rounds))
    
    if dis:
        printTable(t)
        printScore(s)
        print("THE WINNER IS PLAYER "+ str(winner))
        print("in "+ str(rounds)+" rounds")
        print("in "+str(timer)+" Seconds")
        print(str(timer/rounds) + " seconds per round")
    return [winner, rounds, timer, timer/rounds]

def Analyse(data):
    print("Number of Tests: "+str(data[0]))
    print("Average Number of Rounds: "+str(data[1]))
    print("Average Length of Game: "+str(data[2]))
    print("Average Length of a round: "+str(data[3]))
    print("Player 1 Wins: "+str(data[4]))
    print("Player 2 Wins: "+str(data[5]))

def PVP(t,s):
    play(t,s,0,0, True)

def PVA(t,s,ai):
    print("MESTY: " +str(ai))
    play(t,s,0,ai, True)

def AVA(t,s, ai1,ai2):
    play(t,s,ai1,ai2, True)

def aiAnalytics(t,s, ai1,ai2, rounds):
    i = 0
    print(rounds)
    predata = [0,0,0,0]
    data = [0,0,0,0]
    winCount = [0,0]
    while i < rounds:
        new = play(t,s,ai1,ai2, False)
        print("round "+str(i)+" Winner: "+str(new[0]-1))
        winCount[new[0]-1] += 1
        predata[0] +=1
        predata[1] += new[1]
        predata[2] += new[2]
        predata[3] += new[3]
        i +=1
    rounds = predata[0]
    
    i = 0
    for e in predata:
        data[i] = e/rounds
        i += 1
    data[0] = rounds
    data.append(winCount[0])
    data.append(winCount[1])
    return data

def askAI(numOf):
    ai = []
    for i in range(0, numOf):
        print("What AI do you want to use for AI #"+str(i+1)+"?")
        print("1. choose 1")
        print("2. choose 2 if possible")
        print("3. choose last move")
        print("4. choose Random")
        ai.append(intInput(1,4))
    return ai
# end function

def turn(player, table, score, ai, dis):
    end = False
    while end == False:
        if dis:
            printTable(table)
            printScore(score)
            print("Player "+str(player)+"'s turn")
        r= roll(dis)
        if r!=0:
            m= printOptions(player, r, table, score, ai, dis)
            if m == -1:
                if dis:
                    print("There are no moves you can make")
                    print("input anything to conferm")
                    if(ai == 0):
                        input()
                end = True
            end = not(mov(m,r,table,player,score))
        else:
            if dis:
                print("There are no moves you can make")
                print("input anything to conferm")
                if(ai == 0):
                    input()
            end = True
    if score[player-1] == [0,7]:
        return player
    else:
        return 0

# Data        
tbl = [["*"," ","*"],[" "," "," "],[" "," "," "],[" ","*"," "],["%"," ","%"],["%"," ","%"],["*"," ","*"],[" "," "," "]]
Score = [[7,0],[7,0]]

# Program Start
print("Welcome to the Royal Game of Ur")
print("1. Rules")
print("2. Vs AI")
print("3. Vs Human")
print("4. Show Board")
print("5. AI vs AI")
print("6. AI analytics")
print("Enter choice: ")
i= intInput(1,6)

if i==1:
    tbl = [[">","V","<"],["^","V","^"],["^","V","^"],["S","V","S"],["%","V","%"],["%","V","%"],["F","V","F"],["^","<>","^"]]
    printTable(tbl)
    print("Rules of the Royal game of Ur")
    print("=============================")
    print("GOAL:")
    print("   Get 7 pieces from the start(S) to the Finish(F)")
    print("START:")
    print("   Player 1 starts on the left")
    print("   player 2 starts on the right")
    print("ON YOUR TURN:")
    print("   On your turn you will roll a number between 0 and 4")
    print("   weighted to be like 4(d2-1)")
    print("   you will move one of your pieces around the track a")
    print("   a number of spaces equal to that roll")
    print("THE TRACK:")
    print("   each player will start on their side and move up to the top of the board")
    print("   then each player will move down to the bottom of the board through the center column")
    print("   Finally each person will move up their side till they are off the board")
    print("   a player cannot enter a side that is not their own")
    print("   on the middle a player can kick the other player off the board")
    print("THE ROSE:")
    print("   If you land on the rose(*)(see below board) then you get to roll again")
    print("THE END:")
    print("  The game ends when a person move their 7th piece off the board")

    tbl = [["*"," ","*"],[" "," "," "],[" "," "," "],[" ","*"," "],["%"," ","%"],["%"," ","%"],["*"," ","*"],[" "," "," "]]
    printTable(tbl)
if i==2:
    ai = askAI(1)
    PVA(tbl,Score, ai[0])
if i==3:
    PVP(tbl, Score)
if i==4:
    printTable(tbl)
    printScore(Score)
if i==5:
    ai = askAI(2)
    AVA(tbl, Score, ai[0], ai[1])
if i==6:
    print("How many tests?")
    j = intInput(0,9999999999999999999999999999)
    ai = askAI(2)
    print(j)
    data = aiAnalytics(tbl, Score, ai[0], ai[1], j)
    Analyse(data)

        

