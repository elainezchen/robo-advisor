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

We will be referencing an API Key for the program. In order to get your API Key, you should navigate to the site https://www.alphavantage.co/ and click on "Get Your Free API Key Today". Fill out the required information and copy your API Key.

Before running the program, make sure to create a ".env" file. The API Key will be placed in the .env file. Sample file contents could include:

```sh
ALPHAVANTAGE_API_KEY="abc123" # "abc123" being your API Key
```

## Usage

The user should input a stock symbol into the program when prompted (for example, "K", "AAPL", "MSFT"). 

The program will then compile all recent opening and closing prices, as well as highs and lows, and write it into a csv file. In addition, the program will recommend whether or not the user should buy the stock and offer a reason why. 