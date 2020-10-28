from random import randint

from constants import *

def createBoard():
    matrix = []
    
    # Inicializa matriz com -1
    for x in range(SIZE_BOARD):
        for y in range(SIZE_BOARD):
            matrix[x][y] = -1
    
    # Iterar para encaixar todos os navios    
    for ship, shipSize in TYPES_OF_SHIPS:
        fits = False
        
        # Enquanto nao couber o navio
        while not fits:
            
            insertPositionX = randint(0, 9)
            insertPositionY = randint(0, 9)
            
            # Testar se nao ultrapassa o tabuleiro
            if insertPositionX + shipSize <= SIZE_BOARD and \
               insertPositionY + shipSize <= SIZE_BOARD:
                   
                # Testar se o espaço nao esta ocupado
                columnOccupied = False
                for x in range(shipSize):
                    if not matrix[x + insertPositionX][insertPositionY] == -1:
                        columnOccupied = True
                        break
                # Testar se o espaço nao esta ocupado
                lineOccupied = False
                for y in range(shipSize):
                    if not matrix[insertPositionX][y + insertPositionY] == -1:
                        lineOccupied = True
                        break
                
                # Se couber, insira na matriz
                if not lineOccupied:
                    for x in range(insertPositionX):
                        for y in range(insertPositionY):
                            matrix[x][y] = ship
                    fits = True
                elif not columnOccupied:
                    for x in range(insertPositionX):
                        for y in range(insertPositionY):
                            matrix[x][y] = ship
                    fits = True
                    
    return matrix