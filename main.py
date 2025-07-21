#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 REST API 주식 매매 테스트
메인 실행 진입점
"""

import sys
import time
import argparse
from loguru import logger
from config.settings import settings
from kiwoom import KiwoomConnector
from strategy.trading_strategy import TradingStrategy
# from data import StockRanking  # 임시로 주석 처리

def setup_logging():
    """로깅 설정"""
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    logger.add(
        settings.LOG_FILE,
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="1 day",
        retention="30 days"
    )

def check_configuration():
    """설정 확인"""
    logger.info("설정 확인 중..")
    
    required_settings = [
        ('KIWOOM_APP_KEY', settings.KIWOOM_APP_KEY),
        ('KIWOOM_APP_SECRET', settings.KIWOOM_APP_SECRET),
        ('ACCOUNT_NUMBER', settings.ACCOUNT_NUMBER)
    ]
    
    missing_settings = []
    for name, value in required_settings:
        if not value:
            missing_settings.append(name)
    
    if missing_settings:
        logger.error(f"필수 설정이 누락되었습니다: {', '.join(missing_settings)}")
        logger.error("config/settings.py 또는 .env 파일을 확인해주세요.")
        return False
    
    logger.info("설정 확인 완료")
    return True

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
        from kiwoom import MarketDataAPI
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

def run_interactive_mode():
    """대화형 모드 실행"""
    logger.info("대화형 모드 시작")
    
    strategy = TradingStrategy()
    if not strategy.connect():
        logger.error("API 연결 실패")
        return
    
    try:
        while True:
            print("\n=== 키움증권 주식 매매 테스트 ===")
            print("1. 관심종목 추가")
            print("2. 관심종목 제거")
            print("3. 현재가 조회")
            print("4. 포트폴리오 요약")
            print("5. 전략 실행")
            print("6. 연결 상태 확인")
            print("7. 계좌 잔고 조회")
            print("8. 거래량상위 종목 조회")
            print("9. 캐시 통계")
            print("0. 종료")
            
            choice = input("\n선택하세요: ").strip()
            
            if choice == '1':
                stock_code = input("종목 코드를 입력하세요: ").strip()
                strategy.add_to_watchlist(stock_code)
                
            elif choice == '2':
                stock_code = input("종목 코드를 입력하세요: ").strip()
                strategy.remove_from_watchlist(stock_code)
                
            elif choice == '3':
                if strategy.watchlist:
                    prices = strategy.get_watchlist_prices()
                    print("\n=== 관심종목 현재가 ===")
                    for code, price in prices.items():
                        print(f"{code}: {price:,}원")
                else:
                    print("관심종목이 없습니다.")
                    
            elif choice == '4':
                summary = strategy.get_portfolio_summary()
                print("\n=== 포트폴리오 요약 ===")
                print(f"총 자산가치: {summary['total_value']:,.0f}원")
                print(f"총 손익: {summary['total_pnl']:,.0f}원")
                print(f"총 수익률: {summary['total_profit_rate']:.2f}%")
                print(f"보유 종목 수: {len(summary['positions'])}개")
                print(f"사용 가능한 현금: {summary['available_cash']:,.0f}원")
                print(f"총 매입금액: {summary['total_purchase_amount']:,.0f}원")
                print(f"총 대출금액: {summary['total_loan_amount']:,.0f}원")
                
            elif choice == '5':
                print("전략 실행 중..")
                strategy.run_strategy_on_watchlist()
                
            elif choice == '6':
                status = strategy.get_connection_status()
                print("\n=== 연결 상태 ===")
                for key, value in status.items():
                    print(f"{key}: {value}")
                    
            elif choice == '7':
                print("\n=== 계좌 잔고 조회 ===")
                account_summary = strategy.get_account_summary()
                if account_summary:
                    print("계좌 잔고 정보:")
                    print(f"예수금자산금액: {account_summary['cash_bal']:,.0f}원")
                    print(f"총평가금액: {account_summary['total_value']:,.0f}원")
                    print(f"총평가손익: {account_summary['total_pnl']:,.0f}원")
                    print(f"총수익률: {account_summary['total_profit_rate']:.2f}%")
                    print(f"총매입금액: {account_summary['total_purchase_amount']:,.0f}원")
                    print(f"총대출금액: {account_summary['total_loan_amount']:,.0f}원")
                    
                    if account_summary['positions']:
                        print(f"\n보유 종목 ({len(account_summary['positions'])}개):")
                        for i, position in enumerate(account_summary['positions'][:5]):  # 상위 5개만 표시
                            print(f"  {i+1}. {position['stk_nm']} ({position['stk_cd']})")
                            print(f"     보유수량: {int(position['rmnd_qty'])}주")
                            print(f"     현재가: {int(position['cur_prc']):,}원")
                            print(f"     평가손익: {int(position['evltv_prft']):,}원 ({position['prft_rt']}%)")
                        if len(account_summary['positions']) > 5:
                            print(f"  ... 외 {len(account_summary['positions']) - 5}개 종목")
                else:
                    print("계좌 잔고 조회 실패")
                    
            elif choice == '8':
                print("\n=== 거래량상위 종목 조회 ===")
                print("이 기능은 현재 사용할 수 없습니다.")
                print("kiwoom.MarketDataAPI를 직접 사용하세요.")
                # ranking = StockRanking()
                # if ranking.connect():
                #     try:
                #         print("시장 구분 선택:")
                #         print("000: 전체, 001: 코스피, 101: 코스닥")
                #         market_type = input("시장 구분 (기본: 000): ").strip() or "000"
                #         limit = int(input("조회할 종목 수(기본: 20): ") or "20")
                #         
                #         stocks = ranking.get_volume_ranking(limit=limit, market_type=market_type)
                #         if stocks:
                #             market_names = {'000': '전체', '001': '코스피', '101': '코스닥'}
                #             market_name = market_names.get(market_type, market_type)
                #             print(f"\n{market_name} 거래량상위 {len(stocks)}개 종목:")
                #             for i, stock in enumerate(stocks, 1):
                #                 print(f"{i:2d}. {stock['stock_name']} ({stock['stock_code']})")
                #                 print(f"    현재가: {stock['current_price']:,}원 거래량: {stock['volume']:,}")
                #                 print(f"    등락률: {stock['change_rate']:+.2f}%, 거래대금: {stock.get('trade_amount', 0):,}원")
                #                 if 'rank' in stock:
                #                     print(f"    순위: {stock['rank']}위")
                #         else:
                #             print("거래량상위 종목 조회 실패")
                #     finally:
                #         ranking.disconnect()
                # else:
                #     print("API 연결 실패")
                    
            elif choice == '9':
                print("\n=== 캐시 통계 ===")
                print("이 기능은 현재 사용할 수 없습니다.")
                # ranking = StockRanking()
                # if ranking.connect():
                #     try:
                #         stats = ranking.get_ranking_statistics()
                #         print("캐시 정보:")
                #         cache_info = stats.get('cache_info', {})
                #         print(f"  캐시 디렉토리: {cache_info.get('cache_dir', 'N/A')}")
                #         print(f"  총 파일 수: {cache_info.get('total_files', 0)}")
                #         print(f"  캐시 상태:")
                #         for key, valid in stats.get('cache_status', {}).items():
                #             status = "유효" if valid else "만료"
                #             print(f"    {key}: {status}")
                #     finally:
                #         ranking.disconnect()
                # else:
                #     print("API 연결 실패")
                    
            elif choice == '0':
                print("프로그램을 종료합니다.")
                break
                
            else:
                print("잘못된 선택입니다.")
                
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        strategy.disconnect()

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

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='키움증권 주식 매매 테스트')
    parser.add_argument('--mode', choices=['interactive', 'automated', 'test'], 
                       default='interactive', help='실행 모드')
    parser.add_argument('--config-check', action='store_true', 
                       help='설정 확인만 실행')
    
    args = parser.parse_args()
    
    # 로깅 설정
    setup_logging()
    
    logger.info("키움증권 주식 매매 테스트 시작")
    
    # 설정 확인
    if not check_configuration():
        sys.exit(1)
    
    if args.config_check:
        logger.info("설정 확인 완료")
        return
    
    # 연결 테스트
    if not test_connection():
        logger.error("API 연결 테스트 실패")
        sys.exit(1)
    
    # 모드별 실행
    if args.mode == 'interactive':
        run_interactive_mode()
    elif args.mode == 'automated':
        run_automated_mode()
    elif args.mode == 'test':
        logger.info("테스트 모드 완료")
    
    logger.info("프로그램 종료")

if __name__ == "__main__":
    main()
