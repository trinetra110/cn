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
    for i in q:
        print(i,end=" ")

def encode(ds,c,cl,dsl):
    z=[]
    for i in range(len(ds)-1):
        c.append(0)
        z.append(0)
    z.append(0)
    check=cl
    crc(c,dsl,check,z,ds)

def decode(ds,c,cl,dsl):
    z=[]
    for i in range(len(ds)):
        z.append(0)
    check=cl-dsl+1
    crc(c,dsl,check,z,ds)

def main():
    c=input("Enter codeword: ").split(" ")
    c=map(int,c)
    c=list(c)
    ds=input("Enter divisor: ").split(" ")
    ds=map(int,ds)
    ds=list(ds)

    cl=len(c)
    dsl=len(ds)
    print("1. Encode\n2. Decode")
    ch=input("Enter your choice: ")
    if ch=='1':
        encode(ds,c,cl,dsl)
    elif ch=='2':
        decode(ds,c,cl,dsl)
    else:
        print("Invalid choice")

if __name__=="__main__":
    main()