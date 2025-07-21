#!/usr/bin/env python
"""
.env ?�일 ?�성 ?�크립트
env.example.env�?기반?�로 .env ?�일???�성?�니??
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """env.example.env�?.env�?복사"""
    example_file = Path('env.example.env')
    env_file = Path('.env')
    
    if not example_file.exists():
        print("??env.example.env ?�일??존재?��? ?�습?�다.")
        return False
    
    if env_file.exists():
        overwrite = input(".env ?�일???��? 존재?�니?? ??��?�시겠습?�까? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("취소?�었?�니??")
            return False
    
    try:
        shutil.copy2(example_file, env_file)
        print("??.env ?�일???�성?�었?�니??")
        print("?�� .env ?�일???�어???�제 값들???�력?�주?�요:")
        print("   - KIWOOM_ACCESS_TOKEN: ?�큰 발급 ???�력")
        print("   - ACCOUNT_NUMBER: ?�제 계좌번호 ?�력")
        return True
        
    except Exception as e:
        print(f"??.env ?�일 ?�성 ?�패: {e}")
        return False

def main():
    """메인 ?�행 ?�수"""
    print("?��?증권 API .env ?�일 ?�성")
    print("=" * 40)
    
    success = create_env_file()
    
    if success:
        print("\n?�음 ?�계:")
        print("1. .env ?�일???�어???�제 계좌번호�??�력?�세??)
        print("2. python issue_token.py�??�행?�여 ?�큰??발급?�세??)
        print("3. 발급???�큰??.env ?�일???�?�하?�요")
        print("4. python place_order.py�?주문 기능???�스?�하?�요")

if __name__ == '__main__':
    main() 
