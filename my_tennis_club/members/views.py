from django.shortcuts import render, redirect
import yfinance as yf
import matplotlib.pyplot as plt
import os
import tempfile
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def search(request):
    return render(request, 'main.html')
    
    # Handle other POST requests if needed

def search_results(request):
    if request.method == 'GET':
        company_symbol = request.GET.get('q', '')
        try:
            # Calculate the current price
            company = yf.Ticker(company_symbol)
            current_price = company.history
            sector = company.info.get('sector', 'N/A')
            industry = company.info.get('industry', 'N/A')
            chart_file_url = generate_price_chart(company_symbol)
            chart_file_url2 = generate_price_chart2(company_symbol)

        except Exception as e:
            current_price = None

        return render(request, 'search_results.html', {'company_symbol': company_symbol, 'current_price': current_price, 'company': company})
    
def generate_headlines(company_symbol):
    try:
        ticker = yf.Ticker(company_symbol)
        company_name = ticker.info["longName"]
        api_key = '82252f1a81d64bb3a9c492a2c20333e4'
        base_url = 'https://newsapi.org/v2/everything?'
        language = 'en'
        page_size = 1 
        url = f'{base_url}q={company_name}&language={language}&pageSize={page_size}&apiKey={api_key}'
        response = requests.get(url)
        news_data = response.json()
        articles = news_data['articles']
        for article in articles:
          title = article["title"]
          print(title)
          url = article["url"]
          print(url)
        return 0
    
    except Exception as e:
        return None
    
def generate_price_chart2(company_symbol):
    try:
        ticker = yf.Ticker(company_symbol)
        historical_data = ticker.history(period="5d")
        open_prices = historical_data['Open']
        high_prices = historical_data['High']
        close_prices = historical_data['Close']
        dates = historical_data.index
        plt.figure(figsize=(10, 6))
        plt.plot(dates, open_prices, label='Open', marker='o', linestyle='-')
        plt.plot(dates, high_prices, label='High', marker='o', linestyle='-')
        plt.plot(dates, close_prices, label='Close', marker='o', linestyle='-')
        plt.title(f"{company_symbol} Stock Prices - Last 5 Days")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as chart_file:
            plt.savefig(chart_file, format='png')
            chart_file_url2 = chart_file.name

        return chart_file_url2

    except Exception as e:
        return None
    
def generate_price_chart(company_symbol):
    try:
        company = yf.Ticker(company_symbol)
        current_price = company.history(period='1d')
        plt.figure(figsize=(12, 6))
        plt.plot(current_price.index, current_price['Close'], marker='o', linestyle='-', color='b')
        plt.title("Today's Price Changes for {}".format(company_symbol))
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.grid(True)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as chart_file:
            plt.savefig(chart_file, format='png')
            chart_file_url = chart_file.name

        return chart_file_url
    
        
    except Exception as e:
        return None

def see_stock(request):
    # Handle the "See Stock Performances" button click here
    return render(request, 'see_stock.html')

def add_stock(request):
    # Handle the "Add Stocks" button click here
    return render(request, 'add_stock.html')

def main(request):
    # Your view logic here
    return render(request, 'main.html')