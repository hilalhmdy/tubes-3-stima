def findLastOccurence(pattern, x):
    n = len(pattern)
    for i in range (n-1,-1,-1):
        if (pattern[i] == x):
            return i
    return -1
    

def bmMatch (text, pattern):
    text = text
    pattern = pattern
    nText = len(text)
    nPattern = len(pattern)
    i = nPattern-1
    j = nPattern-1

    # No match jika nPattern > nText
    if (nPattern-1 > nText-1):
        return -1
    
    while (i <= nText-1):
        if (pattern[j] == text[i]):
            if (j==0):
                return i # match
            else:
                # Looking glass technique
                i = i - 1
                j = j - 1
        else:
            # Character jump technique
            lo = findLastOccurence(pattern, text[i])
            i = i + nPattern - min(j,lo+1)
            j = nPattern - 1
    return -1


text = "abacaabadcabacabaabb"
pattern = "abacab"
idx = bmMatch(text,pattern)
print(idx)