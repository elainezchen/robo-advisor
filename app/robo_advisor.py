# app/robo_advisor.py

import requests
import json
import os
import csv
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default="OOPS")

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

while True:
    symbol = input("Please input a stock or cryptocurrency symbol: ")
    if (len(symbol) <= 5 and len(symbol) >= 1 and symbol.isnumeric()) == False:
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}" 
        response = requests.get(request_url)
        if "Error Message" in response.text:
            print("OOPS couldn't find that symbol, please try again!")
            exit()
        break
    else:
        print("Are you sure that was a valid symbol? Please try again!")

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) #(consider sorting to ensure first day is first)
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)



csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })
    


print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm") #dynamic
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!") #dynamic
print("RECOMMENDATION REASON: TODO") #dynamic
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

