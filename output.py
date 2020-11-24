from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import locale
import os
locale.setlocale(locale.LC_ALL, '')

#emojis = {"total": 0, "types": {"type": x}, "sent": {"name": {"total": x, "type": y}}}
#reactions = {"total": 0, "types": {}, "gave": {"name": {"total": x, "type": y}}, "got": {"name": {"total": x, "type": y}}}


def mrHtml(version, names, basicStats, fromDay, toDay, times, chat, emojis, reactions):
    file_loader = FileSystemLoader("resources")
    env = Environment(loader=file_loader)

    (people, photos, gifs, stickers, videos, audios, files) = basicStats
    (hours, days, weekdays, months, years) = times

    template = env.get_template('index.html')

    path = os.getcwd()

    name1 = names[0]
    name2 = names[1]
    newNames = changeNames(names)

    pictures = getPics(newNames, path)
    picture1 = pictures.get(newNames[0], False) or f"{path}/resources/placeholder.jpg"
    picture2 = pictures.get(newNames[1], False) or f"{path}/resources/placeholder.jpg"

    wdNames = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    fontSizes = ["300", "275", "250", "225", "200", "180", "160", "140", "120", "100"]
    fontSizesP = ["180", "170", "160", "150", "140", "130", "120", "110", "100", "90"]

    return template.render(
        path=path,
        title=chat,
        version=version,
        fullname1=name1,
        name1=name1.split()[0],
        fullname2=name2,
        name2=name2.split()[0],
        fromDay=fromDay,
        toDay=toDay,
        picture1=picture1,
        picture2=picture2,
        totalMessages=s(people["total"]),
        totalImages=s(photos["total"]),
        totalGifs=s(gifs["total"]),
        totalVideos=s(videos["total"]),
        totalStickers=s(stickers["total"]),
        totalAudios=s(audios["total"]),
        totalFiles=s(files["total"]),
        messages1=s(people.get(name1, 0)),
        images1=s(photos.get(name1, 0)),
        gifs1=s(gifs.get(name1, 0)),
        stickers1=s(stickers.get(name1, 0)),
        audios1=s(audios.get(name1, 0)),
        videos1=s(videos.get(name1, 0)),
        files1=s(files.get(name1, 0)),
        messages2=s(people.get(name2, 0)),
        images2=s(photos.get(name2, 0)),
        gifs2=s(gifs.get(name2, 0)),
        stickers2=s(stickers.get(name2, 0)),
        audios2=s(audios.get(name2, 0)),
        videos2=s(videos.get(name2, 0)),
        files2=s(files.get(name2, 0)),
        names=[name2, name1],
        msgsPeople=[people[names[1]], people[names[0]]],
        topDay=sorted(days.items(), key=lambda item: item[1], reverse=True)[0][0],
        topDayMsgs=s(sorted(days.items(), key=lambda item: item[1], reverse=True)[0][1]),
        topWeekday=wdNames[sorted(weekdays.items(), key=lambda item: item[1], reverse=True)[0][0]],
        topWeekdayMsgs=s(sorted(weekdays.items(), key=lambda item: item[1], reverse=True)[0][1]),
        topMonth=sorted(months.items(), key=lambda item: item[1], reverse=True)[0][0],
        topMonthMsgs=s(sorted(months.items(), key=lambda item: item[1], reverse=True)[0][1]),
        topYear=sorted(years.items(), key=lambda item: item[1], reverse=True)[0][0],
        topYearMsgs=s(sorted(years.items(), key=lambda item: item[1], reverse=True)[0][1]),
        days=list(days.values()),
        daysLab=monthLabel(days),
        stepSizeY=stepSize(days),
        hours=list(hours.values()),
        hoursLab=list(hours.keys()),
        stepSizeYh=stepSize(hours),

        totalEms=s(emojis["total"]),
        diffEms=len(emojis["types"]),
        emojis=zip(topEmojis(emojis)[0], topEmojis(emojis)[1], fontSizes),
        emojisL=len(topEmojis(emojis)[0]),
        totalEms1=s(emojis["sent"][name1]["total"]),
        diffEms1=s(len(emojis["sent"][name1])-1),
        emojisAvg1=round(emojis["sent"][name1]["total"]/people[name1], 2),
        totalEms2=s(emojis["sent"][name2]["total"]),
        diffEms2=s(len(emojis["sent"][name2])-1),
        emojisAvg2=round(emojis["sent"][name2]["total"]/people[name2], 2),
        emojisL1=len(topEmojisP(emojis, name1)[0]),
        emojis1=zip(topEmojisP(emojis, name1)[0], topEmojisP(emojis, name1)[1], fontSizesP),
        emojisL2=len(topEmojisP(emojis, name2)[0]),
        emojis2=zip(topEmojisP(emojis, name2)[0], topEmojisP(emojis, name2)[1], fontSizesP),

        totalRs=s(reactions["total"]),
        diffRs=len(reactions["types"]),
        reacsGave1=s(reactions["gave"][name1]["total"]),
        diffRs1=s(len(reactions["gave"][name1])-1),
        diffRs2=s(len(reactions["gave"][name2])-1),
        reacsGave2=s(reactions["gave"][name2]["total"]),
        reacsGot1=s(reactions["got"][name1]["total"]),
        reacsGot2=s(reactions["got"][name2]["total"]),
        reacsGotAvg1=round(reactions["got"][name1]["total"]/people[name1], 2),
        reacsGotAvg2=round(reactions["got"][name2]["total"]/people[name2], 2),
        reacs=zip(topEmojis(reactions)[0], topEmojis(reactions)[1], fontSizes),
        reacsL=len(topEmojis(reactions)[0]),
        reacs1=zip(topReacsP(reactions, name1)[0], topReacsP(reactions, name1)[1], fontSizesP),
        reacs2=zip(topReacsP(reactions, name2)[0], topReacsP(reactions, name2)[1], fontSizesP),
        reacsL1=len(topReacsP(reactions, name1)[0]),
        reacsL2=len(topReacsP(reactions, name2)[0]),
    )

