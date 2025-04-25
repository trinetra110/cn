import socket

def hamming_code(e,i,n):
    j=(2**i)-1
    f=0
    c=0
    while (j<n):
        if(e[j]==1):
            f=1-f
        c+=1
        if(c==2**i):
            c=0
            j+=((2**i)+1)
        else:
            j+=1
            
    return f
            
def h_decode(code):

    b=code.split()
    b=map(int,b)
    b=list(b)

    n=len(b)
    r=0
    
    while(n >= (2**r)-(r+1)):
        r+=1

    r-=1
    
    s=[]
    b=b[::-1]
    ri=[]
    for i in range(r):
        ri.append((2**i)-1)
        s.append(hamming_code(b,i,n))

    d=0
    for i in range(len(s)):
        d+=(s[i]*(2**i))
    
    if d!=0:
        b[d-1]=1-b[d-1]

    st = "Data: "
    for i in range(n-1,-1,-1):
        if i not in ri:
            st += (str(b[i]) + " ")
    
    return st

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

    msg = conn.recv(1024)
    msgf = msg.decode().split(':')
    print(msg.decode())
    code = msgf[1].strip()
    st = h_decode(code)
    print(st)

    conn.close()