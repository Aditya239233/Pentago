import numpy as np
import random
import copy

from baseEnv import HBDenv
from baseAgent import HBDagent

BOARD_SIZE = 6

class Pentago(HBDenv):
    def __init__(self, size, agents, history_file):

        self.size = size
        self.board = np.zeros((self.size, self.size), dtype = np.int)

        self.done = False
        self.agents = []
        self.winner = 0
        self.agents = agents
        self.file = open(history_file, 'w')
    
        for agent in self.agents:
            self.file.write(agent.__class__.__name__ + ' ')
        self.file.write('\n')
        self.file.write(self.logging() + '\n')

    def game_step(self):
        for i, agent in enumerate(self.agents):
            action = agent.step(copy.deepcopy(self.board))
            self.agent_step(i+1, action)
            if self.done == True:
                if self.winner:
                    self.file.write(f" {self.agents[self.winner-1].__class__.__name__} wins")
                else:
                    self.file.write("Its a draw &__& ")
                break

    def agent_step(self, agentID, action):
        x, y, quadrant, direction = action
        if not self.checkValidMove(x, y, quadrant, direction): 
            #If the bot makes an invalid move, a random move is generated
            while True: 
                x, y = random.randint(0,5), random.randint(0,5)
                quadrant = random.randint(1,4)
                direction = random.choice([1, -1])
                if self.checkValidMove(x, y, quadrant, direction):
                    break

        self.addPiece(x, y, agentID)
        self.rotate(quadrant, direction)

        self.file.write(self.logging() + '\n')
        self.GameOver()

    def addPiece(self, x, y, value):
        '''
            x is the X coordinate and y is the Y coordinate on the board.
    
            Value is the value to be placed on that position. The bot does not have to assaign any value here. It's turn based
        '''
        self.board[x,y] = value
    
    def rotate(self, quadrant, direction):
        '''
        quadrant:
            The board is divided into 4 quadrants - 1,2,3,4
            Each quadrant has 9 blocks annd is arranged in the manner: [1,2
                                                                        3,4]
        direction:
            It is the direction you want to rotate that particular quadrant
            1 = anticlockwise, -1 = clockwise
        '''
        if quadrant == 1:
            self.board[:3, :3] = np.rot90(self.board[:3, :3], direction)
        elif quadrant == 2:
            self.board[:3, 3:] = np.rot90(self.board[:3, 3:], direction)
        elif quadrant == 3:
            self.board[3:, :3] = np.rot90(self.board[3:, :3], direction)
        elif quadrant ==4:
            self.board[3:, 3:] = np.rot90(self.board[3:, 3:], direction)
    
    def checkValidMove(self, x, y, quadrant, direction):
        '''
            Checks whether the move suggested by the bot is valid or not
        '''
        if x < self.size and y < self.size and x >= 0 and y >= 0  and not self.board[x][y]:
            if quadrant in [1, 2, 3, 4] and direction in [1, -1]:
                return True
        return False

    def GameOver(self):
        '''
            Checks whether the game is over or not. 
            It also specifies the winner of the game so that the result can be later stored in history
        '''
        if (len(set(np.diag(self.board)[:-1])) == 1 and np.diag(self.board)[0] != 0) or (len(set(np.diag(self.board)[1:])) == 1 and np.diag(self.board)[1] != 0):
            if np.diag(self.board)[1] == 1:
                self.winner = 1
                self.done = True

            elif np.diag(self.board)[1] == 2:
                self.winner = 2
                self.done = True
            return
        
        if (len(set(np.diag(np.fliplr(self.board))[:-1])) == 1 and np.diag(np.fliplr(self.board))[0] != 0) or (len(set(np.diag(np.fliplr(self.board))[1:])) == 1 and np.diag(self.board)[1] != 0):
            if np.diag(np.fliplr(self.board))[1] == 1:
                self.winner = 1
                self.done = True
            elif np.diag(np.fliplr(self.board))[1] == 2:
                self.winner = 2
                self.done = True
            return
        
        # Checking for other diagonals
        if (len(set(np.diag(self.board[:5, :5])[:])) == 1 and np.diag(self.board)[0] != 0):
            if np.diag(self.board[:5,:5])[1] == 1:
                self.winner = 1
                self.done = True

            elif np.diag(self.board)[1] == 2:
                self.winner = 2
                self.done = True
            return

        if (len(set(np.diag(self.board[1:, :5])[:])) == 1 and np.diag(self.board[1:, :5])[0] != 0):
            if np.diag(self.board[1:,:5])[1] == 1:
                self.winner = 1
                self.done = True

            elif np.diag(self.board[1:,:5])[1] == 2:
                self.winner = 2
                self.done = True
            return

        if (len(set(np.diag(np.fliplr(self.board[:5, 1:]))[:-1])) == 1 and np.diag(np.fliplr(self.board[:5, 1:]))[0] != 0):
            if np.diag(np.fliplr(self.board[:5, 1:]))[1] == 1:
                self.winner = 1
                self.done = True
            elif np.diag(np.fliplr(self.board[:5, 1:]))[1] == 2:
                self.winner = 2
                self.done = True
            return 

        if (len(set(np.diag(np.fliplr(self.board[1:, 1:]))[:-1])) == 1 and np.diag(np.fliplr(self.board[1:, 1:]))[0] != 0):
            if np.diag(np.fliplr(self.board[1:, 1:]))[1] == 1:
                self.winner = 1
                self.done = True
            elif np.diag(np.fliplr(self.board[1:, 1:]))[1] == 2:
                self.winner = 2
                self.done = True
            return 


        for i in range(6):
            if (len(set(self.board[i][:-1])) == 1 or len(set(self.board[i][1:])) == 1) and self.board[i][1] != 0:
                if self.board[i][1] == 1:
                    self.done = True
                    self.winner = 1
                    return

                elif self.board[i][1] == 2:
                    self.done = True
                    self.winner = 2
                    return

            if (len(set(self.board[:, i][:-1])) == 1 or len(set(self.board[:, i][1:])) == 1) and self.board[:, i][1] != 0:
                if self.board[:, i][1] == 1:
                    self.done = True
                    self.winner = 1
                    return
                                        
                elif self.board[:, i][1] == 2:
                    self.done = True
                    self.winner = 2
                    return

        if 0 not in self.board:
            self.done = True
            self.winner = None
            return
    
    def logging(self):
        '''
            logs the entire state of the game
        '''
        serialString =""
        for row in self.board:
            for value in row:
                serialString += str(value)
                serialString += ','
            #serialString += '\n'
        serialString = serialString[:-1]
        return serialString

class randomAgent(HBDagent):
    def __init__(self):
        pass
    def step(self, state):
        '''
            Input:
                state - It's a 2D array of the entire board at the current time

            This function should return :
                x - the x coordinate on the board
                y - the y coordinate on the board
                quadrant - the quadrant that the user wants to rotate 
                            This is divided into 4 parts 
                            1 - board[:3, :3]
                            2 - board[:3, 3:]
                            3 - board[3:, :3]
                            4 - board[3:, 3:]
                direction -  this is the direction in which the quadrant should rotate in
                            1 - anticlockwise
                           -1 - clockwise
        '''
        x, y = random.randint(0,5), random.randint(0,5)
        quadrant = random.randint(1,4)
        direction = random.choice([1, -1])

        return [x, y, quadrant, direction]

if __name__ == "__main__":
    env = Pentago(BOARD_SIZE,[randomAgent(), randomAgent()], 'history.hbd')
    while not env.done:
        env.game_step()
