# app/robo_advisor.py

import requests
import json
import os
import csv
from dotenv import load_dotenv
from datetime import datetime
import matplotlib.pyplot as plt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

d = datetime.now()
dt = d.strftime("%m/%d/%Y %H:%M")

load_dotenv()

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", default="OOPS")

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 1000.2342
    Example: to_usd(1000.2342)
    Returns: $1,000.23
    """
    return "${0:,.2f}".format(my_price)
    
def compile_url(symbol, API_KEY):
    """
    Compiles a url based on a given symbol and API Key.
    Param: symbol (string) like K, API_KEY (string) (hidden)
    Example: compile_url("K", "API_KEY")
    Returns: https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=K&apikey=API_KEY
    """
    return f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"

def get_response(request_url):
    """
    Returns a response object from an inputted url.
    Param: request_url (any url)
    """
    return requests.get(request_url)

def parse_response(response):
    """
    Returns a dictionary parsed from a response object.
    Param: response (response object)
    """
    return json.loads(response.text)

def return_keys(tsd):
    """
    Returns a dictionary made from another dictionary's keys.
    Param: tsd (dictionary)
    """
    return list(tsd.keys())

if __name__ == "__main__":

    while True:
        symbol = input("Please input a stock or cryptocurrency symbol: ")
        if (len(symbol) <= 5 and len(symbol) >= 1 and symbol.isnumeric()) == False:
            request_url = compile_url(symbol, API_KEY)
            response = get_response(request_url)
            if "Error Message" in response.text:
                print("OOPS couldn't find that symbol, please try again!")
                exit()
            break
        else:
            print("Are you sure that was a valid symbol? Please try again!")

    parsed_response = parse_response(response)

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    tsd = parsed_response["Time Series (Daily)"]
    dates = return_keys(tsd) 
    latest_day = dates[0]
    previous_day = dates[1]
    latest_close = float(tsd[latest_day]["4. close"])
    previous_close = float(tsd[previous_day]["4. close"])

    high_prices = []
    low_prices = []
    closing_prices = []

    for date in dates:
        high_price = float(tsd[date]["2. high"])
        low_price = float(tsd[date]["3. low"])
        closing_price = float(tsd[date]["4. close"])
        closing_prices.append(closing_price)
        high_prices.append(high_price)
        low_prices.append(low_price)

    recent_high = float(max(high_prices))
    recent_low = float(min(low_prices))

    if (latest_close <= (1.2 * recent_low)):
        rec = "BUY"
        rec_exp = "The latest closing price of " + symbol + " is less than 20% above its recent low. Now is a good time to buy."
    else:
        rec = "DON'T BUY"
        rec_exp = "The latest closing price of " + symbol + " is more than 20% above its recent low. You should wait until the price drops."

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

    def print_message(message):
        """
        Returns a string value with a line of dashes on top.
        Param: message (string) like "hello"
        Example: message("hello")
        Returns:
        -------------------------
        hello
        """
        print("-------------------------")
        print(message)

    email_message = f"LATEST DAY: {last_refreshed}\n"+f"LATEST CLOSE: {to_usd(latest_close)}"
    email_message += f"\nRECENT HIGH: {to_usd(recent_high)}\n"+f"RECENT LOW: {to_usd(recent_low)}"

    print_message(f"SELECTED SYMBOL: {symbol}")
    print_message("REQUESTING STOCK MARKET DATA...\n"+f"REQUEST AT: {dt}")
    print_message(email_message)
    print_message(f"RECOMMENDATION: {rec}\n"+f"RECOMMENDATION REASON: {rec_exp}") 
    print_message(f"WRITING DATA TO CSV: {csv_file_path}...")
    print_message("HAPPY INVESTING!\n-------------------------")

    while True:
        answer = input("Would you like to create a line graph of recent high, low, and closing prices for " + symbol + "? [Y/N] ")
        if answer.lower() == "y":

            ax = plt.gca()
            plt.plot(dates, high_prices, label = "High Prices")
            plt.plot(dates, low_prices, label = "Low Prices")
            plt.plot(dates, closing_prices, label = "Closing Prices")

            plt.ylabel("Stock Price USD")
            plt.title(symbol + "'s High, Low, and Closing Prices Over Time")
            plt.legend(loc = "upper right")
            ax.axes.get_xaxis().set_visible(False)
            plt.show()
            break

        elif answer.lower() == "n":        
            break
        else:
            print("Please input [Y] or [N] only.")

    while True:
        answer2 = input("Would the customer like to be notified if the price has increased or decreased by more than 5% within the past day? [Y/N] ")
        if answer2.lower() == "y":
            email = input("What is the customer's email address? ")
            number = input("What is the customer's phone number? ")

            SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
            TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
            TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
            SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
            
            client = SendGridAPIClient(SENDGRID_API_KEY)
            subject = "Price Change Notification"
            if (latest_close>=(1.05*previous_close)):
                html_variable = "increased"
            elif (latest_close<=(0.95*previous_close)):
                html_variable = "decreased"
            else:
                print("The email and text will be not be sent since the price has not changed. Thank you for using Robo Advisor!")
                exit()

            html_content = f"""
            <h3>Price Change Notification</h3>
            <p>Current date and time: {dt} </p>
            <p>{email_message}</p>
            <p>{symbol}'s price has {html_variable} by more than 5% in the past day.</p>
            """

            message = Mail(from_email=email, to_emails=email, subject=subject, html_content=html_content)

            try: 
                response = client.send(message)
            except Exception as e:
                print("OOPS", e.message)

            client2 = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            content = f"The price for {symbol} has {html_variable} by more than 5% in the past day."
            message2 = client2.messages.create(to=number, from_=SENDER_SMS, body=content)

            print("The email and text have been sent. Thank you for using Robo Advisor!")
            exit()

        elif answer2.lower() == "n":
            print("Thank you for using Robo Advisor!")
            exit()
        else:
            print("Please input [Y] or [N] only.")

            


