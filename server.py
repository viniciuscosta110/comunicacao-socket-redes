import socket

class jogo:
    def __init__(self):
        self.letras = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.chances = 5
        self.palavra = []       #Palavra a ser advinhada ex: TESTE
        self.advinhando = []        #Palavra sendo revelada  ex: T..T.
        self.strpalavra = "NULL"
        #chama a função ler palavra
        self.ler_palavra()

    def ler_palavra(self):
        #Esse método é pra ser enviado ao jogador cujo turno é
        #ou seja, fica alternando qual usuário tá enviando a palavra
        self.strpalavra = input("digite a palavra:")

        for i in range(0,len(self.strpalavra)):
            self.palavra.append(self.strpalavra[i])
            
            if(self.palavra[i] == ' '):
                self.advinhando.append(' ')
            else:
                self.advinhando.append('.')

    def letra_repetida(self,letra):
        if letra in self.letras:
            self.letras.remove(letra)
            return False
        return True

    def analisar_jogada(self,letra):
        acertou = False #se acertou a letra atual

        for i in range(0,len(self.palavra)):
            if(self.palavra[i] == letra):
                acertou = True
                self.advinhando[i] = self.palavra[i]

        if('.' not in self.advinhando):
            return True

        if(not acertou):
            self.chances -= 1
          
        return False
                
            

def server(host = 'localhost', port=8082):
    data_payload = 4096 #The maximum amount of data to be received at once
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    # Enable reuse address/port 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (host, port)

    sock.bind(server_address)
    # Listen to clients, argument specifies the max no. of queued connections
    sock.listen(1) 
    client, address = sock.accept()
    #A partir daqui já é jogo

    instancia = jogo()

    while instancia.chances > 0: 
        data = client.recv(data_payload) #sempre um char
        data = data.decode('utf-8')
        flag = True #Se a letra tiver sido repetida, vai ficar false e nao vai computar a jogada
        if(instancia.letra_repetida(data)): #Se True, manda mensagem dizendo que repetiu letra
            message = "Letra repetida\n"
            client.send(message.encode('utf-8'))
            flag = False
        
        if(flag):
            if(instancia.analisar_jogada(data)): #Se retornar True, o cabra acertou a palavra
                print("PALAVRA ADVINHADA")
                message = "PALAVRA ADVINHADA\n"
                client.send(message.encode('utf-8'))
                
                message = instancia.strpalavra #Mando a palavra advinhada
                client.send(message.encode('utf-8'))
                return
        
        print(instancia.advinhando)    
        print("Chances restantes: {}".format(instancia.chances))
        
        if(flag): 
            message = instancia.advinhando
            message = "".join(message)

            client.send(message.encode('utf-8')) 
            
        message = "Chances restantes: {}".format(instancia.chances)
        client.send(message.encode('utf-8'))
    
    message = "\nPalavra não advinhada"
    client.send(message.encode('utf-8'))
    print("Palavra não advinhada")
          
server()