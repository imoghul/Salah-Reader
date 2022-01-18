from wsgiref.simple_server import make_server
import falcon
import json
import docx2txt
from reader import *
from emailChecker import *


def getSalahTime(salah):
    retrieveIqaamahTimesDoc()
    times = getTimes()
    return json.dumps(getDays(salah))


class mainPage:
    def on_get(self,req,resp):
        resp.text = "try /mtws-iqaamah-times"

class helpPageResource:
    def on_get(self, req, resp):
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = (
            "Hello! To interact with this API please use GET requests on:\n\n"
            + req.url
            + "mtws-iqaamah-times/<salah>\n\n"
            "Salah names: \n"
            "    /all, /fajr, /thuhr, /asr, /magrib, /ishaa\n"
        )


class All:
    def on_get(self, req, resp):
        retrieveIqaamahTimesDoc()
        resp.text = json.dumps(getSummary(getTimes()))


class Fajr:
    def on_get(self, req, resp):
        resp.text = getSalahTime("Fajr")


class Thuhr:
    def on_get(self, req, resp):
        resp.text = getSalahTime("Thuhr")


class Asr:
    def on_get(self, req, resp):
        resp.text = getSalahTime("Asr")


class Magrib:
    def on_get(self, req, resp):
        resp.text = getSalahTime("Magrib")


class Ishaa:
    def on_get(self, req, resp):
        resp.text = getSalahTime("Ishaa")


app = falcon.App()
main_page = mainPage()
help_page = helpPageResource()
all_page = All()
fajr_page = Fajr()
thuhr_page = Thuhr()
asr_page = Asr()
magrib_page = Magrib()
ishaa_page = Ishaa()

app.add_route("/",main_page)
app.add_route("/mtws-iqaamah-times", help_page)
app.add_route("/mtws-iqaamah-times/all", all_page)
app.add_route("/mtws-iqaamah-times/fajr", fajr_page)
app.add_route("/mtws-iqaamah-times/thuhr", thuhr_page)
app.add_route("/mtws-iqaamah-times/asr", asr_page)
app.add_route("/mtws-iqaamah-times/magrib", magrib_page)
app.add_route("/mtws-iqaamah-times/ishaa", ishaa_page)

if __name__ == "__main__":

    with make_server("", 80, app) as httpd:

        print("Serving REST LED controller on Wormhole...")
        httpd.serve_forever()
