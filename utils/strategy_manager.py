#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TradingStrategy Context Manager
"""

from contextlib import contextmanager
from typing import Optional, Callable, Type
from loguru import logger
# from strategy.simple_ma import SimpleMAStrategy  # 직접 import 제거 (circular import 방지)

@contextmanager
def with_strategy(strategy_cls: Type = None, *args, **kwargs):
    """
    모듈화된 전략 Context Manager
    기본값은 SimpleMAStrategy이나, circular import 방지를 위해 내부에서 import
    """
    if strategy_cls is None:
        from strategy.simple_ma import SimpleMAStrategy
        strategy_cls = SimpleMAStrategy
    strategy = strategy_cls(*args, **kwargs)
    try:
        if not strategy.connect():
            logger.error("API 연결 실패")
            raise ConnectionError("API 연결에 실패했습니다.")
        logger.info(f"{strategy_cls.__name__} 연결 성공")
        yield strategy
    except Exception as e:
        logger.error(f"{strategy_cls.__name__} 실행 중 오류: {e}")
        raise
    finally:
        strategy.disconnect()
        logger.info(f"{strategy_cls.__name__} 연결 해제")

def run_with_strategy(func: Callable, strategy_cls: Type = None, error_handler: Optional[Callable[[Exception], None]] = None, *args, **kwargs):
    """
    모듈화된 전략과 함께 함수 실행하는 헬퍼 함수
    """
    with with_strategy(strategy_cls, *args, **kwargs) as strategy:
        try:
            func(strategy)
        except Exception as e:
            logger.error(f"전략 실행 중 오류: {e}")
            if error_handler:
                error_handler(e)
            else:
                raise 