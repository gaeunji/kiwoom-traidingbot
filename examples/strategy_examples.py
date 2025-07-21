#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TradingStrategy Context Manager 사용 예제
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from utils import with_strategy, run_with_strategy

def example_1_context_manager():
    """예제 1: Context Manager 직접 사용"""
    logger.info("=== 예제 1: Context Manager 직접 사용 ===")
    
    try:
        with with_strategy() as strategy:
            # 관심종목 추가
            strategy.add_to_watchlist('005930')  # 삼성전자
            strategy.add_to_watchlist('000660')  # SK하이닉스
            
            # 현재가 조회
            prices = strategy.get_watchlist_prices()
            for code, price in prices.items():
                logger.info(f"{code}: {price:,}원")
            
            # 포트폴리오 요약
            summary = strategy.get_portfolio_summary()
            logger.info(f"포트폴리오: {summary}")
            
    except Exception as e:
        logger.error(f"예제 1 실행 중 오류: {e}")

def example_2_helper_function():
    """예제 2: 헬퍼 함수 사용"""
    logger.info("=== 예제 2: 헬퍼 함수 사용 ===")
    
    def my_strategy(strategy):
        """사용자 정의 전략"""
        # 관심종목 설정
        watchlist = ['005930', '000660', '035420']
        for stock in watchlist:
            strategy.add_to_watchlist(stock)
        
        # 전략 실행
        strategy.run_strategy_on_watchlist()
        
        # 결과 출력
        summary = strategy.get_portfolio_summary()
        logger.info(f"전략 실행 결과: {summary}")
    
    def error_handler(error):
        """오류 처리 함수"""
        logger.error(f"전략 실행 중 오류 발생: {error}")
    
    # 헬퍼 함수로 전략 실행
    run_with_strategy(my_strategy, error_handler)

def example_3_multiple_strategies():
    """예제 3: 여러 전략 실행"""
    logger.info("=== 예제 3: 여러 전략 실행 ===")
    
    def strategy_1(strategy):
        """전략 1: 삼성전자만 관심종목에 추가"""
        strategy.add_to_watchlist('005930')
        prices = strategy.get_watchlist_prices()
        logger.info(f"전략 1 결과: {prices}")
    
    def strategy_2(strategy):
        """전략 2: SK하이닉스만 관심종목에 추가"""
        strategy.add_to_watchlist('000660')
        prices = strategy.get_watchlist_prices()
        logger.info(f"전략 2 결과: {prices}")
    
    def strategy_3(strategy):
        """전략 3: NAVER만 관심종목에 추가"""
        strategy.add_to_watchlist('035420')
        prices = strategy.get_watchlist_prices()
        logger.info(f"전략 3 결과: {prices}")
    
    # 여러 전략 순차 실행
    strategies = [strategy_1, strategy_2, strategy_3]
    
    for i, strategy_func in enumerate(strategies, 1):
        logger.info(f"전략 {i} 실행 중...")
        try:
            run_with_strategy(strategy_func)
        except Exception as e:
            logger.error(f"전략 {i} 실행 실패: {e}")

def example_4_error_handling():
    """예제 4: 오류 처리"""
    logger.info("=== 예제 4: 오류 처리 ===")
    
    def problematic_strategy(strategy):
        """문제가 있는 전략 (의도적으로 오류 발생)"""
        # 존재하지 않는 메서드 호출
        strategy.non_existent_method()
    
    def custom_error_handler(error):
        """커스텀 오류 처리"""
        logger.warning(f"전략 실행 중 오류가 발생했지만 계속 진행: {error}")
    
    # 오류 처리와 함께 실행
    run_with_strategy(problematic_strategy, custom_error_handler)
    logger.info("오류 처리 후 정상적으로 계속 실행됨")

def main():
    """메인 함수"""
    logger.info("TradingStrategy Context Manager 예제 시작")
    
    examples = [
        ("Context Manager 직접 사용", example_1_context_manager),
        ("헬퍼 함수 사용", example_2_helper_function),
        ("여러 전략 실행", example_3_multiple_strategies),
        ("오류 처리", example_4_error_handling),
    ]
    
    for name, example_func in examples:
        try:
            logger.info(f"\n{'='*50}")
            example_func()
            logger.info(f"✅ {name} 완료")
        except Exception as e:
            logger.error(f"❌ {name} 실패: {e}")
    
    logger.info("\n모든 예제 실행 완료")

if __name__ == "__main__":
    main() 