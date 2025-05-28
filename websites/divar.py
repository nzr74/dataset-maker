from bs4 import BeautifulSoup

from extract.extract import Extract
import utils.utils as util


class Divar:
    categories = {"car": "s/iran/auto"}

    def __init__(self, category,missing_value):
        if category in self.categories:
            self.category = category
        else:
            raise("please insert correct category")
        self.missing_value = missing_value

    def extract_page_urls(self):
        url = f"https://divar.ir/{self.categories[self.category]}"
        path_element = "article[class='unsafe-kt-post-card unsafe-kt-post-card--outlined unsafe-kt-post-card']>a"
        extr_obj = Extract(url, dynamic_content=True)
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
            "motor",
            "gearbox",
            "body",
            "insurance",
            "front chassis",
            "rear chassis",
            "price",
        ]
        destination = "data/divar/car/car_data.csv"
        save = util.Savedata(destination, fields)
        urls = self.extract_page_urls()
        print(len(urls))
        for i ,url in enumerate(urls,1):
            print(i," --> ",url)
            try:
                extr_obj = Extract(url)
                result = extr_obj.get_data()
                soup = BeautifulSoup(result, "html.parser")
                car_details = soup.find_all(
                    "div", class_="kt-base-row kt-base-row--large kt-unexpandable-row"
                )
                car_condition = soup.find_all(
                        "div",
                        class_="kt-base-row kt-base-row--large kt-base-row--has-icon kt-score-row",
                    )

                mileage_year_color = soup.find_all(
                    "td",
                    class_="kt-group-row-item kt-group-row-item__value kt-group-row-item--info-row",
                )
                car_brand = soup.find_all(
                    "span",
                    class_="kt-breadcrumbs__action-text",
                )
                brand = car_brand[3].text
                details = {}

                details["brand"] = brand
                details["year"] = int(mileage_year_color[1].text)
                details["color"] = mileage_year_color[2].text
                details["mileage"] = int(mileage_year_color[0].text.replace("٬", ""))

                for detail in car_details:
                    title = detail.find(
                        "p", class_="kt-base-row__title kt-unexpandable-row__title"
                    ).text
                    if title == "برند و تیپ":
                        details["type"] = detail.find(
                            "div",
                            class_="kt-base-row__end kt-unexpandable-row__value-box",
                        ).text.replace(brand, "")
                    if title == "نوع سوخت":
                        details["fuel"] = detail.find(
                            "div",
                            class_="kt-base-row__end kt-unexpandable-row__value-box",
                        ).text
                    if title == "گیربکس":
                        details["gearbox"] = detail.find(
                            "div",
                            class_="kt-base-row__end kt-unexpandable-row__value-box",
                        ).text
                    if title == "مهلت بیمهٔ شخص ثالث":
                        details["insurance"] = detail.find(
                            "div",
                            class_="kt-base-row__end kt-unexpandable-row__value-box",
                        ).text
                    if title == "قیمت پایه":
                        details["price"] = int(
                            detail.find(
                                "div",
                                class_="kt-base-row__end kt-unexpandable-row__value-box",
                            )
                            .text.replace("٬", "")
                            .replace("تومان", "")
                        )
                for condition in car_condition:
                    title = condition.find("p", class_="kt-score-row__title").text

                    if title == "موتور":
                        details["motor"] = condition.find(
                            "div",
                            class_="kt-score-row__score",
                        ).text
                    if title == "شاسی جلو":
                        details["front chassis"] = condition.find(
                            "div",
                            class_="kt-score-row__score",
                        ).text
                    if title == "شاسی عقب":
                        details["rear chassis"] = condition.find(
                            "div",
                            class_="kt-score-row__score",
                        ).text
                    if title == "وضعیت شاسی‌ها":
                        details["front chassis"] = details["rear chassis"] = (
                            condition.find(
                                "div",
                                class_="kt-score-row__score",
                            ).text
                        )
                    if title == "بدنه":
                        details["body"] = condition.find(
                            "div",
                            class_="kt-score-row__score",
                        ).text

                print(details)
                save.save_data(
                    details=details,
                    missing_value=self.missing_value,
                    site=__class__.__name__.lower(),
                )
            except (ValueError, AttributeError,IndexError):
                print("error")

        print("done!!!!!!!!!")
