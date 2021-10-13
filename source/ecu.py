"""Ecu database."""
import zipfile
import json


class Protocol:
    """Supported protocols.

    KWP2000 FastInit MonoPoint            ?ATSP 5?
    KWP2000 FastInit MultiPoint           ?ATSP 5?
    KWP2000 Init 5 Baud Type I and II     ?ATSP 4?
    DiagOnCAN                             ATSP 6
    CAN Messaging (125 kbps CAN)          ?ATSP B?
    ISO8                                  ?ATSP 3?
    """

    CAN = 'CAN'
    KWP = 'KWP2000'
    ISO8 = 'ISO8'

    SignCAN = 'CAN'
    SignKWP = 'KWP'
    SignISO8 = 'ISO8'

    @staticmethod
    def get(text):
        """Restore protocol from text."""
        text = text.upper()
        protocol = 'UNKNOWN'

        if Protocol.SignCAN in text:
            protocol = Protocol.CAN
        elif Protocol.SignKWP in text:
            protocol = Protocol.KWP
        elif Protocol.SignISO8 in text:
            protocol = Protocol.ISO8

        return protocol


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
        self.protocol = Protocol.get(protocol)
        self.hash_code = diagversion + supplier + soft + version


class Database:
    """Ecu database."""

    def __init__(self, zip_name, known_vehicles):
        """Database instanse."""
        self.zip_name = zip_name
        self.count = 0
        self.targets_by_name = {}
        self.targets_by_href = {}
        self.unknown_vehicles = {}
        self.vehiclemap = {}
        self.protocol_kwp = {}
        self.protocol_can = {}
        self.protocol_unknown = {}

        for href, i in json.loads(zipfile.ZipFile(zip_name, mode='r').read("db.json")).items():
            self.count += 1
            group = i['group']
            protocol = i['protocol']
            projects = i['projects']
            address = str(i['address'])
            name = i['ecuname']
            autoidents = i['autoidents']

            if not autoidents:
                self.add_target(Ident(
                  "", "", "", "",
                  name, group, href, protocol, projects, address
                ))

            for j in autoidents:
                self.add_target(Ident(
                  j['diagnostic_version'],
                  j['supplier_code'],
                  j['soft_version'],
                  j['version'],
                  name, group, href, protocol, projects, address
                ))

            self.add_protocol(protocol, address)
            self.add_projects(projects, known_vehicles, protocol, address)

    def add_target(self, ident):
        """Store ident in target dicts."""
        if ident.name not in self.targets_by_name:
            self.targets_by_name[ident.name] = []
        self.targets_by_name[ident.name].append(ident)

        if ident.href not in self.targets_by_href:
            self.targets_by_href[ident.href] = []
        self.targets_by_href[ident.href].append(ident)

    def add_protocol(self, protocol, address):
        """Store ecu address in protocols."""
        if Protocol.SignKWP in protocol:
            self.protocol_kwp[address] = True
        elif Protocol.SignCAN in protocol:
            self.protocol_can[address] = True
        else:
            self.protocol_unknown[protocol] = True

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
        return self.targets_by_name.get(name, [])

    def get_targets_by_href(self, href):
        """Get targets by href."""
        return self.targets_by_href.get(href, [])
