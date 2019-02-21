#!/usr/bin/env python3

import pendulum
import re
from colors import Color


class BasicUnit:
    """
    A BasicMachine Object is inherited by Units and Subordinates so common
    attributes and functions remain here
    """

    column_names = [
        "Unit",
        "Workload",
        "Agent",
        "Machine",
        "Public address",
        "Ports",
        "Message",
        "Notes",
    ]

    def __init__(self, name, info, controller):
        """
        Create a BasicUnit object with basic information from a unit or
        subordinate object from a juju status output
        """
        # Default Values
        self.notes = []
        self.openports = []
        self.subordinates = []
        self.message = ""
        self.leader = False

        # Required Variables
        self.name = name
        self.workloadstatus = info["workload-status"]["current"]
        self.jujustatus = info["juju-status"]["current"]
        self.jujuversion = info["juju-status"]["version"]
        self.publicaddress = info["public-address"]

        # Required Dates
        if re.match(r"Z$", info["workload-status"]["since"]):
            self.workloadsince = pendulum.from_format(
                info["workload-status"]["since"],
                "DD MMM YYYY HH:mm:ss",
                tz="UTC",
            )
        else:
            self.workloadsince = pendulum.from_format(
                info["workload-status"]["since"], "DD MMM YYYY HH:mm:ssZ"
            )
        controller.update_timestamp(self.workloadsince)
        if re.match(r"Z$", info["juju-status"]["since"]):
            self.jujusince = pendulum.from_format(
                info["juju-status"]["since"], "DD MMM YYYY HH:mm:ss", tz="UTC"
            )
        else:
            self.jujusince = pendulum.from_format(
                info["juju-status"]["since"], "DD MMM YYYY HH:mm:ssZ"
            )
        controller.update_timestamp(self.jujusince)

        # Optional Variables
        if "message" in info["workload-status"]:
            self.message = info["workload-status"]["message"]
        if "open-ports" in info:
            self.openports = info["open-ports"]
        if "leader" in info:
            self.leader = info["leader"]

    def get_workloadstatus_color(self):
        """
        Return a status string with correct colors based on workload status
        """
        if self.workloadstatus == "active":
            return Color.Fg.Green + self.workloadstatus + Color.Reset
        if self.workloadstatus in ("error", "blocked"):
            return Color.Fg.Red + self.workloadstatus + Color.Reset
        if self.workloadstatus == "waiting":
            return self.workloadstatus
        if self.workloadstatus == "maintenance":
            return Color.Fg.Orange + self.workloadstatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.workloadstatus + Color.Reset

    def get_jujustatus_color(self):
        """Return a status string with correct colors based on juju status"""
        if self.jujustatus in ("idle", "executing"):
            return Color.Fg.Green + self.jujustatus + Color.Reset
        if self.jujustatus == "error":
            return Color.Fg.Red + self.jujustatus + Color.Reset
        else:
            return Color.Fg.Yellow + self.jujustatus + Color.Reset
