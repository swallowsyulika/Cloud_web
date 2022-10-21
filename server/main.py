import socket
SERVERHOST = '127.0.0.1'
SERVERPORT = 8822
CLIENTHOST = '127.0.0.1'
CLIENTPORT = 9977
KEEP = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVERHOST, SERVERPORT))
server.listen(10)

while KEEP:
    conn, addr = server.accept()
    clientMessageFromWeb = str(conn.recv(1024), encoding='utf-8')

    print('Client message is:', clientMessageFromWeb)

    worktype, data = clientMessageFromWeb.split(":")
    worktype = int(worktype)


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((CLIENTHOST, CLIENTPORT))

    money = None

    if worktype == 0:
        # stop server
        KEEP = False
        clientMessageToDB = "0:"
    elif worktype == 1:
        # create account
        print(f"now do : {worktype}")
        account, password = data.split(',')

        clientMessageToDB = f"1:{account},{password}"
        client.sendall(clientMessageToDB.encode())


    elif worktype == 2:
        print(f"now do : {worktype}")

        account, password = data.split(',')
        clientMessageToDB = f"2:{account},{password}"
        client.sendall(clientMessageToDB.encode())


    elif worktype == 3:
        print(f"now do : {worktype}")

        account, password = data.split(',')
        clientMessageToDB = f"2:{account},{password}"
        
        client.sendall(clientMessageToDB.encode())
        serverMessageFromDB = str(client.recv(1024), encoding='utf-8')
        money = serverMessageFromDB
        client.close()



        print("now do 3")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CLIENTHOST, CLIENTPORT))
        if money == "Account or password not correct, plz try again.":
            clientMessageToDB = f"2:{account},{password}"
            client.sendall(clientMessageToDB.encode())
        else:
            clientMessageToDB = f"3:{account},{password},{int(money)+100}"
            client.sendall(clientMessageToDB.encode())


    serverMessageFromDB = str(client.recv(1024), encoding='utf-8')
    print('Server:', serverMessageFromDB)
    client.close()

    if money is not None:
        conn.sendall(money.encode())
    else:
        conn.sendall(serverMessageFromDB.encode())
    conn.close()

server.close()
