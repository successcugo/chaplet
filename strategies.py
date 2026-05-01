class Strategy:
    def __init__(self, config):
        self.config = config

    def check_ema_crossover(self, indicators, params):
        """
        EMA Crossover strategy.
        Buy when fast EMA crosses above slow EMA.
        Sell when fast EMA crosses below slow EMA.
        """
        # tradingview-ta provides EMA values if they are requested or standard.
        # Usually: EMA9, EMA21, EMA50, EMA100, EMA200 are available in the indicators dict
        fast_ema_key = f"EMA{params['fast_period']}"
        slow_ema_key = f"EMA{params['slow_period']}"

        fast_ema = indicators.get(fast_ema_key)
        slow_ema = indicators.get(slow_ema_key)

        if fast_ema is None or slow_ema is None:
            return None # Indicators not available

        # For a true crossover we need the previous state,
        # but tradingview-ta mostly gives the current state.
        # We can approximate by checking if it's currently above or below.
        # To be "industry leading", we should ideally have historical data,
        # but tradingview-ta analysis gives recommendations which are already calculated.

        # Alternatively, we can use the 'RECOMMENDATION' for EMA.
        if fast_ema > slow_ema:
            return "BUY"
        elif fast_ema < slow_ema:
            return "SELL"
        return "NEUTRAL"

    def check_rsi_macd_confluence(self, indicators, params):
        """
        RSI and MACD confluence strategy.
        Buy if RSI is oversold and MACD is bullish.
        Sell if RSI is overbought and MACD is bearish.
        """
        rsi = indicators.get("RSI")
        macd = indicators.get("MACD.macd")
        signal = indicators.get("MACD.signal")

        if rsi is None or macd is None or signal is None:
            return None

        # Buy condition: RSI < oversold AND MACD > Signal
        if rsi < params['rsi_oversold'] and macd > signal:
            return "BUY"
        # Sell condition: RSI > overbought AND MACD < Signal
        elif rsi > params['rsi_overbought'] and macd < signal:
            return "SELL"
        return "NEUTRAL"

    def check_bollinger_bands(self, indicators, params):
        """
        Bollinger Bands breakout strategy.
        Buy if price crosses above upper band (momentum) or touches lower band (reversal).
        Let's go with reversal for low capital/safety.
        """
        upper = indicators.get("BB.upper")
        lower = indicators.get("BB.lower")
        close = indicators.get("close")

        if upper is None or lower is None or close is None:
            return None

        if close < lower:
            return "BUY"
        elif close > upper:
            return "SELL"
        return "NEUTRAL"

    def get_signal(self, indicators):
        """
        Evaluates all enabled strategies and returns a combined signal.
        """
        signals = {}

        if self.config['strategies']['ema_crossover']['enabled']:
            sig = self.check_ema_crossover(indicators, self.config['strategies']['ema_crossover'])
            if sig and sig != "NEUTRAL":
                signals["EMA Crossover"] = sig

        if self.config['strategies']['rsi_macd_confluence']['enabled']:
            sig = self.check_rsi_macd_confluence(indicators, self.config['strategies']['rsi_macd_confluence'])
            if sig and sig != "NEUTRAL":
                signals["RSI/MACD Confluence"] = sig

        if self.config['strategies']['bollinger_bands']['enabled']:
            sig = self.check_bollinger_bands(indicators, self.config['strategies']['bollinger_bands'])
            if sig and sig != "NEUTRAL":
                signals["Bollinger Bands"] = sig

        return signals
