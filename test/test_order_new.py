#!/usr/bin/env python
"""
?¤ì?ì¦ê¶Œ API ì£¼ë¬¸ ì²˜ë¦¬ ?ŒìŠ¤???¤í¬ë¦½íŠ¸ (?ˆë¡œ??API)
"""

import sys
import os
from loguru import logger
from kiwoom import OrderHandler, TokenManager

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
        
        # 2. ? í° ?íƒœ ?•ì¸
        logger.info("2. ? í° ?íƒœ ?•ì¸")
        token_manager = order_handler.token_manager
        if token_manager.is_token_valid():
            logger.success("??? í° ? íš¨???•ì¸ ?±ê³µ")
            auth_header = token_manager.get_authorization_header()
            logger.info(f"Authorization ?¤ë”: {auth_header[:30]}...")
        else:
            logger.warning("? ï¸ ? í°??? íš¨?˜ì? ?ŠìŠµ?ˆë‹¤.")
        
        # 3. ë§¤ìˆ˜ ì£¼ë¬¸ ?œë??ˆì´??(?¤ì œ ì£¼ë¬¸?€ ?˜ì? ?ŠìŒ)
        logger.info("3. ë§¤ìˆ˜ ì£¼ë¬¸ ?œë??ˆì´??)
        logger.info("  ?¤ì œ ì£¼ë¬¸?€ ?„í—˜?˜ë?ë¡??œë??ˆì´?˜ë§Œ ì§„í–‰?©ë‹ˆ??")
        
        # ?ŒìŠ¤?¸ìš© ì£¼ë¬¸ ?°ì´??
        test_buy_order = {
            'stock_code': '005930',  # ?¼ì„±?„ì
            'quantity': 1,           # 1ì£?
            'price': 0,              # ?œì¥ê°€
            'trade_type': '3'        # ?œì¥ê°€
        }
        
        logger.info(f"  ?ŒìŠ¤??ë§¤ìˆ˜ ì£¼ë¬¸ ?°ì´?? {test_buy_order}")
        logger.info("  ?¤ì œ ë§¤ìˆ˜ ì£¼ë¬¸???í•˜?œë©´ ì£¼ì„???´ì œ?˜ì„¸??")
        
        # ?¤ì œ ë§¤ìˆ˜ ì£¼ë¬¸???í•  ê²½ìš° ?„ë˜ ì£¼ì„ ?´ì œ
        # success, message = order_handler.place_buy_order(
        #     test_buy_order['stock_code'],
        #     test_buy_order['quantity'],
        #     test_buy_order['price'],
        #     test_buy_order['trade_type']
        # )
        # if success:
        #     logger.success(f"??ë§¤ìˆ˜ ì£¼ë¬¸ ?±ê³µ: {message}")
        # else:
        #     logger.error(f"??ë§¤ìˆ˜ ì£¼ë¬¸ ?¤íŒ¨: {message}")
        
        # 4. ë§¤ë„ ì£¼ë¬¸ ?œë??ˆì´??(?¤ì œ ì£¼ë¬¸?€ ?˜ì? ?ŠìŒ)
        logger.info("4. ë§¤ë„ ì£¼ë¬¸ ?œë??ˆì´??)
        logger.info("  ?¤ì œ ì£¼ë¬¸?€ ?„í—˜?˜ë?ë¡??œë??ˆì´?˜ë§Œ ì§„í–‰?©ë‹ˆ??")
        
        # ?ŒìŠ¤?¸ìš© ì£¼ë¬¸ ?°ì´??
        test_sell_order = {
            'stock_code': '005930',  # ?¼ì„±?„ì
            'quantity': 1,           # 1ì£?
            'price': 0,              # ?œì¥ê°€
            'trade_type': '3'        # ?œì¥ê°€
        }
        
        logger.info(f"  ?ŒìŠ¤??ë§¤ë„ ì£¼ë¬¸ ?°ì´?? {test_sell_order}")
        logger.info("  ?¤ì œ ë§¤ë„ ì£¼ë¬¸???í•˜?œë©´ ì£¼ì„???´ì œ?˜ì„¸??")
        
        # ?¤ì œ ë§¤ë„ ì£¼ë¬¸???í•  ê²½ìš° ?„ë˜ ì£¼ì„ ?´ì œ
        # success, message = order_handler.place_sell_order(
        #     test_sell_order['stock_code'],
        #     test_sell_order['quantity'],
        #     test_sell_order['price'],
        #     test_sell_order['trade_type']
        # )
        # if success:
        #     logger.success(f"??ë§¤ë„ ì£¼ë¬¸ ?±ê³µ: {message}")
        # else:
        #     logger.error(f"??ë§¤ë„ ì£¼ë¬¸ ?¤íŒ¨: {message}")
        
        # 5. ?µí•© ì£¼ë¬¸ ?¨ìˆ˜ ?ŒìŠ¤??
        logger.info("5. ?µí•© ì£¼ë¬¸ ?¨ìˆ˜ ?ŒìŠ¤??)
        logger.info("  ?µí•© ì£¼ë¬¸ ?¨ìˆ˜???Œë¼ë¯¸í„° ê²€ì¦ì„ ?ŒìŠ¤?¸í•©?ˆë‹¤.")
        
        # ? íš¨?˜ì? ?Šì? ì£¼ë¬¸ ?€???ŒìŠ¤??
        success, message = order_handler.place_order('005930', 'invalid', 1, 0)
        logger.info(f"  ?˜ëª»??ì£¼ë¬¸ ?€???ŒìŠ¤?? {success}, {message}")
        
        # 6. ì£¼ë¬¸ ? íš¨??ê²€??
        logger.info("6. ì£¼ë¬¸ ? íš¨??ê²€??)
        
        # ?˜ëª»??ì¢…ëª© ì½”ë“œ ?ŒìŠ¤??
        success, message = order_handler.place_order('INVALID', 'buy', 1, 0)
        logger.info(f"  ?˜ëª»??ì¢…ëª© ì½”ë“œ ?ŒìŠ¤?? {success}, {message}")
        
        # ?˜ëª»???˜ëŸ‰ ?ŒìŠ¤??
        success, message = order_handler.place_order('005930', 'buy', -1, 0)
        logger.info(f"  ?˜ëª»???˜ëŸ‰ ?ŒìŠ¤?? {success}, {message}")
        
        # ?˜ëª»??ê°€ê²??ŒìŠ¤??
        success, message = order_handler.place_order('005930', 'buy', 1, -1000)
        logger.info(f"  ?˜ëª»??ê°€ê²??ŒìŠ¤?? {success}, {message}")
        
    except Exception as e:
        logger.error(f"??ì£¼ë¬¸ ì²˜ë¦¬ ?ŒìŠ¤??ì¤??¤ë¥˜: {e}")
        return False
    finally:
        order_handler.disconnect()
    
    return True

def test_order_parameters():
    """ì£¼ë¬¸ ?Œë¼ë¯¸í„° ?ŒìŠ¤??""
    logger.info("=== ì£¼ë¬¸ ?Œë¼ë¯¸í„° ?ŒìŠ¤???œì‘ ===")
    
    order_handler = OrderHandler()
    
    if not order_handler.connect():
        logger.error("??ì£¼ë¬¸ ì²˜ë¦¬ ?°ê²° ?¤íŒ¨")
        return False
    
    logger.success("??ì£¼ë¬¸ ì²˜ë¦¬ ?°ê²° ?±ê³µ")
    
    try:
        # 1. ì§€?•ê? ë§¤ìˆ˜ ?ŒìŠ¤??
        logger.info("1. ì§€?•ê? ë§¤ìˆ˜ ?ŒìŠ¤??)
        logger.info("  ì§€?•ê? ë§¤ìˆ˜ ì£¼ë¬¸ ?Œë¼ë¯¸í„°ë¥??ŒìŠ¤?¸í•©?ˆë‹¤.")
        
        # ì§€?•ê? ë§¤ìˆ˜ ì£¼ë¬¸ ?°ì´??
        limit_buy_data = {
            'stock_code': '005930',  # ?¼ì„±?„ì
            'quantity': 1,           # 1ì£?
            'price': 70000,          # 70,000??ì§€?•ê?
            'trade_type': '1'        # ì§€?•ê?
        }
        
        logger.info(f"  ì§€?•ê? ë§¤ìˆ˜ ?°ì´?? {limit_buy_data}")
        logger.info("  ?¤ì œ ì£¼ë¬¸???í•˜?œë©´ ì£¼ì„???´ì œ?˜ì„¸??")
        
        # ?¤ì œ ì§€?•ê? ë§¤ìˆ˜ ì£¼ë¬¸???í•  ê²½ìš° ?„ë˜ ì£¼ì„ ?´ì œ
        # success, message = order_handler.place_buy_order(
        #     limit_buy_data['stock_code'],
        #     limit_buy_data['quantity'],
        #     limit_buy_data['price'],
        #     limit_buy_data['trade_type']
        # )
        # if success:
        #     logger.success(f"??ì§€?•ê? ë§¤ìˆ˜ ì£¼ë¬¸ ?±ê³µ: {message}")
        # else:
        #     logger.error(f"??ì§€?•ê? ë§¤ìˆ˜ ì£¼ë¬¸ ?¤íŒ¨: {message}")
        
        # 2. ?œì¥ê°€ ë§¤ìˆ˜ ?ŒìŠ¤??
        logger.info("2. ?œì¥ê°€ ë§¤ìˆ˜ ?ŒìŠ¤??)
        logger.info("  ?œì¥ê°€ ë§¤ìˆ˜ ì£¼ë¬¸ ?Œë¼ë¯¸í„°ë¥??ŒìŠ¤?¸í•©?ˆë‹¤.")
        
        # ?œì¥ê°€ ë§¤ìˆ˜ ì£¼ë¬¸ ?°ì´??
        market_buy_data = {
            'stock_code': '005930',  # ?¼ì„±?„ì
            'quantity': 1,           # 1ì£?
            'price': 0,              # ?œì¥ê°€
            'trade_type': '3'        # ?œì¥ê°€
        }
        
        logger.info(f"  ?œì¥ê°€ ë§¤ìˆ˜ ?°ì´?? {market_buy_data}")
        logger.info("  ?¤ì œ ì£¼ë¬¸???í•˜?œë©´ ì£¼ì„???´ì œ?˜ì„¸??")
        
        # ?¤ì œ ?œì¥ê°€ ë§¤ìˆ˜ ì£¼ë¬¸???í•  ê²½ìš° ?„ë˜ ì£¼ì„ ?´ì œ
        # success, message = order_handler.place_buy_order(
        #     market_buy_data['stock_code'],
        #     market_buy_data['quantity'],
        #     market_buy_data['price'],
        #     market_buy_data['trade_type']
        # )
        # if success:
        #     logger.success(f"???œì¥ê°€ ë§¤ìˆ˜ ì£¼ë¬¸ ?±ê³µ: {message}")
        # else:
        #     logger.error(f"???œì¥ê°€ ë§¤ìˆ˜ ì£¼ë¬¸ ?¤íŒ¨: {message}")
        
        # 3. ?°ì† ì¡°íšŒ ?Œë¼ë¯¸í„° ?ŒìŠ¤??
        logger.info("3. ?°ì† ì¡°íšŒ ?Œë¼ë¯¸í„° ?ŒìŠ¤??)
        logger.info("  ?°ì† ì¡°íšŒ ?Œë¼ë¯¸í„°ë¥??ŒìŠ¤?¸í•©?ˆë‹¤.")
        
        # ?°ì† ì¡°íšŒ ?Œë¼ë¯¸í„°
        cont_params = {
            'stock_code': '005930',
            'quantity': 1,
            'price': 0,
            'trade_type': '3',
            'cont_yn': 'Y',
            'next_key': 'test_key'
        }
        
        logger.info(f"  ?°ì† ì¡°íšŒ ?Œë¼ë¯¸í„°: {cont_params}")
        
    except Exception as e:
        logger.error(f"??ì£¼ë¬¸ ?Œë¼ë¯¸í„° ?ŒìŠ¤??ì¤??¤ë¥˜: {e}")
        return False
    finally:
        order_handler.disconnect()
    
    return True

def main():
    """ë©”ì¸ ?ŒìŠ¤???¨ìˆ˜"""
    setup_logging()
    
    logger.info("?? ?¤ì?ì¦ê¶Œ API ì£¼ë¬¸ ì²˜ë¦¬ ?ŒìŠ¤???œì‘ (?ˆë¡œ??API)")
    
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
        ("ì£¼ë¬¸ ?Œë¼ë¯¸í„°", test_order_parameters),
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
        logger.success("?¤ì?ì¦ê¶Œ API ì£¼ë¬¸ ì²˜ë¦¬ê°€ ?•ìƒ?ìœ¼ë¡??‘ë™?©ë‹ˆ??")
        return True
    else:
        logger.warning("? ï¸ ?¼ë? ?ŒìŠ¤?¸ê? ?¤íŒ¨?ˆìŠµ?ˆë‹¤.")
        logger.warning("?¤íŒ¨???ŒìŠ¤?¸ë? ?•ì¸?˜ê³  ë¬¸ì œë¥??´ê²°?´ì£¼?¸ìš”.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
