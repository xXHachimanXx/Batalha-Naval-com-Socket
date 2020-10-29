import ipaddress
import socket 

# criar um objeto socket
udpConnection = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Método para testar conexão
def testIp(destiny):    
    ip = destiny[0]
    # testar ip
    
    ip = ipaddress.ip_address(ip)                
    
    return (ip != None)
    
# Ler dados do usuário
def readClientData():
    
    while True:
        destiny = input("Informe o ip e a porta da seguinte forma: <ip> <porta>\n").split(' ')        
        
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
    resp = False
    
    if msg == "Ganhou":
        resp = True
        print("Parabéns vocẽ ganhou :D")
        
    elif msg == "Perdeu":
        resp = True
        print("Que pena você perdeu (T_T)")
    
    return resp

def main():
    global udpConnection
    
    destiny = readClientData()
    
    host = destiny[0]
    port = int(destiny[1])
    
    udpConnection.connect((host, port))
    
    flagToExit = False        
    
    while not flagToExit:
        
        print("\nEntre com um código: " + \
              "\nJogar - J <numero> <letra>" + \
              "\nSair da aplicação - E")
        
        try:
            msg = input()
        except EOFError:
            print(msg)
        
        # testar se e' uma flag de saida
        if msg == "E":
            flagToExit = True
            print('Obrigado e até logo :)')
            continue
        
        elif msg == "J":
            msg = msg.encode('UTF-8')
            udpConnection.sendto(msg, (host, port))
        
            # udpConnection.settimeout(5.0)
            msg, client = udpConnection.recvfrom(1024)
            
            # Se ganhou ou perdeu, saia do loop
            if youWinOrLose(msg):
                flagToExit = True                
        else:
            print("\nCódigo inválido")
        
          


main()