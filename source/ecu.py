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


class Item:
    """Database item."""

    def __init__(self, file_name, data):
        """Instanse from database data."""
        self.file_name = file_name
        self.group = data['group']
        self.protocol = Protocol.get(data['protocol'])
        self.projects = data['projects']
        self.address = str(data['address'])
        self.name = data['ecuname']
        self.autoidents = data['autoidents']


class Database:
    """Ecu database."""

    def __init__(self, zip_name, known_vehicles):
        """Read database items from zipped db.json file."""
        self.zip_name = zip_name
        self.count = 0
        self.unknown_vehicles = {}
        self.vehicles = {}
        self.protocol_kwp = {}
        self.protocol_can = {}
        self.protocol_unknown = {}

        for fname, i in json.loads(zipfile.ZipFile(zip_name, mode='r').read("db.json")).items():
            self.count += 1
            item = Item(fname, i)

            # Store ecu address in protocols.
            if item.protocol == Protocol.KWP:
                self.protocol_kwp[item.address] = True
            elif item.protocol == Protocol.CAN:
                self.protocol_can[item.address] = True
            else:
                self.protocol_unknown[item.protocol] = True

            # Store projects from ecu.
            for code in item.projects:
                if code not in known_vehicles:
                    if code not in self.unknown_vehicles:
                        self.unknown_vehicles[code] = 0
                    self.unknown_vehicles[code] += 1
                else:
                    if code not in self.vehicles:
                        self.vehicles[code] = []
                    self.vehicles[code].append(item)
