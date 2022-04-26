import docx2txt, re, PyPDF2, glob


def pdf2words(doc):
    file = open(doc, "rb")
    pdfdoc = PyPDF2.PdfFileReader(file)
    text = pdfdoc.getPage(0).extractText()
    words = text.split(" ")
    while True:
        try:
            words.remove("")
        except:
            break
    words2 = []
    for i in words:
        for j in re.split("\n|\t", i):
            if j != "":
                words2.append(j)
    words2 = "".join(words2)
    return words2


def doc2words(doc):
    text = docx2txt.process(doc)
    words = text.split(" ")
    while True:
        try:
            words.remove("")
        except:
            break
    words2 = []
    for i in words:
        for j in re.split("\n|\t", i):
            if j != "":
                words2.append(j)
    return words2  #''.join(words2)


def identifyDay(day):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"
    if day.lower() in [monday[0 : i + 1] for i in range(len(monday))] + [
        monday[0 : i + 1] + "." for i in range(len(monday))
    ]:
        return 0
    if day.lower() in [tuesday[0 : i + 1] for i in range(len(tuesday))] + [
        tuesday[0 : i + 1] + "." for i in range(len(tuesday))
    ]:
        return 1
    if day.lower() in [wednesday[0 : i + 1] for i in range(len(wednesday))] + [
        wednesday[0 : i + 1] + "." for i in range(len(wednesday))
    ]:
        return 2
    if day.lower() in [thursday[0 : i + 1] for i in range(len(thursday))] + [
        thursday[0 : i + 1] + "." for i in range(len(thursday))
    ]:
        return 3
    if day.lower() in [friday[0 : i + 1] for i in range(len(friday))] + [
        friday[0 : i + 1] + "." for i in range(len(friday))
    ]:
        return 4
    if day.lower() in [saturday[0 : i + 1] for i in range(len(saturday))] + [
        saturday[0 : i + 1] + "." for i in range(len(saturday))
    ]:
        return 5
    if day.lower() in [sunday[0 : i + 1] for i in range(len(sunday))] + [
        sunday[0 : i + 1] + "." for i in range(len(sunday))
    ]:
        return 6


def processWordsDocx(words):
    daysInWeek = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    outlist = {}
    current = None
    # words = re.split("",words)
    print(words)
    for i in range(len(words)):
        if words[i : i + 1] == "AM" or words[i] == "PM":
            if words[i - 2].find(")") != -1:
                days = daysInWeek[
                    identifyDay(words[i - 4][1:]) : 1 + identifyDay(words[i - 2][:-1])
                ]
            else:
                days = daysInWeek
            time = words[i - 1] + words[i]
            outlist[current][time] = days
        if words[i] == "Salaatul" or words[i] == "Salatul":
            outlist[words[i + 1]] = {}
            current = words[i + 1]
    return outlist


def processWordsPdf(words):
    daysInWeek = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    salaahs = ["Fajr", "Thuhr", "Asr", "Magrib", "Ishaa"]
    outlist = {}
    current = None
    for i in [i for i in range(len(words)) if words.startswith(":", i)]:
        days = daysInWeek
        time = words[i - 2 : i + 5]
        if not time[0].isnumeric():
            time = time[1:]
        if words[i - 3] == ")":
            counter = i
            while words[counter] != "(":
                counter -= 1
            days = words[counter : i - 2]
        elif words[i - 2] == ")":
            counter = i
            while words[counter] != "(":
                counter -= 1
            days = words[counter : i - 1]
        if type(days) != list:
            days = days[1:-1]
            loc = days.find("-")
            if loc != -1:
                days = daysInWeek[
                    identifyDay(days[:loc]) : identifyDay(days[loc + 1 :]) + 1
                ]
            else:
                for loc in range(1, len(days)):
                    try:
                        days = daysInWeek[
                            identifyDay(days[:loc]) : identifyDay(days[loc:]) + 1
                        ]
                        break
                    except:
                        pass
        counter = i
        while words[counter : counter + 8] != "Salaatul":
            counter -= 1
        if words[counter + 8 : counter + 11] == "Faj":
            salaah = "Fajr"
        elif words[counter + 8 : counter + 11] == "Thu":
            salaah = "Thuhr"
        elif words[counter + 8 : counter + 11] == "Asr":
            salaah = "Asr"
        elif words[counter + 8 : counter + 11] == "Mag":
            salaah = "Magrib"
        elif words[counter + 8 : counter + 11] == "Ish":
            salaah = "Ishaa"
        try:
            outlist[salaah][time] = days
        except:
            outlist[salaah] = {time: days}
    return outlist


def getTimes():
    for i in glob.glob("iqaamahdoc/*.pdf"):
        return processWordsPdf(pdf2words("iqaamahdoc/Iqaamah Times.pdf"))
    return processWordsDocx(doc2words("iqaamahdoc/Iqaamah Times.docx"))


def getSummary(times):
    res = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": [],
    }
    # times = getTimes()
    for salah in times:
        for time in times[salah]:
            for day in times[salah][time]:
                res[day].append(time)
    return res


def getDays(salah):
    return getSummary({salah: getTimes()[salah]})


print(getTimes())
