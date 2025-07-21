#!/usr/bin/env python
"""
?¤ì?ì¦ê¶Œ API ?°ê²° ?ŒìŠ¤???¤í¬ë¦½íŠ¸
"""

import sys
import os
from loguru import logger
from kiwoom import KiwoomConnector, KiwoomAPI, MarketDataAPI

def setup_logging():
    """ë¡œê¹… ?¤ì •"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def test_basic_connection():
    """ê¸°ë³¸ ?°ê²° ?ŒìŠ¤??""
    logger.info("=== ê¸°ë³¸ ?°ê²° ?ŒìŠ¤???œì‘ ===")
    
    # 1. Connector ?ŒìŠ¤??
    logger.info("1. KiwoomConnector ?ŒìŠ¤??)
    connector = KiwoomConnector()
    
    # ?°ê²° ?íƒœ ?•ì¸
    status = connector.get_connection_status()
    logger.info(f"ì´ˆê¸° ?°ê²° ?íƒœ: {status}")
    
    # ?°ê²° ?œë„
    if connector.connect():
        logger.success("??KiwoomConnector ?°ê²° ?±ê³µ")
        
        # ? í° ? íš¨???•ì¸
        if connector.is_token_valid():
            logger.success("???¡ì„¸??? í° ? íš¨")
        else:
            logger.warning("? ï¸ ?¡ì„¸??? í° ë§Œë£Œ ?ëŠ” ë¬´íš¨")
        
        connector.disconnect()
    else:
        logger.error("??KiwoomConnector ?°ê²° ?¤íŒ¨")
        return False
    
    return True

def test_api_client():
    """API ?´ë¼?´ì–¸???ŒìŠ¤??""
    logger.info("=== API ?´ë¼?´ì–¸???ŒìŠ¤???œì‘ ===")
    
    api = KiwoomAPI()
    
    if not api.connect():
        logger.error("??API ?´ë¼?´ì–¸???°ê²° ?¤íŒ¨")
        return False
    
    logger.success("??API ?´ë¼?´ì–¸???°ê²° ?±ê³µ")
    
    try:
        # 1. ê³„ì¢Œ ?•ë³´ ì¡°íšŒ (ê¸°ì¡´ ë°©ì‹)
        logger.info("1. ê³„ì¢Œ ?•ë³´ ì¡°íšŒ (ê¸°ì¡´ ë°©ì‹)")
        account_info = api.get_account_info()
        if account_info:
            logger.success("??ê³„ì¢Œ ?•ë³´ ì¡°íšŒ ?±ê³µ")
            logger.info(f"ê³„ì¢Œ ?•ë³´: {account_info}")
        else:
            logger.warning("? ï¸ ê³„ì¢Œ ?•ë³´ ì¡°íšŒ ?¤íŒ¨")
        
        # 2. ê³„ì¢Œ?‰ê??”ê³ ?´ì—­ ì¡°íšŒ (?ˆë¡œ??ë°©ì‹)
        logger.info("2. ê³„ì¢Œ?‰ê??”ê³ ?´ì—­ ì¡°íšŒ (?ˆë¡œ??ë°©ì‹)")
        account_balance = api.get_account_balance()
        if account_balance:
            logger.success("??ê³„ì¢Œ?‰ê??”ê³ ?´ì—­ ì¡°íšŒ ?±ê³µ")
            logger.info(f"?‘ë‹µ ?íƒœ: {account_balance.get('status_code')}")
            logger.info(f"?°ì´??ê°œìˆ˜: {len(account_balance.get('data', []))}")
        else:
            logger.warning("? ï¸ ê³„ì¢Œ?‰ê??”ê³ ?´ì—­ ì¡°íšŒ ?¤íŒ¨")
        
        # 3. ì£¼ì‹ ?„ì¬ê°€ ì¡°íšŒ
        logger.info("3. ì£¼ì‹ ?„ì¬ê°€ ì¡°íšŒ")
        test_stocks = ['005930', '000660', '035420']  # ?¼ì„±?„ì, SK?˜ì´?‰ìŠ¤, NAVER
        
        for stock_code in test_stocks:
            price_data = api.get_stock_price(stock_code)
            if price_data:
                current_price = price_data.get('stck_prpr', 0)
                logger.success(f"??{stock_code} ?„ì¬ê°€: {current_price:,}??)
            else:
                logger.warning(f"? ï¸ {stock_code} ?„ì¬ê°€ ì¡°íšŒ ?¤íŒ¨")
        
        # 4. ë³´ìœ  ì¢…ëª© ì¡°íšŒ
        logger.info("4. ë³´ìœ  ì¢…ëª© ì¡°íšŒ")
        holdings = api.get_holdings()
        if holdings:
            logger.success(f"??ë³´ìœ  ì¢…ëª© ì¡°íšŒ ?±ê³µ: {len(holdings)}ê°?)
            for holding in holdings[:3]:  # ì²˜ìŒ 3ê°œë§Œ ì¶œë ¥
                logger.info(f"  - {holding}")
        else:
            logger.warning("? ï¸ ë³´ìœ  ì¢…ëª© ì¡°íšŒ ?¤íŒ¨")
        
    except Exception as e:
        logger.error(f"??API ?´ë¼?´ì–¸???ŒìŠ¤??ì¤??¤ë¥˜: {e}")
        return False
    finally:
        api.disconnect()
    
    return True

def test_market_data():
    """?œì¥ ?°ì´??API ?ŒìŠ¤??""
    logger.info("=== ?œì¥ ?°ì´??API ?ŒìŠ¤???œì‘ ===")
    
    market_api = MarketDataAPI()
    
    if not market_api.connect():
        logger.error("???œì¥ ?°ì´??API ?°ê²° ?¤íŒ¨")
        return False
    
    logger.success("???œì¥ ?°ì´??API ?°ê²° ?±ê³µ")
    
    try:
        # 1. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (?„ì²´)
        logger.info("1. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (?„ì²´)")
        volume_stocks = market_api.get_top_volume_stocks(limit=5, market_type='000')
        if volume_stocks:
            logger.success(f"??ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?±ê³µ: {len(volume_stocks)}ê°?)
            for i, stock in enumerate(volume_stocks[:3], 1):
                logger.info(f"  {i}. {stock['stock_name']} ({stock['stock_code']})")
                logger.info(f"     ?„ì¬ê°€: {stock['current_price']:,}?? ê±°ë˜?? {stock['volume']:,}")
                logger.info(f"     ?±ë½ë¥? {stock['change_rate']:+.2f}%")
        else:
            logger.warning("? ï¸ ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?¤íŒ¨")
        
        # 2. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (ì½”ìŠ¤??
        logger.info("2. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (ì½”ìŠ¤??")
        kospi_stocks = market_api.get_top_volume_stocks(limit=3, market_type='001')
        if kospi_stocks:
            logger.success(f"??ì½”ìŠ¤??ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?±ê³µ: {len(kospi_stocks)}ê°?)
            for stock in kospi_stocks:
                logger.info(f"  - {stock['stock_name']} ({stock['stock_code']})")
        else:
            logger.warning("? ï¸ ì½”ìŠ¤??ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?¤íŒ¨")
        
        # 3. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (ì½”ìŠ¤??
        logger.info("3. ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ (ì½”ìŠ¤??")
        kosdaq_stocks = market_api.get_top_volume_stocks(limit=3, market_type='101')
        if kosdaq_stocks:
            logger.success(f"??ì½”ìŠ¤??ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?±ê³µ: {len(kosdaq_stocks)}ê°?)
            for stock in kosdaq_stocks:
                logger.info(f"  - {stock['stock_name']} ({stock['stock_code']})")
        else:
            logger.warning("? ï¸ ì½”ìŠ¤??ê±°ë˜???ìœ„ ì¢…ëª© ì¡°íšŒ ?¤íŒ¨")
        
    except Exception as e:
        logger.error(f"???œì¥ ?°ì´??API ?ŒìŠ¤??ì¤??¤ë¥˜: {e}")
        return False
    finally:
        market_api.disconnect()
    
    return True

def main():
    """ë©”ì¸ ?ŒìŠ¤???¨ìˆ˜"""
    setup_logging()
    
    logger.info("?? ?¤ì?ì¦ê¶Œ API ?°ê²° ?ŒìŠ¤???œì‘")
    
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
        ("ê¸°ë³¸ ?°ê²°", test_basic_connection),
        ("API ?´ë¼?´ì–¸??, test_api_client),
        ("?œì¥ ?°ì´??, test_market_data),
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
