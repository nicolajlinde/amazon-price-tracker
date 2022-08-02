import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pprint import pprint
import smtplib

load_dotenv()

URL = "https://www.amazon.com/dp/B0762PG24T"
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Accept-Language": "en-US,en;q=0.5"
}


response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

price_whole = soup.find(name="span", class_="a-price-whole").getText()
price_fraction = soup.find(name="span", class_="a-price-fraction").getText()

price = float(price_whole + price_fraction)
name = soup.find(name="span", class_="a-size-large").getText().encode("utf-8").strip()

price = 90
if price <= 100:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=USER, password=PASSWORD)
        connection.sendmail(
            from_addr=USER,
            to_addrs="nicolajlpedersen@gmail.com",
            msg=f"Subject:AMAZON Price Alert\n\n{name} is now ${price}\n{URL}"
        )
