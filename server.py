import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import rpyc

class StockPriceService(rpyc.Service):
    def on_connect(self, conn):
        print("Client connected.")

    def on_disconnect(self, conn):
        #print("Client disconnected.")
        pass

    def exposed_get_stock_price(self, symbol):
        stock_data = yf.Ticker(symbol)
        #current_price = stock_data.history(period='1d')["Close"][0]
        #return f"{symbol}: {current_price}"
        #stock_data = yf.Ticker(symbol)
        #current_price = stock_data.history(period='2d')#["Close"][0]
        av = TimeSeries(key='X4K3URDCASFL3Z5J', output_format='pandas')

        try:
            data, _ = av.get_quote_endpoint(symbol=symbol)
            return f"{symbol}: {data['05. price'][0]}"

        except ValueError as ve:
            current_price = stock_data.history(period='2d')["Close"][0]
            return f"{symbol}: {current_price}"

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(StockPriceService(), port=5000)
    print("Starting server...")
    server.start()
