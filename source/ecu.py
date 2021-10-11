# -*- coding: utf-8 -*-
"""Ecu databse."""
import os
import zipfile
import json
import glob

__author__ = "Cedric PAILLE"
__copyright__ = "Copyright 2016-2018"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Cedric PAILLE"
__email__ = "cedricpaille@gmail.com"
__status__ = "Beta"

GROUP_MAPPING = {
  "02": "Suspension pilotee",
  "51": "Cluster/TdB",
  "29": "Climatisation",
  "D2": "GATEWAY",
  "00": "CAN sniffer",
  "1E": "4WD",
  "01": "ABS/ESC",
  "95": "EVC",
  "26": "BCM/UCH",
  "60": "HMD",
  "50": "Tachometer",
  "A1": "HFM",
  "93": "LBC",
  "6E": "BVA",
  "04": "Power steering",
  "68": "PEB",
  "58": "Navigation",
  "2B": "RADAR",
  "F7": "LDCM",
  "08": "TPMS",
  "C0": "HFM",
  "13": "Audio",
  "59": "MIU",
  "F8": "RDCM",
  "24": "ACC",
  "27": "EMM",
  "A8": "LBC2",
  "23": "4WS",
  "11": "ADAS-Sub",
  "2E": "UBP",
  "67": "BCB",
  "0E": "Aide au parking",
  "0D": "Frein de parking electrique",
  "28": "CSHV",
  "FF": "CAN2",
  "62": "FCAM",
  "DA": "EVC-HCM-VCM",
  "E8": "SVS",
  "2F": "IKEY",
  "64": "SOW_right",
  "07": "HLS",
  "D3": "Urea pump",
  "77": "TCU",
  "86": "AAU",
  "3A": "AAM",
  "4D": "SCU",
  "DF": "Cluster",
  "A5": "DCM",
  "10": "Injection NISSAN",
  "0B": "ACC",
  "61": "Video",
  "46": "Engineering",
  "EA": "TCASE",
  "87": "C-Box",
  "1B": "DIFF LOCK",
  "72": "Lampes a decharge a droite",
  "ED": "Audio",
  "EC": "TPAD",
  "1C": "Pilotage capote",
  "37": "Onduleur",
  "D0": "GATEWAY",
  "32": "Superviseur",
  "A6": "PDCM",
  "66": "VCCU",
  "71": "HLL_DDL2",
  "E9": "EPS",
  "25": "IDM",
  "79": "GPL",
  "E2": "C-Display",
  "A7": "PBD",
  "6B": "Pre-heater",
  "2D": "ABS-ESC",
  "97": "PLC/PLGW",
  "DE": "ASBMD",
  "31": "Transpondeur",
  "63": "SOW Left",
  "E6": "SCCM",
  "2A": "ADP",
  "0F": "HFCK",
  "EB": "HU",
  "78": "DCM",
  "73": "Embrayage pilote",
  "5B": "ADAS Insulator",
  "5A": "ODS_DDL2",
  "3F": "GPS Alarm",
  "81": "VSP",
  "40": "TSR_FRONTCAM",
  "06": "EMCU",
  "E1": "CCU",
  "1A": "Additional Heater",
  "E3": "HMI GateWay",
  "AE": "UCBIC ISO8",
  "91": "LBC (HEV) CPC",
  "09": "MC HEV FSCM",
  "EE": "Controlographe",
  "52": "Synthese de la parole",
  "D1": "UDM",
  "E7": "SCRCM",
  "41": "GATEWAY",
  "2C": "Airbag",
  "70": "Lampes a decharge",
  "E4": "IBS",
  "E0": "HERMES",
  "7A": "Injection",
  "AB": "Regulateur de vitesse (ISO 8)",
  "B0": "Transpondeur (ISO8)",
  "82": "WCGS",
}


def hex16_tosigned(value):
    """Return signed value from 16 bits (2 bytes)."""
    return -(value & 0x8000) | (value & 0x7fff)


def hex8_tosigned(value):
    """Return signed value from 8 bits (1 byte)."""
    return -(value & 0x80) | (value & 0x7f)


# Protocols:
# KWP2000 FastInit MonoPoint            ?ATSP 5?
# KWP2000 FastInit MultiPoint           ?ATSP 5?
# KWP2000 Init 5 Baud Type I and II     ?ATSP 4?
# DiagOnCAN                             ATSP 6
# CAN Messaging (125 kbps CAN)          ?ATSP B?
# ISO8                                  ?ATSP 3?

class Ident:
    """Ident item."""

    def __init__(
      self,
      diagversion,
      supplier,
      soft,
      version,
      name,
      group,
      href,
      protocol,
      projects,
      address,
      zipped=False
    ):
        """Ident item."""
        self.diagversion = diagversion
        self.supplier = supplier
        self.soft = soft
        self.version = version
        self.name = name
        self.group = group
        self.projects = projects
        self.href = href
        self.addr = address
        if "CAN" in protocol.upper():
            self.protocol = 'CAN'
        elif "KWP" in protocol.upper():
            self.protocol = 'KWP2000'
        elif "ISO8" in protocol.upper():
            self.protocol = 'ISO8'
        else:
            self.protocol = 'UNKNOWN'
        self.hash = diagversion + supplier + soft + version
        self.zipped = zipped

    def check_with(self, diagversion, supplier, soft, version, addr):
        """Checking."""
        if self.diagversion == "":
            return None
        supplier_strip = self.supplier.strip()
        soft_strip = self.soft.strip()
        version_strip = self.version.strip()
        if int("0x" + self.diagversion, 16) != int("0x" + diagversion, 16):
            return False
        if supplier_strip != supplier.strip()[:len(supplier_strip)]:
            return False
        if soft_strip != soft.strip()[:len(soft_strip)]:
            return False
        if version_strip != version.strip()[:len(version_strip)]:
            return False

        self.addr = addr
        return True

    def dump(self):
        """Dump data."""
        return {
          'diagnostic_version': self.diagversion,
          'supplier_code': self.supplier,
          'soft_version': self.soft,
          'version': self.version,
          'group': self.group,
          'projects': list(self.projects),
          'protocol': self.protocol,
          'address': self.addr,
        }


