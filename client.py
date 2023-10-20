import rpyc
import time


class StockPriceClient:
    def get_stock_price(self, symbol):
        attempts = 0
        max_attempts = 5
        retry_interval = 1  # Retry interval in seconds
        max_retry_time = 5 * 60  # Maximum retry time in seconds (5 minutes)
        start_time = time.time()
        
        while attempts < max_attempts and (time.time() - start_time) < max_retry_time:
            try:
                conn = rpyc.connect("stock-server", 8080)  # Use the service name from docker-compose.yml
                price = conn.root.get_stock_price(symbol)
                conn.close()

                return price
            except ConnectionRefusedError:
                print("Connection refused. Retrying...")
                attempts += 1
                time_elapsed = time.time() - start_time
                remaining_time = max_retry_time - time_elapsed
                print(f"Time remaining for retries: {remaining_time:.2f} seconds")

                # Wait until retry_interval seconds have passed
                while time.time() - start_time < time_elapsed + retry_interval:
                    pass
        
        print("Failed to connect to the server after multiple attempts.")
        return None

if __name__ == "__main__":
    symbols = ['TSLA', 'AAPL', 'MSFT']
    client = StockPriceClient()
    print("Getting stock prices from server...")
    while True:
        for symbol in symbols:
            price = client.get_stock_price(symbol)
            print(price)
        # Wait for 10 seconds before retrying all symbols
        start_time = time.time()
        while time.time() - start_time < 10:
            pass
        print(" ===== END OF WAIT ===== ")
