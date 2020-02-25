# "Robo Advisor" Project

## Introduction

This app will help your customers decide when making investment decisions and stock trading recommendations. 

## Repo Setup

The repository can be accessed at https://github.com/elainezchen/robo-advisor. 

Download or "clone" it onto your computer. Choose a familiar download location like the Desktop. After downloading or cloning the repo, navigate there using the following command line:

```sh
cd ~/Desktop/robo-advisor
```

## Environment Setup

Create and activate new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```
From within the virtual environment, install the required packages specified in the "requirements.txt" file:

```sh
pip install -r requirements.txt
```

To run the Python script from within the virtual environment:
```sh
python app/robo_advisor.py
```

## Security Requirements

We will be referencing an API Key for the program. In order to get your API Key, you should navigate to <a href="https://www.alphavantage.co/">this site</a>  and click on "Get Your Free API Key Today". Fill out the required information and copy your API Key.

Before running the program, make sure to create a ".env" file. The API Key will be stored in the .env file under "ALPHAVANTAGE_API_KEY". 

We will also need a SendGrid API Key. Log into your account <a href="https://signup.sendgrid.com/">here</a> or sign up for a free account if you do not have one already. Make sure to click on the confirmation email to verify your account once you sign up. After that, <a href="https://app.sendgrid.com/settings/api_keys">create</a> an API Key with "full access" permissions. Store the Sendgrid API Key in an environment variable called "SENDGRID_API_KEY" in the .env file as well.

Sample file contents of the .env file could include:

```sh
ALPHAVANTAGE_API_KEY="abc123" # "abc123" being your API Key
SENDGRID_API_KEY="123abc"
```

## Usage

The user should input a stock symbol into the program when prompted (for example, "K", "AAPL", "MSFT"). 

The program will then compile all recent opening and closing prices, as well as highs and lows, and write it into a csv file. In addition, the program will recommend whether or not the user should buy the stock and offer a reason why. 