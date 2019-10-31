import frappe
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json


@frappe.whitelist()
def test_integration(testtoken):
    url = frappe.db.get_single_value("TR TCMB EVDS Integration Settings", "server")
    servicepath = "/service/evds/"
    servicetype = "serieList/"
    # her sorgunun ayrı başlığı var
    servicedata = ""
    servicedata = servicedata + "&key=" + testtoken
    servicedata = servicedata + "&type=" + frappe.db.get_single_value("TR TCMB EVDS Integration Settings", "type")
    servicedata = servicedata + "&code=" + "TP.DK.USD.A"

    requesturl = url + servicepath + servicetype + servicedata

    req = Request(requesturl)
    try:
        response = urlopen(req)
        with response as f:
            return f.read().decode('utf-8')
    except HTTPError as e:
        return 'The server couldn\'t fulfill the request. ' + 'Error code: ' + str(e.code)
    except URLError as e:
        return 'We failed to reach a server. ' + 'Reason: ' + e.reason
