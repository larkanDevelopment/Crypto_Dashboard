import ccxt

class CryptoDataFetcher:
    def __init__(self):
        self.exchange = ccxt.binance()

    def fetch_crypto_data(self):
        symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "ADA/USDT", "XRP/USDT", "DOT/USDT", "LINK/USDT", "LTC/USDT", "BCH/USDT"]
        crypto_data = {}

        for symbol in symbols:
            try:
                ticker = self.exchange.fetch_ticker(symbol)
                crypto_data[symbol] = {
                    'price': ticker['last'],
                    'change': ticker['percentage']
                }
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                crypto_data[symbol] = {
                    'price': None,
                    'change': None
                }

        return crypto_data

    def get_data(self):
        return self.fetch_crypto_data()
