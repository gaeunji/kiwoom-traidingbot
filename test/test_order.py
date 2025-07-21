#!/usr/bin/env python
"""
주문 처리 ?�스???�크립트
"""

import sys
import os
from loguru import logger
from kiwoom import OrderHandler

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
        
        # 2. 주문 ?�역 조회 (?�제 주문?� ?��? ?�음)
        logger.info("2. 주문 ?�역 조회")
        order_history = order_handler.get_order_history()
        if order_history:
            logger.success(f"??주문 ?�역 조회 ?�공: {len(order_history)}�?)
            for order in order_history[:3]:  # 처음 3개만 출력
                logger.info(f"  - 주문: {order}")
        else:
            logger.warning("?�️ 주문 ?�역 조회 ?�패 ?�는 주문 ?�역 ?�음")
        
        # 3. 주문 ?�태 조회 (?�시)
        logger.info("3. 주문 ?�태 조회 (?�시)")
        # ?�제 주문 ID가 ?�요?��?�??�시로만 ?�스??
        logger.info("  주문 ?�태 조회 기능?� ?�제 주문 ID가 ?�요?�니??")
        
        # 4. 주문 취소 (?�시)
        logger.info("4. 주문 취소 (?�시)")
        logger.info("  주문 취소 기능?� ?�제 주문 ID가 ?�요?�니??")
        
        # 5. 매수 주문 ?��??�이??(?�제 주문?� ?��? ?�음)
        logger.info("5. 매수 주문 ?��??�이??)
        logger.info("  ?�제 주문?� ?�험?��?�??��??�이?�만 진행?�니??")
        
        # ?�스?�용 주문 ?�이??
        test_order = {
            'stock_code': '005930',  # ?�성?�자
            'quantity': 1,           # 1�?
            'price': 70000           # 70,000??
        }
        
        logger.info(f"  ?�스??주문 ?�이?? {test_order}")
        logger.info("  ?�제 주문???�하?�면 주석???�제?�세??")
        
        # ?�제 주문???�할 경우 ?�래 주석 ?�제
        # success, message = order_handler.place_buy_order(
        #     test_order['stock_code'],
        #     test_order['quantity'],
        #     test_order['price']
        # )
        # if success:
        #     logger.success(f"??매수 주문 ?�공: {message}")
        # else:
        #     logger.error(f"??매수 주문 ?�패: {message}")
        
    except Exception as e:
        logger.error(f"??주문 처리 ?�스??�??�류: {e}")
        return False
    finally:
        order_handler.disconnect()
    
    return True

def test_order_validation():
    """주문 ?�효??검???�스??""
    logger.info("=== 주문 ?�효??검???�스???�작 ===")
    
    order_handler = OrderHandler()
    
    if not order_handler.connect():
        logger.error("??주문 처리 ?�결 ?�패")
        return False
    
    logger.success("??주문 처리 ?�결 ?�공")
    
    try:
        # 1. ?�못??종목 코드 ?�스??
        logger.info("1. ?�못??종목 코드 ?�스??)
        success, message = order_handler.place_order('INVALID', 'buy', 1, 1000)
        logger.info(f"  ?�못??종목 코드 결과: {success}, {message}")
        
        # 2. ?�못??주문 ?�???�스??
        logger.info("2. ?�못??주문 ?�???�스??)
        success, message = order_handler.place_order('005930', 'invalid', 1, 1000)
        logger.info(f"  ?�못??주문 ?�??결과: {success}, {message}")
        
        # 3. ?�못???�량 ?�스??
        logger.info("3. ?�못???�량 ?�스??)
        success, message = order_handler.place_order('005930', 'buy', -1, 1000)
        logger.info(f"  ?�못???�량 결과: {success}, {message}")
        
        # 4. ?�못??가�??�스??
        logger.info("4. ?�못??가�??�스??)
        success, message = order_handler.place_order('005930', 'buy', 1, -1000)
        logger.info(f"  ?�못??가�?결과: {success}, {message}")
        
    except Exception as e:
        logger.error(f"??주문 ?�효??검???�스??�??�류: {e}")
        return False
    finally:
        order_handler.disconnect()
    
    return True

def main():
    """메인 ?�스???�수"""
    setup_logging()
    
    logger.info("?? 주문 처리 ?�스???�작")
    
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
        ("주문 ?�효??검??, test_order_validation),
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
        return True
    else:
        logger.warning("?�️ ?��? ?�스?��? ?�패?�습?�다.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
