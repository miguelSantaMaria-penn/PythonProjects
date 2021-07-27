import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

TWILIO_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ALPHA_API_KEY = os.environ.get('ALPHAVANTAGE_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "datatype": "json",
    "apikey": ALPHA_API_KEY,

}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()

stock_data = stock_response.json()["Time Series (Daily)"]

stock_data_list = [value for (key, value) in stock_data.items()]

yesterday_closing_price = float(stock_data_list[0]["4. close"])

day_before_yesterday_closing_price = float(stock_data_list[1]["4. close"])
#print(yesterday_closing_price, day_before_yesterday_closing_price)

difference = yesterday_closing_price - day_before_yesterday_closing_price

diff_emoji = None

if difference < 0:
    diff_emoji = "🔻"
else:
    diff_emoji = "🔺"


diff_percentage = (difference/yesterday_closing_price) * 100
diff_percentage = round(diff_percentage, 2)


if diff_percentage > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"][:3]
    formatted_articles = [f"TSLA: {diff_percentage}{diff_emoji}\n Headline: {article['title']}\n Brief: {article['description']}" for article in articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+13236885644',
            to='+16263401442')














