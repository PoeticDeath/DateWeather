import re
import requests
import watch as wt
import widgets as wd
import datetime as dt
from random import randint

c = 0
temp = ""

def raec(text):
    return re.sub(r"\x1b\[[0-9;]*[mG]", "", text)

class DateWeatherProvider(wt.ComplicationsProvider):
    def name(self):
        return "Date and Weather"
            
    def timeline(self, after_date, limit):
        global temp
        res = requests.get("https://wttr.in/{}".format(requests.get("https://ipinfo.io/").json()["city"]))
        temp = raec(res.text)
        temp = temp[:temp.find("(")]
        temp = temp[temp.rfind(" ") + 1:] + "°F"
        dates = []
        for i in range(limit):
            delta = dt.timedelta(seconds=i*3)
            date = after_date + delta
            dates.append(date)
        return dates
        
    def complication(self, date):
        global c
        tday = dt.timedelta(days=1)
        lday = (date - tday).date().day
        day = date.date().day
        nday = (date + tday).date().day
        week = date.ctime().split(" ")[0]
        font = wd.Font("Arial", 1)
        daytext = wd.Text(str(lday) + "|" + str(day) + "|" + str(nday), font=font)
        weektext = wd.Text(week, font=font)
        temptext1 = wd.Text(temp[:-2], font=font)
        temptext2 = wd.Text(temp[-2:], font=font)
        fname = wd.Text("Tony", font=font)
        lname = wd.Text("Kerr", font=font)
        comp = wt.Complication()
        if not randint(0, 9):
            comp.circular.add_row(row=[fname])
            comp.circular.add_row(row=[lname])
        else:
            if not c:
                comp.circular.add_row(row=[daytext])
            if c == 1:
                comp.circular.add_row(row=[weektext])
            if c == 2:
                comp.circular.add_row(row=[temptext1])
                comp.circular.add_row(row=[temptext2])
                c = 0
            else:
                c += 1
        return comp

wt.add_complications_provider(DateWeatherProvider())

