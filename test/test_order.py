#!/usr/bin/env python
"""
ì£¼ë¬¸ ì²˜ë¦¬ ?ŒìŠ¤???¤í¬ë¦½íŠ¸
"""

import sys
import os
from loguru import logger
from kiwoom import OrderHandler

def setup_logging():
    """ë¡œê¹… ?¤ì •"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def test_order_handler():
    """ì£¼ë¬¸ ì²˜ë¦¬ ?ŒìŠ¤??""
    logger.info("=== ì£¼ë¬¸ ì²˜ë¦¬ ?ŒìŠ¤???œì‘ ===")
    
    order_handler = OrderHandler()
    
    if not order_handler.connect():
        logger.error("??ì£¼ë¬¸ ì²˜ë¦¬ ?°ê²° ?¤íŒ¨")
        return False
    
    logger.success("??ì£¼ë¬¸ ì²˜ë¦¬ ?°ê²° ?±ê³µ")
    
    try:
        # 1. ?°ê²° ?íƒœ ?•ì¸
        logger.info("1. ?°ê²° ?íƒœ ?•ì¸")
        status = order_handler.get_connection_status()
        logger.info(f"?°ê²° ?íƒœ: {status}")
        
        # 2. ì£¼ë¬¸ ?´ì—­ ì¡°íšŒ (?¤ì œ ì£¼ë¬¸?€ ?˜ì? ?ŠìŒ)
        logger.info("2. ì£¼ë¬¸ ?´ì—­ ì¡°íšŒ")
        order_history = order_handler.get_order_history()
        if order_history:
            logger.success(f"??ì£¼ë¬¸ ?´ì—­ ì¡°íšŒ ?±ê³µ: {len(order_history)}ê°?)
            for order in order_history[:3]:  # ì²˜ìŒ 3ê°œë§Œ ì¶œë ¥
                logger.info(f"  - ì£¼ë¬¸: {order}")
        else:
            logger.warning("? ï¸ ì£¼ë¬¸ ?´ì—­ ì¡°íšŒ ?¤íŒ¨ ?ëŠ” ì£¼ë¬¸ ?´ì—­ ?†ìŒ")
        
        # 3. ì£¼ë¬¸ ?íƒœ ì¡°íšŒ (?ˆì‹œ)
        logger.info("3. ì£¼ë¬¸ ?íƒœ ì¡°íšŒ (?ˆì‹œ)")
        # ?¤ì œ ì£¼ë¬¸ IDê°€ ?„ìš”?˜ë?ë¡??ˆì‹œë¡œë§Œ ?ŒìŠ¤??
        logger.info("  ì£¼ë¬¸ ?íƒœ ì¡°íšŒ ê¸°ëŠ¥?€ ?¤ì œ ì£¼ë¬¸ IDê°€ ?„ìš”?©ë‹ˆ??")
        
        # 4. ì£¼ë¬¸ ì·¨ì†Œ (?ˆì‹œ)
        logger.info("4. ì£¼ë¬¸ ì·¨ì†Œ (?ˆì‹œ)")
        logger.info("  ì£¼ë¬¸ ì·¨ì†Œ ê¸°ëŠ¥?€ ?¤ì œ ì£¼ë¬¸ IDê°€ ?„ìš”?©ë‹ˆ??")
        
        # 5. ë§¤ìˆ˜ ì£¼ë¬¸ ?œë??ˆì´??(?¤ì œ ì£¼ë¬¸?€ ?˜ì? ?ŠìŒ)
        logger.info("5. ë§¤ìˆ˜ ì£¼ë¬¸ ?œë??ˆì´??)
        logger.info("  ?¤ì œ ì£¼ë¬¸?€ ?„í—˜?˜ë?ë¡??œë??ˆì´?˜ë§Œ ì§„í–‰?©ë‹ˆ??")
        
        # ?ŒìŠ¤?¸ìš© ì£¼ë¬¸ ?°ì´??
        test_order = {
            'stock_code': '005930',  # ?¼ì„±?„ì
            'quantity': 1,           # 1ì£?
            'price': 70000           # 70,000??
        }
        
        logger.info(f"  ?ŒìŠ¤??ì£¼ë¬¸ ?°ì´?? {test_order}")
        logger.info("  ?¤ì œ ì£¼ë¬¸???í•˜?œë©´ ì£¼ì„???´ì œ?˜ì„¸??")
        
        # ?¤ì œ ì£¼ë¬¸???í•  ê²½ìš° ?„ë˜ ì£¼ì„ ?´ì œ
        # success, message = order_handler.place_buy_order(
        #     test_order['stock_code'],
        #     test_order['quantity'],
        #     test_order['price']
        # )
        # if success:
        #     logger.success(f"??ë§¤ìˆ˜ ì£¼ë¬¸ ?±ê³µ: {message}")
        # else:
        #     logger.error(f"??ë§¤ìˆ˜ ì£¼ë¬¸ ?¤íŒ¨: {message}")
        
    except Exception as e:
        logger.error(f"??ì£¼ë¬¸ ì²˜ë¦¬ ?ŒìŠ¤??ì¤??¤ë¥˜: {e}")
        return False
    finally:
        order_handler.disconnect()
    
    return True

def test_order_validation():
    """ì£¼ë¬¸ ? íš¨??ê²€???ŒìŠ¤??""
    logger.info("=== ì£¼ë¬¸ ? íš¨??ê²€???ŒìŠ¤???œì‘ ===")
    
    order_handler = OrderHandler()
    
    if not order_handler.connect():
        logger.error("??ì£¼ë¬¸ ì²˜ë¦¬ ?°ê²° ?¤íŒ¨")
        return False
    
    logger.success("??ì£¼ë¬¸ ì²˜ë¦¬ ?°ê²° ?±ê³µ")
    
    try:
        # 1. ?˜ëª»??ì¢…ëª© ì½”ë“œ ?ŒìŠ¤??
        logger.info("1. ?˜ëª»??ì¢…ëª© ì½”ë“œ ?ŒìŠ¤??)
        success, message = order_handler.place_order('INVALID', 'buy', 1, 1000)
        logger.info(f"  ?˜ëª»??ì¢…ëª© ì½”ë“œ ê²°ê³¼: {success}, {message}")
        
        # 2. ?˜ëª»??ì£¼ë¬¸ ?€???ŒìŠ¤??
        logger.info("2. ?˜ëª»??ì£¼ë¬¸ ?€???ŒìŠ¤??)
        success, message = order_handler.place_order('005930', 'invalid', 1, 1000)
        logger.info(f"  ?˜ëª»??ì£¼ë¬¸ ?€??ê²°ê³¼: {success}, {message}")
        
        # 3. ?˜ëª»???˜ëŸ‰ ?ŒìŠ¤??
        logger.info("3. ?˜ëª»???˜ëŸ‰ ?ŒìŠ¤??)
        success, message = order_handler.place_order('005930', 'buy', -1, 1000)
        logger.info(f"  ?˜ëª»???˜ëŸ‰ ê²°ê³¼: {success}, {message}")
        
        # 4. ?˜ëª»??ê°€ê²??ŒìŠ¤??
        logger.info("4. ?˜ëª»??ê°€ê²??ŒìŠ¤??)
        success, message = order_handler.place_order('005930', 'buy', 1, -1000)
        logger.info(f"  ?˜ëª»??ê°€ê²?ê²°ê³¼: {success}, {message}")
        
    except Exception as e:
        logger.error(f"??ì£¼ë¬¸ ? íš¨??ê²€???ŒìŠ¤??ì¤??¤ë¥˜: {e}")
        return False
    finally:
        order_handler.disconnect()
    
    return True

def main():
    """ë©”ì¸ ?ŒìŠ¤???¨ìˆ˜"""
    setup_logging()
    
    logger.info("?? ì£¼ë¬¸ ì²˜ë¦¬ ?ŒìŠ¤???œì‘")
    
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
        ("ì£¼ë¬¸ ì²˜ë¦¬", test_order_handler),
        ("ì£¼ë¬¸ ? íš¨??ê²€??, test_order_validation),
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
