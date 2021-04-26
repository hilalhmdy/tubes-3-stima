import boyermoore
import re
import datetime
#import timedelta
from datetime import timedelta

KataPenting = []
dbReminder = []
listAngka = ["Nol","Satu","Dua","Tiga","Empat","Lima","Enam","Tujuh","Delapan","Sembilan"]
listBulan = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
periodeWaktu = ["antara", "sampai", "minggu ke depan","hari ke depan","hari ini"]

def findQueueMonth(bulan):
    n = len(listBulan)
    for i in range (n):
        # Apply regex
        textSource = listBulan[i]
        search = boyermoore.getRawString(bulan)
        pattern1 = re.compile(search, re.IGNORECASE)
        match = pattern1.findall(textSource)
        if (match):
            if (i>9):
                return str(i+1)
            else:
                return "0"+str(i+1)

def textToAngka(hari):
    n = len(listAngka)
    for i in range (n):
        # Apply regex
        textSource = listAngka[i]
        search = boyermoore.getRawString(hari)
        pattern1 = re.compile(search, re.IGNORECASE)
        match = pattern1.findall(textSource)
        if (match):
            return i


def removeSpaceStartEnd(inputString):
    if (inputString[len(inputString)-1]!=' ' and inputString[0]!=' '):
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

def normalizeDatePattern(tanggal):
    # patternTanggal = re.compile(r'[0-9]{1,2}[/][0-9]{1,2}[/][0-9]{4}')
    # matchTanggal = patternTanggal.findall(tanggal)
    # if(matchTanggal):
    #     return tanggal
    patternTanggal = re.compile(r'[0-9]{1,2}[-][0-9]{1,2}[-][0-9]{4}')
    matchTanggal = patternTanggal.findall(tanggal)
    if(matchTanggal):
        resultTanggal = re.sub("-", "/", tanggal)
        return resultTanggal
    patternTanggal = re.compile(r'[0-9]{1,2}\s\w+\s[0-9]{4}')
    matchTanggal = patternTanggal.findall(tanggal)
    if(matchTanggal):
        matchBulan = re.findall(r'\s\w+\s',tanggal)
        matchBulan[0] = removeSpaceStartEnd(matchBulan[0])
        bulan = matchBulan[0]
        resultTanggal = re.sub("\s", "/", tanggal)
        resultTanggal = re.sub(bulan, findQueueMonth(bulan), resultTanggal)
        return resultTanggal
    return tanggal


# Fungsi 1 (Menambahkan task ke reminder)
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
    TanggalReminder = normalizeDatePattern(TanggalReminder)
    print(TanggalReminder)
    # Topik (BELUM)
    namaTopik = "XXXX"
    # Add it to list of db
    id = len(dbReminder)+1
    statusTask = 0
    dbReminder.append([id,TanggalReminder, NamaMatkul, tipeReminder, namaTopik, statusTask])
    print("[TASK BERHASIL DICATAT]")
    print("(ID:{0}) {1}-{2}-{3}-{4}".format(id,TanggalReminder,NamaMatkul,tipeReminder,namaTopik))

# Fungsi 2
# Menampilkan seluruh task
def showAllTask():
    global dbReminder
    n = len(dbReminder)
    result = []
    # print("[Daftar Deadline]")
    for i in range (n):
        if (dbReminder[i][5]==0):
            currentID = "ID:" + str(dbReminder[i][0])
            # print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
            result.append([currentID, dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]])
    return result

