import ipaddress
import socket

# criar um objeto socket
udpConnection = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientBoard = None
clientShips = {"1": 5, "2": 4, "3": 3, "4": 2}
clientHitsCounter = 5 + 4 + 3 + 2

# Método para testar conexão
def testIp(destiny):
    ip = destiny[0]
    # testar ip

    ip = ipaddress.ip_address(ip)

    return ip != None


# Ler dados do usuário
def readConnectionData():

    while True:
        # destiny = input(
        #     "Informe o ip e a porta da seguinte forma: <ip> <porta>\n"
        # ).split(" ")
        # DEBUG
        destiny = ["localhost", 3333]

        if destiny[0] == "localhost":
            hostname = socket.gethostname()
            destiny[0] = socket.gethostbyname(hostname)

        if len(destiny) == 2 and testIp(destiny):
            break
        else:
            print(destiny)
            print("Ip ou porta inválida! Tente de novo: ")

    return destiny


def createBoard():
    global clientBoard

    with open('./boards/client-board.txt', "r") as clientBoardFile:
        clientBoard = [
            [int(num) for num in line.rstrip().split(' ')] for line in clientBoardFile
        ]

def youWinOrLose(msg):
    global clientHitsCounter

    resp = False
    msg = msg.split(" ")
    serverCounter = int(msg[2])

    if serverCounter == 0:
        resp = True
        print("Parabéns vocẽ ganhou :D")

    elif clientHitsCounter == 0:
        resp = True
        print("Que pena você perdeu (T_T)")

    return resp


def getBoardLine(boardLetter):

    boardLine = ord(boardLetter.lower()) - 97

    # Testar se a posição não é válida
    if not (boardLine >= 0 and boardLine <= 9):
        boardLine = -1

    return boardLine


def countShot(line, column):
    global clientHitsCounter
    global clientBoard

    # tentar pegar posição de algum navio
    position = clientBoard[line][column]

    if position == -1:
        response = "Errou -1"
    else:
        response = "Acertou " + str(clientBoard[line][column])
        clientBoard[line][column] = -1
        clientHitsCounter = clientHitsCounter - 1

    return response


def validateShot(msg):

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

    return response + " " + str(clientHitsCounter)


def formatResponse(subject, response):
    global clientHitsCounter

    temp = response.split(" ")
    print("teeeeeeeeeeemmm")
    print(temp)

    if temp[0] == "Acertou":
        formatedResponse = "\n{}: \n{} o tiro \nTipo navio acertado: {} \nTiro do Server: {} {} \
            \nFaltam {} acertos".format(
            subject, temp[0], temp[1], temp[3], temp[4], temp[2]
        )
    else:
        formatedResponse = "\n{}: \n{} o tiro \nTiro do Server: {} {} \
        \nFaltam {} acertos".format(
            subject, temp[0], temp[3], temp[4], temp[2]
        )

    return formatedResponse


def main():
    global udpConnection

    # Receber dados para a conexao
    destiny = readConnectionData()
    host = destiny[0]
    port = int(destiny[1])

    # Conectar ao servidor
    udpConnection.connect((host, port))

    # Flag caso o usuário queira sair do programa
    flagToExit = False
    
    # Inicializar tabuleiro
    createBoard()

    # Status iniciais
    statusFire = "Errou"
    typeShipHitted = "-1"

    # Fluxo do jogo
    while not flagToExit:

        print(
            "\nEntre com um código: "
            + "\nJogar - J <letra> <numero>"
            + "\nSair da aplicação - E"
        )

        try:
            msg = input()
            msg = msg.split(" ")

            # msg -> J <Errou|Acertou> <tipo-navio> <letra> <numero>
            msg = (
                msg[0]
                + " "
                + statusFire
                + " "
                + typeShipHitted
                + " "
                + " ".join(msg[1:])
            )
        except EOFError:
            print(msg)

        # testar se e' uma flag de saida
        if msg[0] == "E":
            flagToExit = True
            print("Obrigado e até logo :)")
            continue

        elif msg[0] == "J":
            msg = msg.encode("UTF-8")
            udpConnection.sendto(msg, (host, port))

            # Recuperar mensagem do servidor
            msg, client = udpConnection.recvfrom(1024)

            msg = msg.decode("utf-8")

            # Formatar e mostrar status do tiro do CLIENT
            response = formatResponse("CLIENT", msg)
            print(response)

            # Se ganhou ou perdeu, saia do loop
            if youWinOrLose(msg):
                flagToExit = True
                continue

            # Formatar e mostrar status do tiro do SERVER
            response = validateShot(msg.split(" "))
            response = formatResponse("SERVER", msg)
            print(response)

        else:
            print("\nCódigo inválido")


main()