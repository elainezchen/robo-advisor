import os
import json
from dotenv import load_dotenv
from app.robo_advisor import to_usd
from app.robo_advisor import compile_url
from app.robo_advisor import get_response

def test_to_usd():
    assert to_usd(1000.2342) == "$1,000.23"

def test_compile_url():
    assert compile_url("K", "API_KEY") == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=K&apikey=API_KEY"

def test_get_response():
    load_dotenv()
    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    request_url = compile_url("K", API_KEY)
    response = get_response(request_url)
    parsed_response = json.loads(response.text)
    assert type(parsed_response) is dict
    assert 'Meta Data' in parsed_response
    assert 'Time Series (Daily)' in parsed_response