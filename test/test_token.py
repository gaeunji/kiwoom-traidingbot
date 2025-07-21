#!/usr/bin/env python
"""
?��?증권 API ?�근 ?�큰 발급 ?�스???�크립트
"""

import sys
import os
from loguru import logger
from kiwoom import TokenManager

def setup_logging():
    """로깅 ?�정"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def test_token_issuance():
    """?�큰 발급 ?�스??""
    logger.info("=== ?�큰 발급 ?�스???�작 ===")
    
    token_manager = TokenManager()
    
    # 1. ?�큰 발급
    logger.info("1. ?�근 ?�큰 발급")
    result = token_manager.issue_access_token()
    
    if result and result.get('success'):
        logger.success("???�큰 발급 ?�공")
        
        # ?�큰 ?�보 출력
        logger.info("발급???�큰 ?�보:")
        logger.info(f"  ?�세???�큰: {result['access_token'][:20]}...")
        logger.info(f"  ?�큰 ?�?? {result['token_type']}")
        logger.info(f"  만료 ?�간: {result['expires_at']}")
        logger.info(f"  ?�코?? {result['scope']}")
        
        # 2. Authorization ?�더 ?�스??
        logger.info("2. Authorization ?�더 ?�성")
        auth_header = token_manager.get_authorization_header()
        if auth_header:
            logger.success(f"??Authorization ?�더 ?�성 ?�공: {auth_header[:30]}...")
        else:
            logger.error("??Authorization ?�더 ?�성 ?�패")
            return False
        
        # 3. ?�큰 ?�효???�인
        logger.info("3. ?�큰 ?�효???�인")
        is_valid = token_manager.is_token_valid()
        if is_valid:
            logger.success("???�큰 ?�효???�인 ?�공")
        else:
            logger.warning("?�️ ?�큰 ?�효???�인 ?�패")
        
        # 4. ?�큰 갱신 ?�스??
        logger.info("4. ?�큰 갱신 ?�스??)
        refresh_success = token_manager.refresh_token_if_needed()
        if refresh_success:
            logger.success("???�큰 갱신 ?�스???�공")
        else:
            logger.warning("?�️ ?�큰 갱신 ?�스???�패")
        
        # 5. ?�큰 초기???�스??
        logger.info("5. ?�큰 초기???�스??)
        token_manager.clear_token()
        is_valid_after_clear = token_manager.is_token_valid()
        if not is_valid_after_clear:
            logger.success("???�큰 초기???�공")
        else:
            logger.error("???�큰 초기???�패")
        
        return True
    else:
        logger.error("???�큰 발급 ?�패")
        if result:
            logger.error(f"?�러: {result.get('error', 'Unknown error')}")
            logger.error(f"?�태 코드: {result.get('status_code', 'N/A')}")
        return False

def test_token_with_custom_credentials():
    """?�용???�의 ?�격 증명?�로 ?�큰 발급 ?�스??""
    logger.info("=== ?�용???�의 ?�격 증명 ?�스???�작 ===")
    
    # ?�경 변?�에???�격 증명 가?�오�?
    app_key = os.getenv('KIWOOM_APP_KEY')
    secret_key = os.getenv('KIWOOM_APP_SECRET')
    
    if not app_key or not secret_key:
        logger.warning("?�️ ?�용???�의 ?�격 증명???�정?��? ?�았?�니??")
        logger.info("?�경 변??KIWOOM_APP_KEY?� KIWOOM_APP_SECRET???�정?�주?�요.")
        return False
    
    token_manager = TokenManager()
    
    # ?�용???�의 ?�격 증명?�로 ?�큰 발급
    result = token_manager.issue_access_token(app_key, secret_key)
    
    if result and result.get('success'):
        logger.success("???�용???�의 ?�격 증명?�로 ?�큰 발급 ?�공")
        logger.info(f"?�키: {app_key[:10]}...")
        logger.info(f"?�크릿키: {secret_key[:10]}...")
        return True
    else:
        logger.error("???�용???�의 ?�격 증명?�로 ?�큰 발급 ?�패")
        if result:
            logger.error(f"?�러: {result.get('error', 'Unknown error')}")
        return False

def main():
    """메인 ?�스???�수"""
    setup_logging()
    
    logger.info("?? ?��?증권 API ?�근 ?�큰 발급 ?�스???�작")
    
    # ?�경 변???�인
    required_vars = ['KIWOOM_APP_KEY', 'KIWOOM_APP_SECRET']
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
        ("?�큰 발급", test_token_issuance),
        ("?�용???�의 ?�격 증명", test_token_with_custom_credentials),
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
        logger.success("?��?증권 API ?�근 ?�큰 발급???�상?�으�??�동?�니??")
        return True
    else:
        logger.warning("?�️ ?��? ?�스?��? ?�패?�습?�다.")
        logger.warning("?�패???�스?��? ?�인?�고 문제�??�결?�주?�요.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
