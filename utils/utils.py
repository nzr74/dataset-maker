import csv
import os
import sys
import time


class Savedata:

    def __init__(self, destination, fields):

        self.destination = destination
        self.fields = fields
        if not os.path.exists(self.destination):
            directory = self.destination.rsplit("/", 1)[0]
            if not os.path.exists(directory):
                os.makedirs(directory)
            print(f"Created new file: {self.destination}")

        with open(self.destination, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writeheader()

    def save_data(self, details, missing_value, site):
        full_data_size = {"divar": 13, "bama": 9}

        def save():
            with open(self.destination, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fields)
                writer.writerow(details)
                csvfile.close()

        if missing_value:
            if len(details) == full_data_size[site]:
                save()
        else:
            save()

stop_flag = False

def spinning_loader():
    chars = "/—\\|"
    global stop_flag
    while not stop_flag:
        for char in chars:
            sys.stdout.write("\rPlease wait... " + char)
            sys.stdout.flush()
            time.sleep(0.1)


def complete_loading():
    global stop_flag
    stop_flag = True
    os.system("clear")
