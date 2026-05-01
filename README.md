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

## Hosting on Wasmer Edge

This project is configured for Wasmer Edge. You can deploy it using:
```bash
wasmer deploy
```

### Persistence & Secrets

- **Secrets**: For production, it is highly recommended to use environment variables for `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` instead of hardcoding them in `config.json`.
- **Persistence**: Wasmer Edge's filesystem is ephemeral. Changes made via the Streamlit GUI to `config.json` will be lost when the instance restarts. For permanent changes, update `config.json` in your repository and redeploy.
