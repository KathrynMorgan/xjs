#!/usr/bin/env python3

from datetime import datetime
from colors import Color
from packaging import version


class Model:
    # TODO get latest juju version dynamically
    latest_juju_version = version.parse("2.5.1")
    column_names = [
        "Model",
        "Controller",
        "Cloud/Region",
        "Version",
        "SLA",
        "Timestamp",
        "Model-Status",
        "Meter-Status",
        "Message",
        "Notes",
    ]

    def __init__(self, modelinfo, controller):
        # Default Values
        self.notes = []
        self.applications = []
        self.machines = []
        self.containers = []
        self.meterstatus = ""
        self.message = ""
        self.upgradeavailable = ""

        # Required Variables
        self.name = modelinfo["name"]
        self.type = modelinfo["type"]
        self.controller = controller
        self.controller.name = modelinfo["controller"]
        self.cloud = modelinfo["cloud"]
        self.version = modelinfo["version"]
        self.modelstatus = modelinfo["model-status"]["current"]
        self.sla = modelinfo["sla"]

        # Required Dates
        self.since = datetime.strptime(
            modelinfo["model-status"]["since"], "%d %b %Y %H:%M:%SZ"
        )
        controller.update_timestamp(self.since)

        # Optional Variables
        if "meter-status" in modelinfo:
            self.meterstatus = modelinfo["meter-status"]["color"]
            self.message = modelinfo["meter-status"]["message"]
        if "upgrade-available" in modelinfo:
            self.upgradeavailable = modelinfo["upgrade-available"]
            self.notes.append("upgrade available: " + self.upgradeavailable)

    def add_application(self, application):
        self.applications.append(application)

    def add_machine(self, machine):
        self.machines.append(machine)

    def add_container(self, container):
        self.containers.append(container)

    def get_machine(self, machinename):
        for machine in self.machines:
            if machine.name == machinename:
                return machine
        else:
            return None

    def get_container(self, containername):
        for container in self.containers:
            if container.name == containername:
                return container
        else:
            return None

    def get_version_color(self):
        model_version = version.parse(self.version)
        if (
            model_version < version.parse("2.0.0")
            or model_version > Model.latest_juju_version
        ):
            return Color.Fg.Red + self.version + Color.Reset
        elif model_version < Model.latest_juju_version:
            return Color.Fg.Yellow + self.version + Color.Reset
        else:
            return Color.Fg.Green + self.version + Color.Reset

    # TODO Figure out all possible values of all options and color accordingly
    def get_modelstatus_color(self):
        if self.modelstatus == "available":
            return Color.Fg.Green + self.modelstatus + Color.Reset
        else:
            return Color.Fg.Red + self.modelstatus + Color.Reset

    def get_meterstatus_color(self):
        if not self.meterstatus:
            return ""
        if self.meterstatus == "green":
            return Color.Fg.Green + self.meterstatus + Color.Reset
        elif self.meterstatus == "red":
            return Color.Fg.Red + self.meterstatus + Color.Reset
        elif self.meterstatus == "amber":
            return Color.Fg.Orange + self.meterstatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.meterstatus + Color.Reset

    def get_row(self, color):
        if not self.controller.timestampprovided:
            if color:
                self.notes.append(
                    Color.Fg.Yellow + "Guessing at timestamp" + Color.Reset
                )
            else:
                self.notes.append("Guessing at timestamp")
        notesstr = ", ".join(self.notes)
        timestampstr = self.controller.timestamp.strftime("%H:%M:%SZ")
        if color:
            return [
                self.name,
                self.controller.name,
                self.cloud,
                self.get_version_color(),
                self.sla,
                timestampstr,
                self.get_modelstatus_color(),
                self.get_meterstatus_color(),
                self.message,
                notesstr,
            ]
        else:
            return [
                self.name,
                self.controller.name,
                self.cloud,
                self.version,
                self.sla,
                timestampstr,
                self.modelstatus,
                self.meterstatus,
                self.message,
                notesstr,
            ]
