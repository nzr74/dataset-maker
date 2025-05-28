import csv


class Savedata:

    def __init__(self, destination, fields):

        self.destination = destination
        self.fields = fields

    def save_data(self, details, missing_value, site):
        full_data_size = {"divar": 13, "bama": 9}
       
        def save():
            with open(self.destination, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fields)
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow(details)
                csvfile.close()

        if missing_value:
            if len(details) > full_data_size[site]:
                save()
        else:
            save()
