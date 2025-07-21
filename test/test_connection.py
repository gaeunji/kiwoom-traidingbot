#!/usr/bin/env python
"""
?��?증권 API ?�결 ?�스???�크립트
"""

import sys
import os
from loguru import logger
from kiwoom import KiwoomConnector, KiwoomAPI, MarketDataAPI

def setup_logging():
    """로깅 ?�정"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def test_basic_connection():
    """기본 ?�결 ?�스??""
    logger.info("=== 기본 ?�결 ?�스???�작 ===")
    
    # 1. Connector ?�스??
    logger.info("1. KiwoomConnector ?�스??)
    connector = KiwoomConnector()
    
    # ?�결 ?�태 ?�인
    status = connector.get_connection_status()
    logger.info(f"초기 ?�결 ?�태: {status}")
    
    # ?�결 ?�도
    if connector.connect():
        logger.success("??KiwoomConnector ?�결 ?�공")
        
        # ?�큰 ?�효???�인
        if connector.is_token_valid():
            logger.success("???�세???�큰 ?�효")
        else:
            logger.warning("?�️ ?�세???�큰 만료 ?�는 무효")
        
        connector.disconnect()
    else:
        logger.error("??KiwoomConnector ?�결 ?�패")
        return False
    
    return True

def test_api_client():
    """API ?�라?�언???�스??""
    logger.info("=== API ?�라?�언???�스???�작 ===")
    
    api = KiwoomAPI()
    
    if not api.connect():
        logger.error("??API ?�라?�언???�결 ?�패")
        return False
    
    logger.success("??API ?�라?�언???�결 ?�공")
    
    try:
        # 1. 계좌 ?�보 조회 (기존 방식)
        logger.info("1. 계좌 ?�보 조회 (기존 방식)")
        account_info = api.get_account_info()
        if account_info:
            logger.success("??계좌 ?�보 조회 ?�공")
            logger.info(f"계좌 ?�보: {account_info}")
        else:
            logger.warning("?�️ 계좌 ?�보 조회 ?�패")
        
        # 2. 계좌?��??�고?�역 조회 (?�로??방식)
        logger.info("2. 계좌?��??�고?�역 조회 (?�로??방식)")
        account_balance = api.get_account_balance()
        if account_balance:
            logger.success("??계좌?��??�고?�역 조회 ?�공")
            logger.info(f"?�답 ?�태: {account_balance.get('status_code')}")
            logger.info(f"?�이??개수: {len(account_balance.get('data', []))}")
        else:
            logger.warning("?�️ 계좌?��??�고?�역 조회 ?�패")
        
        # 3. 주식 ?�재가 조회
        logger.info("3. 주식 ?�재가 조회")
        test_stocks = ['005930', '000660', '035420']  # ?�성?�자, SK?�이?�스, NAVER
        
        for stock_code in test_stocks:
            price_data = api.get_stock_price(stock_code)
            if price_data:
                current_price = price_data.get('stck_prpr', 0)
                logger.success(f"??{stock_code} ?�재가: {current_price:,}??)
            else:
                logger.warning(f"?�️ {stock_code} ?�재가 조회 ?�패")
        
        # 4. 보유 종목 조회
        logger.info("4. 보유 종목 조회")
        holdings = api.get_holdings()
        if holdings:
            logger.success(f"??보유 종목 조회 ?�공: {len(holdings)}�?)
            for holding in holdings[:3]:  # 처음 3개만 출력
                logger.info(f"  - {holding}")
        else:
            logger.warning("?�️ 보유 종목 조회 ?�패")
        
    except Exception as e:
        logger.error(f"??API ?�라?�언???�스??�??�류: {e}")
        return False
    finally:
        api.disconnect()
    
    return True

def test_market_data():
    """?�장 ?�이??API ?�스??""
    logger.info("=== ?�장 ?�이??API ?�스???�작 ===")
    
    market_api = MarketDataAPI()
    
    if not market_api.connect():
        logger.error("???�장 ?�이??API ?�결 ?�패")
        return False
    
    logger.success("???�장 ?�이??API ?�결 ?�공")
    
    try:
        # 1. 거래???�위 종목 조회 (?�체)
        logger.info("1. 거래???�위 종목 조회 (?�체)")
        volume_stocks = market_api.get_top_volume_stocks(limit=5, market_type='000')
        if volume_stocks:
            logger.success(f"??거래???�위 종목 조회 ?�공: {len(volume_stocks)}�?)
            for i, stock in enumerate(volume_stocks[:3], 1):
                logger.info(f"  {i}. {stock['stock_name']} ({stock['stock_code']})")
                logger.info(f"     ?�재가: {stock['current_price']:,}?? 거래?? {stock['volume']:,}")
                logger.info(f"     ?�락�? {stock['change_rate']:+.2f}%")
        else:
            logger.warning("?�️ 거래???�위 종목 조회 ?�패")
        
        # 2. 거래???�위 종목 조회 (코스??
        logger.info("2. 거래???�위 종목 조회 (코스??")
        kospi_stocks = market_api.get_top_volume_stocks(limit=3, market_type='001')
        if kospi_stocks:
            logger.success(f"??코스??거래???�위 종목 조회 ?�공: {len(kospi_stocks)}�?)
            for stock in kospi_stocks:
                logger.info(f"  - {stock['stock_name']} ({stock['stock_code']})")
        else:
            logger.warning("?�️ 코스??거래???�위 종목 조회 ?�패")
        
        # 3. 거래???�위 종목 조회 (코스??
        logger.info("3. 거래???�위 종목 조회 (코스??")
        kosdaq_stocks = market_api.get_top_volume_stocks(limit=3, market_type='101')
        if kosdaq_stocks:
            logger.success(f"??코스??거래???�위 종목 조회 ?�공: {len(kosdaq_stocks)}�?)
            for stock in kosdaq_stocks:
                logger.info(f"  - {stock['stock_name']} ({stock['stock_code']})")
        else:
            logger.warning("?�️ 코스??거래???�위 종목 조회 ?�패")
        
    except Exception as e:
        logger.error(f"???�장 ?�이??API ?�스??�??�류: {e}")
        return False
    finally:
        market_api.disconnect()
    
    return True

def main():
    """메인 ?�스???�수"""
    setup_logging()
    
    logger.info("?? ?��?증권 API ?�결 ?�스???�작")
    
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
        ("기본 ?�결", test_basic_connection),
        ("API ?�라?�언??, test_api_client),
        ("?�장 ?�이??, test_market_data),
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
