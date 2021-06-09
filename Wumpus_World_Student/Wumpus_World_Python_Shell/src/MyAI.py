# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from collections import defaultdict
from queue import PriorityQueue

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.board = [["NV","NV","NV","NV","NV","NV","NV"],
                ["NV","NV","NV","NV","NV","NV","NV"],
              ["NV","NV","NV","NV","NV","NV","NV"],
              ["NV","NV","NV","NV","NV","NV","NV"],
              ["NV","NV","NV","NV","NV","NV","NV"],
              ["NV","NV","NV","NV","NV","NV","NV"],
              ["NV","NV","NV","NV","NV","NV","NV"]]
        """
        each tile is a node in the dictionary with the tile value(i,j) being the key.
        the value is another dict with keys being adjacent,percepts and safe each of which is a set.
        representation is:
        {(i,j):{adjacent:set();percepts:set();safe:set()}
        """
        self.know=dict()
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.know.update({(i,j):{"adjacent":set(),"percepts":set(),"safe":set()}})
        self._update_adjacents()
        self._update_safe()

        self.X=6
        self.Y=0
        self.exit=(6,0)
        self.turn_counter=0
        self.direction= "R"
        self.foundGold= False
        self.wumpusMarked=False
        self.haveArrow=True
        self.wumpusAlive=True
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        #self._print_board()
        #print("wumpusmarked: ",self.wumpusMarked,"haveArrow: ",self.haveArrow)
        if scream:
            self.wumpusAlive=False
            self.mark_ok()
            return self.find_best_move()
        if not self.foundGold:
            if glitter:
                self.foundGold=True
                return Agent.Action.GRAB
            elif bump:
                return self.handle_bump()
            elif stench and not breeze and not self.wumpusAlive:
                self.mark_ok()
                return self.find_best_move()
            elif stench and breeze:
                return self.find_best_move(danger="both")
            elif stench and not self.wumpusMarked:
                return self.find_best_move(danger="stench")
            elif stench and self.wumpusMarked:
                #self.mark_front_okay()
                return self.find_best_move(danger="stench")
            elif breeze:
                return self.find_best_move(danger="breeze")
            else:
                return self.find_best_move()
        else:
            return self.find_best_move()
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def find_best_move(self,danger=None):
        if self.foundGold:
            if self.X==len(self.board)-1 and self.Y==0:
                return Agent.Action.CLIMB
            exit_path=self.find_path_exit()
            if self.direction!=exit_path[0][1]:
                return self.find_best_turn(self.direction,exit_path[0][1])
            self.move_forward()
            return Agent.Action.FORWARD
        elif danger==None:
            #print("danger=None")
            self.mark_ok()
            s_path=self.find_path_ok()
            if s_path != None:
                if self.direction!=s_path[0][1]:
                    return self.find_best_turn(self.direction,s_path[0][1])###
                self.move_forward()
                return Agent.Action.FORWARD
            if s_path == None and not self.wumpusMarked:
                wumpus_path=self.find_path_stench()#find the nearest aquare with only a stench
                #print(wumpus_path)
                if wumpus_path != None:
                    if self.direction!=wumpus_path[0][1]:
                        return self.find_best_turn(self.direction,wumpus_path[0][1])###
                    self.move_forward()
                    return Agent.Action.FORWARD
                else:
                    if self.X==len(self.board)-1 and self.Y==0:
                        return Agent.Action.CLIMB
                    exit_path=self.find_path_exit()
                    if self.direction!=exit_path[0][1]:
                        return self.find_best_turn(self.direction,exit_path[0][1])###
                    self.move_forward()
                    return Agent.Action.FORWARD
            if s_path == None and self.wumpusMarked:
                if self.X==len(self.board)-1 and self.Y==0:
                    return Agent.Action.CLIMB
                exit_path=self.find_path_exit()
                if self.direction!=exit_path[0][1]:
                    return self.find_best_turn(self.direction,exit_path[0][1])###
                self.move_forward()
                return Agent.Action.FORWARD
        elif danger=="stench":
            self.mark_dangerous("stench")
            s_path=self.find_path_ok()
            if s_path != None:
                if self.direction!=s_path[0][1]:
                    return self.find_best_turn(self.direction,s_path[0][1])###
                self.move_forward()
                return Agent.Action.FORWARD
            elif s_path == None and not self.wumpusMarked:
                #print("Entered")
                wumpus_path=self.find_path_wumpus()#find the nearest dangerous tile
                #print(wumpus_path)#find the nearest dangerous square whos adjacent has a stench and no breeze
                if wumpus_path != None:
                    if self.direction!=wumpus_path[0][1]:
                        return self.find_best_turn(self.direction,wumpus_path[0][1])###
                    else:
                        #print("Shooting")
                        self.wumpusMarked=True
                        self.haveArrow=False
                        self.mark_front_okay()
                        return Agent.Action.SHOOT
            else:
                #print("exiting")#stench and gold not found and no safe squares
                if self.X==len(self.board)-1 and self.Y==0:
                    return Agent.Action.CLIMB
                exit_path=self.find_path_exit()
                if self.direction!=exit_path[0][1]:
                    return self.find_best_turn(self.direction,exit_path[0][1])###
                self.move_forward()
                return Agent.Action.FORWARD
        elif danger=="breeze":
            if self.X==len(self.board)-1 and self.Y==0:
                return Agent.Action.CLIMB
            self.mark_dangerous("breeze")
            s_path=self.find_path_ok()
            if s_path != None:
                if self.direction!=s_path[0][1]:
                    return self.find_best_turn(self.direction,s_path[0][1])###
                self.move_forward()
                return Agent.Action.FORWARD
            else:#breeze and gold not found and no safe squares
                if s_path == None and not self.wumpusMarked:
                    wumpus_path=self.find_path_stench()#find the nearest aquare with only a stench
                    #print(wumpus_path)
                    if wumpus_path != None:
                        if self.direction!=wumpus_path[0][1]:
                            return self.find_best_turn(self.direction,wumpus_path[0][1])###
                        self.move_forward()
                        return Agent.Action.FORWARD
                    else:
                        if self.X==len(self.board)-1 and self.Y==0:
                            return Agent.Action.CLIMB
                        exit_path=self.find_path_exit()
                        if self.direction!=exit_path[0][1]:
                            return self.find_best_turn(self.direction,exit_path[0][1])###
                        self.move_forward()
                        return Agent.Action.FORWARD
            if s_path == None and self.wumpusMarked:
                if self.X==len(self.board)-1 and self.Y==0:
                    return Agent.Action.CLIMB
                exit_path=self.find_path_exit()
                if self.direction!=exit_path[0][1]:
                    return self.find_best_turn( self.direction,exit_path[0][1])###
                self.move_forward()
                return Agent.Action.FORWARD
        elif danger=="both":
            if self.X==len(self.board)-1 and self.Y==0:
                return Agent.Action.CLIMB
            self.mark_dangerous("both")
            s_path=self.find_path_ok()
            if s_path != None:
                if self.direction!=s_path[0][1]:
                    return self.find_best_turn(self.direction,s_path[0][1])###
                self.move_forward()
                return Agent.Action.FORWARD
            else:#breeze and gold not found and no safe squares
                if self.X==len(self.board)-1 and self.Y==0:
                    return Agent.Action.CLIMB
                exit_path=self.find_path_exit()
                if self.direction!=exit_path[0][1]:
                    return self.find_best_turn(self.direction,exit_path[0][1])###
                self.move_forward()
                return Agent.Action.FORWARD

    def handle_bump(self):
        if self.direction=="R":
            self.update_bump("R")
            self._update_adjacents()
            self._update_safe()
            self.change_dir_left()
            self.Y-=1
            return Agent.Action.TURN_LEFT
        elif self.direction=="L":
            self.Y+=1
            if self.X==0 and self.Y==0:
                self.change_dir_left()
                return Agent.Action.TURN_LEFT
            else:
                self.change_dir_right()
                return Agent.Action.TURN_RIGHT
        elif self.direction=="U":
            self.update_bump("U")
            self._update_adjacents()
            self._update_safe()
            self.change_dir_left()
            #self.X+=1
            return Agent.Action.TURN_LEFT
        elif self.direction=="D":
            self.change_dir_right()
            self.X-=1
            return Agent.Action.TURN_RIGHT

    def update_bump(self,sit:str):
        """R,L,U,D taken for bumps"""
        if sit=="R":
            new_board=[]
            for row in self.board:
                new_board.append(row[0:self.Y])
            self.board=new_board
            for key in list(self.know.keys()):
                if key[1]>=self.Y:
                    self.know.pop(key)
        elif sit=="U":
            temp=dict()
            for i in range(len(self.board)-(self.X+1)):
                for j in range(len(self.board[0])):
                    temp.update({(i,j):self.know[(i+self.X+1,j)]})
            self.know=temp
            new_board=self.board[self.X+1:]
            self.board=new_board
            self.exit=(len(new_board)-1,0)
            self.X=0
        return None

    def move_forward(self):
        self.board[self.X][self.Y]="SA"
        if self.direction=="R":
            self.Y+=1
        elif self.direction=="L":
            self.Y-=1
        elif self.direction=="D":
            self.X+=1
        elif self.direction=="U":
            self.X-=1
        self._update_safe()
        return None

    def mark_ok(self):
        if self._is_valid(self.X-1,self.Y) and self.board[self.X-1][self.Y] !="SA":
            self.board[self.X-1][self.Y] = "OK"
            #self.know[(self.X-1,self.Y)]["percepts"].add("OK")
        if self._is_valid(self.X+1,self.Y) and self.board[self.X+1][self.Y] !="SA":
            self.board[self.X+1][self.Y] = "OK"
            #self.know[(self.X+1,self.Y)]["percepts"].add("OK")
        if self._is_valid(self.X,self.Y-1) and self.board[self.X][self.Y-1] !="SA":
            self.board[self.X][self.Y-1] = "OK"
            #self.know[(self.X,self.Y-1)]["percepts"].add("OK")
        if self._is_valid(self.X,self.Y+1)  and self.board[self.X][self.Y+1] !="SA":
            self.board[self.X][self.Y+1] = "OK"
            #self.know[(self.X,self.Y+1)]["percepts"].add("OK")
        self._update_safe()
        return None

    def mark_front_okay(self):
        if self.direction=="L" and self._is_valid(self.X,self.Y-1):
            self.board[self.X][self.Y-1]="OK"
            #self.know[(self.X,self.Y-1)]["percepts"].add("OK")
        if self.direction=="R" and self._is_valid(self.X,self.Y+1):
            self.board[self.X][self.Y+1]="OK"
            #self.know[(self.X,self.Y+1)]["percepts"].add("OK")
        if self.direction=="U" and self._is_valid(self.X-1,self.Y):
            self.board[self.X-1][self.Y]="OK"
            #self.know[(self.X-1,self.Y)]["percepts"].add("OK")
        if self.direction=="D" and self._is_valid(self.X+1,self.Y):
            self.board[self.X+1][self.Y]="OK"
            #self.know[(self.X+1,self.Y)]["percepts"].add("OK")
        self._update_safe()
        return None

    def mark_dangerous(self,danger:str):
        self.know[(self.X,self.Y)]["percepts"].add(danger)
        if self._is_valid(self.X-1,self.Y) and (self.board[self.X-1][self.Y] !="SA" and self.board[self.X-1][self.Y] !="OK"):
            self.board[self.X-1][self.Y] = "DA"
        if self._is_valid(self.X+1,self.Y) and (self.board[self.X+1][self.Y] !="SA" and self.board[self.X+1][self.Y] !="OK"):
            self.board[self.X+1][self.Y] = "DA"
        if self._is_valid(self.X,self.Y-1)and (self.board[self.X][self.Y-1] !="SA" and self.board[self.X][self.Y-1] !="OK"):
            self.board[self.X][self.Y-1] = "DA"
        if self._is_valid(self.X,self.Y+1) and (self.board[self.X][self.Y+1] !="SA" and self.board[self.X][self.Y+1] !="OK"):
            self.board[self.X][self.Y+1] = "DA"
        self._update_safe()
        return None

    def change_dir_left(self):
        if self.direction == "R":
            self.direction = "U"
        elif self.direction == "L":
            self.direction ="D"
        elif self.direction == "D":
            self.direction = "R"
        elif self.direction == "U":
            self.direction = "L"
            return None

    def change_dir_right(self):
        if self.direction == "R":
            self.direction = "D"
        elif self.direction == "L":
            self.direction ="U"
        elif self.direction == "D":
            self.direction = "L"
        elif self.direction == "U":
            self.direction = "R"
        return None

    def find_path_ok(self):
        if self._ok_exists():
            #node=(cost,co-ordinates,direction,parent)
            node=(0,(self.X,self.Y),self.direction,(self.X,self.Y))
            frontier=PriorityQueue()
            frontier.put(node)
            explored=set()
            path=[]
            while not frontier.empty():
                node=frontier.get()
                path.append(node)
                if node[1] != (self.X,self.Y) and self.board[node[1][0]][node[1][1]]=="OK":
                    #print(path)
                    result=[(path[-1][3],path[-1][2])]
                    prev=path[-1][3]
                    for n in path[-2::-1]:
                        if n[1]!=n[3] and n[1]==prev:
                            result.append((n[3],n[2]))
                            prev=n[3]
                    result.reverse()
                    #print(result)
                    return result
                explored.add(node[1])
                for tile in self.know[node[1]]["safe"]:
                    path_cost,dir=self._cost(node[1][0],node[1][1],tile[0],tile[1],node[2])
                    safe_node=(path_cost+node[0],(tile[0],tile[1]),dir,node[1])
                    if safe_node[1] not in explored:
                        frontier.put(safe_node)
        return None

    def find_path_exit(self):
        #node=(cost,co-ordinates,direction,parent)
        node=(0,(self.X,self.Y),self.direction,(self.X,self.Y))
        frontier=PriorityQueue()
        frontier.put(node)
        explored=set()
        path=[]
        while not frontier.empty():
            node=frontier.get()
            path.append(node)
            if node[1] == (len(self.board)-1,0):
                #print(path)
                result=[(path[-1][3],path[-1][2])]
                prev=path[-1][3]
                for n in path[-2::-1]:
                    if n[1]!=n[3] and n[1]==prev:
                        result.append((n[3],n[2]))
                        prev=n[3]
                result.reverse()
                #print(result)
                return result
            explored.add(node[1])
            for tile in self.know[node[1]]["safe"]:
                path_cost,dir=self._cost(node[1][0],node[1][1],tile[0],tile[1],node[2])
                safe_node=(path_cost+node[0],(tile[0],tile[1]),dir,node[1])
                if safe_node[1] not in explored:
                    frontier.put(safe_node)
        return None

    def find_path_stench(self):
        #node=(cost,co-ordinates,direction,parent)
        #print("Entered 2")
        node=(0,(self.X,self.Y),self.direction,(self.X,self.Y))
        frontier=PriorityQueue()
        frontier.put(node)
        explored=set()
        path=[]
        while not frontier.empty():
            node=frontier.get()
            #print(node[1])
            path.append(node)
            if "stench" in self.know[(node[1][0],node[1][1])]["percepts"]:
                result=[(path[-1][3],path[-1][2])]
                prev=path[-1][3]
                for n in path[-2::-1]:
                    if n[1]!=n[3] and n[1]==prev:
                        result.append((n[3],n[2]))
                        prev=n[3]
                result.reverse()
                return result
            explored.add(node[1])
            for tile in self.know[node[1]]["safe"]:
                path_cost,dir=self._cost(node[1][0],node[1][1],tile[0],tile[1],node[2])
                safe_node=(path_cost+node[0],(tile[0],tile[1]),dir,node[1])
                if safe_node[1] not in explored:
                    frontier.put(safe_node)
        return None

    def find_path_wumpus(self):
        #node=(cost,co-ordinates,direction,parent)
        #print("Entered 2")
        node=(0,(self.X,self.Y),self.direction,(self.X,self.Y))
        frontier=PriorityQueue()
        frontier.put(node)
        explored=set()
        path=[]
        while not frontier.empty():
            node=frontier.get()
            #print(node[1])
            path.append(node)
            if self.board[node[1][0]][node[1][1]]=="DA":
                result=[(path[-1][3],path[-1][2])]
                prev=path[-1][3]
                for n in path[-2::-1]:
                    if n[1]!=n[3] and n[1]==prev:
                        result.append((n[3],n[2]))
                        prev=n[3]
                result.reverse()
                return result
            explored.add(node[1])
            for tile in self.know[node[1]]["adjacent"]:
                path_cost,dir=self._cost(node[1][0],node[1][1],tile[0],tile[1],node[2])
                safe_node=(path_cost+node[0],(tile[0],tile[1]),dir,node[1])
                if safe_node[1] not in explored:
                    frontier.put(safe_node)
        return None


    def find_best_turn(self,curr,final):
        if curr=="L":
            if final=="U" or final=="R":
                self.change_dir_right()
                return Agent.Action.TURN_RIGHT
            elif final=="D":
                self.change_dir_left()
                return Agent.Action.TURN_LEFT
        elif curr=="R":
            if final=="U":
                self.change_dir_left()
                return Agent.Action.TURN_LEFT
            elif final=="D" or final =="L":
                self.change_dir_right()
                return Agent.Action.TURN_RIGHT
        elif curr=="U":
            if final=="R" or final=="D":
                self.change_dir_right()
                return Agent.Action.TURN_RIGHT
            elif final=="L":
                self.change_dir_left()
                return Agent.Action.TURN_LEFT
        elif curr=="D":
            if final=="L" or final=="U":
                self.change_dir_right()
                return Agent.Action.TURN_RIGHT
            elif final=="R":
                self.change_dir_left()
                return Agent.Action.TURN_LEFT


    def _cost(self,start_x,start_y,end_x,end_y,dir)->"""(int,final direction)""":
        """returns the number of moves needed to move to the adjacent square"""
        if start_x==end_x and start_y==end_y:
            return 0
        if end_x==start_x:#in same row left or right
            if start_y<end_y:#left
                return (self._num_turns(dir,"R")+1,"R")
            if start_y>end_y:#right
                return (self._num_turns(dir,"L")+1,"L")
        elif end_y==start_y:#in same column up or down
            if start_x<end_x:#down
                return (self._num_turns(dir,"D")+1,"D")
            if start_x>end_x:#up
                return (self._num_turns(dir,"U")+1,"U")
            
    
    def _num_turns(self,curr,final):
        "Number of turns required to face a given direction"
        if curr==final:
            return 0
        elif curr=="L":
            return 1 if final=="R" else 2
        elif curr=="U":
            return 1 if final=="D" else 2
        elif curr=="D":
            return 1 if final=="U" else 2
        elif curr=="R":
            return 1 if final=="L" else 2


    def _is_valid(self,x,y):
        return x>=0 and x<len(self.board) and y>=0 and y<len(self.board[0])

    

    def _update_adjacents(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.know[(i,j)]["adjacent"].clear()
                if self._is_valid(i+1,j):
                    self.know[(i,j)]["adjacent"].add((i+1,j))
                if self._is_valid(i-1,j):
                    self.know[(i,j)]["adjacent"].add((i-1,j))
                if self._is_valid(i,j+1):
                    self.know[(i,j)]["adjacent"].add((i,j+1))
                if self._is_valid(i,j-1):
                    self.know[(i,j)]["adjacent"].add((i,j-1))
        return None

    def _update_safe(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.know[(i,j)]["safe"].clear()
                if self._is_valid(i+1,j) and (self.board[i+1][j] == "SA" or self.board[i+1][j] == "OK"):
                    self.know[(i,j)]["safe"].add((i+1,j))
                if self._is_valid(i-1,j) and (self.board[i-1][j] =="SA" or self.board[i-1][j] == "OK"):
                    self.know[(i,j)]["safe"].add((i-1,j))
                if self._is_valid(i,j+1) and (self.board[i][j+1] =="SA" or self.board[i][j+1] == "OK"):
                    self.know[(i,j)]["safe"].add((i,j+1))
                if self._is_valid(i,j-1) and (self.board[i][j-1] =="SA" or self.board[i][j-1] == "OK"):
                    self.know[(i,j)]["safe"].add((i,j-1))
        return None

    def _ok_exists(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j]=="OK":
                    return True
        return False

    def _print_board(self):
        for key in self.know:
            print(key,self.know[key]["percepts"])
        for row in self.board:
            print(row)
        print("X:",self.X, "Y:", self.Y)
        print("DIR: ",self.direction)
        return None

    def _only_stench_around(self,x,y):
        if self._is_valid(x,y-1):
            if "stench" in self.know[(x,y-1)]["percepts"]:
                return True
        if self._is_valid(x,y+1):
            if "stench" in self.know[(x,y+1)]["percepts"]:
                return True
        if self._is_valid(x-1,y):
            if "stench" in self.know[(x-1,y)]["percepts"]:
                return True
        if self._is_valid(x+1,y):
            #print(self.know[(x+1,y)])
            if "stench" in self.know[(x+1,y)]["percepts"]:
                return True
        return False

                
        
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================