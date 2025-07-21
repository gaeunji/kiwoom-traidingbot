#!/usr/bin/env python
"""
ê±°ë˜ ?„ëµ ?ŒìŠ¤???¤í¬ë¦½íŠ¸
"""

import sys
import os
from loguru import logger
from strategy.trading_strategy import TradingStrategy
from data import StockRanking, CacheManager

def setup_logging():
    """ë¡œê¹… ?¤ì •"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def test_trading_strategy():
    """ê±°ë˜ ?„ëµ ?ŒìŠ¤??""
    logger.info("=== ê±°ë˜ ?„ëµ ?ŒìŠ¤???œì‘ ===")
    
    strategy = TradingStrategy()
    
    if not strategy.connect():
        logger.error("??ê±°ë˜ ?„ëµ ?°ê²° ?¤íŒ¨")
        return False
    
    logger.success("??ê±°ë˜ ?„ëµ ?°ê²° ?±ê³µ")
    
    try:
        # 1. ê´€??ì¢…ëª© ê´€ë¦??ŒìŠ¤??
        logger.info("1. ê´€??ì¢…ëª© ê´€ë¦??ŒìŠ¤??)
        test_stocks = ['005930', '000660', '035420']  # ?¼ì„±?„ì, SK?˜ì´?‰ìŠ¤, NAVER
        
        for stock_code in test_stocks:
            strategy.add_to_watchlist(stock_code)
        
        logger.success(f"??ê´€??ì¢…ëª© ì¶”ê? ?„ë£Œ: {strategy.watchlist}")
        
        # 2. ?„ì¬ê°€ ì¡°íšŒ ?ŒìŠ¤??
        logger.info("2. ?„ì¬ê°€ ì¡°íšŒ ?ŒìŠ¤??)
        for stock_code in test_stocks:
            price = strategy.get_current_price(stock_code)
            if price:
                logger.success(f"??{stock_code} ?„ì¬ê°€: {price:,}??)
            else:
                logger.warning(f"? ï¸ {stock_code} ?„ì¬ê°€ ì¡°íšŒ ?¤íŒ¨")
        
        # 3. ?¬ìš© ê°€?¥í•œ ?„ê¸ˆ ì¡°íšŒ
        logger.info("3. ?¬ìš© ê°€?¥í•œ ?„ê¸ˆ ì¡°íšŒ")
        available_cash = strategy.get_available_cash()
        logger.info(f"?¬ìš© ê°€?¥í•œ ?„ê¸ˆ: {available_cash:,}??)
        
        # 4. ?¬íŠ¸?´ë¦¬???”ì•½
        logger.info("4. ?¬íŠ¸?´ë¦¬???”ì•½")
        summary = strategy.get_portfolio_summary()
        logger.info(f"?¬íŠ¸?´ë¦¬???”ì•½: {summary}")
        
        # 5. ê´€??ì¢…ëª© ?„ì¬ê°€ ?¼ê´„ ì¡°íšŒ
        logger.info("5. ê´€??ì¢…ëª© ?„ì¬ê°€ ?¼ê´„ ì¡°íšŒ")
        prices = strategy.get_watchlist_prices()
        for stock_code, price in prices.items():
            logger.info(f"  {stock_code}: {price:,}??)
        
        # 6. ?„ëµ ? í˜¸ ?ŒìŠ¤??(?¤ì œ ì£¼ë¬¸?€ ?˜ì? ?ŠìŒ)
        logger.info("6. ?„ëµ ? í˜¸ ?ŒìŠ¤??)
        for stock_code in test_stocks[:2]:  # ì²˜ìŒ 2ê°œë§Œ ?ŒìŠ¤??
            signal = strategy.simple_moving_average_strategy(stock_code)
            logger.info(f"  {stock_code} ?„ëµ ? í˜¸: {signal}")
        
        # 7. ê´€??ì¢…ëª© ?œê±° ?ŒìŠ¤??
        logger.info("7. ê´€??ì¢…ëª© ?œê±° ?ŒìŠ¤??)
        strategy.remove_from_watchlist('035420')  # NAVER ?œê±°
        logger.info(f"ê´€??ì¢…ëª© ëª©ë¡: {strategy.watchlist}")
        
    except Exception as e:
        logger.error(f"??ê±°ë˜ ?„ëµ ?ŒìŠ¤??ì¤??¤ë¥˜: {e}")
        return False
    finally:
        strategy.disconnect()
    
    return True

def test_stock_ranking():
    """ì¢…ëª© ??‚¹ ?ŒìŠ¤??""
    logger.info("=== ì¢…ëª© ??‚¹ ?ŒìŠ¤???œì‘ ===")
    
    ranking = StockRanking()
    
    if not ranking.connect():
        logger.error("??ì¢…ëª© ??‚¹ ?°ê²° ?¤íŒ¨")
        return False
    
    logger.success("??ì¢…ëª© ??‚¹ ?°ê²° ?±ê³µ")
    
    try:
        # 1. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (ìºì‹œ ?¬ìš©)
        logger.info("1. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (ìºì‹œ ?¬ìš©)")
        volume_stocks = ranking.get_volume_ranking(limit=5, market_type='000', use_cache=True)
        if volume_stocks:
            logger.success(f"??ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?±ê³µ: {len(volume_stocks)}ê°?)
            for i, stock in enumerate(volume_stocks[:3], 1):
                logger.info(f"  {i}. {stock['stock_name']} ({stock['stock_code']})")
                logger.info(f"     ?„ì¬ê°€: {stock['current_price']:,}??)
                logger.info(f"     ê±°ë˜?? {stock['volume']:,}")
                logger.info(f"     ?±ë½ë¥? {stock['change_rate']:+.2f}%")
        else:
            logger.warning("? ï¸ ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?¤íŒ¨")
        
        # 2. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (ìºì‹œ ë¬´ì‹œ)
        logger.info("2. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (ìºì‹œ ë¬´ì‹œ)")
        fresh_stocks = ranking.get_volume_ranking(limit=3, market_type='001', use_cache=False)
        if fresh_stocks:
            logger.success(f"??ì½”ìŠ¤??ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?±ê³µ: {len(fresh_stocks)}ê°?)
            for stock in fresh_stocks:
                logger.info(f"  - {stock['stock_name']} ({stock['stock_code']})")
        else:
            logger.warning("? ï¸ ì½”ìŠ¤??ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?¤íŒ¨")
        
        # 3. ??‚¹ ?µê³„ ì¡°íšŒ
        logger.info("3. ??‚¹ ?µê³„ ì¡°íšŒ")
        stats = ranking.get_ranking_statistics()
        logger.info(f"ìºì‹œ ?•ë³´: {stats.get('cache_info', {})}")
        logger.info(f"?¬ìš© ê°€?¥í•œ ??‚¹: {stats.get('available_rankings', [])}")
        
        # 4. ?¤ì–‘??ê¸°ì??¼ë¡œ ??‚¹ ì¡°íšŒ
        logger.info("4. ?¤ì–‘??ê¸°ì??¼ë¡œ ??‚¹ ì¡°íšŒ")
        for criteria in ['volume', 'gainers', 'losers']:
            stocks = ranking.get_ranking_by_criteria(criteria, limit=2)
            logger.info(f"  {criteria} ??‚¹: {len(stocks)}ê°?ì¢…ëª©")
        
    except Exception as e:
        logger.error(f"??ì¢…ëª© ??‚¹ ?ŒìŠ¤??ì¤??¤ë¥˜: {e}")
        return False
    finally:
        ranking.disconnect()
    
    return True

def test_cache_manager():
    """ìºì‹œ ê´€ë¦¬ì ?ŒìŠ¤??""
    logger.info("=== ìºì‹œ ê´€ë¦¬ì ?ŒìŠ¤???œì‘ ===")
    
    cache = CacheManager(cache_dir="test_cache", cache_duration=60)  # 1ë¶?ìºì‹œ
    
    try:
        # 1. ìºì‹œ ?€???ŒìŠ¤??
        logger.info("1. ìºì‹œ ?€???ŒìŠ¤??)
        test_data = {
            'test_key': 'test_value',
            'numbers': [1, 2, 3, 4, 5],
            'nested': {'key': 'value'}
        }
        
        cache.set_cached_data('test_key', test_data)
        logger.success("??ìºì‹œ ?€???±ê³µ")
        
        # 2. ìºì‹œ ì¡°íšŒ ?ŒìŠ¤??
        logger.info("2. ìºì‹œ ì¡°íšŒ ?ŒìŠ¤??)
        cached_data = cache.get_cached_data('test_key')
        if cached_data and cached_data.get('data') == test_data:
            logger.success("??ìºì‹œ ì¡°íšŒ ?±ê³µ")
        else:
            logger.warning("? ï¸ ìºì‹œ ì¡°íšŒ ?¤íŒ¨")
        
        # 3. ìºì‹œ ? íš¨???•ì¸
        logger.info("3. ìºì‹œ ? íš¨???•ì¸")
        is_valid = cache.is_cache_valid('test_key')
        logger.info(f"ìºì‹œ ? íš¨?? {is_valid}")
        
        # 4. ìºì‹œ ?•ë³´ ì¡°íšŒ
        logger.info("4. ìºì‹œ ?•ë³´ ì¡°íšŒ")
        cache_info = cache.get_cache_info()
        logger.info(f"ìºì‹œ ?”ë ‰? ë¦¬: {cache_info.get('cache_dir')}")
        logger.info(f"ìºì‹œ ì§€?ì‹œê°? {cache_info.get('cache_duration')}ì´?)
        logger.info(f"ìºì‹œ ?Œì¼ ?? {cache_info.get('total_files')}")
        
        # 5. ìºì‹œ ?? œ ?ŒìŠ¤??
        logger.info("5. ìºì‹œ ?? œ ?ŒìŠ¤??)
        cache.clear_cache('test_key')
        deleted_data = cache.get_cached_data('test_key')
        if deleted_data is None:
            logger.success("??ìºì‹œ ?? œ ?±ê³µ")
        else:
            logger.warning("? ï¸ ìºì‹œ ?? œ ?¤íŒ¨")
        
    except Exception as e:
        logger.error(f"??ìºì‹œ ê´€ë¦¬ì ?ŒìŠ¤??ì¤??¤ë¥˜: {e}")
        return False
    
    return True

def main():
    """ë©”ì¸ ?ŒìŠ¤???¨ìˆ˜"""
    setup_logging()
    
    logger.info("?? ê±°ë˜ ?„ëµ ?ŒìŠ¤???œì‘")
    
    # ?˜ê²½ ë³€???•ì¸
    required_vars = ['KIWOOM_APP_KEY', 'KIWOOM_APP_SECRET', 'ACCOUNT_NUMBER']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"???„ìˆ˜ ?˜ê²½ ë³€?˜ê? ?¤ì •?˜ì? ?Šì•˜?µë‹ˆ?? {', '.join(missing_vars)}")
        logger.error("?“ .env ?Œì¼???ì„±?˜ê³  ?„ìš”???•ë³´ë¥??…ë ¥?´ì£¼?¸ìš”.")
        return False
    
    logger.success("???˜ê²½ ë³€???¤ì • ?•ì¸ ?„ë£Œ")
    
    # ?ŒìŠ¤???¤í–‰
    tests = [
        ("ê±°ë˜ ?„ëµ", test_trading_strategy),
        ("ì¢…ëª© ??‚¹", test_stock_ranking),
        ("ìºì‹œ ê´€ë¦?, test_cache_manager),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"?ŒìŠ¤?? {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"??{test_name} ?ŒìŠ¤??ì¤??ˆì™¸ ë°œìƒ: {e}")
            results.append((test_name, False))
    
    # ê²°ê³¼ ?”ì•½
    logger.info(f"\n{'='*50}")
    logger.info("?ŒìŠ¤??ê²°ê³¼ ?”ì•½")
    logger.info(f"{'='*50}")
    
    success_count = 0
    for test_name, result in results:
        status = "???±ê³µ" if result else "???¤íŒ¨"
        logger.info(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    logger.info(f"\n?„ì²´ ?ŒìŠ¤?? {len(results)}ê°?ì¤?{success_count}ê°??±ê³µ")
    
    if success_count == len(results):
        logger.success("?‰ ëª¨ë“  ?ŒìŠ¤?¸ê? ?±ê³µ?ˆìŠµ?ˆë‹¤!")
        return True
    else:
        logger.warning("? ï¸ ?¼ë? ?ŒìŠ¤?¸ê? ?¤íŒ¨?ˆìŠµ?ˆë‹¤.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
