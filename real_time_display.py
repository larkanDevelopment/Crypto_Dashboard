import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from large_transaction_monitor import LargeTransactionMonitor

class RealTimeDisplay:
    def __init__(self, data_fetcher, transaction_monitor):
        self.data_fetcher = data_fetcher
        self.transaction_monitor = transaction_monitor
        self.console = Console()
        self.layout = Layout()

        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
        )
        
        self.layout["main"].split_row(
            Layout(name="crypto_prices"),
            Layout(name="large_transactions")
        )

        self.layout["header"].update(Panel("Real-Time Crypto Data"))

        # Define a color map for each currency
        self.color_map = {
            "BTC/USDT": "cyan",
            "ETH/USDT": "purple",
            "SOL/USDT": "bright_cyan",
            "BNB/USDT": "magenta",
            "ADA/USDT": "blue",
            "XRP/USDT": "magenta",
            "DOT/USDT": "blue",
            "LINK/USDT": "purple",
            "LTC/USDT": "blue",
            "BCH/USDT": "bright_magenta"
        }

    def create_price_table(self, price_data):
        table = Table(expand=True)
        table.add_column("Symbol", justify="center", style="bold")
        table.add_column("Price", justify="center", style="bold")
        table.add_column("Change (%)", justify="center", style="bold")
        for symbol, data in price_data.items():
            color = self.color_map.get(symbol, "cyan")
            table.add_row(
                f"[{color}]{symbol}[/{color}]",
                f"[{color}]${data['price']:,.2f}[/{color}]" if data['price'] is not None else f"[{color}]N/A[/{color}]",
                f"[{color}]{data['change']:.2f}%[/{color}]" if data['change'] is not None else f"[{color}]N/A[/{color}]"
            )
        return table

    def create_large_transaction_table(self, transaction_data):
        table = Table(expand=True, style="bright_magenta")
        table.add_column("Amount (BTC)", justify="center", style="bold")
        table.add_column("Timestamp", justify="center", style="bold")
        table.add_column("Address", justify="center", style="bold")
        table.add_column("TXID", justify="center", style="bold")

        for tx in transaction_data:
            table.add_row(
                f"{tx['amount']:.2f} BTC",
                tx['timestamp'],
                tx['address'],
                tx['txid'][:10] + '...'  # Truncate TXID for better display
            )
        return table

    def display(self):
        while True:
            price_data = self.data_fetcher.get_data()
            large_transactions = self.transaction_monitor.get_large_transactions()

            price_table = self.create_price_table(price_data)
            large_transaction_table = self.create_large_transaction_table(large_transactions)

            self.layout["crypto_prices"].update(
                Panel(price_table, title="Crypto Prices", subtitle="Real-Time Data", border_style="magenta")
            )

            self.layout["large_transactions"].update(
                Panel(large_transaction_table, title="Large BTC Transactions", subtitle="Transactions > 1 Mill in BTC", border_style="purple")
            )

            self.console.clear()
            self.console.print(self.layout)
            time.sleep(10)  # Refresh every 10 seconds

# Ensure to disable logging output in the console to prevent flickering
import logging
logging.disable(logging.CRITICAL)
