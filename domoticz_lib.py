from pathlib import Path

import requests
import re

class Domoticz:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        model = Path("/sys/firmware/devicetree/base/model").read_text().replace("Raspberry", "R")
        serial = Path("/sys/firmware/devicetree/base/serial-number").read_text().lstrip("0")
        hardwareName = model + "s"+serial
        hardwareName = re.sub(r'\W+', '', hardwareName)
        print("harwarename : ", hardwareName, " ", len(hardwareName))
        self.IDX_HARDWARE = self.findIdxHardware(hardwareName);
        if self.IDX_HARDWARE == -1 :
            self.sendDomoticz("/json.htm?type=command&param=addhardware&htype=15&name=" + hardwareName + "&enabled=true&datatimeout=0")
            self.IDX_HARDWARE = self.findIdxHardware(hardwareName)
            print("Hardware added to domoticz ", self.IDX_HARDWARE)

    def sendDomoticz(self, url):
        r = requests.get("http://"+self.host + ":" + str(self.port) + url)        
        print("[sendDomoticz] >> ", url, " (", r.status_code, ")")
        if r.status_code == requests.codes.ok :
            return r.json()
        return None

    def idx_of_jsonvar(self, json):
        return json["idx"]
    
    def findIdxHardware(self, name):
        result = self.sendDomoticz("/json.htm?type=hardware")
        if result["result"] != None :
            print( "found devices ", [ x["Name"] for x in result["result"] ], " SEARCH ", name)
            goodname = list(filter(lambda x: x["Name"] == name, result["result"]))
            if len(goodname) > 0:
                return self.idx_of_jsonvar(goodname[0])
        return -1

    def findIdx(self, hardwareID) :
        result = self.sendDomoticz("/json.htm?type=devices")
        if result["result"] != None :
            goodID = list(filter(lambda x : x["HardwareID"] == hardwareID))
            if len(goodID) > 0 :
                return self.idx_of_jsonvar(goodID[0])
        return -1

    def findIdxSensorOfHardware(self, idHardware, prop, value, skip) :
        result = self.sendDomoticz("/json.htm?type=devices")
        if result["result"] != None :
            selected = list(filter(lambda x : x["HardwareID"] == idHardware and str(x[prop]) == str(value)))
            if len(selected) > skip :
                return self.idx_of_jsonvar(selected[skip])
        return -1

    def relayID(self, nth) :
        return self.findIdxSensorOfHardware(IDX_HARDWARE, "SwitchTypeVal", 0, nth)

    def deviceStatus(self, IDX) :
        return self.sendDomoticz("/json.htm?type=devices&rid="+String(IDX))

    def isRelayOn(self, IDX):
        if IDX == -1 :
            return false
        return str(self.deviceStatus(IDX)[ "result" ][0]["Status"]) == "On"


    def createVirtualSensor(self, name, ty) :
        return self.idx_of_jsonvar(self.sendDomoticz("/json.htm?type=createvirtualsensor&idx=" + String(IDX_HARDWARE) + "&sensorname="+name+"&sensortype="+String(ty)))

    def ceateDevice(self, name, ty, subtype) :
        return self.idx_of_jsonvar(self.sendDomoticz("/json.htm?type=createdevice&idx=" + str(self.IDX_HARDWARE) + "&sensorname="+name+"&devicetype="+str(ty)+"&devicesubtype="+str(subtype)));


    def sendValue(self, IDX, value) :
        self.sendDomoticz("/json.htm?type=command&param=udevice&idx=" + str(IDX) + "&nvalue=0&svalue=" + str(value))

    def sendSValue(self, IDX, value) :
        self.sendDomoticz("/json.htm?type=command&param=udevice&idx=" + str(IDX) + "&svalue=" + str(value))

