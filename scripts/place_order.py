#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 API 주문 처리 스크립트
OrderHandler 클래스를 사용하여 주문 처리
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from kiwoom import OrderHandler

# .env 파일 로드
load_dotenv()

def main():
    """메인 실행 함수"""
    print("키움증권 API 주문 처리")
    print("=" * 50)
    
    # OrderHandler 초기화
    order_handler = OrderHandler()
    
    # API 연결
    if not order_handler.connect():
        print("❌ API 연결에 실패했습니다.")
        print("📝 .env 파일의 설정을 확인해주세요.")
        return
    
    print("✅ API 연결 성공")
    
    # 토큰 상태 확인
    token_manager = order_handler.token_manager
    if token_manager.is_token_valid():
        print("✅ 토큰 유효성 확인 완료")
    else:
        print("⚠️ 토큰이 유효하지 않습니다. 토큰을 갱신합니다.")
        if not token_manager.refresh_token_if_needed():
            print("❌ 토큰 갱신에 실패했습니다.")
            return
    
    print()
    
    # 기본 주문 데이터
    default_stock = '005930'  # 삼성전자
    default_quantity = 1
    
    print("주문 옵션:")
    print("1. 매수 주문 (시장가)")
    print("2. 매도 주문 (시장가)")
    print("3. 지정가 매수 주문")
    print("4. 지정가 매도 주문")
    print("5. 종목 변경")
    print("6. 연결 상태 확인")
    print("7. 거래량 상위 종목 조회")
    print("8. 종료")
    print()
    
    while True:
        choice = input("선택하세요 (1-8): ").strip()
        
        try:
            if choice == '1':
                print(f"\n🚀 매수 주문 실행 (시장가) - {default_stock}")
                print("⚠️ 실제 주문 시에는 주석을 해제할 것")
                
                # 시장가 매수 주문 데이터
                buy_params = {
                    'stock_code': default_stock,
                    'quantity': default_quantity,
                    'price': 0,  # 시장가
                    'trade_type': '3'  # 시장가
                }
                
                print(f"주문 데이터: {buy_params}")
                
                # 실제 매수 주문을 원할 경우 아래 주석 해제
                # success, message = order_handler.place_buy_order(
                #     buy_params['stock_code'],
                #     buy_params['quantity'],
                #     buy_params['price'],
                #     buy_params['trade_type']
                # )
                # if success:
                #     print(f"\n✅ 매수 주문 성공: {message}")
                # else:
                #     print(f"\n❌ 매수 주문 실패: {message}")
                
            elif choice == '2':
                print(f"\n🚀 매도 주문 실행 (시장가) - {default_stock}")
                print("⚠️ 실제 주문 시에는 주석을 해제할 것")
                
                # 시장가 매도 주문 데이터
                sell_params = {
                    'stock_code': default_stock,
                    'quantity': default_quantity,
                    'price': 0,  # 시장가
                    'trade_type': '3'  # 시장가
                }
                
                print(f"주문 데이터: {sell_params}")
                
                # 실제 매도 주문을 원할 경우 아래 주석 해제
                # success, message = order_handler.place_sell_order(
                #     sell_params['stock_code'],
                #     sell_params['quantity'],
                #     sell_params['price'],
                #     sell_params['trade_type']
                # )
                # if success:
                #     print(f"\n✅ 매도 주문 성공: {message}")
                # else:
                #     print(f"\n❌ 매도 주문 실패: {message}")
                
            elif choice == '3':
                print(f"\n🚀 지정가 매수 주문 - {default_stock}")
                price = input("매수 가격을 입력하세요 (원): ").strip()
                quantity = input("매수 수량을 입력하세요 (주): ").strip()
                
                try:
                    price = int(price)
                    quantity = int(quantity)
                except ValueError:
                    print("❌ 잘못된 가격 또는 수량입니다.")
                    continue
                
                limit_buy_params = {
                    'stock_code': default_stock,
                    'quantity': quantity,
                    'price': price,
                    'trade_type': '1'  # 지정가
                }
                
                print(f"지정가 매수 주문 데이터: {limit_buy_params}")
                print("⚠️ 실제 주문을 원하시면 주석을 해제하세요.")
                
                # 실제 지정가 매수 주문을 원할 경우 아래 주석 해제
                # success, message = order_handler.place_buy_order(
                #     limit_buy_params['stock_code'],
                #     limit_buy_params['quantity'],
                #     limit_buy_params['price'],
                #     limit_buy_params['trade_type']
                # )
                # if success:
                #     print(f"\n✅ 지정가 매수 주문 성공: {message}")
                # else:
                #     print(f"\n❌ 지정가 매수 주문 실패: {message}")
                
            elif choice == '4':
                print(f"\n🚀 지정가 매도 주문 - {default_stock}")
                price = input("매도 가격을 입력하세요 (원): ").strip()
                quantity = input("매도 수량을 입력하세요 (주): ").strip()
                
                try:
                    price = int(price)
                    quantity = int(quantity)
                except ValueError:
                    print("❌ 잘못된 가격 또는 수량입니다.")
                    continue
                
                limit_sell_params = {
                    'stock_code': default_stock,
                    'quantity': quantity,
                    'price': price,
                    'trade_type': '1'  # 지정가
                }
                
                print(f"지정가 매도 주문 데이터: {limit_sell_params}")
                print("⚠️ 실제 주문을 원하시면 주석을 해제하세요.")
                
                # 실제 지정가 매도 주문을 원할 경우 아래 주석 해제
                # success, message = order_handler.place_sell_order(
                #     limit_sell_params['stock_code'],
                #     limit_sell_params['quantity'],
                #     limit_sell_params['price'],
                #     limit_sell_params['trade_type']
                # )
                # if success:
                #     print(f"\n✅ 지정가 매도 주문 성공: {message}")
                # else:
                #     print(f"\n❌ 지정가 매도 주문 실패: {message}")
                
            elif choice == '5':
                print("\n📝 종목 변경")
                new_stock = input("새로운 종목 코드를 입력하세요 (예: 005930): ").strip()
                if new_stock:
                    default_stock = new_stock
                    print(f"✅ 기본 종목이 {default_stock}로 변경되었습니다.")
                else:
                    print("❌ 종목 코드를 입력해주세요.")
                
            elif choice == '6':
                print("\n🔍 연결 상태 확인")
                status = order_handler.get_connection_status()
                print(f"연결 상태: {status}")
                
                # 토큰 정보 확인
                token_info = {
                    'has_token': token_manager.access_token is not None,
                    'is_valid': token_manager.is_token_valid(),
                    'token_type': token_manager.token_type,
                    'expires_at': token_manager.token_expires_at
                }
                print(f"토큰 정보: {token_info}")
                
            elif choice == '7':
                print("\n📊 거래량 상위 종목 조회")
                from kiwoom import MarketDataAPI
                
                market_api = MarketDataAPI()
                
                # 조회 옵션
                print("조회 옵션:")
                print("1. 전체 시장 상위 20개")
                print("2. 코스피 상위 20개")
                print("3. 코스닥 상위 20개")
                print("4. 사용자 정의")
                
                sub_choice = input("선택하세요 (1-4): ").strip()
                
                try:
                    if sub_choice == '1':
                        stocks = market_api.get_top_volume_stocks(limit=20, market_type='000')
                    elif sub_choice == '2':
                        stocks = market_api.get_top_volume_stocks(limit=20, market_type='001')
                    elif sub_choice == '3':
                        stocks = market_api.get_top_volume_stocks(limit=20, market_type='101')
                    elif sub_choice == '4':
                        limit = input("조회할 종목 수 (1-50): ").strip()
                        market = input("시장 (000:전체, 001:코스피, 101:코스닥): ").strip()
                        stocks = market_api.get_top_volume_stocks(limit=int(limit), market_type=market)
                    else:
                        print("잘못된 선택입니다.")
                        continue
                    
                    if stocks:
                        print(f"\n✅ 거래량 상위 종목 ({len(stocks)}개)")
                        print("-" * 50)
                        for i, stock in enumerate(stocks[:10]):  # 상위 10개만 표시
                            rank = stock.get('rank', i+1)
                            code = stock.get('stock_code', 'N/A')
                            name = stock.get('stock_name', 'N/A')
                            price = stock.get('current_price', 0)
                            volume = stock.get('volume', 0)
                            change_rate = stock.get('change_rate', 0)
                            
                            print(f"{rank:2d}. {code} {name}")
                            print(f"    💰 {price:,}원 | 📊 {volume:,}주 | 📈 {change_rate:+.2f}%")
                            print()
                    else:
                        print("❌ 조회 결과가 없습니다.")
                        
                except Exception as e:
                    print(f"❌ 조회 중 오류: {e}")
                
            elif choice == '8':
                print("종료합니다.")
                break
                
            else:
                print("잘못된 선택입니다.")
                
        except Exception as e:
            print(f"\n❌ 주문 처리 중 오류 발생: {e}")
        
        print("\n" + "-" * 50)
    
    # 연결 해제
    order_handler.disconnect()
    print("✅ API 연결이 해제되었습니다.")

if __name__ == '__main__':
    main() 
