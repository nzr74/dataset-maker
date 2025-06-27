import csv



    with open('data/divar/car/car_data.csv', "r+") as csvfile:
        reader = csv.reader(csvfile)
        try:
            next(reader)  # Try to read the first row
        except StopIteration:
            writer = csv.DictWriter(csvfile, fieldnames=['a','b'])
            writer.writeheader()



    

