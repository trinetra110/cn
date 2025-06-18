# CRC using sockets
""" SAMPLE INPUT
Enter your name: User
Enter codeword: 1 0 0 1
Enter divisor: 1 0 1 1
Remainder/Syndrome: 1 1 0 
"""

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
    st = ""
    for i in q:
        print(i,end=" ")
        st += (str(i) + " ")
    print()    
    
    st = st.strip()
    return st

def c_encode(ds,c,cl,dsl):
    z=[]
    for i in range(len(ds)-1):
        c.append(0)
        z.append(0)
    z.append(0)
    check=cl
    st = crc(c,dsl,check,z,ds)
    return st


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
name = input("Enter your name: ")
port = 23456

s.connect((host, port))

while True:
    codeword = input("Enter codeword: ").strip()
    if codeword.lower().strip() in ['exit','']:
        msg = name + ': ' + codeword + ','
        s.send(msg.encode())
        print("Connection closed")
        break
    
    c=codeword.split()
    c=map(int,c)
    c=list(c)
    divisor = input("Enter divisor: ").strip()
    ds=divisor.split()
    ds=map(int,ds)
    ds=list(ds)

    cl=len(c)
    dsl=len(ds)
    st = c_encode(ds,c,cl,dsl)
    msg = name + ': ' + codeword + ' ' + st + ', ' + divisor
    s.send(msg.encode())

s.close()