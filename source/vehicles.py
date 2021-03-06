"""Known vehicles."""

DATA = {
  "xBA": "KWID CN",
  "xBB": "KWID BR",
  "x06": "TWINGO",
  "x44": "TWINGO II",
  "x07": "TWINGO III",
  "x07Ph2": "TWINGO III Ph2",
  "x77": "MODUS",
  "x35": "SYMBOL/THALIA",
  "x65": "CLIO II",
  "x85": "CLIO III",
  "x98": "CLIO IV",
  "xJA": "CLIO V",
  "x87": "CAPTUR",
  "xJB": "CAPTUR II",
  "xHA": "KAPTUR",
  "xHAPh2": "KAPTUR Ph2",
  "xJE": "CAPTUR II CN",
  "xBC": "CAPTUR II IN",
  "xJC": "ARKANA",
  "x38": "FLUENCE",

  "xFF": "FLUENCE II",
  # "xFF": "MEGANE IV SEDAN",

  "x64": "MEGANE/SCENIC I",
  "x84": "MEGANE/SCENIC II",
  "x84Ph2": "MEGANE/SCENIC II Ph2",
  "x95": "MEGANE/SCENIC III",
  "x95Ph2": "MEGANE/SCENIC III Ph2",
  "xFB": "MEGANE IV",
  "xFBPh2": "MEGANE IV Ph2",
  "xFA": "SCENIC IV",
  "xFAPh2": "SCENIC IV Ph2",
  "x56": "LAGUNA",
  "x74": "LAGUNA II",
  "x74Ph2": "LAGUNA II Phase 2",
  "x91": "LAGUNA III",
  "x47": "LAGUNA III (tricorps)",
  "x66": "ESPACE III",
  "x81": "ESPACE IV",
  "xFC": "ESPACE V",
  "xFCPh2": "ESPACE V Ph2",
  "x73": "VELSATIS",
  "x43": "LATITUDE",
  "xFD": "TALISMAN",
  "xFDPh2": "TALISMAN Ph2",
  "H45": "KOLEOS",
  "xZG": "KOLEOS II",
  "xZJ": "KOLEOS II CN",
  "HFE": "KADJAR",
  "HFEPh2": "KADJAR Ph2",
  "xZH": "KADJAR CN",
  "x33": "WIND",
  "x09": "TWIZY",
  "x10": "ZOE",
  "x10Ph2": "ZOE Ph2",
  "x76": "KANGOO I",
  "x61": "KANGOO II",
  "x61Ph2": "KANGOO II Ph2",
  "xFK": "KANGOO III",
  "x24": "MASCOTT",
  "x83": "TRAFFIC II",
  "x82": "TRAFFIC III",
  "x70": "MASTER II",
  "x62": "MASTER III",
  "x62Ph2": "MASTER III Ph2",

  "x90": "LOGAN/SANDERO",
  # "x90": "LARGUS",

  "x52": "LOGAN/SANDERO II",
  "xJI": "LOGAN/SANDERO III",
  "x79": "DUSTER",
  "x79Ph2": "DUSTER Ph2",
  "xJD": "DUSTER II",
  "x67": "DOKKER",
  "xJK": "Dokker II",
  "x92": "LODGY",
  "xGA": "XRAY",
  "AS1": "ALPINE",
  "x02E": "MICRA",
  "x21B": "NOTE",
  "x13A": "JUKE",
  "x60A": "NAVARRA ALASKAN",
  "xNN": "KICKS",
  "p32": "QASHQAI",
}

# list from github version of ddt4all at 2021
DATA2021 = {
  "xBA": "KWID CN",
  "xBB": "KWID BR",
  "x06": "TWINGO",
  "x44": "TWINGO II",
  "x07": "TWINGO III",
  "x77": "MODUS",
  "x35": "SYMBOL/THALIA",
  "xJC": "SYMBOL/THALIA II",
  "x65": "CLIO II",
  "x85": "CLIO III",
  "x98": "CLIO IV",
  "xJA": "CLIO V",
  "x87": "CAPTUR",
  "xJB": "CAPTUR II",
  "xJE": "CAPTUR II CN",
  "x38": "FLUENCE",

  "xFF": "FLUENCE II",
  # "xFF": "MEGANE IV SEDAN",

  "x64": "MEGANE/SCENIC I",
  "x84": "MEGANE/SCENIC II",
  "x84ph2": "MEGANE/SCENIC II Phase 2",
  "x95": "MEGANE/SCENIC III",
  "xFB": "MEGANE IV",
  "xFA": "SCENIC IV",
  "x56": "LAGUNA",
  "x74": "LAGUNA II",
  "x74ph2": "LAGUNA II Phase 2",
  "x91": "LAGUNA III",
  "x47": "LAGUNA III (tricorps)",
  "x66": "ESPACE III",
  "x81": "ESPACE IV",
  "xFC": "ESPACE V",
  "x73": "VELSATIS",
  "x43": "LATITUDE",
  "xFD": "TALISMAN",
  "H45": "KOLEOS",
  "xZG": "KOLEOS II",
  "xZJ": "KOLEOS II CN",
  "HFE": "KADJAR",
  "xZH": "KADJAR CN",
  "x33": "WIND",
  "x09": "TWIZY",
  "x10": "ZOE",
  "x10Ph2": "ZOE Ph2",
  "x76": "KANGOO I",
  "x61": "KANGOO II",
  "xFK": "KANGOO III",
  "x24": "MASCOTT",
  "x83": "TRAFFIC II",
  "x82": "TRAFFIC III",
  "x70": "MASTER II",
  "x62": "MASTER III",
  "x90": "LOGAN/SANDERO",
  "x52": "LOGAN/SANDERO II",
  "x79": "DUSTER",
  "x79Ph2": "DUSTER Ph2",
  "xJD": "DUSTER II",
  "x67": "DOKKER",
  "x92": "LODGY",
  "xGA": "BM LADA",
  "AS1": "ALPINE",
  "x02": "MICRA (NISSAN)",
  "x02E": "MICRA (NISSAN)",
  "x21": "NOTE (NISSAN)",
}


class Vehicle:
    """Vehicle with ecu data."""

    def __init__(self, code, ecu_list):
        """Instanse from ecu data."""
        self.code = code
        self.name = DATA[code]
        self.groups = {}
        self.protocols = []
        self.ecu_count = 0

        for i in ecu_list:
            self.ecu_count += 1

            if i.group not in self.groups:
                self.groups[i.group] = []
            self.groups[i.group].append(i)

            if i.protocol not in self.protocols:
                self.protocols.append(i.protocol)

    def __str__(self):
        """String representation."""
        return "{} ecus: {} groups: {} {}".format(
          self.name,
          self.ecu_count,
          len(self.groups),
          self.protocols,
        )

    def dump_group(self, group):
        """Return group items as text."""
        return '\n'.join(sorted([str(i) for i in self.groups[group]]))
