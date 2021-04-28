import boyermoore
import re
import datetime
#import timedelta
from datetime import timedelta

namaDatabase = "database.txt"
KataPenting = []
dbReminder = []
listAngka = ["Nol","Satu","Dua","Tiga","Empat","Lima","Enam","Tujuh","Delapan","Sembilan"]
listBulan = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
periodeWaktu = ["antara", "sampai", "minggu ke depan","hari ke depan","hari ini","sejauh ini"]
listKeywords = ["Tambah","Apa saja","Kapan","Diundur","Selesai","Help","Apa yang bisa assistant lakukan","Chatan YUK"]

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

def writeListToTXT(inputList, sourceFile):
    file1 = open(sourceFile,"w")
    for input in inputList:
        # print(input)
        file1.write(input)
        file1.write("\n")
    file1.close()

def writeDatabase(sourceFile):
    listDatabase = []
    for i in range (len(dbReminder)):
        currentData = ""
        for j in range (6):
            if (j == 5):
                currentData = currentData + str(dbReminder[i][j])
            else:
                currentData = currentData + str(dbReminder[i][j]) + ","
        listDatabase.append(currentData)
    # print(listDatabase)
    writeListToTXT(listDatabase, sourceFile)

def readDatabase(sourceFile):
    global dbReminder
    dbReminder = []
    resultRead = readFileTXT(sourceFile)
    for result in resultRead:
        currentResult = result.split(',')
        dbReminder.append(currentResult)
    for i in range (len(dbReminder)):
        dbReminder[i][0] = int(dbReminder[i][0])
        dbReminder[i][5] = int(dbReminder[i][5])


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

def isNumber(input):
    patternInput = re.compile(r'[0-9]+')
    matchInput = patternInput.findall(input)
    # print(matchInput)
    if (matchInput):
        return True
    else:
        return False

def findPeriodeWaktu(inputText):
    tipeperiode = ''
    idxTipePeriode = -1
    isFound = False
    for periode in periodeWaktu:
        idxTipePeriode +=1
        if (boyermoore.bmMatch(inputText,periode) != -1):
            tipeperiode = periode
            isFound = True
            break
    if (isFound == False):
        idxTipePeriode += 1
    # print(tipeperiode,idxTipePeriode)
    return tipeperiode,idxTipePeriode

def findDate(inputText):
    # Tanggal
    # Format tanggal : 14/02/2021 ATAU 14-02-2021 ATAU 14 April 2021
    patternTanggal = re.compile(r'[0-9]{2}[/-]?\s?\w+[/-]?\s?[0-9]{4}')
    matchTanggal = patternTanggal.findall(inputText)
    return matchTanggal

def findMatkul(inputText):
    # Nama matkul
    # Format matkul : XXYYYY, IF2211, if2211
    patternMatkul = re.compile(r'[a-zA-Z]{2}[0-9]{4}')
    matchMatkul = patternMatkul.findall(inputText)
    return matchMatkul

def findTipeReminder(inputText):
    # Jenis reminder
    tipeReminder = ''
    for kata in KataPenting:
        if (boyermoore.bmMatch(inputText,kata) != -1):
            tipeReminder = kata
    print(tipeReminder)
    return tipeReminder

def findTopic(inputText):
    # Mencari topic dari string input
    patternTopic = re.compile(r'[a-zA-Z]{2}[0-9]{4}\s(.+)\s\w+\s[0-9]{2}[/-]?\s?\w+[/-]?\s?[0-9]{4}')
    matchTopic = patternTopic.findall(inputText)
    return matchTopic

def resultToString(result):
    if len(result) == 0:
        return "Tidak Ada"
    else:
        string = "[Daftar Deadline]"
        for i in range (len(result)):
            string += ("</span></p><p class=\"botText\"><span>{0}. (ID:{1}) {2}-{3}-{4}-{5}".format(i+1,result[i][0],result[i][1],result[i][2],result[i][3],result[i][4]))
        return string

