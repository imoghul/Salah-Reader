from wsgiref.simple_server import make_server
import falcon
import json
import docx2txt
from reader import *
from emailChecker import *


def getSalahTime(salah):
    retrieveIqaamahTimesDoc()
    times = getTimes()
    return json.dumps(times[salah])


class helpPageResource:
    def on_get(self, req, resp):
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = (
            "Hello! To interact with this API please use GET requests on:\n\n"
            + req.url
            + "<salah>\n\n"
            "Salah names: \n"
            "    /fajr, /thuhr, /asr, /magrib, /ishaa\n"
        )


class Fajr:
    def on_get(self, req, resp):
        resp.text = getSalahTime("Fajr")
        print(resp.text)


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
help_page = helpPageResource()
fajr_page = Fajr()
thuhr_page = Thuhr()
asr_page = Asr()
magrib_page = Magrib()
ishaa_page = Ishaa()

app.add_route("/", help_page)
app.add_route("/fajr", fajr_page)
app.add_route("/thuhr", thuhr_page)
app.add_route("/asr", asr_page)
app.add_route("/magrib", magrib_page)
app.add_route("/ishaa", ishaa_page)

if __name__ == "__main__":

    with make_server("", 80, app) as httpd:

        print("Serving REST LED controller on Wormhole...")
        httpd.serve_forever()
