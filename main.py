import json
import time
import logging
from data_provider import DataProvider
from strategies import Strategy
from telegram_notifier import TelegramNotifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("generator.log"),
        logging.StreamHandler()
    ]
)

import os

def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Override with environment variables if present
    env_token = os.environ.get("TELEGRAM_TOKEN")
    env_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if env_token:
        config['telegram']['token'] = env_token
    if env_chat_id:
        config['telegram']['chat_id'] = env_chat_id

    return config

def main():
    logging.info("Starting Trading Signal Generator...")
    config = load_config()

    data_provider = DataProvider(config)
    strategy_evaluator = Strategy(config)

    token = config['telegram'].get('token')
    chat_id = config['telegram'].get('chat_id')

    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN":
        logging.error("Telegram Token not configured. Please set TELEGRAM_TOKEN env var or update config.json")
        return

    notifier = TelegramNotifier(token, chat_id)

    # Send initial test signal
    notifier.send_test_signal()

    # Track last signals to avoid spamming
    last_signals = {}

    while True:
        try:
            # Refresh config in case it was changed
            config = load_config()
            tickers = config.get('tickers', [])
            interval_min = config.get('check_frequency_minutes', 5)
            tp_sl_ratio = config.get('tp_sl_ratio', 2.0)

            logging.info(f"Checking {len(tickers)} tickers...")

            for ticker in tickers:
                symbol = ticker['symbol']
                exchange = ticker['exchange']
                screener = ticker['screener']

                indicators = data_provider.get_indicators(symbol, exchange, screener)
                if not indicators:
                    continue

                signals = strategy_evaluator.get_signal(indicators)

                for strategy_name, direction in signals.items():
                    signal_key = f"{symbol}_{strategy_name}"

                    # Only send if the direction changed or if it's a new signal
                    if last_signals.get(signal_key) != direction:
                        logging.info(f"New Signal: {symbol} - {strategy_name} - {direction}")
                        notifier.send_signal(
                            symbol,
                            direction,
                            strategy_name,
                            indicators,
                            tp_sl_ratio
                        )
                        last_signals[signal_key] = direction

            logging.info(f"Sleeping for {interval_min} minutes...")
            time.sleep(interval_min * 60)

        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            time.sleep(60) # Wait a minute before retrying

if __name__ == "__main__":
    main()
