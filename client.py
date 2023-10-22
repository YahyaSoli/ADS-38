import rpyc
import time

class StockPriceClient:
    def get_stock_price(self, symbol):
        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            try:
                conn = rpyc.connect("172.19.0.6", 5000)  # Use the service name from docker-compose.yml
                price = conn.root.get_stock_price(symbol)
                conn.close()
                return price
            except ConnectionRefusedError:
                print("Connection refused. Retrying...")
                attempts += 1
                time.sleep(1)  # Wait for 1 second before retrying
        print("Failed to connect to the server after multiple attempts.")
        return None

if __name__ == "__main__":
    symbols = ['TSLA', 'IBM', 'AAPL', 'GOOGL', 'AMZN', 'NFLX', 'MCD', 'DIS']
    client = StockPriceClient()
    print("Getting stock prices from server...")
    for index, symbol in enumerate(symbols):
        if index == 0:
            t_start = time.perf_counter()
        price = client.get_stock_price(symbol)
        print(price)
        if index == 7:
            t_stop = time.perf_counter()
    print("Elapsed time:", t_stop - t_start)
