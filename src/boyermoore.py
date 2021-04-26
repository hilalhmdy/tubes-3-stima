import re

def getRawString(text):
    strRaw = repr(text)
    strRaw2 = ''
    for i in range (1, len(strRaw)-1,1):
        strRaw2 = strRaw2 + strRaw[i]
    return strRaw2

def findLastOccurence(pattern, x):
    n = len(pattern)
    for i in range (n-1,-1,-1):
        # Apply regex
        textSource = pattern[i]
        search = getRawString(x)
        pattern1 = re.compile(search, re.IGNORECASE)
        match = pattern1.findall(textSource)
        
        # IF pattern[i]==x
        if (match):
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
        # Apply regex
        textSource = pattern[j]
        search = getRawString(text[i])
        pattern1 = re.compile(search, re.IGNORECASE)
        match = pattern1.findall(textSource)

        # IF pattern[j] == text[i]
        if (match):
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
text1 = "aaaatUbESaaaa"
pattern1 = "tubes"
idx = bmMatch(text,pattern)
print(idx)
print(bmMatch(text1,pattern1))