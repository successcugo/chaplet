import logging
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import logging
try:
    from tvdatafeed import TvDatafeed, Interval as TvInterval
except ImportError:
    TvDatafeed = None

class DataProvider:
    def __init__(self, config):
        self.config = config
        self.provider_type = config.get("data_provider", "tradingview-ta")
        self.tv = None
        if self.provider_type == "tvdatafeed" and TvDatafeed:
            try:
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
            # tvdatafeed returns a dataframe
            # We would need to calculate indicators manually here if not provided by TV
            # For simplicity, if using tvdatafeed, we'll try to map common values
            data = self.tv.get_hist(symbol=symbol, exchange=exchange, n_bars=100)
            if data is not None and not data.empty:
                # Basic mock of indicators dict for the strategy
                indicators = {
                    "close": data['close'].iloc[-1],
                    "open": data['open'].iloc[-1],
                    "high": data['high'].iloc[-1],
                    "low": data['low'].iloc[-1],
                }
                # In a real scenario, we'd use talib or pandas_ta here
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
            return self.get_indicators_tv(symbol, exchange, interval)
