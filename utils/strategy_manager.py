#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TradingStrategy Context Manager
"""

from contextlib import contextmanager
from typing import Optional, Callable
from loguru import logger
from strategy.trading_strategy import TradingStrategy

@contextmanager
def with_strategy():
    """
    TradingStrategy Context Manager
    
    사용법:
        with with_strategy() as strategy:
            strategy.add_to_watchlist('005930')
            strategy.run_strategy_on_watchlist()
    """
    strategy = TradingStrategy()
    
    try:
        # 연결 시도
        if not strategy.connect():
            logger.error("API 연결 실패")
            raise ConnectionError("API 연결에 실패했습니다.")
        
        logger.info("TradingStrategy 연결 성공")
        yield strategy
        
    except Exception as e:
        logger.error(f"TradingStrategy 실행 중 오류: {e}")
        raise
    finally:
        # 연결 해제
        strategy.disconnect()
        logger.info("TradingStrategy 연결 해제")

def run_with_strategy(func: Callable[[TradingStrategy], None], 
                     error_handler: Optional[Callable[[Exception], None]] = None):
    """
    TradingStrategy와 함께 함수 실행하는 헬퍼 함수
    
    Args:
        func: TradingStrategy를 인자로 받는 함수
        error_handler: 오류 처리 함수 (선택사항)
    
    사용법:
        def my_strategy(strategy):
            strategy.add_to_watchlist('005930')
            strategy.run_strategy_on_watchlist()
        
        run_with_strategy(my_strategy)
    """
    with with_strategy() as strategy:
        try:
            func(strategy)
        except Exception as e:
            logger.error(f"전략 실행 중 오류: {e}")
            if error_handler:
                error_handler(e)
            else:
                raise 