# Fungsi 1 (Menambahkan task ke reminder)
def addReminder(input):
    global dbReminder
    # Jenis reminder
    tipeReminder = findTipeReminder(input)
    print("Tipe Reminder : " + tipeReminder)
    if (tipeReminder == ''):
        return ("Maaf, parameter/atribut masukan masih kurang")
    # Nama matkul
    # Format matkul : XXYYYY, IF2211, if2211
    matchMatkul = findMatkul(input)
    if (not matchMatkul):
        return ("Maaf, parameter/atribut masukan masih kurang")
    NamaMatkul = matchMatkul[0]
    print("Nama Matkul : " + NamaMatkul)
    # Tanggal
    # Format tanggal : 14/02/2021 ATAU 14-02-2021 ATAU 14 April 2021
    matchTanggal = findDate(input)
    if (not matchTanggal):
        return ("Maaf, parameter/atribut masukan masih kurang")
    TanggalReminder = normalizeDatePattern(matchTanggal[0])
    print("Date : " + TanggalReminder)
    # Topik (BELUM)
    matchTopik = findTopic(input)
    if (not matchTopik):
        return ("Maaf, parameter/atribut masukan masih kurang")
    namaTopik = matchTopik[0]
    print("Nama Topik : " + namaTopik)
    # # Check if the parameters are complete
    # if (tipeReminder == '' or not matchMatkul or not matchTanggal or not matchTopik):
    #     return ("Maaf, parameter/atribut masukan masih kurang")
    
    # Check if task already exists
    for i in range (len(dbReminder)):
        if (dbReminder[i][1]==TanggalReminder and dbReminder[i][2]==NamaMatkul and dbReminder[i][3] == tipeReminder and dbReminder[i][4]==namaTopik):
            return ("Task yang coba dimasukan sudah ada di dalam database")
    # Add it to list of db
    id = len(dbReminder)+1
    statusTask = 0
    dbReminder.append([id,TanggalReminder, NamaMatkul, tipeReminder, namaTopik, statusTask])
    # print("[TASK BERHASIL DICATAT]")
    # print("(ID:{0}) {1}-{2}-{3}-{4}".format(id,TanggalReminder,NamaMatkul,tipeReminder,namaTopik))
    writeDatabase(namaDatabase)
    return ("[TASK BERHASIL DICATAT]</span></p><p class=\"botText\"><span>(ID:{0}) {1}-{2}-{3}-{4}".format(id,TanggalReminder,NamaMatkul,tipeReminder,namaTopik))

# Fungsi 2
# Menampilkan seluruh task
def showAllTask():
    global dbReminder
    n = len(dbReminder)
    result = []
    # print("[Daftar Deadline]")
    for i in range (n):
        if (dbReminder[i][5]==0):
            result.append(dbReminder[i])
    return resultToString(result)

# Berdasarkan periode waktu
def periodeTask(inputText):
    global dbReminder
    # menentukan jenis periode
    tipeperiode, idxTipePeriode = findPeriodeWaktu(inputText)
    print(tipeperiode,idxTipePeriode)
    if (idxTipePeriode == 0 or idxTipePeriode == 1):
        # ---------Pada periode tertentu (DATE_1 until DATE_2)------------#
        # Mendapatkan 2 Tanggal
        # Format tanggal : 14/02/2021 ATAU 14-02-2021 ATAU 14 April 2021
        matchTanggal = findDate(inputText)
        # Check apakah ada 2 parameter tanggal/date
        if(len(matchTanggal)!=2):
            return ("Maaf, jumlah argumen tanggal harus berjumlah 2")
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
            if ((dt1 < currentdt and currentdt < dt2) and dbReminder[i][5]==0):
                print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return resultToString(result)
    elif (idxTipePeriode == 2):
        # -------------N minggu ke depan-------------#
        # findN = boyermoore.bmMatch(inputText,periodeWaktu[2])
        # print(findN)
        textSource = inputText
        patternN = re.compile(r'(\w+)\sminggu ke depan',re.IGNORECASE)
        matchN = patternN.findall(textSource)
        print(matchN)
        nHari = 0
        # Check apakah N merupakan integer(angka/desimal) atau bukan
        if (isNumber(matchN[0]) == False):
            nHari = int(textToAngka(matchN[0]))*7
        else:
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
            if ((dt1 < currentdt and currentdt < dt2) and dbReminder[i][5]==0):
                print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return resultToString(result)
    elif (idxTipePeriode == 3):
        # -------------N hari ke depan-------------#
        textSource = inputText
        patternN = re.compile(r'(\w+)\shari ke depan',re.IGNORECASE)
        matchN = patternN.findall(textSource)
        print(matchN)
        nHari = 0
        # Check apakah N merupakan integer(angka/desimal) atau bukan
        if (isNumber(matchN[0]) == False):
            nHari = int(textToAngka(matchN[0]))
        else:
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
            if ((dt1 < currentdt and currentdt < dt2) and dbReminder[i][5]==0):
                print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return resultToString(result)
    elif (idxTipePeriode == 4):
        # --------Hari ini--------
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
            if (dt1 == currentdt and dbReminder[i][5]==0):
                print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return resultToString(result)
    elif (idxTipePeriode == 5):
        # ------------Seluruh task yang sudah tercatat oleh assistant------------
        return showAllTask()

def showAllTaskWithType(tipeTask):
    global dbReminder
    n = len(dbReminder)
    result = []
    # print("[Daftar Deadline]")
    for i in range (n):
        if (dbReminder[i][5]==0 and tipeTask==dbReminder[i][3]):
            result.append(dbReminder[i])
    return resultToString(result)

