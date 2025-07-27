import os
from datetime import datetime
from typing import List, Optional, Dict

from loguru import logger

from .base import BaseStrategy
from kiwoom import KiwoomConnector, OrderHandler
from utils.chart_api import get_daily_chart, get_weekly_chart
from service.portfolio_service import PortfolioService


class SimpleMAStrategy(BaseStrategy):
    """
    단순 이동평균 전략
    - timeframe: 'daily' 또는 'weekly'
    - 골든크로스 시 매수, 데드크로스 시 매도
    """

    def __init__(
        self,
        watchlist: Optional[List[str]] = None,
        short_window: int = 50,
        long_window: int = 200,
        timeframe: str = "daily",
    ):
        # 환경변수에서 토큰 로드
        self.token = os.getenv("MY_ACCESS_TOKEN")
        if not self.token:
            logger.warning("환경변수 MY_ACCESS_TOKEN이 설정되지 않았습니다.")
        # API 커넥터 및 주문 핸들러 초기화
        self.api = KiwoomConnector()
        self.order_handler = OrderHandler()
        
        # 포트폴리오 서비스 초기화
        self.portfolio_service = PortfolioService(self.api)

        # 전략 파라미터 설정
        self.watchlist = watchlist or ["005930"]
        self.short_window = short_window
        self.long_window = long_window
        self.timeframe = timeframe.lower()
        if self.timeframe not in ("daily", "weekly"):
            raise ValueError("timeframe은 'daily' 또는 'weekly'만 지원합니다.")

    def connect(self) -> bool:
        logger.info("SimpleMAStrategy: API 연결 시도")
        return self.api.connect()

    def run(self):
        # 현재 날짜를 YYYYMMDD 형식으로
        base_dt = datetime.now().strftime("%Y%m%d")

        for code in self.watchlist:
            params = {
                "stk_cd": code,
                "base_dt": base_dt,
                "upd_stkpc_tp": "1",
            }

            # 차트 데이터 조회
            try:
                if self.timeframe == "daily":
                    df = get_daily_chart(self.token, params)
                else:
                    df = get_weekly_chart(self.token, params)
            except Exception as e:
                logger.error(f"{code}: 차트 조회 실패 → {e}")
                continue

            # 데이터 유효성 검사
            if df is None or df.empty:
                logger.warning(f"{code}: {self.timeframe} 차트 데이터가 없습니다.")
                continue
            if "close" not in df.columns:
                logger.warning(f"{code}: 'close' 컬럼이 없습니다.")
                continue

            # 최소 데이터 개수 검사
            min_len = max(self.short_window, self.long_window) + 2
            if len(df) < min_len:
                logger.warning(
                    f"{code}: 데이터 개수({len(df)})가 부족합니다. 최소 {min_len}개 필요."
                )
                continue

            # 이동평균 계산
            df["sma_short"] = df["close"].rolling(self.short_window).mean()
            df["sma_long"] = df["close"].rolling(self.long_window).mean()

            # 직전일 대비 신호 판정
            prev_short = df["sma_short"].iloc[-2]
            prev_long = df["sma_long"].iloc[-2]
            curr_short = df["sma_short"].iloc[-1]
            curr_long = df["sma_long"].iloc[-1]

            # 매매 실행
            if prev_short <= prev_long and curr_short > curr_long:
                logger.info(f"{code}: 골든크로스 → 매수")
                self.order_handler.buy(code, qty=1)
            elif prev_short >= prev_long and curr_short < curr_long:
                logger.info(f"{code}: 데드크로스 → 매도")
                self.order_handler.sell(code, qty=1)

    def disconnect(self):
        logger.info("SimpleMAStrategy: API 연결 해제")
        self.api.disconnect()

    def get_current_price(self, stock_code: str) -> Optional[float]:
        """
        현재가 조회
        """
        return self.portfolio_service._get_current_price(stock_code)

    @property
    def api_connector(self):
        """API 커넥터 인스턴스 반환"""
        return self.api

    def add_to_watchlist(self, stock_code: str):
        """관심종목 추가"""
        if stock_code not in self.watchlist:
            self.watchlist.append(stock_code)
            logger.info(f"관심종목 추가: {stock_code}")
        else:
            logger.warning(f"이미 관심종목에 존재: {stock_code}")

    def remove_from_watchlist(self, stock_code: str):
        """관심종목 제거"""
        if stock_code in self.watchlist:
            self.watchlist.remove(stock_code)
            logger.info(f"관심종목 제거: {stock_code}")
        else:
            logger.warning(f"관심종목에 존재하지 않음: {stock_code}")

    def get_watchlist_prices(self) -> Dict[str, float]:
        """관심종목 현재가 조회"""
        return self.portfolio_service.get_watchlist_prices(self.watchlist)

    def get_account_summary(self) -> Optional[Dict]:
        """계좌 잔고 요약 정보 조회"""
        return self.portfolio_service.get_account_summary()

    def get_portfolio_summary(self) -> Dict:
        """포트폴리오 요약 정보 조회"""
        return self.portfolio_service.get_portfolio_summary()

    def run_strategy_on_watchlist(self):
        """관심종목에 대해 전략 실행"""
        logger.info(f"관심종목 {len(self.watchlist)}개에 대해 전략 실행")
        self.run()


