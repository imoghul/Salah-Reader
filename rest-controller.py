from wsgiref.simple_server import make_server
import falcon
import json
import docx2txt
from reader import *
from emailChecker import *



class mainPage:
    def on_get(self, req, resp):
        resp.text = "try /mtws-iqaamah-times"


class helpPageResource:
    def on_get(self, req, resp):
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = (
            "Hello! To interact with this API please use GET requests on:\n\n"
            + req.url
            + "mtws-iqaamah-times/<options>\n\n"
            "Salah names: \n"
            "    /email, /all, /fajr, /thuhr, /asr, /magrib, /ishaa\n"
        )

class Salah:
    salahName = ""
    val = {}
    def on_get(self, req, resp):
        if (not updateDoc() and self.val != {}):
            resp.text = self.val
            return
        if self.salahName == "All": self.val = json.dumps(getSummary(getTimes()))
        else: self.val = getSalahTime(self.salahName)
        resp.text = self.val
        with open("salahTimes/"+self.salahName+'.json', 'w', encoding='utf-8') as f:
            json.dump(self.val, f, ensure_ascii=False, indent=4)
class All(Salah):
    salahName = "All"

class Fajr(Salah):
    salahName = "Fajr"

class Thuhr(Salah):
    salahName = "Thuhr"

class Asr(Salah):
    salahName = "Asr"

class Magrib(Salah):
    salahName = "Magrib"

class Ishaa(Salah):
    salahName = "Ishaa"

class CurrEmail:
    currEmail = None  # {'current email':"NOTHING"}

    def on_get(self, req, resp):
        resp.text = json.dumps(CurrEmail.currEmail)

    # def on_put(self, req, resp):
    #    change = json.loads(str(req.bounded_stream.read().decode('utf-8')))
    #    CurrEmail.currEmail=change
    #    resp.text = json.dumps(change)


app = falcon.App()
main_page = mainPage()
help_page = helpPageResource()
all_page = All()
fajr_page = Fajr()
thuhr_page = Thuhr()
asr_page = Asr()
magrib_page = Magrib()
ishaa_page = Ishaa()
curremail_page = CurrEmail()

def updateDoc():
    latestEmail = latest()
    if latestEmail["subject"] != CurrEmail.currEmail:
        CurrEmail.currEmail = latestEmail["subject"]
        retrieveIqaamahTimesDoc(email_message=latestEmail)
        all_page.val = {}
        fajr_page.val = {}
        thuhr_page.val = {}
        asr_page.val = {}
        magrib_page.val = {}
        ishaa_page.val = {}
        return True
    return False


def getSalahTime(salah):
    updateDoc()
    return json.dumps(getDays(salah))




app.add_route("/", main_page)
app.add_route("/mtws-iqaamah-times", help_page)
app.add_route("/mtws-iqaamah-times/all", all_page)
app.add_route("/mtws-iqaamah-times/fajr", fajr_page)
app.add_route("/mtws-iqaamah-times/thuhr", thuhr_page)
app.add_route("/mtws-iqaamah-times/asr", asr_page)
app.add_route("/mtws-iqaamah-times/magrib", magrib_page)
app.add_route("/mtws-iqaamah-times/ishaa", ishaa_page)
app.add_route("/mtws-iqaamah-times/email", curremail_page)

if __name__ == "__main__":

    with make_server("", 80, app) as httpd:

        print("Serving REST controller on Wormhole...")
        httpd.serve_forever()