def periodeTaskWithTaskType(inputText):
    global dbReminder
    # Menentukan Type Task
    tipeTask = ''
    for kata in KataPenting:
        if (boyermoore.bmMatch(inputText,kata) != -1):
            tipeTask = kata
    print(tipeTask)
    # menentukan jenis periode
    tipeperiode, idxTipePeriode = findPeriodeWaktu(inputText)
    print(tipeperiode,idxTipePeriode)
    if (idxTipePeriode == 0 or idxTipePeriode == 1):
        # ---------Pada periode tertentu (DATE_1 until DATE_2)------------#
        # Mendapatkan 2 Tanggal
        # Format tanggal : 14/02/2021 ATAU 14-02-2021 ATAU 14 April 2021
        matchTanggal = findDate(inputText)
        # Check apakah ada 2 parameter tanggal/date
        if(len(matchTanggal)!=2):
            return ("Maaf, jumlah argumen tanggal harus berjumlah 2")
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
            if ((dt1 < currentdt and currentdt < dt2) and tipeTask == dbReminder[i][3] and dbReminder[i][5]==0):
                print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return resultToString(result)
    elif (idxTipePeriode == 2):
        # -------------N minggu ke depan-------------#
        # findN = boyermoore.bmMatch(inputText,periodeWaktu[2])
        # print(findN)
        textSource = inputText
        patternN = re.compile(r'(\w+)\sminggu ke depan',re.IGNORECASE)
        matchN = patternN.findall(textSource)
        # print(matchN)
        nHari = 0
        if (isNumber(matchN[0]) == False):
            nHari = int(textToAngka(matchN[0]))*7
        else:
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
            if ((dt1 < currentdt and currentdt < dt2) and tipeTask == dbReminder[i][3] and dbReminder[i][5]==0):
                # print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return resultToString(result)
    elif (idxTipePeriode == 3):
        textSource = inputText
        patternN = re.compile(r'(\w+)\shari ke depan',re.IGNORECASE)
        matchN = patternN.findall(textSource)
        print(matchN)
        nHari = 0
        # Check apakah N merupakan integer(angka/desimal) atau bukan
        if (isNumber(matchN[0]) == False):
            nHari = int(textToAngka(matchN[0]))
        else:
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
            if ((dt1 < currentdt and currentdt < dt2) and tipeTask == dbReminder[i][3] and dbReminder[i][5]==0):
                print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return resultToString(result)
    elif (idxTipePeriode == 4):
        # ---------Hari ini-----------
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
            if ((dt1 == currentdt) and tipeTask == dbReminder[i][3] and dbReminder[i][5]==0):
                print("(ID:{0}) {1}-{2}-{3}-{4}".format(dbReminder[i][0],dbReminder[i][1],dbReminder[i][2],dbReminder[i][3],dbReminder[i][4]))
                result.append(dbReminder[i])
        return resultToString(result)
    elif (idxTipePeriode == 5):
        return showAllTaskWithType(tipeTask)

def showListOfTask(inputText):
    # Menentukan Type Task
    isTipeTaskFound = False
    tipeTask = ''
    for kata in KataPenting:
        if (boyermoore.bmMatch(inputText,kata) != -1):
            tipeTask = kata
            isTipeTaskFound = True
    print(tipeTask)
    if(isTipeTaskFound==False):
        print("Tipe task found false")
        return periodeTask(inputText)
    else:
        print("Tipe task found true")
        return periodeTaskWithTaskType(inputText)


# Fungsi 3
def showTaskDeadlines(inputText):
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
    return resultToString(result)

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
    # Check apakah ada 1 parameter tanggal/date
    if(len(matchTanggal)!=1):
        return ("Maaf, jumlah argumen tanggal harus berjumlah 1")
    newTanggalReminder = matchTanggal[0]
    newTanggalReminder = normalizeDatePattern(newTanggalReminder)
    print(newTanggalReminder)
    operationValidity = False
    for i in range (len(dbReminder)):
        if (dbReminder[i][0] == int(NamaID)):
            dbReminder[i][1] = newTanggalReminder
            operationValidity = True
    if (operationValidity):
        writeDatabase(namaDatabase)
        return ("Deadline task {0} telah diperbarui".format(NamaID))
    else :
        return ("Task {0} tidak ditemukan untuk diperbarui jadwalnya".format(NamaID))

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
            writeDatabase(namaDatabase)
            return ("Status Task {0} telah diperbarui,</span></p><p class=\"botText\"><span>Selamat anda telah selesai mengerjakan task tersebut".format(NamaID))
        else :
            return ("Task {0} tidak ditemukan untuk diperabarui statusnya".format(NamaID))

