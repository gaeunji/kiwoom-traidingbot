#!/usr/bin/env python
"""
거래 ?�략 ?�스???�크립트
"""

import sys
import os
from loguru import logger
from strategy.trading_strategy import TradingStrategy
from data import StockRanking, CacheManager

def setup_logging():
    """로깅 ?�정"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def test_trading_strategy():
    """거래 ?�략 ?�스??""
    logger.info("=== 거래 ?�략 ?�스???�작 ===")
    
    strategy = TradingStrategy()
    
    if not strategy.connect():
        logger.error("??거래 ?�략 ?�결 ?�패")
        return False
    
    logger.success("??거래 ?�략 ?�결 ?�공")
    
    try:
        # 1. 관??종목 관�??�스??
        logger.info("1. 관??종목 관�??�스??)
        test_stocks = ['005930', '000660', '035420']  # ?�성?�자, SK?�이?�스, NAVER
        
        for stock_code in test_stocks:
            strategy.add_to_watchlist(stock_code)
        
        logger.success(f"??관??종목 추�? ?�료: {strategy.watchlist}")
        
        # 2. ?�재가 조회 ?�스??
        logger.info("2. ?�재가 조회 ?�스??)
        for stock_code in test_stocks:
            price = strategy.get_current_price(stock_code)
            if price:
                logger.success(f"??{stock_code} ?�재가: {price:,}??)
            else:
                logger.warning(f"?�️ {stock_code} ?�재가 조회 ?�패")
        
        # 3. ?�용 가?�한 ?�금 조회
        logger.info("3. ?�용 가?�한 ?�금 조회")
        available_cash = strategy.get_available_cash()
        logger.info(f"?�용 가?�한 ?�금: {available_cash:,}??)
        
        # 4. ?�트?�리???�약
        logger.info("4. ?�트?�리???�약")
        summary = strategy.get_portfolio_summary()
        logger.info(f"?�트?�리???�약: {summary}")
        
        # 5. 관??종목 ?�재가 ?�괄 조회
        logger.info("5. 관??종목 ?�재가 ?�괄 조회")
        prices = strategy.get_watchlist_prices()
        for stock_code, price in prices.items():
            logger.info(f"  {stock_code}: {price:,}??)
        
        # 6. ?�략 ?�호 ?�스??(?�제 주문?� ?��? ?�음)
        logger.info("6. ?�략 ?�호 ?�스??)
        for stock_code in test_stocks[:2]:  # 처음 2개만 ?�스??
            signal = strategy.simple_moving_average_strategy(stock_code)
            logger.info(f"  {stock_code} ?�략 ?�호: {signal}")
        
        # 7. 관??종목 ?�거 ?�스??
        logger.info("7. 관??종목 ?�거 ?�스??)
        strategy.remove_from_watchlist('035420')  # NAVER ?�거
        logger.info(f"관??종목 목록: {strategy.watchlist}")
        
    except Exception as e:
        logger.error(f"??거래 ?�략 ?�스??�??�류: {e}")
        return False
    finally:
        strategy.disconnect()
    
    return True

def test_stock_ranking():
    """종목 ??�� ?�스??""
    logger.info("=== 종목 ??�� ?�스???�작 ===")
    
    ranking = StockRanking()
    
    if not ranking.connect():
        logger.error("??종목 ??�� ?�결 ?�패")
        return False
    
    logger.success("??종목 ??�� ?�결 ?�공")
    
    try:
        # 1. 거래???�위 종목 조회 (캐시 ?�용)
        logger.info("1. 거래???�위 종목 조회 (캐시 ?�용)")
        volume_stocks = ranking.get_volume_ranking(limit=5, market_type='000', use_cache=True)
        if volume_stocks:
            logger.success(f"??거래???�위 종목 조회 ?�공: {len(volume_stocks)}�?)
            for i, stock in enumerate(volume_stocks[:3], 1):
                logger.info(f"  {i}. {stock['stock_name']} ({stock['stock_code']})")
                logger.info(f"     ?�재가: {stock['current_price']:,}??)
                logger.info(f"     거래?? {stock['volume']:,}")
                logger.info(f"     ?�락�? {stock['change_rate']:+.2f}%")
        else:
            logger.warning("?�️ 거래???�위 종목 조회 ?�패")
        
        # 2. 거래???�위 종목 조회 (캐시 무시)
        logger.info("2. 거래???�위 종목 조회 (캐시 무시)")
        fresh_stocks = ranking.get_volume_ranking(limit=3, market_type='001', use_cache=False)
        if fresh_stocks:
            logger.success(f"??코스??거래???�위 종목 조회 ?�공: {len(fresh_stocks)}�?)
            for stock in fresh_stocks:
                logger.info(f"  - {stock['stock_name']} ({stock['stock_code']})")
        else:
            logger.warning("?�️ 코스??거래???�위 종목 조회 ?�패")
        
        # 3. ??�� ?�계 조회
        logger.info("3. ??�� ?�계 조회")
        stats = ranking.get_ranking_statistics()
        logger.info(f"캐시 ?�보: {stats.get('cache_info', {})}")
        logger.info(f"?�용 가?�한 ??��: {stats.get('available_rankings', [])}")
        
        # 4. ?�양??기�??�로 ??�� 조회
        logger.info("4. ?�양??기�??�로 ??�� 조회")
        for criteria in ['volume', 'gainers', 'losers']:
            stocks = ranking.get_ranking_by_criteria(criteria, limit=2)
            logger.info(f"  {criteria} ??��: {len(stocks)}�?종목")
        
    except Exception as e:
        logger.error(f"??종목 ??�� ?�스??�??�류: {e}")
        return False
    finally:
        ranking.disconnect()
    
    return True

def test_cache_manager():
    """캐시 관리자 ?�스??""
    logger.info("=== 캐시 관리자 ?�스???�작 ===")
    
    cache = CacheManager(cache_dir="test_cache", cache_duration=60)  # 1�?캐시
    
    try:
        # 1. 캐시 ?�???�스??
        logger.info("1. 캐시 ?�???�스??)
        test_data = {
            'test_key': 'test_value',
            'numbers': [1, 2, 3, 4, 5],
            'nested': {'key': 'value'}
        }
        
        cache.set_cached_data('test_key', test_data)
        logger.success("??캐시 ?�???�공")
        
        # 2. 캐시 조회 ?�스??
        logger.info("2. 캐시 조회 ?�스??)
        cached_data = cache.get_cached_data('test_key')
        if cached_data and cached_data.get('data') == test_data:
            logger.success("??캐시 조회 ?�공")
        else:
            logger.warning("?�️ 캐시 조회 ?�패")
        
        # 3. 캐시 ?�효???�인
        logger.info("3. 캐시 ?�효???�인")
        is_valid = cache.is_cache_valid('test_key')
        logger.info(f"캐시 ?�효?? {is_valid}")
        
        # 4. 캐시 ?�보 조회
        logger.info("4. 캐시 ?�보 조회")
        cache_info = cache.get_cache_info()
        logger.info(f"캐시 ?�렉?�리: {cache_info.get('cache_dir')}")
        logger.info(f"캐시 지?�시�? {cache_info.get('cache_duration')}�?)
        logger.info(f"캐시 ?�일 ?? {cache_info.get('total_files')}")
        
        # 5. 캐시 ??�� ?�스??
        logger.info("5. 캐시 ??�� ?�스??)
        cache.clear_cache('test_key')
        deleted_data = cache.get_cached_data('test_key')
        if deleted_data is None:
            logger.success("??캐시 ??�� ?�공")
        else:
            logger.warning("?�️ 캐시 ??�� ?�패")
        
    except Exception as e:
        logger.error(f"??캐시 관리자 ?�스??�??�류: {e}")
        return False
    
    return True

def main():
    """메인 ?�스???�수"""
    setup_logging()
    
    logger.info("?? 거래 ?�략 ?�스???�작")
    
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
        ("거래 ?�략", test_trading_strategy),
        ("종목 ??��", test_stock_ranking),
        ("캐시 관�?, test_cache_manager),
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
