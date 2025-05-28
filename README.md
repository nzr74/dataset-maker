# 🌐 Web Scraping Project (dataset maker)

A Python-based web scraping project that extracts useful information from product listing websites (e.g. Divar, Bama ...) and presents it in a structured format. It is useful for collecting data for research or creating machine learning models.

## 📁 Repository

🔗 [GitHub Repo](https://github.com/nzr74/web-scraping)

## ⚙️ Features

- Scrapes dynamic and static websites
- Parses and structures HTML data using BeautifulSoup
- Supports custom target category
- Export scraped data to CSV
- Clean and modular Python code

## 🛠️ Technologies Used

- Python 3
- `selenium` for get content website
- `BeautifulSoup` for HTML parsing

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/nzr74/dataset-maker.git
cd dataset-maker
```
### 🧰 Install Dependencies

```bash
python -m venv .venv

# On Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
pip install -r requirements.txt
```
### ⚠️ Selenium & ChromeDriver Setup
This project uses Selenium with Google Chrome. Make sure you have:

- Google Chrome installed

- Chromedriver set up properly

#### 🛠 Manual Setup
If you're not using webdriver-manager, set the path to the ChromeDriver manually:

```bash
import sys
sys.path.insert(0, "path-to-chromedriver") 
```

Make sure chromedriver is downloaded from:
👉 https://sites.google.com/chromium.org/driver

Place it in your system PATH, or reference its location explicitly in your script.



## 📦 How to Use
```bash
python main.py --s {website} --c {category-name} --mv {True or False}
```
- c : category name for example -> car
- s : site name for example -> divar
- mv : Abbreviation of Missing Value, if False, items whose information is incomplete will also be saved.
#### By default, the value is mv false.

The scraped data will be saved as data/{website} folder.

## 🙋‍♂️ Contributing
Pull requests are welcome! If you'd like to contribute:

Fork the repo

Create a feature branch (git checkout -b feature/your-feature)

Commit your changes (git commit -m 'Add feature')

Push to your branch (git push origin feature/your-feature)

Open a pull request


## 📬 Contact
If you have any questions, feel free to open an issue or contact me at @Nzr74 on telegram






