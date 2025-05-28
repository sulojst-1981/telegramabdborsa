import os
import requests
import yfinance as yf
from datetime import datetime, timedelta

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

def analyze_stock(ticker):
    stock = yf.Ticker(ticker)
    end = datetime.now()
    start = end - timedelta(days=90)
    data = stock.history(start=start, end=end)
    
    if data.empty or len(data) < 21:
        return f"{ticker}: Yetersiz veri"

    close = data['Close']
    ma5 = close.rolling(5).mean()
    ma20 = close.rolling(20).mean()
    latest = close[-1]
    ma5_val = ma5[-1]
    ma20_val = ma20[-1]

    reco = "TUT"
    if ma5_val > ma20_val: reco = "AL"
    elif ma5_val < ma20_val: reco = "SAT"

    pct_2w = ((close[-1] - close[-10]) / close[-10]) * 100 if len(close) > 10 else 0
    pct_1m = ((close[-1] - close[-21]) / close[-21]) * 100 if len(close) > 21 else 0
    pct_3m = ((close[-1] - close[0]) / close[0]) * 100 if len(close) > 60 else 0

    return (f"📈 {ticker}\n"
            f"Fiyat: {latest:.2f}$\n"
            f"MA5: {ma5_val:.2f} / MA20: {ma20_val:.2f}\n"
            f"Değişim: 2h: {pct_2w:.1f}% | 1ay: {pct_1m:.1f}% | 3ay: {pct_3m:.1f}%\n"
            f"📊 Öneri: {reco}\n")

def main():
    send_telegram("🔔 ABD Borsa Teknik Raporu Başladı")
    for ticker in tickers:
        try:
            msg = analyze_stock(ticker)
            send_telegram(msg)
        except Exception as e:
            send_telegram(f"{ticker} için hata: {str(e)}")

if __name__ == "__main__":
    main()
