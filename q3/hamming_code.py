# 3. Write Python program to implement Hamming code.
"""SAMPLE
ENCODE
Enter your choice: 1
Enter the data: 11001011
Hamming code: 1 1 0 0 0 1 0 1 1 1 1 0 

DECODE
Enter your choice: 2
Enter the hamming code: 100110100101
Data: 1 0 0 0 0 1 0 1 
"""

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
            
def encode():
    
    a=input("Enter the data: ")
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
    for i in a[::-1]:
        print(i,end=" ")
        
def decode():

    b=input("Enter the hamming code: ")
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

    #for i in range(r):
    #    s.append(hamming_code(b,i,n))

    d=0
    for i in range(len(s)):
        d+=(s[i]*(2**i))

    if d!=0:
        b[d-1]=1-b[d-1]

    print("Data: ",end="")
    for i in range(n-1,-1,-1):
        if i not in ri:
            print(b[i],end=" ")

def main():
    print("1. Encode\n2. Decode")
    ch=input("Enter your choice: ")
    if ch=='1':
        encode()
    elif ch=='2':
        decode()
    else:
        print("Invalid choice")

if __name__=="__main__":
    main()