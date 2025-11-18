import pandas as pd

def format_status(self) -> str:
    if not self.ready_to_trade:
        return 'Market connectors are not ready.'
    lines = []
    if self.all_candles_ready:
        lines.extend(['\n############################################ Market Data ############################################\n'])
        for candles in [self.eth_1w_candles, self.eth_1m_candles, self.eth_1h_candles]:
            candles_df = candles.candles_df
            candles_df.ta.rsi(length=14, append=True)
            candles_df.ta.bbands(length=20, std=2, append=True)
            candles_df.ta.ema(length=14, offset=None, append=True)
            candles_df['timestamp'] = pd.to_datetime(candles_df['timestamp'], unit='ms')
            lines.extend([f'Candles: {candles.name} | Interval: {candles.interval}'])
            lines.extend(['    ' + line for line in candles_df.tail().to_string(index=False).split('\n')])
            lines.extend(['\n-----------------------------------------------------------------------------------------------------------\n'])
    else:
        lines.extend(['', '  No data collected.'])
    return '\n'.join(lines)