import socket
from random import randint

from constants import *

serversocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverBoard = None
serverHitsCounter = 5 + 4 + 3 + 2

serverShips = {"1": 5, "2": 4, "3": 3, "4": 2}


def createBoard():
    """Método para inicializar o tabuleiro do server.

    Returns
    ----------
    matrix : Matrix
        Matriz do tabuleiro do servidor.
    """
    
    matrix = None

    # Inicializa matriz com -1
    matrix = [[-1 for x in range(SIZE_BOARD)] for y in range(SIZE_BOARD)]

    # Iterar para encaixar todos os navios
    for ship in TYPES_OF_SHIPS:
        fits = False

        # Enquanto nao couber o navio
        while not fits:

            insertPositionX = randint(0, 9)
            insertPositionY = randint(0, 9)

            # Testar se nao ultrapassa o tabuleiro
            if (
                insertPositionX + TYPES_OF_SHIPS[ship] <= SIZE_BOARD
                and insertPositionY + TYPES_OF_SHIPS[ship] <= SIZE_BOARD
            ):

                # Testar se o espaço nao esta ocupado
                columnOccupied = False
                for x in range(TYPES_OF_SHIPS[ship]):
                    if not matrix[x + insertPositionX][insertPositionY] == -1:
                        columnOccupied = True
                        break
                # Testar se o espaço nao esta ocupado
                lineOccupied = False
                for y in range(TYPES_OF_SHIPS[ship]):
                    if not matrix[insertPositionX][y + insertPositionY] == -1:
                        lineOccupied = True
                        break

                # Se couber, insira na matriz
                if not lineOccupied:
                    for y in range(TYPES_OF_SHIPS[ship]):
                        matrix[insertPositionX][y] = ship
                    fits = True
                elif not columnOccupied:
                    for x in range(TYPES_OF_SHIPS[ship]):
                        matrix[x][insertPositionY] = ship
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
    return len(msg) == 5 and (msg[0] == "J")


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
        "Client: "
        + address[0]
        + ":"
        + str(address[1])
        + "\nJogada: "
        + str(msg)
        + "\nStatus: "
        + successFlag
        + "\n"
    )


def getBoardLine(boardLetter):        
    """Converte coordenada do tabuleiro de letra para inteiro.

    Parameters
    ----------
    boardLetter : str
        Letra do tabuleiro.

    Returns
    -------
    boardLine : int
        Número da linha do tabuleiro.
    """

    boardLine = ord(boardLetter.lower()) - 97

    # Testar se a posição não é válida
    if not (boardLine >= 0 and boardLine <= 9):
        boardLine = -1

    return boardLine


def countShot(line, column):
    """Contabiliza tiro.

    Parameters
    ----------
    line : int
        Linha do tabuleiro.
    column : int
        Coluna do tabuleiro

    Returns
    -------
    response : str
        Resposta formatada do tiro contabilizado.
    """
    
    global serverHitsCounter
    global serverBoard

    # tentar pegar posição de algum navio
    position = serverBoard[line][column]

    if position == -1:
        response = "Errou -1"
    else:
        response = "Acertou " + str(serverBoard[line][column])
        serverBoard[line][column] = -1
        serverHitsCounter = serverHitsCounter - 1

    return response


def validateShot(msg):
    """Valida tiro dado e retorna uma resposta formatada.

    Parameters
    ----------
    msg : str
        Mensagem do client.

    Returns
    -------
    response : str
        Resposta formatada.
    """

    # Pegar linha e coluna do tabuleiro
    line = msg[3]  # linha
    column = msg[4]  # coluna

    response = ""

    # Testar se linha é uma letra e se a coluna é um numero
    if line.isalpha() and column.isnumeric():

        # transformar letra em um índice
        line = getBoardLine(line)
        column = int(column)

        # Validar indices linha e coluna
        if line >= 0 and (column >= 0 and column <= 9):
            response += countShot(line, column)
        else:
            response += "Errou -1"
    else:
        response += "Errou -1"

    return response + " " + str(serverHitsCounter)


def shot():
    """Gerar coordenadas do tiro aleatóriamente.

    Returns
    -------
    shotCoordinate : str
        Coordenadas do tiro.
    """
    line = randint(0, 9)
    column = randint(0, 9)

    shotCoordinate = chr(line + 97).upper() + " " + str(column)
    
    return shotCoordinate


def main():
    """Função principal.
    """
    print("Bem-vindo à Batalha Naval com Socket!")
    port = int(
        input("Digite a porta a ser escutada pelo servidor para inicializá-lo: ")
    )

    # # DEBUG
    # port = 3333

    initServer(port)

    global serverBoard

    while True:
        global serversocket
        global serverHitsCounter
        success = False

        msg, client = serversocket.recvfrom(1024)
        msg = msg.decode("utf-8").split(" ")

        if checkInput(msg):

            # cadastro
            if msg[0] == "J":
                print("Mensagem recebida!")
                success = True
                consoleWarning(msg, success, client)
                response = validateShot(msg)
                response += " " + shot()

                serversocket.sendto(response.encode("utf-8"), client)
        else:
            consoleWarning(msg, success, client)
            serversocket.sendto(
                "Server - Erro: Entrada de dados inválida!".encode("utf-8"), client
            )

    # Fechar conexao
    serversocket.close()


if __name__ == "__main__":
    main()