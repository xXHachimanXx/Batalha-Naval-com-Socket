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


def countShot(msg):
    global clientBoard
    msg = msg.split()


def formatServerResponse(response):
    global clientHitsCounter

    temp = response.split(" ")
    print("teeeeeeeeeeemmm")
    print(temp)

    if temp[0] == "Acertou":
        formatedResponse = "\n{} \nTipo navio acertado: {} \nTiro do Server: {} {} \
            \nFaltam {} acertos".format(
            temp[0], temp[1], temp[3], temp[4], temp[2]
        )
    else:
        formatedResponse = "\n{} \nTiro do Server: {} {} \
        \nFaltam {} acertos".format(
            temp[0], temp[3], temp[4], temp[2]
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

            countShot(msg)

            response = formatServerResponse(msg.decode("utf-8"))
            print(response)

            # Se ganhou ou perdeu, saia do loop
            if youWinOrLose(msg):
                flagToExit = True
        else:
            print("\nCódigo inválido")


main()