# Berdasarkan periode waktu
def periodeTask(inputText):
    global dbReminder
    # Jenis periode
    tipeperiode = ''
    idxTipePeriode = -1
    for periode in periodeWaktu:
        idxTipePeriode +=1
        if (boyermoore.bmMatch(inputText,periode) != -1):
            tipeperiode = periode
            break
    print(tipeperiode,idxTipePeriode)
    # menentukan jenis periode
    if (idxTipePeriode == 0 or idxTipePeriode == 1):
        print("antara-sampai")
        # Mendapatkan 2 Tanggal
        # Format tanggal : 14/02/2021 ATAU 14-02-2021 ATAU 14 April 2021
        textSource = inputText
        patternTanggal = re.compile(r'[0-9]{2}[/-]?\s?\w+[/-]?\s?[0-9]{4}')
        matchTanggal = patternTanggal.findall(textSource)
        normalPatternTanggal = []
        for i in range (len(matchTanggal)):
            normalPatternTanggal.append(normalizeDatePattern(matchTanggal[i]))
        # print(matchTanggal)
        # print(normalPatternTanggal)
        # date in yyyy/mm/dd format
        y1 = int(normalPatternTanggal[0][6:10])
        m1 = int(normalPatternTanggal[0][3:5])
        d1 = int(normalPatternTanggal[0][0:2])
        y2 = int(normalPatternTanggal[1][6:10])
        m2 = int(normalPatternTanggal[1][3:5])
        d2 = int(normalPatternTanggal[1][0:2])
        dt1 = datetime.datetime(y1,m1,d1)
        dt2 = datetime.datetime(y2,m2,d2)
        n = len(dbReminder)
        result=[]
        for i in range (n):
            currentYear = int(dbReminder[i][1][6:10])
            currentMonth = int(dbReminder[i][1][3:5])
            currentDay = int(dbReminder[i][1][0:2])
            currentdt = datetime.datetime(currentYear, currentMonth, currentDay)
            if (dt1 < currentdt and currentdt < dt2):
                print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return result
    elif (idxTipePeriode == 2):
        # findN = boyermoore.bmMatch(inputText,periodeWaktu[2])
        # print(findN)
        textSource = inputText
        patternN = re.compile(r'(\w+)\sminggu ke depan',re.IGNORECASE)
        matchN = patternN.findall(textSource)
        print(matchN)
        if (isinstance(int(matchN[0]),(int,float))):
            nHari = int(matchN[0])*7
            nowDate = datetime.datetime.now()
            nowDateGap = nowDate + timedelta(days=nHari)
            y1 = int(nowDate.year)
            m1 = int(nowDate.month)
            d1 = int(nowDate.day)
            y2 = int(nowDateGap.year)
            m2 = int(nowDateGap.month)
            d2 = int(nowDateGap.day)
            dt1 = datetime.datetime(y1,m1,d1)
            dt2 = datetime.datetime(y2,m2,d2)
            n = len(dbReminder)
            result = []
            for i in range (n):
                currentYear = int(dbReminder[i][1][6:10])
                currentMonth = int(dbReminder[i][1][3:5])
                currentDay = int(dbReminder[i][1][0:2])
                currentdt = datetime.datetime(currentYear, currentMonth, currentDay)
                if (dt1 < currentdt and currentdt < dt2):
                    print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                    result.append(dbReminder[i])
            return result
        else :
            nHari = int(textToAngka(matchN[0]))*7
            nowDate = datetime.datetime.now()
            nowDateGap = nowDate + timedelta(days=nHari)
            y1 = int(nowDate.year)
            m1 = int(nowDate.month)
            d1 = int(nowDate.day)
            y2 = int(nowDateGap.year)
            m2 = int(nowDateGap.month)
            d2 = int(nowDateGap.day)
            dt1 = datetime.datetime(y1,m1,d1)
            dt2 = datetime.datetime(y2,m2,d2)
            n = len(dbReminder)
            result = []
            for i in range (n):
                currentYear = int(dbReminder[i][1][6:10])
                currentMonth = int(dbReminder[i][1][3:5])
                currentDay = int(dbReminder[i][1][0:2])
                currentdt = datetime.datetime(currentYear, currentMonth, currentDay)
                if (dt1 < currentdt and currentdt < dt2):
                    print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                    result.append(dbReminder[i])
            return result
    elif (idxTipePeriode == 3):
        textSource = inputText
        patternN = re.compile(r'(\w+)\shari ke depan',re.IGNORECASE)
        matchN = patternN.findall(textSource)
        print(matchN)
        if (isinstance(int(matchN[0]),(int,float))):
            nHari = int(matchN[0])
            nowDate = datetime.datetime.now()
            nowDateGap = nowDate + timedelta(days=nHari)
            y1 = int(nowDate.year)
            m1 = int(nowDate.month)
            d1 = int(nowDate.day)
            y2 = int(nowDateGap.year)
            m2 = int(nowDateGap.month)
            d2 = int(nowDateGap.day)
            dt1 = datetime.datetime(y1,m1,d1)
            dt2 = datetime.datetime(y2,m2,d2)
            n = len(dbReminder)
            result = []
            for i in range (n):
                currentYear = int(dbReminder[i][1][6:10])
                currentMonth = int(dbReminder[i][1][3:5])
                currentDay = int(dbReminder[i][1][0:2])
                currentdt = datetime.datetime(currentYear, currentMonth, currentDay)
                if (dt1 < currentdt and currentdt < dt2):
                    print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                    result.append(dbReminder[i])
            return result
        else :
            nHari = int(textToAngka(matchN[0]))
            nowDate = datetime.datetime.now()
            nowDateGap = nowDate + timedelta(days=nHari)
            y1 = int(nowDate.year)
            m1 = int(nowDate.month)
            d1 = int(nowDate.day)
            y2 = int(nowDateGap.year)
            m2 = int(nowDateGap.month)
            d2 = int(nowDateGap.day)
            dt1 = datetime.datetime(y1,m1,d1)
            dt2 = datetime.datetime(y2,m2,d2)
            n = len(dbReminder)
            result = []
            for i in range (n):
                currentYear = int(dbReminder[i][1][6:10])
                currentMonth = int(dbReminder[i][1][3:5])
                currentDay = int(dbReminder[i][1][0:2])
                currentdt = datetime.datetime(currentYear, currentMonth, currentDay)
                if (dt1 < currentdt and currentdt < dt2):
                    print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                    result.append(dbReminder[i])
            return result
    elif (idxTipePeriode == 4):
        nowDate = datetime.datetime.now()
        y1 = int(nowDate.year)
        m1 = int(nowDate.month)
        d1 = int(nowDate.day)
        dt1 = datetime.datetime(y1,m1,d1)
        n = len(dbReminder)
        result = []
        for i in range (n):
            currentYear = int(dbReminder[i][1][6:10])
            currentMonth = int(dbReminder[i][1][3:5])
            currentDay = int(dbReminder[i][1][0:2])
            currentdt = datetime.datetime(currentYear, currentMonth, currentDay)
            if (dt1 == currentdt):
                print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return result


