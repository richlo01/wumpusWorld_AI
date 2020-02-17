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

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        
        #(x,y) = "OK", "NV"not visited, "Safe", "D"anger, "Boundary"
        self.board = [["NV","NV","NV","NV","NV","NV","NV"],
                       ["NV","NV","NV","NV","NV","NV","NV"],
                       ["NV","NV","NV","NV","NV","NV","NV"],
                       ["NV","NV","NV","NV","NV","NV","NV"],
                       ["NV","NV","NV","NV","NV","NV","NV"],
                       ["NV","NV","NV","NV","NV","NV","NV"],
                       ["NV","NV","NV","NV","NV","NV","NV"]]
        
        self.positionX = 0
        self.positionY = 0
        
        # directions = ["R"ight, "L"eft, "U"p, "D"own]
        self.direction = "R"
        
        self.lastAction = str()
        self.foundGold = False
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        return Agent.Action.CLIMB
#         print(self.board)
#         if bump:
#             if self.positionX < 0:
#                 self.positionX+=1
#             if self.positionY < 0:
#                 self.positionY+=1
#             #print(str(self.positionX)+":"+str(self.positionY)+"\n")
#             return self.moveForward()
#         elif glitter:
#             self.board[self.positionX][self.positionY]="SAFE"
#             return Agent.Action.GRAB
#         elif breeze and self.board[self.positionX][self.positionY]!="SAFE":
#             self.board[self.positionX][self.positionY]="SAFE"
#             self.updateBoard(True)
#             return self.moveForward()
#         elif breeze:
#             return self.moveForward()
#         elif stench and self.board[self.positionX][self.positionY]!="SAFE":
#             self.board[self.positionX][self.positionY]="SAFE"
#             self.updateBoard(True)
#             return self.moveForward()
#         elif stench:
#             return self.moveForward()
#         elif self.lastAction == "backtrack":
#             print("CHECKING SURROUNDINGS-----")
#             return self.checkSurrounding()
#         else:
#             self.board[self.positionX][self.positionY]="SAFE"
#             self.updateBoard()
#             return self.moveForward()
        
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def updateBoard(self,situation=False):
        if situation != True:
            if self.direction == "R":
                self.board[self.positionX+1][self.positionY] = "OK"
                self.board[self.positionX][self.positionY+1] = "OK"
            elif self.direction == "L":
                self.board[self.positionX-1][self.positionY] = "OK"
                self.board[self.positionX][self.positionY+1] = "OK"
            elif self.direction == "U":
                self.board[self.positionX][self.positionY+1] = "OK"
                if self.positionX-1 >=0 and self.board[self.positionX-1][self.positionY] != "SAFE":
                    self.board[self.positionX-1][self.positionY] = "OK"
                if self.board[self.positionX+1][self.positionY] != "SAFE":
                    self.board[self.positionX+1][self.positionY] = "OK"
            elif self.direction == "D":
                if self.board[self.positionX][self.positionY-1] != "SAFE":
                    self.board[self.positionX][self.positionY+1] = "OK"
                if self.positionX-1 >=0 and self.board[self.positionX-1][self.positionY] != "SAFE":
                    self.board[self.positionX-1][self.positionY] = "OK"
                if self.board[self.positionX+1][self.positionY] != "SAFE":
                    self.board[self.positionX+1][self.positionY] = "OK"
        else:
            if self.direction == "R":
                self.board[self.positionX+1][self.positionY] = "DANGER"
                self.board[self.positionX][self.positionY+1] = "DANGER"
            elif self.direction == "L":
                self.board[self.positionX-1][self.positionY] = "DANGER"
                self.board[self.positionX][self.positionY+1] = "DANGER" 
            elif self.direction == "U":
                self.board[self.positionX][self.positionY+1] = "DANGER"
    
    def moveForward(self):
        if self.direction == "R" and self.board[self.positionX+1][self.positionY] in ["OK","SAFE"]:
            self.positionX+=1
            return Agent.Action.FORWARD
        elif self.direction == "L" and self.board[self.positionX-1][self.positionY] in ["OK","SAFE"]:
            self.positionX-=1
            return Agent.Action.FORWARD
        elif self.direction == "U" and self.board[self.positionX][self.positionY+1] in ["OK","SAFE"]:
            self.positionY+=1
            return Agent.Action.FORWARD
        elif self.direction == "D" and self.board[self.positionX][self.positionY-1] in ["OK","SAFE"]:
            self.positionY-=1
            return Agent.Action.FORWARD
        elif self.positionX == 0 and self.positionY == 0 and self.board[self.positionX+1][self.positionY]=="DANGER" and self.board[self.positionX][self.positionY+1]=="DANGER":
            return Agent.Action.CLIMB
        else:
            self.lastAction = "backtrack"
            self.changeDirection()
            return Agent.Action.TURN_LEFT
    
    def changeDirection(self):
        if self.direction == "R":
            self.direction = "U"
        elif self.direction == "L":
            self.direction ="D"
        elif self.direction == "D":
            self.direction == "R"
        elif self.direction == "U":
            self.direction = "L"
            
    def checkSurrounding(self):
        print(self.board[self.positionX+1][self.positionY], self.board[self.positionX][self.positionY+1])
        if self.positionX == 0 and self.positionY == 0 and self.board[self.positionX+1][self.positionY] in ["DANGER","SAFE"] and self.board[self.positionX][self.positionY+1] in ["DANGER", "SAFE"]:
            return Agent.Action.CLIMB
        elif self.board[self.positionX][self.positionY-1] == "OK":
            if self.direction == "L":
                self.changeDirection()
                return Agent.Action.TURN_LEFT
            elif self.direction == "R":
                self.direction == "D"
                return Agent.Action.TURN_RIGHT
            elif self.direction == "D":
                self.lastAction = ""
                print(self.board[self.positionX+1][self.positionY], self.board[self.positionX][self.positionY])
                self.board[self.positionX][self.positionY]="SAFE"
                return self.moveForward()
            else:
                self.changeDirection()
                return Agent.Action.TURN_LEFT
        elif self.board[self.positionX][self.positionY+1] == "OK":
            if self.direction == "R":
                self.changeDirection()
                return Agent.Action.TURN_LEFT 
            elif self.direction == "L":
                self.direction = "U"
                return Agent.Action.TURN_RIGHT
            elif self.direction == "U":
                self.lastAction = ""
                print(self.board[self.positionX+1][self.positionY], self.board[self.positionX][self.positionY])
                self.board[self.positionX][self.positionY]="SAFE"
                return self.moveForward()
            else:
                self.changeDirection()
                return Agent.Action.TURN_LEFT
        else:
            return self.moveForward()
        
        
    
            
            
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================