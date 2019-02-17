#!/usr/bin/env python3

import re
from datetime import datetime
from colors import Color
from unit import Unit


class Application:
    column_names = [
        "App",
        "Version",
        "Status",
        "Scale",
        "Charm",
        "Store",
        "Rev",
        "OS",
        "Series",
        "Notes",
    ]

    def __init__(self, appname, appinfo, model):
        # Default Values
        self.notes = []
        self.units = []
        self.version = ""
        self.message = ""
        self.relations = {}
        self.endpointbindings = {}
        self.charmlatestrev = -1

        # Required Variables
        self.name = appname
        self.model = model
        self.charm = appinfo["charm"]
        self.series = appinfo["series"]
        self.os = appinfo["os"]
        self.charmorigin = appinfo["charm-origin"]
        self.charmname = appinfo["charm-name"]
        self.charmrev = int(appinfo["charm-rev"])
        self.exposed = appinfo["exposed"]
        self.status = appinfo["application-status"]["current"]

        # Required Dates
        self.since = datetime.strptime(
            appinfo["application-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        model.controller.update_timestamp(self.since)

        # Optional Variables
        if "message" in appinfo["application-status"]:
            self.message = appinfo["application-status"]["message"]
        # TODO Figure out how to compare app versions and get latest from the
        # charm store
        if "version" in appinfo:
            self.version = appinfo["version"]
        if "relations" in appinfo:
            self.relations = appinfo["relations"]
        if "endpoint-bindings" in appinfo:
            self.endpointbindings = appinfo["endpoint-bindings"]
        if "can-upgrade-to" in appinfo:
            # TODO Get latest revision from charm store
            match = re.match(r"\D+(\d+)$", appinfo["can-upgrade-to"])
            self.charmlatestrev = int(match.group(1))
            self.canupgradeto = appinfo["can-upgrade-to"]

        # Calculated Values
        if self.exposed:
            self.notes.append("exposed")

        # Handle Units
        if "units" in appinfo:
            for unitname, unitinfo in appinfo["units"].items():
                unit = Unit(unitname, unitinfo, self)
                self.units.append(unit)

    def get_scale(self):
        # TODO This is a problem, if an application is subbordinate we need to
        # count those
        return len(self.units)

    def get_status_color(self):
        if self.status == "active":
            return Color.Fg.Green + self.status + Color.Reset
        elif self.status in ("error", "blocked"):
            return Color.Fg.Red + self.status + Color.Reset
        elif self.status == "waiting":
            return self.status
        elif self.status == "maintenance":
            return Color.Fg.Orange + self.status + Color.Reset
        else:
            return Color.Fg.Yellow + self.status + Color.Reset

    def get_scale_color(self):
        scale = self.get_scale()
        if scale == 0:
            return Color.Fg.Red + str(scale) + Color.Reset
        else:
            return str(scale)

    def get_charmrev_color(self):
        if self.charmlatestrev == -1:
            return str(self.charmrev)
        if self.charmrev < self.charmlatestrev:
            return Color.Fg.Yellow + str(self.charmrev) + Color.Reset
        elif self.charmrev == self.charmlatestrev:
            return Color.Fg.Green + str(self.charmrev) + Color.Reset
        else:
            return Color.Fg.Red + str(self.charmrev) + Color.Reset

    def get_charmorigin_color(self):
        if self.charmorigin != "jujucharms":
            return Color.Fg.Yellow + self.charmorigin + Color.Reset
        else:
            return self.charmorigin

    def get_row(self, color):
        notesstr = ", ".join(self.notes)

        if color:
            return [
                self.name,
                self.version,
                self.get_status_color(),
                self.get_scale_color(),
                self.charm,
                self.get_charmorigin_color(),
                self.get_charmrev_color(),
                self.os,
                self.series,
                notesstr,
            ]
        else:
            return [
                self.name,
                self.version,
                self.status,
                str(self.get_scale()),
                self.charm,
                self.charmorigin,
                str(self.charmrev),
                self.os,
                self.series,
                notesstr,
            ]