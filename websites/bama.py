from bs4 import BeautifulSoup
from extract.extract import Extract
import utils.utils as util


class Bama:
    categories = {"car": "car", "motorcycle": "motorcycle", "truck": "truck"}

    def __init__(self, category, missing_value):
        if category in self.categories:
            self.category = category
            util.loader_thread.start()
        else:
            raise("please insert correct category")
        self.missing_value = missing_value

    def extract_page_urls(self):
        url = f"https://bama.ir/{self.categories[self.category]}"
        page_urls = []
        path_element = "a[class='bama-ad listing']"
        extr_obj = Extract(url)
        page_urls = extr_obj.get_urls(path_element=path_element)
        return page_urls

    def extract_car_data(self):
        fields = [
            "brand",
            "type",
            "year",
            "color",
            "mileage",
            "fuel",
            "gearbox",
            "body",
            "price",
        ]
        destination = "data/bama/car/car_data.csv"
        save = util.Savedata(destination, fields)
        urls = self.extract_page_urls()
        util.util_obj.complete_loading()
        print(len(urls))
        for i, url in enumerate(urls, 1):
            print(i, " --> ", url)
            try:
                extr_obj = Extract(url)
                result = extr_obj.get_data()
                soup = BeautifulSoup(result, "html.parser")
                price = soup.find(
                    "span", class_="bama-ad-detail-price__price-text"
                ).text.replace(",", "")
                brand_and_type = soup.find(
                    "h1", class_="bama-ad-detail-title__title"
                ).text
                type_and_year = soup.find_all(
                    "span", class_="bama-ad-detail-title__subtitle"
                )
                car_details = soup.find(
                    "div", class_="bama-vehicle-detail-with-icon"
                ).find_all("p")
                year = type_and_year[0].text.strip()
                car_type = f"{brand_and_type.partition('،')[2].strip()} - {type_and_year[1].text.strip()}"
                mileage = car_details[0].text.replace(",", "").replace("km", "").strip()
                details = {}
                details["brand"] = brand_and_type.partition("،")[0]
                details["type"] = car_type
                details["year"] = int(year)
                details["mileage"] = int(mileage)
                details["fuel"] = car_details[1].text
                details["gearbox"] = car_details[2].text
                details["body"] = car_details[3].text
                details["color"] = car_details[4].text
                details["price"] = int(price)
                save.save_data(
                    details=details,
                    missing_value=self.missing_value,
                    site=__class__.__name__.lower(),
                )
            except (ValueError, AttributeError,IndexError):
                print("error")

        print("done!!!!!!!!!")
