import requests
import threading
import time
from datetime import datetime
from requests.exceptions import RequestException

# Configure logging to output warnings and errors only
import logging
logging.basicConfig(filename='large_transactions.log', level=logging.WARNING, 
                    format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

class LargeTransactionMonitor:
    def __init__(self, threshold_btc=1):  # Set threshold as needed
        self.threshold_btc = threshold_btc
        self.large_transactions = []
        self.api_base_url = "https://blockchain.info"

    def fetch_with_retry(self, url, max_retries=3, backoff_factor=1):
        for attempt in range(max_retries):
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(backoff_factor * (2 ** attempt))

    def fetch_large_transactions(self):
        try:
            latest_block_url = f"{self.api_base_url}/latestblock"
            latest_block_data = self.fetch_with_retry(latest_block_url)
            latest_block_hash = latest_block_data['hash']

            block_url = f"{self.api_base_url}/rawblock/{latest_block_hash}"
            block_data = self.fetch_with_retry(block_url)

            large_txs = []
            for tx in block_data['tx']:
                for output in tx['out']:
                    amount_btc = output['value'] / 1e8  # Convert satoshis to BTC
                    if amount_btc >= self.threshold_btc:
                        large_txs.append({
                            'amount': amount_btc,
                            'timestamp': datetime.fromtimestamp(block_data['time']).isoformat(),
                            'txid': tx['hash'],
                            'address': output.get('addr', 'N/A')
                        })

            self.large_transactions = large_txs

        except RequestException as e:
            logger.error(f"Network error occurred: {e}")
        except ValueError as e:
            logger.error(f"JSON parsing error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def start_monitoring(self):
        self.monitoring_thread = threading.Thread(target=self.monitor)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def monitor(self):
        while True:
            self.fetch_large_transactions()
            time.sleep(600)  # Wait 10 minutes before checking the next block

    def get_large_transactions(self):
        # Return sorted transactions by amount in descending order
        return sorted(self.large_transactions, key=lambda x: x['amount'], reverse=True)
