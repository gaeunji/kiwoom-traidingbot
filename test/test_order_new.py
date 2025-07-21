#!/usr/bin/env python
"""
?��?증권 API 주문 처리 ?�스???�크립트 (?�로??API)
"""

import sys
import os
from loguru import logger
from kiwoom import OrderHandler, TokenManager

def setup_logging():
    """로깅 ?�정"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def test_order_handler():
    """주문 처리 ?�스??""
    logger.info("=== 주문 처리 ?�스???�작 ===")
    
    order_handler = OrderHandler()
    
    if not order_handler.connect():
        logger.error("??주문 처리 ?�결 ?�패")
        return False
    
    logger.success("??주문 처리 ?�결 ?�공")
    
    try:
        # 1. ?�결 ?�태 ?�인
        logger.info("1. ?�결 ?�태 ?�인")
        status = order_handler.get_connection_status()
        logger.info(f"?�결 ?�태: {status}")
        
        # 2. ?�큰 ?�태 ?�인
        logger.info("2. ?�큰 ?�태 ?�인")
        token_manager = order_handler.token_manager
        if token_manager.is_token_valid():
            logger.success("???�큰 ?�효???�인 ?�공")
            auth_header = token_manager.get_authorization_header()
            logger.info(f"Authorization ?�더: {auth_header[:30]}...")
        else:
            logger.warning("?�️ ?�큰???�효?��? ?�습?�다.")
        
        # 3. 매수 주문 ?��??�이??(?�제 주문?� ?��? ?�음)
        logger.info("3. 매수 주문 ?��??�이??)
        logger.info("  ?�제 주문?� ?�험?��?�??��??�이?�만 진행?�니??")
        
        # ?�스?�용 주문 ?�이??
        test_buy_order = {
            'stock_code': '005930',  # ?�성?�자
            'quantity': 1,           # 1�?
            'price': 0,              # ?�장가
            'trade_type': '3'        # ?�장가
        }
        
        logger.info(f"  ?�스??매수 주문 ?�이?? {test_buy_order}")
        logger.info("  ?�제 매수 주문???�하?�면 주석???�제?�세??")
        
        # ?�제 매수 주문???�할 경우 ?�래 주석 ?�제
        # success, message = order_handler.place_buy_order(
        #     test_buy_order['stock_code'],
        #     test_buy_order['quantity'],
        #     test_buy_order['price'],
        #     test_buy_order['trade_type']
        # )
        # if success:
        #     logger.success(f"??매수 주문 ?�공: {message}")
        # else:
        #     logger.error(f"??매수 주문 ?�패: {message}")
        
        # 4. 매도 주문 ?��??�이??(?�제 주문?� ?��? ?�음)
        logger.info("4. 매도 주문 ?��??�이??)
        logger.info("  ?�제 주문?� ?�험?��?�??��??�이?�만 진행?�니??")
        
        # ?�스?�용 주문 ?�이??
        test_sell_order = {
            'stock_code': '005930',  # ?�성?�자
            'quantity': 1,           # 1�?
            'price': 0,              # ?�장가
            'trade_type': '3'        # ?�장가
        }
        
        logger.info(f"  ?�스??매도 주문 ?�이?? {test_sell_order}")
        logger.info("  ?�제 매도 주문???�하?�면 주석???�제?�세??")
        
        # ?�제 매도 주문???�할 경우 ?�래 주석 ?�제
        # success, message = order_handler.place_sell_order(
        #     test_sell_order['stock_code'],
        #     test_sell_order['quantity'],
        #     test_sell_order['price'],
        #     test_sell_order['trade_type']
        # )
        # if success:
        #     logger.success(f"??매도 주문 ?�공: {message}")
        # else:
        #     logger.error(f"??매도 주문 ?�패: {message}")
        
        # 5. ?�합 주문 ?�수 ?�스??
        logger.info("5. ?�합 주문 ?�수 ?�스??)
        logger.info("  ?�합 주문 ?�수???�라미터 검증을 ?�스?�합?�다.")
        
        # ?�효?��? ?��? 주문 ?�???�스??
        success, message = order_handler.place_order('005930', 'invalid', 1, 0)
        logger.info(f"  ?�못??주문 ?�???�스?? {success}, {message}")
        
        # 6. 주문 ?�효??검??
        logger.info("6. 주문 ?�효??검??)
        
        # ?�못??종목 코드 ?�스??
        success, message = order_handler.place_order('INVALID', 'buy', 1, 0)
        logger.info(f"  ?�못??종목 코드 ?�스?? {success}, {message}")
        
        # ?�못???�량 ?�스??
        success, message = order_handler.place_order('005930', 'buy', -1, 0)
        logger.info(f"  ?�못???�량 ?�스?? {success}, {message}")
        
        # ?�못??가�??�스??
        success, message = order_handler.place_order('005930', 'buy', 1, -1000)
        logger.info(f"  ?�못??가�??�스?? {success}, {message}")
        
    except Exception as e:
        logger.error(f"??주문 처리 ?�스??�??�류: {e}")
        return False
    finally:
        order_handler.disconnect()
    
    return True

def test_order_parameters():
    """주문 ?�라미터 ?�스??""
    logger.info("=== 주문 ?�라미터 ?�스???�작 ===")
    
    order_handler = OrderHandler()
    
    if not order_handler.connect():
        logger.error("??주문 처리 ?�결 ?�패")
        return False
    
    logger.success("??주문 처리 ?�결 ?�공")
    
    try:
        # 1. 지?��? 매수 ?�스??
        logger.info("1. 지?��? 매수 ?�스??)
        logger.info("  지?��? 매수 주문 ?�라미터�??�스?�합?�다.")
        
        # 지?��? 매수 주문 ?�이??
        limit_buy_data = {
            'stock_code': '005930',  # ?�성?�자
            'quantity': 1,           # 1�?
            'price': 70000,          # 70,000??지?��?
            'trade_type': '1'        # 지?��?
        }
        
        logger.info(f"  지?��? 매수 ?�이?? {limit_buy_data}")
        logger.info("  ?�제 주문???�하?�면 주석???�제?�세??")
        
        # ?�제 지?��? 매수 주문???�할 경우 ?�래 주석 ?�제
        # success, message = order_handler.place_buy_order(
        #     limit_buy_data['stock_code'],
        #     limit_buy_data['quantity'],
        #     limit_buy_data['price'],
        #     limit_buy_data['trade_type']
        # )
        # if success:
        #     logger.success(f"??지?��? 매수 주문 ?�공: {message}")
        # else:
        #     logger.error(f"??지?��? 매수 주문 ?�패: {message}")
        
        # 2. ?�장가 매수 ?�스??
        logger.info("2. ?�장가 매수 ?�스??)
        logger.info("  ?�장가 매수 주문 ?�라미터�??�스?�합?�다.")
        
        # ?�장가 매수 주문 ?�이??
        market_buy_data = {
            'stock_code': '005930',  # ?�성?�자
            'quantity': 1,           # 1�?
            'price': 0,              # ?�장가
            'trade_type': '3'        # ?�장가
        }
        
        logger.info(f"  ?�장가 매수 ?�이?? {market_buy_data}")
        logger.info("  ?�제 주문???�하?�면 주석???�제?�세??")
        
        # ?�제 ?�장가 매수 주문???�할 경우 ?�래 주석 ?�제
        # success, message = order_handler.place_buy_order(
        #     market_buy_data['stock_code'],
        #     market_buy_data['quantity'],
        #     market_buy_data['price'],
        #     market_buy_data['trade_type']
        # )
        # if success:
        #     logger.success(f"???�장가 매수 주문 ?�공: {message}")
        # else:
        #     logger.error(f"???�장가 매수 주문 ?�패: {message}")
        
        # 3. ?�속 조회 ?�라미터 ?�스??
        logger.info("3. ?�속 조회 ?�라미터 ?�스??)
        logger.info("  ?�속 조회 ?�라미터�??�스?�합?�다.")
        
        # ?�속 조회 ?�라미터
        cont_params = {
            'stock_code': '005930',
            'quantity': 1,
            'price': 0,
            'trade_type': '3',
            'cont_yn': 'Y',
            'next_key': 'test_key'
        }
        
        logger.info(f"  ?�속 조회 ?�라미터: {cont_params}")
        
    except Exception as e:
        logger.error(f"??주문 ?�라미터 ?�스??�??�류: {e}")
        return False
    finally:
        order_handler.disconnect()
    
    return True

def main():
    """메인 ?�스???�수"""
    setup_logging()
    
    logger.info("?? ?��?증권 API 주문 처리 ?�스???�작 (?�로??API)")
    
    # ?�경 변???�인
    required_vars = ['KIWOOM_APP_KEY', 'KIWOOM_APP_SECRET', 'ACCOUNT_NUMBER']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"???�수 ?�경 변?��? ?�정?��? ?�았?�니?? {', '.join(missing_vars)}")
        logger.error("?�� .env ?�일???�성?�고 ?�요???�보�??�력?�주?�요.")
        return False
    
    logger.success("???�경 변???�정 ?�인 ?�료")
    
    # ?�스???�행
    tests = [
        ("주문 처리", test_order_handler),
        ("주문 ?�라미터", test_order_parameters),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"?�스?? {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"??{test_name} ?�스??�??�외 발생: {e}")
            results.append((test_name, False))
    
    # 결과 ?�약
    logger.info(f"\n{'='*50}")
    logger.info("?�스??결과 ?�약")
    logger.info(f"{'='*50}")
    
    success_count = 0
    for test_name, result in results:
        status = "???�공" if result else "???�패"
        logger.info(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    logger.info(f"\n?�체 ?�스?? {len(results)}�?�?{success_count}�??�공")
    
    if success_count == len(results):
        logger.success("?�� 모든 ?�스?��? ?�공?�습?�다!")
        logger.success("?��?증권 API 주문 처리가 ?�상?�으�??�동?�니??")
        return True
    else:
        logger.warning("?�️ ?��? ?�스?��? ?�패?�습?�다.")
        logger.warning("?�패???�스?��? ?�인?�고 문제�??�결?�주?�요.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
