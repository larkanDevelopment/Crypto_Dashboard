from crypto_data_fetcher import CryptoDataFetcher
from real_time_display import RealTimeDisplay
from large_transaction_monitor import LargeTransactionMonitor

def main():
    data_fetcher = CryptoDataFetcher()
    transaction_monitor = LargeTransactionMonitor(threshold_btc=1)  # Set threshold as needed
    transaction_monitor.start_monitoring()
    
    display = RealTimeDisplay(data_fetcher, transaction_monitor)
    display.display()

if __name__ == "__main__":
    main()
