import boyermoore
import re

KataPenting = []
dbReminder = []

def removeSpaceStartEnd(inputString):
    if (inputString[len(inputString)-1]!='' and inputString[0]!=''):
        return inputString
    else :
        result = ''
        for i in range (1, len(inputString)-1,1):
            result = result + inputString[i]
        return result

def readFileTXT(sourceFile):
    file1 = open(sourceFile,"r+")
    listOfRows = file1.read().splitlines()
    file1.close()
    return listOfRows

def addReminer(input):
    print("addreminer")
    global dbReminder
    # Jenis reminder
    tipeReminder = ''
    for kata in KataPenting:
        if (boyermoore.bmMatch(input,kata) != -1):
            tipeReminder = kata
    print(tipeReminder)
    # Nama matkul
    # Format matkul : XXYYYY, IF2211, if2211
    patternMatkul = re.compile(r'[a-zA-Z]{2}[0-9]{4}')
    matchMatkul = patternMatkul.findall(input)
    NamaMatkul = matchMatkul[0]
    print(NamaMatkul)
    # Tanggal
    # Format tanggal : 14/02/2021 ATAU 14-02-2021 ATAU 14 April 2021
    textSource = input
    patternTanggal = re.compile(r'[0-9]{2}[/-]?\s?\w+[/-]?\s?[0-9]{4}')
    matchTanggal = patternTanggal.findall(textSource)
    TanggalReminder = matchTanggal[0]
    print(TanggalReminder)
    # Topik (BELUM)
    namaTopik = "XXXX"
    dbReminder.append([TanggalReminder, NamaMatkul, tipeReminder, namaTopik])
    print("[TASK BERHASIL DICATAT]")
    print("(ID:{0}) {1}-{2}-{3}-{4}".format(str(len(dbReminder)),TanggalReminder,NamaMatkul,tipeReminder,namaTopik))




# file1 = open("KataPenting.txt","r+")
# KataPenting = file1.read().splitlines()
# file1.close()
KataPenting =  readFileTXT("KataPenting.txt")
print(KataPenting)
contohinput = "Tubes IF2211 String Matching pada 14 April 2021"
dbReminder.append(["13/03/2021","IF2210","TUBES","Tugas2an"])

addReminer(contohinput)
print(dbReminder)