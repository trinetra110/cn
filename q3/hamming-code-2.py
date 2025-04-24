def calcRB(m):
    # formula: 2^r >= m + r + 1 
    for i in range(m):
        if(2**i >= m + i + 1):
            return i

def posRB(data, r):
    j = 0
    k = 1
    m = len(data)
    res = ''
    for i in range(1, m + r + 1):
        if(i == 2**j):
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1
    return res[::-1]

def calcPB(arr, r):
    n = len(arr)
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            if(j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])
        arr = arr[:n - (2**i)] + str(val) + arr[n - (2**i) + 1:]
    return arr

def detect_error(codeword, r):
    n = len(codeword)
    error_pos = 0
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            if(j & (2**i) == (2**i)):
                val = val ^ int(codeword[-1 * j])
        if val != 0:
            error_pos += (2**i)
    
    return error_pos 

def correct_error(codeword, error_pos):
    if error_pos == 0:
        return codeword  

    error_pos -= 1 
    codeword = list(codeword)
    codeword.reverse()
    if codeword[error_pos] == '0':
        codeword[error_pos] = '1'
    else:
        codeword[error_pos] = '0'
    codeword.reverse()
    return ''.join(codeword)

def removePB(codeword, r):
    n = len(codeword)
    result = ""
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0: 
            result += codeword[-i]
    return result[::-1]

data = input("Enter the data to be transmitted (binary): ")
m = len(data)
r = calcRB(m)
arr = posRB(data, r)
arr = calcPB(arr, r)
print("Data transferred is " + arr)

received_codeword = input("Enter the received codeword (binary): ")
error_pos = detect_error(received_codeword, r)

if error_pos == 0:
    print("No error detected")
else:
    print(f"Error detected at position {error_pos}")
    corrected_codeword = correct_error(received_codeword, error_pos)
    final_dataword = removePB(corrected_codeword, r)
    print(f"Corrected dataword (without parity bits) is: {final_dataword}")