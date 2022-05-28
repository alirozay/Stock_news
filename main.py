import requests
from twilio.rest import Client
from datetime import datetime, timedelta
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_STOCK = os.environ['API_KEY_STOCK']
API_KEY_NEWS = os.environ['API_KEY_NEWS']
acc_id = os.environ['ACC_ID']
auth_key = os.environ['AUTH_KEY']
phone = os.environ['PHONE']
to_phone = os.environ['TO_PHONE']

today = datetime.today().date()
parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCK
}
parameters_news = {
    "q": "tesla",
    "from": str(today),
    "sortBy": "publishedAt",
    "apiKey": API_KEY_NEWS
}

response_one = requests.get(url="https://www.alphavantage.co/query",
                            params=parameters_stock)
response_one.raise_for_status()
data = response_one.json()
yesterday = today - timedelta(days=1)
day_before_yesterday = yesterday - timedelta(days=1)
stock_price_one = float(data["Time Series (Daily)"][str(yesterday)]['4. close'])
stock_price_two = \
    float(data["Time Series (Daily)"][str(day_before_yesterday)]['4. close'])
percentage = ((stock_price_one - stock_price_two)/stock_price_one) * 100
if abs(percentage) >= 5:
    response_two = requests.get(url="https://newsapi.org/v2/everything?",
                                params=parameters_news)
    response_two.raise_for_status()
    data_news = response_two.json()["articles"][:3]
    msg = ""
    if percentage < 0:
        msg += f"{STOCK} 🔻{round(percentage,2)}%"
    else:
        msg += f"{STOCK} 🔺{round(percentage,2)}%"
    for news in data_news:
        msg += f"\nHeadline: {news['title']}\nBrief: {news['description']}"
    client = Client(acc_id, auth_key)
    message = client.messages.create(body=msg, from_=phone, to=to_phone)
    print(message.status)


