import argparse, sys
from websites.bama import Bama
from websites.divar import Divar

parser = argparse.ArgumentParser()
parser.add_argument("--s", help="website")
parser.add_argument("--c", help="category")
parser.add_argument("--mv", help="missing value default is False", default=False)

args = parser.parse_args()
site = args.s
category = args.c
missing_value = args.mv
if site and category:
    if site == "bama":
        bama_obj = Bama(category=category, missing_value=missing_value)
        if category == "car":
            bama_obj.extract_car_data()
    elif site == "divar":
        divar_obj = Divar(category=category, missing_value=missing_value)
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
