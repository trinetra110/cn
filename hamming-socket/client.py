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
            
def h_encode(msg):
    
    a=msg.split(" ")
    a=map(int,a)
    a=list(a)

    k=len(a)
    r=0
    while(k >= (2**r)-(r+1)):
        r+=1
        
    n=k+r

    a=a[::-1]
    ri=[]
    for i in range(r):
        ri.append(2**i)
        
    for i in ri:
        a.insert(i-1,0)

    for i in range(r):
        a[(2**i)-1]=hamming_code(a,i,n)

    print("Hamming code: ",end="")

    st = ""   
    for i in a[::-1]:
        print(i,end=" ")
        st += (str(i) + " ")
    print()

    return st

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
name = input("Enter your name: ")
port = 23456

s.connect((host, port))

while True:
    msg = input(name + ': ')
    if msg.lower().strip() in ['exit','']:
        s.send(msg.encode())
        print("Connection closed")
        break
    
    msg = h_encode(msg)
    msgf = name + ': ' + msg
    s.send(msgf.encode())

s.close()