def main(inputText):
    global KataPenting
    global dbReminder
    readDatabase("database.txt")
    KataPenting =  readFileTXT("KataPenting.txt")
    command = [False, False, False, False, False, False, False]
    # Cek apakah memenuhi fungsi addReminder
    date = findDate(inputText)
    NamaMatkul = findMatkul(inputText)
    typeTask = findTipeReminder(inputText)
    topic = findTopic(inputText)
    if (date and NamaMatkul and topic and typeTask):
        command[0] = True
        print("Memenuhi add")
    else :
        print("Tidak memenuhi")
    # Cek keywords
    listKey = []
    i = 0
    for keyword in listKeywords:
        if (boyermoore.bmMatch(inputText,keyword) != -1):
            listKey.append(keyword)
            if (i <= 4):
                command[i] = True
            elif (i>=5 and i<=6) :
                command[5] = True
            elif (i == 7):
                command[6] = True
        i = i + 1
    print(listKey)
    print(command)
    nTrue = 0
    nFalse = 0
    for i in range (len(command)):
        if (command[i]==True):
            nTrue = nTrue + 1
        else:
            nFalse = nFalse + 1
    if (nTrue>1):
        print("Maaf, pesan tidak dikenali")
        return ("Maaf, pesan tidak dikenali")
    elif (nFalse == 7):
        print("Maaf, pesan tidak dikenali")
        return ("Maaf, pesan tidak dikenali")
    else:
        if (command[0] == True):
            return(addReminder(inputText))
        elif (command[1] == True):
            return(showListOfTask(inputText))
        elif (command[2] == True):
            return (showTaskDeadlines(inputText))
        elif (command[3] == True):
            return (renewDeadline(inputText))
        elif (command[4] == True):
            return (markTask(inputText))
        elif (command[5] == True):
            Help = "[Fitur]"
            Help += "</span></p><p class=\"botText\"><span>1. Menambahkan task baru"
            Help += "</span></p><p class=\"botText\"><span>2. Melihat daftar task"
            Help += "</span></p><p class=\"botText\"><span>3. Menampilkan deadline dari task"
            Help += "</span></p><p class=\"botText\"><span>4. Memperbarui task tertentu"
            Help += "</span></p><p class=\"botText\"><span>5. Menandai task sudah selesai dikerjakan"
            Help += "</span></p><p class=\"botText\"><span>[Daftar kata penting]"
            Help += "</span></p><p class=\"botText\"><span>1. Kuis"
            Help += "</span></p><p class=\"botText\"><span>2. Ujian"
            Help += "</span></p><p class=\"botText\"><span>3. Tucil"
            Help += "</span></p><p class=\"botText\"><span>4. Tubes"
            Help += "</span></p><p class=\"botText\"><span>5. Praktikum"
            return (Help)
        elif (command[6] == True) :
            return "YUK!"


# KataPenting =  readFileTXT("KataPenting.txt")
# print(KataPenting)
# contohinput = "Tubes IF2299 String Matching pada 14/02/2021"
# print("Read database......")
# readDatabase("database.txt")
# print(dbReminder)
# writeDatabase("database.txt")

# Fungsi 1 - add reminder
# print("\nFungsi 1 - add reminder")
# print(addReminder("Tubes IF2299 String Matching pada"))
# print(dbReminder)

# # Fungsi 2
# print("\nFungsi 2-Show all task")
# print(dbReminder)
# resultAll = showAllTask()
# print(resultAll)

# print("\nApa saja deadline antara 10/02/2021 sampai 10/04/2021")
# resultAntara = periodeTask("Apa saja deadline antara 10/02/2021 sampai")
# print(resultAntara)

# print("\n3 minggu ke depan ada kuis apa saja")
# resultMinggu = periodeTaskWithTaskType ("3 minggu ke depan ada tubes apa saja")
# print(resultMinggu)

# print("\n3 hari ke depan ada kuis apa saja")
# resultHari = periodeTaskWithTaskType ("3 hari ke depan ada tubes apa saja")
# print(resultHari)

# print("determinae fungsi 2")
# resultt = showListOfTask("Apa saja deadline yang dimiliki sejauh ini")
# print(resultt)

# print("Show deadlines")
# resultSD = showTaskDeadlines("Deadline tugas IF2211 itu kapan")
# print(resultSD)

# print("RENEW DEadline")
# resultRD = renewDeadline("Deadline task 1 diundur menjadi 28/04/2021")
# print(resultRD)
# print(dbReminder)

# print("Markselesai")
# resultMS = markTask("Saya sudah selesai mengerjakan task 1")
# print(resultMS)

# print(dbReminder)

# print("Main program")
# main("Apa saja deadline yang dimiliki sejauh ini")

# print("Cari topic")
# print(findTopic("Tubes IF2211 String Matching Pada 14 April 2021"))

# print(findTipeReminder("Tubes IF2211 String Matching Pada 14 April 2021"))

# print(normalizeDatePattern("14 April 2021"))
# print(findQueueMonth("april"))
# print("IsNumber")
# print(isNumber("empat"))