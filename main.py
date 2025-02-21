import argparse, sys
from websites.bama import Bama
from websites.divar import Divar

parser = argparse.ArgumentParser()
parser.add_argument("--site", help="website")
parser.add_argument("--category", help="category")

args = parser.parse_args()
site = args.site
category = args.category
if site and category:
    if site == "bama":
        bama_obj = Bama(category=category)
        if category == "car":
            bama_obj.extract_car_data()
    elif site == "divar":
        divar_obj = Divar(category=category)
        if category == "car":
            divar_obj.extract_car_data()
    elif site == "sheypoor":
        pass
    elif site == "esam":
        pass
    else:
        print("please insert correct site")
else:
    print("please insert site and category")