class Database:
    """Ecu database."""

    jsonfile = "json/ecus.zip"

    def __init__(self, forceXML=False):
        """Database instanse."""
        self.targets = []
        self.vehiclemap = {}
        self.numecu = 0
        self.available_addr_kwp = []
        self.available_addr_can = []
        self.addr_group_mapping_long = {}

        inp = open("./json/addressing.json", "r")
        jsn = json.loads(inp.read())
        inp.close()

        for key, val in jsn.iteritems():
            GROUP_MAPPING[key] = val[0]
            self.addr_group_mapping_long[key] = val[1]

        jsonecu_files = glob.glob("./json/*.json.targets")
        for jsonecu_file in jsonecu_files:
            self.numecu += 1
            json_file = open(jsonecu_file, "r")
            json_data = json_file.read()
            json_file.close()
            ecus_dict = json.loads(json_data)
            for ecu_dict in ecus_dict:
                href = jsonecu_file.replace(".targets", "")
                name = os.path.basename(href)
                # Fix typo bug
                diagversion = ""
                if 'diagnostic_version' in ecu_dict:
                    diagversion = ecu_dict['diagnostic_version']
                else:
                    diagversion = ecu_dict['diagnotic_version']

                addr = ecu_dict['address']

                if 'KWP' in ecu_dict['protocol']:
                    if addr not in self.available_addr_kwp:
                        self.available_addr_kwp.append(str(addr))
                elif 'CAN' in ecu_dict['protocol']:
                    if addr not in self.available_addr_can:
                        self.available_addr_can.append(str(addr))

                if str(addr) not in GROUP_MAPPING:
                    print("Adding group ", addr,  ecu_dict['group'])
                    GROUP_MAPPING[str(addr)] = ecu_dict['group']

                ecu_ident = Ident(
                  diagversion,
                  ecu_dict['supplier_code'],
                  ecu_dict['soft_version'], ecu_dict['version'],
                  name, ecu_dict['group'], href, ecu_dict['protocol'],
                  ecu_dict['projects'], addr
                )

                for proj in ecu_dict['projects']:
                    projname = proj[0:3].upper()
                    if projname not in self.vehiclemap:
                        self.vehiclemap[projname] = []
                    self.vehiclemap[projname].append((ecu_dict['protocol'], addr))

                self.targets.append(ecu_ident)

        if os.path.exists("ecu.zip") and not forceXML:
            jsdb = zipfile.ZipFile("ecu.zip", mode='r').read("db.json")
            dbdict = json.loads(jsdb)
            for href, targetv in dbdict.iteritems():
                self.numecu += 1
                ecugroup = targetv['group']
                ecuprotocol = targetv['protocol']
                ecuprojects = targetv['projects']
                ecuaddress = targetv['address']
                ecuname = targetv['ecuname']

                if 'KWP' in ecuprotocol:
                    if ecuaddress not in self.available_addr_kwp:
                        self.available_addr_kwp.append(str(ecuaddress))
                elif 'CAN' in ecuprotocol:
                    if ecuaddress not in self.available_addr_can:
                        self.available_addr_can.append(str(ecuaddress))

                if str(ecuaddress) not in GROUP_MAPPING:
                    GROUP_MAPPING[ecuaddress] = targetv['group']

                if len(targetv['autoidents']) == 0:
                    ecu_ident = Ident(
                      "", "", "", "",
                      ecuname, ecugroup, href, ecuprotocol,
                      ecuprojects, ecuaddress, True
                    )
                    self.targets.append(ecu_ident)
                else:
                    for target in targetv['autoidents']:
                        ecu_ident = Ident(
                          target['diagnostic_version'],
                          target['supplier_code'],
                          target['soft_version'],
                          target['version'],
                          ecuname, ecugroup, href, ecuprotocol,
                          ecuprojects, ecuaddress, True
                        )

                        self.targets.append(ecu_ident)

                for proj in ecuprojects:
                    projname = proj[0:3].upper()
                    if projname not in self.vehiclemap:
                        self.vehiclemap[projname] = []
                    self.vehiclemap[projname].append((ecuprotocol, ecuaddress))

                self.targets.append(ecu_ident)

    def get_target(self, name):
        """Get target."""
        for i in self.targets:
            if i.name == name:
                return i
        return None

    def get_targets(self, name):
        """Get targets."""
        tgt = []
        for i in self.targets:
            if i.name == name:
                tgt.append(i)
        return tgt

    def get_targets_by_href(self, href):
        """Get targets by href."""
        tgt = []
        for i in self.targets:
            if i.href == href:
                tgt.append(i)
        return tgt

    def dump(self):
        """Dump data."""
        jsn = []
        for i in self.targets:
            if i.protocol in ['CAN', 'KWP2000', 'ISO8']:
                jsn.append(i.dump())
        return json.dumps(jsn, indent=1)
