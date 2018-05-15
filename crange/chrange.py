import math

def to_chr_index(index,lower=False):

    res = ""
    getchar = lambda y: chr( ord('a' if lower else 'A' ) + y - 1)
    times = math.floor(math.log(index,26))
    
    for i in range(times,0,-1):
        if index <= 26:
            break
        tmp = index // (26 ** i)
        res += getchar(26 if tmp == 0 else tmp )
        index = index - tmp * (26 ** i)
        
    res += getchar( 26 if index==0 else index)

    return res

def to_num_index(index):
    
    sum = 0
    str_index_lower = index.lower()
    length = len(str_index_lower) - 1

    for i in range(length,-1,-1):
        sum += pow( 26,i )*( ord( str_index_lower[length-i] )-ord('a') + 1 )

    return sum

def crange(start,end,step=1):
    
    s = to_num_index(start)
    e = to_num_index(end)

    for i in range(s,e+1,step):
        yield to_chr_index(i)

if __name__ == "__main__":
    for x in crange("a","z",2):
        print(x)

