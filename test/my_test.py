from app.robo_advisor import to_usd
from app.robo_advisor import compile_url


def test_to_usd():
    assert to_usd(1000.2342) == "$1,000.23"

def test_compile_url():
    assert compile_url("K", "API_KEY") == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=K&apikey=API_KEY"