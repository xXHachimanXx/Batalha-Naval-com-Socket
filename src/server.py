from random import randint

from constants import *

def createBoard():
    matrix = []
    
    # Inicializa matriz com -1
    for x in range(SIZE_BOARD):
        for y in range(SIZE_BOARD):
            matrix[x][y] = -1
    
    # Iterar para encaixar todos os navios
    for shipSize in TYPES_OF_SHIPS.values():
        fits = False
        
        # Enquanto nao couber o navio
        while not fits:
            
            insertPosition = randint(0, 9)
            
            if insertPosition + shipSize <= SIZE_BOARD:                
                for target_list in expression_list:
                    pass
            
    
    return None