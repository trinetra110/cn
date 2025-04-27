import socket

def xor(a,b):
    o=[]
    #print("a,b:",a,b)
    for i in range(len(a)):
        o.append(a[i]^b[i])
    #print("o: ",o)
    return o

def crc(c,dsl,check,z,ds):
    q=c[:dsl]
    for i in range(check):
        #print("q:",q)
        if q[0]==1:
            q=xor(q,ds)
        else:
            q=xor(q,z)
        q.pop(0)
        if i<check-1:
            q.append(c[i+dsl])

    print("Remainder/Syndrome:",end=" ")
    flag = 0
    for i in q:
        print(i,end=" ")
        if i==1:
            flag = 1
    
    if flag == 1:
        print("\nDiscarded")
    else:
        print("\nAccepted")

def c_decode(ds,c,cl,dsl):
    z=[]
    for i in range(len(ds)):
        z.append(0)
    check=cl-dsl+1
    crc(c,dsl,check,z,ds)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket is created successfully")

host = socket.gethostname()
name = "Server: "
port = 23456

sock.bind((host, port))
print ("Socket is binded to %s" %(port))

sock.listen(5)
print ("Socket is listening")

while True:
    conn, addr = sock.accept()
    print ('Got connection from', addr )

    while True:
        msg = conn.recv(1024)
        msgf = msg.decode().split(':')
        if len(msgf) == 1 or msgf[1].lower().strip() in ["exit,", ","]:
            print(msgf[0].strip() + " disconnected")
            break
        
        print(msg.decode())
        content = msgf[1].strip()
        codeword = content.split(',')[0].strip()
        divisor = content.split(',')[1].strip()
        
        c=codeword.split()
        c=map(int,c)
        c=list(c)
        ds=divisor.split()
        ds=map(int,ds)
        ds=list(ds)

        cl=len(c)
        dsl=len(ds)
        c_decode(ds,c,cl,dsl)

    conn.close()