def s(n):
    if n != 1:
        return "{0:n}".format(n)
    else:
        return n

def changeNames(names):
    no = 'ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝßàáâãäåçèéêëìíîïñòóôõöùúûüýÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſ'
    yes = 'AAAAAACEEEEIIIINOOOOOUUUUYsaaaaaaceeeeiiiinooooouuuuyyAaAaAaCcCcCcCcDdDdEeEeEeEeEeGgGgGgGgHhHhIiIiIiIiIiKkkLlLlLlLlLlNnNnNnNnNOoOoOoRrRrRrSsSsSsSsTtTtTtUuUuUuUuUuUuWwYyYZzZzZzs'
    newNames = []
    for n in names:
        s = list(n)
        s.remove(" ")
        for char in s:
            if char in no:
                ind = s.index(char)
                old = no.index(char)
                s[ind] = yes[old]
        newNames.append("".join(s).lower())
    return newNames

def getPics(newNames, path):
    pics = {}
    for n in newNames:
        for p in os.listdir(f"{path}/resources"):
            if p.startswith(n):
                pics[n] = f"{path}/resources/{p}"
    return pics

def stepSize(days):
    x = sorted(days.items(), key=lambda item: item[1], reverse=True)[0][1]
    if x < 100:
        y = x if x % 10 == 0 else x + 10 - x % 10
    elif x > 100:
        y = x if x % 100 == 0 else x + 100 - x % 100
    return y/2

def monthLabel(days):
    l = list(days.keys())
    for i in range(len(l)):
        l[i] = l[i][:7]
    return l

def topEmojis(emojis):
    l = sorted(emojis["types"].items(), key=lambda item: item[1], reverse=True)
    types = []
    counts = []
    for e in l:
        types.append(e[0])
        counts.append(s(e[1]))
    return [types[:10], counts[:10]]

def topEmojisP(emojis, name):
    l = sorted(emojis["sent"][name].items(), key=lambda item: item[1], reverse=True)
    types = []
    counts = []
    for e in l:
        types.append(e[0])
        counts.append(s(e[1]))
    return [types[1:11], counts[1:11]]

def topReacsP(reactions, name):
    l = sorted(reactions["got"][name].items(), key=lambda item: item[1], reverse=True)
    types = []
    counts = []
    for e in l:
        types.append(e[0])
        counts.append(s(e[1]))
    return [types[1:11], counts[1:11]]
