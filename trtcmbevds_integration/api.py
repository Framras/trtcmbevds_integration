import frappe
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json


def communicate_with_uts(servicepath, servicerequestdatafields):
    url = ""
    company = frappe.defaults.get_user_default("Company")
    # This should only be used if the integration is enabled
    if frappe.db.get_single_value("TR TCMB EVDS Integration Settings", "enable") == 1:
        # Select the server according to the mode of the integration
        url = frappe.db.get_single_value("TR TCMB EVDS Integration Settings", "server")

        # her web servis çağrısının başlık (header) kısmına utsToken etiketiyle sistem token’ının değerini eklemelidir
        servicedata = servicerequestdatafields
        servicedata = "&key=" + frappe.db.get_value("TR TCMB EVDS Company Settings",
                                                    "company", "key")
        servicedata = servicedata + "&type=" + frappe.db.get_single_value("TR TCMB EVDS Integration Settings", "type")

        requesturl = url + servicepath + servicedata

        req = Request(requesturl)
        try:
            response = urlopen(req)
            with response as f:
                return f.read().decode('utf-8')
        except HTTPError as e:
            return 'The server couldn\'t fulfill the request. ' + 'Error code: ' + str(e.code)
        except URLError as e:
            return 'We failed to reach a server. ' + 'Reason: ' + e.reason


# FİRMA SORGULAMA SERVİSİ
# Firmaların MERSİS numarası, vergi numarası, ÇKYS numarası ve/ya firma unvanı ile firma tanımlayıcı numarası
# içeren firma bilgilerini sorgulamasını sağlayan servistir.
def firmasorgula(mrs, vrg, unv, krn, cky):
    servicepath = "/UTS/rest/kurum/firmaSorgula"
    servicedata = "{"
    if mrs != "":
        servicedata = servicedata + "\"MRS\":\"" + mrs + "\","
    if vrg != "":
        servicedata = servicedata + "\"VRG\":\"" + vrg + "\""
    if unv != "":
        servicedata = servicedata + "\"UNV\":\"" + unv + "\","
    if krn != "":
        servicedata = servicedata + "\"KRN\":" + krn + ","
    if cky != "":
        servicedata = servicedata + "\"CKY\":\"" + cky + "\""
    servicedata = servicedata + "}"

    return communicate_with_uts(servicepath, servicedata)


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
