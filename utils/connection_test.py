#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API 연결 테스트 유틸리티
"""

from loguru import logger
from kiwoom import KiwoomConnector, MarketDataAPI

def test_connection():
    """API 연결 테스트"""
    logger.info("API 연결 테스트 중..")
    
    connector = KiwoomConnector()
    if connector.connect():
        status = connector.get_connection_status()
        logger.info(f"연결 상태: {status}")
        
        # 계좌평가잔고내역 조회 테스트
        account_balance = connector.get_account_balance()
        if account_balance:
            logger.info("계좌평가잔고내역 조회 성공")
            logger.debug(f"응답 데이터: {account_balance}")
        else:
            logger.warning("계좌평가잔고내역 조회 실패")
        
        # 거래량상위 종목 조회 테스트
        market_api = MarketDataAPI()
        volume_stocks = market_api.get_top_volume_stocks(limit=5)
        if volume_stocks:
            logger.info("거래량상위 종목 조회 성공")
            logger.debug(f"조회된 종목 수: {len(volume_stocks)}")
        else:
            logger.warning("거래량상위 종목 조회 실패")
        
        connector.disconnect()
        return True
    else:
        logger.error("API 연결 실패")
        return False 