import requests
import os
from twilio.rest import Client


# Initialize constants
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# TWILIO API account ID and API authorization token - ENV variables
TWILIO_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')


# Stock and News API endpoints
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Stock and News API Keys - ENV variables
ALPHA_API_KEY = os.environ.get('ALPHAVANTAGE_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')


# Stock API, GET params
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "datatype": "json",
    "apikey": ALPHA_API_KEY,

}

# GET request to Stock API
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()

# retrieve json of stock data, get time series daily key
stock_data = stock_response.json()["Time Series (Daily)"]

# get list of stock values for the day- each value is dictionary of  open, close, etc stock values
stock_data_list = [value for (key, value) in stock_data.items()]

# get closing price as float of yesterday's stock
yesterday_closing_price = float(stock_data_list[0]["4. close"])

# get closing price as float of day before yesterday
day_before_yesterday_closing_price = float(stock_data_list[1]["4. close"])

# get difference between yesterday and day before
difference = yesterday_closing_price - day_before_yesterday_closing_price

# if the difference is positive or zero, set text emoji upwards, else downwards
diff_emoji = None

if difference < 0:
    diff_emoji = "🔻"
else:
    diff_emoji = "🔺"

# get difference as formatted percentage
diff_percentage = (difference/yesterday_closing_price) * 100
diff_percentage = round(diff_percentage, 2)

# if difference is plus or minus  at least 5%, send text message with price and article data
if diff_percentage > 5 or diff_percentage < -5:

    # set params for news API, including key and TESLA to search for in headline
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    # news GET request
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()

    # slice and grab up to 3 articles from response
    articles = news_response.json()["articles"][:3]

    # format text message with stock info at top, and each article headlien and description
    formatted_articles = [f"TSLA: {diff_percentage}{diff_emoji}\n Headline: {article['title']}\n Brief: {article['description']}" for article in articles]

    # initialize TWILIO API client to send SMS messages
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # for each article in list (up to 3), send a message with the information
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+13236885644',
            to='+16263401442')










