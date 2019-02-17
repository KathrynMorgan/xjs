#!/usr/bin/env python3

from basicmachine import BasicMachine
from colors import Color


class Container(BasicMachine):
    iscontainer = True

    def __init__(self, containername, containerinfo, machine):
        # Setup the BasicMachine
        BasicMachine.__init__(
            self, containername, containerinfo, machine.model.controller
        )

        # Required Variables
        self.machine = machine

    def get_machinemessage_color(self):
        if self.machinemessage == "Container started":
            return Color.Fg.Green + self.machinemessage + Color.Reset
        else:
            return Color.Fg.Yellow + self.machinemessage + Color.Reset

    def get_row(self, color):
        notesstr = ", ".join(self.notes)

        if color:
            return [
                self.name,
                self.get_jujustatus_color(),
                self.get_machinestatus_color(),
                self.dnsname,
                self.instanceid,
                self.series,
                "",
                "",
                "",
                "",
                self.get_machinemessage_color(),
                notesstr,
            ]
        else:
            return [
                self.name,
                self.jujustatus,
                self.machinestatus,
                self.dnsname,
                self.instanceid,
                self.series,
                "",
                "",
                "",
                "",
                self.machinemessage,
                notesstr,
            ]
