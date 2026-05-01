import requests
import logging

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def send_message(self, text):
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error sending Telegram message: {e}")
            return None

    def send_signal(self, symbol, direction, strategy, indicators, tp_sl_ratio):
        """
        Sends a formatted trading signal.
        """
        close = indicators.get("close")
        # Simple SL/TP calculation (example)
        # In a real scenario, we might use ATR for SL
        atr = indicators.get("ATR", close * 0.01) # fallback to 1%

        if direction == "BUY":
            sl = close - atr
            tp = close + (atr * tp_sl_ratio)
            emoji = "🚀"
        else:
            sl = close + atr
            tp = close - (atr * tp_sl_ratio)
            emoji = "📉"

        message = (
            f"{emoji} *NEW SIGNAL: {symbol}*\n\n"
            f"Direction: *{direction}*\n"
            f"Strategy: {strategy}\n"
            f"Entry Price: `{close:.5f}`\n"
            f"Take Profit: `{tp:.5f}`\n"
            f"Stop Loss: `{sl:.5f}`\n"
            f"TP/SL Ratio: {tp_sl_ratio}\n\n"
            f"Indicators:\n"
            f"- RSI: {indicators.get('RSI'):.2f}\n"
            f"- MACD: {indicators.get('MACD.macd'):.5f}\n"
            f"- EMA9: {indicators.get('EMA9'):.5f}"
        )
        return self.send_message(message)

    def send_test_signal(self):
        return self.send_message("🔔 *Telegram Integration Test*: Connection successful! Signal generator is ready.")
