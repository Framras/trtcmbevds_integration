import frappe
import urllib.request
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

    req = urllib.request.Request(requesturl)
    response = urllib.request.urlopen(req)
    with response as f:
        return f.read().decode('utf-8')
