#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
자동화 모드 실행 스크립트
"""

import time
from loguru import logger
from strategy.trading_strategy import TradingStrategy

def run_automated_mode():
    """자동화 모드 실행"""
    logger.info("자동화 모드 시작")
    
    strategy = TradingStrategy()
    if not strategy.connect():
        logger.error("API 연결 실패")
        return
    
    try:
        # 예시 관심종목 추가 (실제 사용 시 설정 필요)
        example_stocks = ['005930', '000660', '035420']  # 삼성전자, SK하이닉스, NAVER
        for stock in example_stocks:
            strategy.add_to_watchlist(stock)
        
        logger.info(f"관심종목 설정: {strategy.watchlist}")
        
        while True:
            logger.info("전략 실행 중..")
            strategy.run_strategy_on_watchlist()
            
            # 포트폴리오 요약 출력
            summary = strategy.get_portfolio_summary()
            logger.info(f"포트폴리오 요약: {summary}")
            
            # 5분 대기
            time.sleep(300)
            
    except KeyboardInterrupt:
        logger.info("자동화 모드 종료")
    finally:
        strategy.disconnect()

if __name__ == "__main__":
    # 독립 실행을 위한 설정
    import sys
    import os
    
    # 프로젝트 루트 디렉토리를 Python 경로에 추가
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    from utils.logging_setup import setup_logging
    from utils.config_check import check_configuration
    from utils.connection_test import test_connection
    
    # 로깅 설정
    setup_logging()
    
    # 설정 확인
    if not check_configuration():
        sys.exit(1)
    
    # 연결 테스트
    if not test_connection():
        logger.error("API 연결 테스트 실패")
        sys.exit(1)
    
    # 자동화 모드 실행
    run_automated_mode() 