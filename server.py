import yfinance as yf
import rpyc

class StockPriceService(rpyc.Service):
    def on_connect(self, conn):
        print("Client connected.")

    def on_disconnect(self, conn):
        print("Client disconnected.")

    def exposed_get_stock_price(self, symbol):
        stock_data = yf.Ticker(symbol)
        current_price = 10#stock_data.history(period='1d')["Close"][0]
        return f"{symbol}: {current_price}"

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(StockPriceService(), port=5000)
    print("Starting server...")
    server.start()
