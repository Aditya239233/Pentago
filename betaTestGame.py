import pygame
import numpy as np

pygame.init()

size = (6,6)
window_size = 60
tile_size = 10

def drawCircle(gameDisplay,pos, value):
    if value == 0:
        return
    elif value == 1:
        pygame.draw.circle(gameDisplay, (255,0,0), pos, 15)
    elif value == 2:
        pygame.draw.circle(gameDisplay, (0,255,0), pos, 15)

def drawGrid(gameDisplay, board):
    for x in range(6):
        for y in range(6):
            rect = pygame.Rect(y*window_size, x*window_size,
                               window_size, window_size)
            pygame.draw.rect(gameDisplay, (0,0,0), rect, 1)
            drawCircle(gameDisplay, rect.center, board[x][y])
    draw_line(gameDisplay)

def draw_line(gameDisplay):
    pygame.draw.line(gameDisplay,(212,175,55),(0,180),(600,180), 3)
    pygame.draw.line(gameDisplay,(212,175,55),(180,0),(180,600), 3)

def convertToArray(string):
    array =  list(map(int,string.split(',')))
    array = np.array(array)
    return np.reshape(array, (-1, 6))

def main():
        f = open("history.hbd")
        history = f.readlines()
        f.close()
        gameDisplay=pygame.display.set_mode(tuple([x*window_size for x in size]))
        pygame.display.set_caption("PENTAGO")
        pygame.display.update()
        clock=pygame.time.Clock()
        print(history[0])
        i = 1
        board = convertToArray(history[i])
        while True:
            gameDisplay.fill((255,255,255))
            drawGrid(gameDisplay, board)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and i < len(history) -2:
                    i +=1
                    board = convertToArray(history[i])
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(history[-1])
                    pygame.quit()
                    quit()

            pygame.display.update()
main()