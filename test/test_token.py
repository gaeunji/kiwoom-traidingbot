#!/usr/bin/env python
"""
?¤ì?ì¦ê¶Œ API ?‘ê·¼ ? í° ë°œê¸‰ ?ŒìŠ¤???¤í¬ë¦½íŠ¸
"""

import sys
import os
from loguru import logger
from kiwoom import TokenManager

def setup_logging():
    """ë¡œê¹… ?¤ì •"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def test_token_issuance():
    """? í° ë°œê¸‰ ?ŒìŠ¤??""
    logger.info("=== ? í° ë°œê¸‰ ?ŒìŠ¤???œì‘ ===")
    
    token_manager = TokenManager()
    
    # 1. ? í° ë°œê¸‰
    logger.info("1. ?‘ê·¼ ? í° ë°œê¸‰")
    result = token_manager.issue_access_token()
    
    if result and result.get('success'):
        logger.success("??? í° ë°œê¸‰ ?±ê³µ")
        
        # ? í° ?•ë³´ ì¶œë ¥
        logger.info("ë°œê¸‰??? í° ?•ë³´:")
        logger.info(f"  ?¡ì„¸??? í°: {result['access_token'][:20]}...")
        logger.info(f"  ? í° ?€?? {result['token_type']}")
        logger.info(f"  ë§Œë£Œ ?œê°„: {result['expires_at']}")
        logger.info(f"  ?¤ì½”?? {result['scope']}")
        
        # 2. Authorization ?¤ë” ?ŒìŠ¤??
        logger.info("2. Authorization ?¤ë” ?ì„±")
        auth_header = token_manager.get_authorization_header()
        if auth_header:
            logger.success(f"??Authorization ?¤ë” ?ì„± ?±ê³µ: {auth_header[:30]}...")
        else:
            logger.error("??Authorization ?¤ë” ?ì„± ?¤íŒ¨")
            return False
        
        # 3. ? í° ? íš¨???•ì¸
        logger.info("3. ? í° ? íš¨???•ì¸")
        is_valid = token_manager.is_token_valid()
        if is_valid:
            logger.success("??? í° ? íš¨???•ì¸ ?±ê³µ")
        else:
            logger.warning("? ï¸ ? í° ? íš¨???•ì¸ ?¤íŒ¨")
        
        # 4. ? í° ê°±ì‹  ?ŒìŠ¤??
        logger.info("4. ? í° ê°±ì‹  ?ŒìŠ¤??)
        refresh_success = token_manager.refresh_token_if_needed()
        if refresh_success:
            logger.success("??? í° ê°±ì‹  ?ŒìŠ¤???±ê³µ")
        else:
            logger.warning("? ï¸ ? í° ê°±ì‹  ?ŒìŠ¤???¤íŒ¨")
        
        # 5. ? í° ì´ˆê¸°???ŒìŠ¤??
        logger.info("5. ? í° ì´ˆê¸°???ŒìŠ¤??)
        token_manager.clear_token()
        is_valid_after_clear = token_manager.is_token_valid()
        if not is_valid_after_clear:
            logger.success("??? í° ì´ˆê¸°???±ê³µ")
        else:
            logger.error("??? í° ì´ˆê¸°???¤íŒ¨")
        
        return True
    else:
        logger.error("??? í° ë°œê¸‰ ?¤íŒ¨")
        if result:
            logger.error(f"?ëŸ¬: {result.get('error', 'Unknown error')}")
            logger.error(f"?íƒœ ì½”ë“œ: {result.get('status_code', 'N/A')}")
        return False

def test_token_with_custom_credentials():
    """?¬ìš©???•ì˜ ?ê²© ì¦ëª…?¼ë¡œ ? í° ë°œê¸‰ ?ŒìŠ¤??""
    logger.info("=== ?¬ìš©???•ì˜ ?ê²© ì¦ëª… ?ŒìŠ¤???œì‘ ===")
    
    # ?˜ê²½ ë³€?˜ì—???ê²© ì¦ëª… ê°€?¸ì˜¤ê¸?
    app_key = os.getenv('KIWOOM_APP_KEY')
    secret_key = os.getenv('KIWOOM_APP_SECRET')
    
    if not app_key or not secret_key:
        logger.warning("? ï¸ ?¬ìš©???•ì˜ ?ê²© ì¦ëª…???¤ì •?˜ì? ?Šì•˜?µë‹ˆ??")
        logger.info("?˜ê²½ ë³€??KIWOOM_APP_KEY?€ KIWOOM_APP_SECRET???¤ì •?´ì£¼?¸ìš”.")
        return False
    
    token_manager = TokenManager()
    
    # ?¬ìš©???•ì˜ ?ê²© ì¦ëª…?¼ë¡œ ? í° ë°œê¸‰
    result = token_manager.issue_access_token(app_key, secret_key)
    
    if result and result.get('success'):
        logger.success("???¬ìš©???•ì˜ ?ê²© ì¦ëª…?¼ë¡œ ? í° ë°œê¸‰ ?±ê³µ")
        logger.info(f"?±í‚¤: {app_key[:10]}...")
        logger.info(f"?œí¬ë¦¿í‚¤: {secret_key[:10]}...")
        return True
    else:
        logger.error("???¬ìš©???•ì˜ ?ê²© ì¦ëª…?¼ë¡œ ? í° ë°œê¸‰ ?¤íŒ¨")
        if result:
            logger.error(f"?ëŸ¬: {result.get('error', 'Unknown error')}")
        return False

def main():
    """ë©”ì¸ ?ŒìŠ¤???¨ìˆ˜"""
    setup_logging()
    
    logger.info("?? ?¤ì?ì¦ê¶Œ API ?‘ê·¼ ? í° ë°œê¸‰ ?ŒìŠ¤???œì‘")
    
    # ?˜ê²½ ë³€???•ì¸
    required_vars = ['KIWOOM_APP_KEY', 'KIWOOM_APP_SECRET']
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
        ("? í° ë°œê¸‰", test_token_issuance),
        ("?¬ìš©???•ì˜ ?ê²© ì¦ëª…", test_token_with_custom_credentials),
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
        logger.success("?¤ì?ì¦ê¶Œ API ?‘ê·¼ ? í° ë°œê¸‰???•ìƒ?ìœ¼ë¡??‘ë™?©ë‹ˆ??")
        return True
    else:
        logger.warning("? ï¸ ?¼ë? ?ŒìŠ¤?¸ê? ?¤íŒ¨?ˆìŠµ?ˆë‹¤.")
        logger.warning("?¤íŒ¨???ŒìŠ¤?¸ë? ?•ì¸?˜ê³  ë¬¸ì œë¥??´ê²°?´ì£¼?¸ìš”.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
