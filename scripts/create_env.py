#!/usr/bin/env python
"""
.env ?ì¼ ?ì± ?¤í¬ë¦½í¸
env.example.envë¥?ê¸°ë°?¼ë¡ .env ?ì¼???ì±?©ë??
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """env.example.envë¥?.envë¡?ë³µì¬"""
    example_file = Path('env.example.env')
    env_file = Path('.env')
    
    if not example_file.exists():
        print("??env.example.env ?ì¼??ì¡´ì¬?ì? ?ìµ?ë¤.")
        return False
    
    if env_file.exists():
        overwrite = input(".env ?ì¼???´ë? ì¡´ì¬?©ë?? ??´?°ìê² ìµ?ê¹? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("ì·¨ì?ì?µë??")
            return False
    
    try:
        shutil.copy2(example_file, env_file)
        print("??.env ?ì¼???ì±?ì?µë??")
        print("? .env ?ì¼???´ì´???¤ì  ê°ë¤???ë ¥?´ì£¼?¸ì:")
        print("   - KIWOOM_ACCESS_TOKEN: ? í° ë°ê¸ ???ë ¥")
        print("   - ACCOUNT_NUMBER: ?¤ì  ê³ì¢ë²í¸ ?ë ¥")
        return True
        
    except Exception as e:
        print(f"??.env ?ì¼ ?ì± ?¤í¨: {e}")
        return False

def main():
    """ë©ì¸ ?¤í ?¨ì"""
    print("?¤ì?ì¦ê¶ API .env ?ì¼ ?ì±")
    print("=" * 40)
    
    success = create_env_file()
    
    if success:
        print("\n?¤ì ?¨ê³:")
        print("1. .env ?ì¼???´ì´???¤ì  ê³ì¢ë²í¸ë¥??ë ¥?ì¸??)
        print("2. python issue_token.pyë¥??¤í?ì¬ ? í°??ë°ê¸?ì¸??)
        print("3. ë°ê¸??? í°??.env ?ì¼????¥í?¸ì")
        print("4. python place_order.pyë¡?ì£¼ë¬¸ ê¸°ë¥???ì¤?¸í?¸ì")

if __name__ == '__main__':
    main() 
