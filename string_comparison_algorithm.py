def preKMP(x):
    kmpNext = [0]*(len(x) +1)
    i = 0
    j = -1
    kmpNext[0] = -1
    while(i < len(x) -1):
        while j > -1 and x[i] != x[j]:
            j = kmpNext[j]
        i +=1 
        j += 1
        if x[i] == x[j]:
            kmpNext[i] = kmpNext[j]
        else: kmpNext[i] = j
    return kmpNext
    
def search(x,y,listCity):
    kmpNext = preKMP(x)
    i = 0
    m = 0
    while m <= len(y) - len(x):
        if x[i] == y[m+i]:
            i += 1
            if i == len(x):
                listCity.append(x)
                m += i - kmpNext[i]
                i = kmpNext[i]
        else:
            m += i - kmpNext[i]
            i = 0
    return 0
