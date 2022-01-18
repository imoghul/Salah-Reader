import docx2txt, re


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
    return words2


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


def processWords(words):
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
    for i in range(len(words)):
        if words[i] == "AM" or words[i] == "PM":
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


def getTimes():
    return processWords(doc2words("iqaamahdoc/Iqaamah Times.docx"))


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
    return getSummary({salah:getTimes()[salah]})
print(getTimes())
