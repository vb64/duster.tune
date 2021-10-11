# -*- coding: utf-8 -*-
"""Ecu databse."""
import zipfile
import json


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


class Database:
    """Ecu database."""

    def __init__(self, zip_name, vehicles):
        """Database instanse."""
        self.numecu = 0
        self.targets = []
        self.unknown_vehicles = {}
        self.vehiclemap = {}
        self.protocol_kwp = []
        self.protocol_can = []

        for href, targetv in json.loads(zipfile.ZipFile(zip_name, mode='r').read("db.json")).items():
            self.numecu += 1
            ecugroup = targetv['group']
            ecuprotocol = targetv['protocol']
            ecuprojects = targetv['projects']
            ecuaddress = str(targetv['address'])
            ecuname = targetv['ecuname']

            if 'KWP' in ecuprotocol:
                if ecuaddress not in self.protocol_kwp:
                    self.protocol_kwp.append(ecuaddress)
            elif 'CAN' in ecuprotocol:
                if ecuaddress not in self.protocol_can:
                    self.protocol_can.append(ecuaddress)

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

            self.add_projects(ecuprojects, vehicles, ecuprotocol, ecuaddress)

    def add_projects(self, projects, vehicles, protocol, address):
        """Store projects from ecu."""
        for i in projects:
            if i not in vehicles:
                if i not in self.unknown_vehicles:
                    self.unknown_vehicles[i] = 0
                self.unknown_vehicles[i] += 1
            else:
                if i not in self.vehiclemap:
                    self.vehiclemap[i] = []
                self.vehiclemap[i].append((protocol, address))

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
