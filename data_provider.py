import logging
from tradingview_ta import TA_Handler, Interval
try:
    from tvdatafeed import TvDatafeed
except (ImportError, Exception):
    TvDatafeed = None

class DataProvider:
    def __init__(self, config):
        self.config = config
        self.provider_type = config.get("data_provider", "tradingview-ta")
        self.tv = None
        if self.provider_type == "tvdatafeed" and TvDatafeed:
            try:
                # tvdatafeed might still depend on pandas internally,
                # but we'll try to initialize it safely.
                self.tv = TvDatafeed()
            except Exception as e:
                logging.error(f"Failed to initialize tvdatafeed: {e}")

    def get_indicators_ta(self, symbol, exchange, screener, interval):
        try:
            handler = TA_Handler(
                symbol=symbol,
                exchange=exchange,
                screener=screener,
                interval=interval
            )
            analysis = handler.get_analysis()
            return analysis.indicators
        except Exception as e:
            logging.error(f"Error fetching TA data for {symbol}: {e}")
            return None

    def get_indicators_tv(self, symbol, exchange, interval):
        if not self.tv:
            return None
        try:
            # tvdatafeed returns a pandas dataframe by default.
            # If pandas is missing, this will likely fail.
            data = self.tv.get_hist(symbol=symbol, exchange=exchange, n_bars=1)
            if data is not None and hasattr(data, 'empty') and not data.empty:
                # Try to extract close price without needing full pandas logic if possible
                # or just use the last row.
                last_row = data.iloc[-1]
                indicators = {
                    "close": float(last_row['close']),
                    "open": float(last_row['open']),
                    "high": float(last_row['high']),
                    "low": float(last_row['low']),
                }
                return indicators
        except Exception as e:
            logging.error(f"Error fetching TV data for {symbol}: {e}")
        return None

    def get_indicators(self, symbol, exchange, screener, interval=Interval.INTERVAL_1_HOUR):
        """
        Returns a dictionary of indicators.
        """
        if self.provider_type == "tradingview-ta":
            return self.get_indicators_ta(symbol, exchange, screener, interval)
        else:
            # If we are in an environment without pandas, tvdatafeed will likely fail.
            return self.get_indicators_tv(symbol, exchange, interval)
