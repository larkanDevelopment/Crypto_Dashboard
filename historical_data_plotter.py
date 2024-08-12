import matplotlib.pyplot as plt

class HistoricalDataPlotter:
    def __init__(self, data_fetcher):
        self.data_fetcher = data_fetcher

    def calculate_indicators(self, df):
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['close'].ewm(span=50, adjust=False).mean()
        return df

    def plot_historical_data(self, symbol):
        df = self.data_fetcher.fetch_historical_data(symbol)
        df = self.calculate_indicators(df)

        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['close'], label='Close Price', color='blue')
        plt.plot(df.index, df['SMA_20'], label='20-Day SMA', color='red')
        plt.plot(df.index, df['SMA_50'], label='50-Day SMA', color='orange')
        plt.plot(df.index, df['EMA_20'], label='20-Day EMA', color='green')
        plt.plot(df.index, df['EMA_50'], label='50-Day EMA', color='purple')
        plt.title(f'Historical Data for {symbol} with Technical Indicators')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True)
        plt.show()