# Fungsi 3
def showDeadlines(inputText):
    global dbReminder
    # Nama matkul
    # Format matkul : XXYYYY, IF2211, if2211
    patternMatkul = re.compile(r'[a-zA-Z]{2}[0-9]{4}')
    matchMatkul = patternMatkul.findall(inputText)
    NamaMatkul = matchMatkul[0]
    print(matchMatkul)
    result = []
    for i in range (len(dbReminder)):
        if (boyermoore.bmMatch(dbReminder[i][2],NamaMatkul)!=-1):
            result.append(dbReminder[i])
    return result

# fungsi 4
def renewDeadline(inputText):
    global dbReminder
    # Find ID task
    # Format ID Task : task X
    patternID = re.compile(r'task\s(\w+)',re.IGNORECASE)
    matchID = patternID.findall(inputText)
    NamaID = matchID[0]
    print(NamaID)
    # Find new date
    # Format tanggal : 14/02/2021 ATAU 14-02-2021 ATAU 14 April 2021
    patternTanggal = re.compile(r'[0-9]{2}[/-]?\s?\w+[/-]?\s?[0-9]{4}')
    matchTanggal = patternTanggal.findall(inputText)
    newTanggalReminder = matchTanggal[0]
    newTanggalReminder = normalizeDatePattern(newTanggalReminder)
    print(newTanggalReminder)
    operationValidity = False
    for i in range (len(dbReminder)):
        if (dbReminder[i][0] == int(NamaID)):
            dbReminder[i][1] = newTanggalReminder
            operationValidity = True
    if (operationValidity):
        return ("Deadline task {0} telah diperbarui".format(NamaID))
    else :
        return ("Task {0} tidak ditemukan untuk diperabarui jadwalnya".format(NamaID))

# fungsi 5
def markTask(inputText):
    global dbReminder
    # Find ID task
    # Format ID Task : task X
    patternID = re.compile(r'task\s(\w+)',re.IGNORECASE)
    matchID = patternID.findall(inputText)
    NamaID = matchID[0]
    print(NamaID)
    # Find "Selesai" keyword
    isSelesai = boyermoore.bmMatch(inputText,"Selesai")
    if (isSelesai != -1):
        operationValidity = False
        for i in range (len(dbReminder)):
            if (dbReminder[i][0] == int(NamaID)):
                dbReminder[i][5] = 1
                operationValidity = True
        if (operationValidity):
            print(dbReminder)
            return ("Status Task {0} telah diperbarui, Selamat anda telah selesai mengerjakan task tersebut".format(NamaID))
        else :
            return ("Task {0} tidak ditemukan untuk diperabarui statusnya".format(NamaID))

# file1 = open("KataPenting.txt","r+")
# KataPenting = file1.read().splitlines()
# file1.close()
KataPenting =  readFileTXT("KataPenting.txt")
print(KataPenting)
dbReminder.append([1,"13/03/2021","IF2210","Tubes","Tugas2an",0])
contohinput = "Tubes IF2211 String Matching pada 14/02/2021"

# Fungsi 1 - add reminder
addReminer(contohinput)
print(dbReminder)

print("Fungsi 2-Show all task")
resultAll = showAllTask()
print(resultAll)

# result = periodeTask("Deadline hari ini apa saja")
# print(result)
# print(datetime.datetime.now().year )
# print(textToAngka("tiga"))

# print("Show deadlines")
# resultSD = showDeadlines("Deadline tugas IF2211 itu kapan")

# print("RENEW DEadline")
# resultRD = renewDeadline("Deadline task 1 diundur menjadi 28/04/2021")
# print(resultRD)
# print(dbReminder)

# print("Markselesai")
# resultMS = markTask("Saya sudah selesai mengerjakan task 1")
# print(resultMS)

# print(dbReminder)

# print(normalizeDatePattern("14 April 2021"))
# print(findQueueMonth("april"))