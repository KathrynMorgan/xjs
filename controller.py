#!/usr/bin/env python3

from datetime import datetime


class Controller:
    zerodate = datetime.strptime("00:00:00Z", "%H:%M:%SZ")

    def __init__(self, controllerinfo={}):
        # Default Values
        self.notes = []
        self.models = []

        # Required Variables
        self.timestampprovided = False
        self.timestamp = Controller.zerodate

        # Calculated Values
        if "timestamp" in controllerinfo:
            self.timestampprovided = True
            self.timestamp = datetime.strptime(
                controllerinfo["timestamp"], "%H:%M:%SZ"
            )

    def update_timestamp(self, date):
        # if the timestamp was not provided use the latest date
        # if it was provided we only have a time but no date, we should use
        # the latest date from any other status gathered
        if self.timestampprovided:
            # Hard Case - Get the time from the existing timestamp:
            # Goal Format %d %b %Y %H:%M:%SZ
            str_time = self.timestamp.strftime("%H:%M:%SZ")
            # Get the date from the passed in date
            str_date = date.strftime("%d %b %Y")
            # create a tempdate:
            temp_date = datetime.strptime(
                str_date + " " + str_time, "%d %b %Y %H:%M:%SZ"
            )
            if temp_date > self.timestamp:
                self.timestamp = temp_date
        else:
            if date > self.timestamp:
                self.timestamp = date

    def add_model(self, model):
        self.models.append(model)