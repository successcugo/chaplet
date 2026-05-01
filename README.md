# Trading Signal Generator

A 24/7 Trading Signal Generator that monitors Crypto, Forex, and Stocks using TradingView data and sends signals to Telegram.

## Setup

1. Copy `config.json.template` to `config.json`.
2. Fill in your Telegram Bot Token and Chat ID in `config.json`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the generator:
   ```bash
   python main.py
   ```
5. (Optional) Run the management GUI:
   ```bash
   streamlit run gui.py
   ```

## Hosting on Wasmer

This project is configured for Wasmer. You can deploy it using:
```bash
wasmer deploy
```
