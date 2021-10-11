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
      address
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
        self.hash_code = diagversion + supplier + soft + version


class Database:
    """Ecu database."""

    def __init__(self, zip_name, known_vehicles):
        """Database instanse."""
        self.count = 0
        self.targets = []
        self.unknown_vehicles = {}
        self.vehiclemap = {}
        self.protocol_kwp = []
        self.protocol_can = []

        for href, i in json.loads(zipfile.ZipFile(zip_name, mode='r').read("db.json")).items():
            self.count += 1
            group = i['group']
            protocol = i['protocol']
            projects = i['projects']
            address = str(i['address'])
            name = i['ecuname']
            autoidents = i['autoidents']

            if 'KWP' in protocol:
                if address not in self.protocol_kwp:
                    self.protocol_kwp.append(address)
            elif 'CAN' in protocol:
                if address not in self.protocol_can:
                    self.protocol_can.append(address)

            if not autoidents:
                self.targets.append(Ident(
                  "", "", "", "",
                  name, group, href, protocol, projects, address
                ))

            for j in autoidents:
                self.targets.append(Ident(
                  j['diagnostic_version'],
                  j['supplier_code'],
                  j['soft_version'],
                  j['version'],
                  name, group, href, protocol, projects, address
                ))

            self.add_projects(projects, known_vehicles, protocol, address)

    def add_projects(self, projects, known_vehicles, protocol, address):
        """Store projects from ecu."""
        for i in projects:
            if i not in known_vehicles:
                if i not in self.unknown_vehicles:
                    self.unknown_vehicles[i] = 0
                self.unknown_vehicles[i] += 1
            else:
                if i not in self.vehiclemap:
                    self.vehiclemap[i] = []
                self.vehiclemap[i].append((protocol, address))

    def get_targets_by_name(self, name):
        """Get targets by name."""
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
