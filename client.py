import socket
def client(host = 'localhost', port=8082): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_address = (host, port)

    sock.connect(server_address)
    try: 
        # Send data 
        while(1):
            message = input("Digite uma letra maiúscula: ")
            print ("Sending %s" % message) 
            sock.sendall(message.encode('utf-8')) 
            # Look for the response 
            amount_received = 0 
            amount_expected = len(message) 

            data = sock.recv(4096)

            if("PALAVRA ADVINHADA" in data.decode('utf-8') or "Palavra não advinhada" in data.decode('utf-8')):
                print (data.decode('utf-8'), "\n")
                break

            print ("Received: %s" % data.decode('utf-8'))

            data = sock.recv(4096)

            if("PALAVRA ADVINHADA" in data.decode('utf-8') or "Palavra não advinhada" in data.decode('utf-8')):
                print (data.decode('utf-8'), "\n")
                break

            print (data.decode('utf-8'), "\n")

    except socket.error as e: 
        print ("Socket error: %s" %str(e)) 
    except Exception as e: 
        print ("Other exception: %s" %str(e)) 
    finally: 
        print ("Obrigado por jogar!") 
        sock.close() 

client()