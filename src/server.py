import socket
from random import randint

from constants import *

serversocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverBoard = []

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

def initServer(port):
    """Método para inicializar o servidor e carrgar dados da database.        

        Parameters
        ----------
        port : int
            A porta a ser escutada pelo servidor.
    """
    global serversocket
    global serverBoard
    
    # pegar nome da maquina local
    host = socket.gethostname()
    
    # conectar e setar tamanho do backlog
    serversocket.bind((host, port))
    
    # setar tabuleiro do servidor
    serverBoard = createBoard()
    
    print("Servidor pronto para jogar!\n")
    
def checkInput(msg):
    """Função para checar entrada do client.

        Parameters
        ----------
        msg : str
            Mensagem do client.
            
        Returns
        -------
        boolean
           Validez da mensagem
    """
    return (
        len(msg) == 3 and
        (msg[0] == 'J')
    )

def consoleWarning(msg, success, address):
    """Método para mostrar a situação da operação.

        Parameters
        ----------
        msg : str
            Mensagem do client.
        success : boolean
            Flag de sucesso/fracasso da operação.
        client : socket
            Objeto que representa o client da operação.
    """
    successFlag = "Sucesso"
    
    if not success:        
        successFlag = "Fracasso"
        
    print(
        "Client: " + address[0] + ":" + str(address[1]) +
        "\nMensagem: " + str(msg) +
        "\nStatus: " + successFlag + "\n"        
    )  

def main():
    print("Bem-vindo à Batalha Naval com Socket!")
    port = int(input("Digite a porta a ser escutada pelo servidor para inicializá-lo: "))
    
    initServer(port)

    while True:
        global serverBoard
        global serversocket
        success = False
        
        msg, client = serversocket.recvfrom(1024)        
        msg = msg.decode('utf-8').split(' ')
        
        if(checkInput(msg)):
            
            # cadastro
            if msg[0] == 'J':
                print("Mensagem recebida!")
                success = True
                consoleWarning(msg, success, client)
                # if shotStatus ? 
                serversocket.sendto("Status tiro".encode('utf-8'), client)
        else:            
            consoleWarning(msg, success, client)
            serversocket.sendto(
                "Server - Erro: Entrada de dados inválida!".encode("utf-8"),
                client
            )

    # Fechar conexao
    serversocket.close()

main()