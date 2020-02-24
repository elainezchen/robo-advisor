# app/robo_advisor.py

import requests
import json
import os
import csv
from dotenv import load_dotenv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

d = datetime.now()
dt = d.strftime("%m/%d/%Y %H:%M")

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
dates = list(tsd.keys()) 
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []
closing_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    closing_price = tsd[date]["4. close"]
    closing_prices.append(float(closing_price))
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

if (float(latest_close) <= (1.2 * float(recent_low))):
    rec = "BUY"
    rec_exp = "The latest closing price of " + symbol + " is less than 20% above its recent low. Now is a good time to buy."
else:
    rec = "DON'T BUY"
    rec_exp = "The latest closing price of " + symbol + " is more than 20% above its recent low. You should wait until the price drops."

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv") #can add symbol but makes new file every time
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
print(f"REQUEST AT: {dt}") 
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {rec}") 
print(f"RECOMMENDATION REASON: {rec_exp}") 
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


print("----------------")
print("GENERATING LINE GRAPH...")

stock_dates = mdates.drange()
stock_price = [d for d in high_prices]

plt.plot(dates, high_prices, label = "High Prices")
plt.plot(dates, low_prices, label = "Low Prices")
plt.plot(dates, closing_prices, label = "Closing Prices")

plt.xlabel("Date")
plt.ylabel("Stock Price USD")
plt.title("Line Chart")
plt.legend(loc = "upper right")
plt.show()