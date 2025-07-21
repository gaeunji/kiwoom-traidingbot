#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
대화형 모드 실행 스크립트
"""

from loguru import logger
from strategy.trading_strategy import TradingStrategy

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
                    
            elif choice == '9':
                print("\n=== 캐시 통계 ===")
                print("이 기능은 현재 사용할 수 없습니다.")
                    
            elif choice == '0':
                print("프로그램을 종료합니다.")
                break
                
            else:
                print("잘못된 선택입니다.")
                
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
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
    
    # 로깅 설정
    setup_logging()
    
    # 설정 확인
    if not check_configuration():
        sys.exit(1)
    
    # 대화형 모드 실행
    run_interactive_mode() 