import pandas as pd
from typing import Type, Dict, Any
from loguru import logger
from strategy.base import BaseStrategy

class Backtester:
    """
    전략 클래스와 과거 데이터(DataFrame)를 받아 백테스트를 수행하는 모듈
    """
    def __init__(self, strategy_cls: Type[BaseStrategy], data: pd.DataFrame, **strategy_kwargs):
        self.strategy_cls = strategy_cls
        self.data = data
        self.strategy_kwargs = strategy_kwargs
        self.results = None

    def run(self) -> Dict[str, Any]:
        """
        전략 인스턴스를 생성하여 백테스트 실행
        Returns: dict (성과지표, 매매내역 등)
        """
        logger.info(f"{self.strategy_cls.__name__} 백테스트 시작")
        # 전략 인스턴스 생성 (신호 생성용)
        strategy = self.strategy_cls(**self.strategy_kwargs)
        df = self.data.copy()
        # 이동평균 파라미터 추출 (기본값: 50, 200)
        short_window = getattr(strategy, 'short_window', 50)
        long_window = getattr(strategy, 'long_window', 200)
        # 1) 이동평균 계산
        df['SMA_short'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
        df['SMA_long']  = df['Close'].rolling(window=long_window,  min_periods=1).mean()
        # 2) 신호 생성
        df['signal'] = (df['SMA_short'] > df['SMA_long']).astype(int)
        df['position'] = df['signal'].diff().fillna(0)
        # 3) 수익률 계산
        df['market_return'] = df['Close'].pct_change()
        df['strategy_return'] = df['market_return'] * df['signal'].shift(1)
        df['cum_market'] = (1 + df['market_return']).cumprod() - 1
        df['cum_strategy'] = (1 + df['strategy_return']).cumprod() - 1
        # 4) 매매 시점 기록
        trades = []
        buy_signals = df[df['position'] == 1]
        sell_signals = df[df['position'] == -1]
        
        for idx in buy_signals.index:
            trades.append({'date': idx, 'type': 'buy', 'price': df.loc[idx, 'Close']})
        for idx in sell_signals.index:
            trades.append({'date': idx, 'type': 'sell', 'price': df.loc[idx, 'Close']})
        # 5) 결과 요약
        result = {
            'final_market_return': df['cum_market'].iloc[-1],
            'final_strategy_return': df['cum_strategy'].iloc[-1],
            'trades': trades,
            'equity_curve': df[['cum_market', 'cum_strategy']]
        }
        logger.info(f"{self.strategy_cls.__name__} 백테스트 완료 (전략 수익률: {result['final_strategy_return']:.2%})")
        self.results = result
        return self.results

# 사용 예시 (simple_ma.py와 연동)
if __name__ == "__main__":
    import yfinance as yf
    from strategy.simple_ma import SimpleMAStrategy

    symbol = "AAPL"
    df = yf.download(symbol, start="2020-01-01", end="2025-07-20")

    backtester = Backtester(SimpleMAStrategy, df)
    results = backtester.run()
    print(results)
