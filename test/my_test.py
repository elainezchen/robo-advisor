import os
from dotenv import load_dotenv
from app.robo_advisor import to_usd
from app.robo_advisor import compile_url
from app.robo_advisor import get_response
from app.robo_advisor import parse_response
from app.robo_advisor import return_keys

def test_to_usd():
    """
    Tests the to_usd function.
    """
    assert to_usd(1000.2342) == "$1,000.23"

def test_compile_url():
    """
    Tests the compile_url function.
    """
    assert compile_url("K", "API_KEY") == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=K&apikey=API_KEY"

def test_get_response():
    """
    Tests the get_response function.
    """
    load_dotenv()
    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    request_url = compile_url("K", API_KEY)
    response = get_response(request_url)
    parsed_response = parse_response(response)
    assert type(parsed_response) is dict
    assert 'Meta Data' in parsed_response
    assert 'Time Series (Daily)' in parsed_response

def test_return_keys():
    """
    Tests the return_keys function.
    """
    load_dotenv()
    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    request_url = compile_url("K", API_KEY)
    response = get_response(request_url)
    parsed_response = parse_response(response)
    tsd = parsed_response["Time Series (Daily)"]
    dates = return_keys(tsd)
    assert '2020-04-14' in dates
    assert '2020-04-07' in dates

