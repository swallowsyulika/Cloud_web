import sqlite3
import socket

db_name = "bank.db"
TABLENAME = "CLIENT"

conn = sqlite3.connect(db_name)
c = conn.cursor()

# create table
c.execute(f"""create table if not exists {TABLENAME} (
            account text,
            password text,
            money integer)""")

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())
conn.commit()

def insert_data(account, password, money=-1000):
    c.execute(f"SELECT account FROM {TABLENAME}")
    res = [i[0] for i in c.fetchall()]
    
    if account in res:
        return False
    else:
        c.execute(f"INSERT INTO {TABLENAME} VALUES ('{account}', '{password}', {money})")
        conn.commit()
        return True

def update_data(account, password, money):
    c.execute(f"SELECT account FROM {TABLENAME} WHERE account = '{account}' AND password = '{password}'")
    res = [i[0] for i in c.fetchall()]
    
    if account in res:
        c.execute(f"UPDATE {TABLENAME} SET money = {money} WHERE account = '{account}'")
        conn.commit()
        return True
    else:
        return False

def show_all_data():
    c.execute(f"SELECT * FROM {TABLENAME}")
    res = c.fetchall()
    print(f"----------TABLE {TABLENAME}----------")
    for ele in res:
        print(ele)
    conn.commit()

def get_money(account, password):
    c.execute(f"SELECT money FROM {TABLENAME} WHERE account = '{account}' and password = '{password}'")
    res = c.fetchone()
    if res is not None:
        return res[0]
    else:
        return False

def customized_sql(sql):
    c.execute(sql)
    conn.commit()

# insert_data('Root', 'root', 'password', 100)
# show_all_data()
# update_data('david', 'aalucy', 700)
show_all_data()
# get_money('david', 'lucy')



HOST = '192.168.56.40'
PORT = 9977
KEEP = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)

while KEEP:
    connt, addr = server.accept()
    clientMessage = str(connt.recv(1024), encoding='utf-8')

    print('Client message is:', clientMessage)

    # type 0: create data, 1: show data, 2: updata data
    # example message >>  type:name,account,password
    worktype, data = clientMessage.split(':')
    worktype = int(worktype)
    serverMessage = ""

    if worktype == 0:
        # stop server
        KEEP = False
        serverMessage = 'stop db server.'
        connt.sendall(serverMessage.encode())
        connt.close()

    elif worktype == 1:
        # create new account
        account, password = data.split(",")
        r = insert_data(account, password)
        if r:
            serverMessage = 'Account created.'
        else:
            serverMessage = 'Account name repeated, plz try new account name.'

        show_all_data()

    elif worktype == 2:
        # show money
        account, password = data.split(",")
        r = get_money(account, password)
        if isinstance(r, bool) and r == False:
            serverMessage = 'Account or password not correct, plz try again.'
        else:
            serverMessage = f'{r}'

    elif worktype == 3:
        # update money
        account, password, money = data.split(",")
        r = update_data(account, password, money)
        if r:
            serverMessage = 'Updata successed.'
        else:
            serverMessage = 'Account or password not correct, plz try again.'

    connt.sendall(serverMessage.encode())
    connt.close()

server.close()
conn.close()

