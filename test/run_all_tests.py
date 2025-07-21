#!/usr/bin/env python
"""
?µí•© ?ŒìŠ¤???¤í–‰ ?¤í¬ë¦½íŠ¸
ëª¨ë“  ?ŒìŠ¤?¸ë? ?œì°¨?ìœ¼ë¡??¤í–‰?©ë‹ˆ??
"""

import sys
import os
import subprocess
import time
from loguru import logger

def setup_logging():
    """ë¡œê¹… ?¤ì •"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def run_test_script(script_name, description):
    """ê°œë³„ ?ŒìŠ¤???¤í¬ë¦½íŠ¸ ?¤í–‰"""
    logger.info(f"\n{'='*60}")
    logger.info(f"?ŒìŠ¤???¤í–‰: {description}")
    logger.info(f"?¤í¬ë¦½íŠ¸: {script_name}")
    logger.info(f"{'='*60}")
    
    try:
        # Python ?¤í¬ë¦½íŠ¸ ?¤í–‰
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5ë¶??€?„ì•„??
        )
        
        if result.returncode == 0:
            logger.success(f"??{description} ?ŒìŠ¤???±ê³µ")
            if result.stdout:
                logger.info("ì¶œë ¥:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        logger.info(f"  {line}")
            return True
        else:
            logger.error(f"??{description} ?ŒìŠ¤???¤íŒ¨ (ì¢…ë£Œ ì½”ë“œ: {result.returncode})")
            if result.stderr:
                logger.error("?ëŸ¬ ì¶œë ¥:")
                for line in result.stderr.strip().split('\n'):
                    if line.strip():
                        logger.error(f"  {line}")
            if result.stdout:
                logger.info("?œì? ì¶œë ¥:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        logger.info(f"  {line}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"??{description} ?ŒìŠ¤???€?„ì•„??(5ë¶?ì´ˆê³¼)")
        return False
    except FileNotFoundError:
        logger.error(f"???ŒìŠ¤???¤í¬ë¦½íŠ¸ë¥?ì°¾ì„ ???†ìŠµ?ˆë‹¤: {script_name}")
        return False
    except Exception as e:
        logger.error(f"??{description} ?ŒìŠ¤???¤í–‰ ì¤??¤ë¥˜: {e}")
        return False

def check_environment():
    """?˜ê²½ ?¤ì • ?•ì¸"""
    logger.info("?” ?˜ê²½ ?¤ì • ?•ì¸")
    
    # ?„ìˆ˜ ?˜ê²½ ë³€???•ì¸
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
    
    # ?„ìˆ˜ ?Œì¼ ?•ì¸
    required_files = [
        'test_connection.py',
        'test_strategy.py', 
        'test_order.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"???„ìˆ˜ ?ŒìŠ¤???Œì¼???†ìŠµ?ˆë‹¤: {', '.join(missing_files)}")
        return False
    
    logger.success("???ŒìŠ¤???Œì¼ ?•ì¸ ?„ë£Œ")
    
    return True

def main():
    """ë©”ì¸ ?¨ìˆ˜"""
    setup_logging()
    
    logger.info("?? ?¤ì?ì¦ê¶Œ ì£¼ì‹ ë§¤ë§¤ ?œìŠ¤???µí•© ?ŒìŠ¤???œì‘")
    
    # ?˜ê²½ ?¤ì • ?•ì¸
    if not check_environment():
        logger.error("???˜ê²½ ?¤ì • ?•ì¸ ?¤íŒ¨")
        return False
    
    # ?ŒìŠ¤???¤í¬ë¦½íŠ¸ ëª©ë¡
    tests = [
        ('test_token.py', '? í° ë°œê¸‰ ?ŒìŠ¤??),
        ('test_connection.py', 'API ?°ê²° ?ŒìŠ¤??),
        ('test_strategy.py', 'ê±°ë˜ ?„ëµ ?ŒìŠ¤??),
        ('test_order.py', 'ì£¼ë¬¸ ì²˜ë¦¬ ?ŒìŠ¤??),
        ('test_order_new.py', '?ˆë¡œ??ì£¼ë¬¸ API ?ŒìŠ¤??),
    ]
    
    # ?ŒìŠ¤???¤í–‰
    results = []
    start_time = time.time()
    
    for script_name, description in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"?ŒìŠ¤???œì‘: {description}")
        logger.info(f"{'='*60}")
        
        test_start_time = time.time()
        success = run_test_script(script_name, description)
        test_end_time = time.time()
        
        test_duration = test_end_time - test_start_time
        logger.info(f"?ŒìŠ¤???Œìš” ?œê°„: {test_duration:.2f}ì´?)
        
        results.append((description, success, test_duration))
        
        # ?ŒìŠ¤??ê°?ê°„ê²©
        if success:
            logger.info("?¤ìŒ ?ŒìŠ¤?¸ë¡œ ì§„í–‰?©ë‹ˆ??..")
        else:
            logger.warning("?ŒìŠ¤???¤íŒ¨. ê³„ì† ì§„í–‰? ì? ?•ì¸?˜ì„¸??")
            response = input("ê³„ì† ì§„í–‰?˜ì‹œê² ìŠµ?ˆê¹Œ? (y/N): ").strip().lower()
            if response != 'y':
                logger.info("?ŒìŠ¤??ì¤‘ë‹¨")
                break
    
    # ê²°ê³¼ ?”ì•½
    total_time = time.time() - start_time
    logger.info(f"\n{'='*60}")
    logger.info("?µí•© ?ŒìŠ¤??ê²°ê³¼ ?”ì•½")
    logger.info(f"{'='*60}")
    
    success_count = 0
    total_duration = 0
    
    for description, success, duration in results:
        status = "???±ê³µ" if success else "???¤íŒ¨"
        logger.info(f"{description}: {status} ({duration:.2f}ì´?")
        if success:
            success_count += 1
        total_duration += duration
    
    logger.info(f"\n?„ì²´ ?ŒìŠ¤?? {len(results)}ê°?ì¤?{success_count}ê°??±ê³µ")
    logger.info(f"ì´??Œìš” ?œê°„: {total_time:.2f}ì´?)
    
    if success_count == len(results):
        logger.success("?‰ ëª¨ë“  ?ŒìŠ¤?¸ê? ?±ê³µ?ˆìŠµ?ˆë‹¤!")
        logger.success("?¤ì?ì¦ê¶Œ ì£¼ì‹ ë§¤ë§¤ ?œìŠ¤?œì´ ?•ìƒ?ìœ¼ë¡??‘ë™?©ë‹ˆ??")
        return True
    else:
        logger.warning("? ï¸ ?¼ë? ?ŒìŠ¤?¸ê? ?¤íŒ¨?ˆìŠµ?ˆë‹¤.")
        logger.warning("?¤íŒ¨???ŒìŠ¤?¸ë? ?•ì¸?˜ê³  ë¬¸ì œë¥??´ê²°?´ì£¼?¸ìš”.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
