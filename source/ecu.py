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


class Control:
    """Base class for Ecu controls."""

    def __init__(self, ecu_data):
        """Control instanse from ecu data."""
        self.data = ecu_data

    def strip(self, name):
        """Clear spaces from data field."""
        return ' '.join(self.data[name].split())

    def __str__(self):
        """String representation for Label."""
        return self.strip('text')


class Label(Control):
    """Ecu label."""


class Button(Control):
    """Ecu button.

    Fields: messages send text uniquename
    """


class Presend(Control):
    """Ecu presend."""

    def __str__(self):
        """String representation for Label."""
        return "{} [{}]".format(self.data['RequestName'], self.data['Delay'])


class Display(Control):
    """Ecu display."""

    @property
    def request(self):
        """Request name."""
        return self.data["request"]


class Input(Display):
    """Ecu input."""


class Screen:
    """Ecu screen."""

    def __init__(self, ecu_data):
        """Screen instanse from ecu data."""
        self.data = ecu_data

    def __str__(self):
        """String representation for screen."""
        return str(list(sorted(self.data.keys())))

    @property
    def buttons(self):
        """Section buttons."""
        return [Button(i) for i in self.data["buttons"]]

    @property
    def displays(self):
        """Section displays."""
        return [Display(i) for i in self.data["displays"]]

    @property
    def inputs(self):
        """Section inputs."""
        return [Input(i) for i in self.data["inputs"]]

    @property
    def labels(self):
        """Section labels."""
        return [Label(i) for i in self.data["labels"]]

    @property
    def presend(self):
        """Section presend."""
        return [Presend(i) for i in self.data["presend"]]


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

        self.data_layout = None
        self.data_json = None

    def __str__(self):
        """String representation."""
        return "{} [{} {}] {}".format(self.name, self.protocol, self.address, self.file_name)

    def load_data(self, ecu_db):
        """String representation."""
        if self.data_json is None:
            self.data_json = ecu_db.load_json(self.file_name)
        if self.data_layout is None:
            self.data_layout = ecu_db.load_json(self.file_name + '.layout')

        return self

    @property
    def categories(self):
        """Return list of categories."""
        if self.data_layout is None:
            return []

        return list(self.data_layout["categories"].keys())

    def category(self, key):
        """Return list of given category items."""
        return self.data_layout["categories"][key]

    def screen(self, key):
        """Return Screen object for given key."""
        return Screen(self.data_layout["screens"][key])


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

        for fname, i in self.load_json("db.json").items():
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

    def load_json(self, file_name):
        """Load and return content of given json file from db zip."""
        return json.loads(zipfile.ZipFile(self.zip_name, mode='r').read(file_name))
