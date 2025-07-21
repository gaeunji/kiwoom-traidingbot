#!/usr/bin/env python
"""
.env ?Œì¼ ?ì„± ?¤í¬ë¦½íŠ¸
env.example.envë¥?ê¸°ë°˜?¼ë¡œ .env ?Œì¼???ì„±?©ë‹ˆ??
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """env.example.envë¥?.envë¡?ë³µì‚¬"""
    example_file = Path('env.example.env')
    env_file = Path('.env')
    
    if not example_file.exists():
        print("??env.example.env ?Œì¼??ì¡´ì¬?˜ì? ?ŠìŠµ?ˆë‹¤.")
        return False
    
    if env_file.exists():
        overwrite = input(".env ?Œì¼???´ë? ì¡´ì¬?©ë‹ˆ?? ??–´?°ì‹œê² ìŠµ?ˆê¹Œ? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("ì·¨ì†Œ?˜ì—ˆ?µë‹ˆ??")
            return False
    
    try:
        shutil.copy2(example_file, env_file)
        print("??.env ?Œì¼???ì„±?˜ì—ˆ?µë‹ˆ??")
        print("?“ .env ?Œì¼???´ì–´???¤ì œ ê°’ë“¤???…ë ¥?´ì£¼?¸ìš”:")
        print("   - KIWOOM_ACCESS_TOKEN: ? í° ë°œê¸‰ ???…ë ¥")
        print("   - ACCOUNT_NUMBER: ?¤ì œ ê³„ì¢Œë²ˆí˜¸ ?…ë ¥")
        return True
        
    except Exception as e:
        print(f"??.env ?Œì¼ ?ì„± ?¤íŒ¨: {e}")
        return False

def main():
    """ë©”ì¸ ?¤í–‰ ?¨ìˆ˜"""
    print("?¤ì?ì¦ê¶Œ API .env ?Œì¼ ?ì„±")
    print("=" * 40)
    
    success = create_env_file()
    
    if success:
        print("\n?¤ìŒ ?¨ê³„:")
        print("1. .env ?Œì¼???´ì–´???¤ì œ ê³„ì¢Œë²ˆí˜¸ë¥??…ë ¥?˜ì„¸??)
        print("2. python issue_token.pyë¥??¤í–‰?˜ì—¬ ? í°??ë°œê¸‰?˜ì„¸??)
        print("3. ë°œê¸‰??? í°??.env ?Œì¼???€?¥í•˜?¸ìš”")
        print("4. python place_order.pyë¡?ì£¼ë¬¸ ê¸°ëŠ¥???ŒìŠ¤?¸í•˜?¸ìš”")

if __name__ == '__main__':
    main() 
