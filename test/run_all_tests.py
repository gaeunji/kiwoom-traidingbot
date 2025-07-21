#!/usr/bin/env python
"""
?�합 ?�스???�행 ?�크립트
모든 ?�스?��? ?�차?�으�??�행?�니??
"""

import sys
import os
import subprocess
import time
from loguru import logger

def setup_logging():
    """로깅 ?�정"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def run_test_script(script_name, description):
    """개별 ?�스???�크립트 ?�행"""
    logger.info(f"\n{'='*60}")
    logger.info(f"?�스???�행: {description}")
    logger.info(f"?�크립트: {script_name}")
    logger.info(f"{'='*60}")
    
    try:
        # Python ?�크립트 ?�행
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5�??�?�아??
        )
        
        if result.returncode == 0:
            logger.success(f"??{description} ?�스???�공")
            if result.stdout:
                logger.info("출력:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        logger.info(f"  {line}")
            return True
        else:
            logger.error(f"??{description} ?�스???�패 (종료 코드: {result.returncode})")
            if result.stderr:
                logger.error("?�러 출력:")
                for line in result.stderr.strip().split('\n'):
                    if line.strip():
                        logger.error(f"  {line}")
            if result.stdout:
                logger.info("?��? 출력:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        logger.info(f"  {line}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"??{description} ?�스???�?�아??(5�?초과)")
        return False
    except FileNotFoundError:
        logger.error(f"???�스???�크립트�?찾을 ???�습?�다: {script_name}")
        return False
    except Exception as e:
        logger.error(f"??{description} ?�스???�행 �??�류: {e}")
        return False

def check_environment():
    """?�경 ?�정 ?�인"""
    logger.info("?�� ?�경 ?�정 ?�인")
    
    # ?�수 ?�경 변???�인
    required_vars = ['KIWOOM_APP_KEY', 'KIWOOM_APP_SECRET', 'ACCOUNT_NUMBER']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"???�수 ?�경 변?��? ?�정?��? ?�았?�니?? {', '.join(missing_vars)}")
        logger.error("?�� .env ?�일???�성?�고 ?�요???�보�??�력?�주?�요.")
        return False
    
    logger.success("???�경 변???�정 ?�인 ?�료")
    
    # ?�수 ?�일 ?�인
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
        logger.error(f"???�수 ?�스???�일???�습?�다: {', '.join(missing_files)}")
        return False
    
    logger.success("???�스???�일 ?�인 ?�료")
    
    return True

def main():
    """메인 ?�수"""
    setup_logging()
    
    logger.info("?? ?��?증권 주식 매매 ?�스???�합 ?�스???�작")
    
    # ?�경 ?�정 ?�인
    if not check_environment():
        logger.error("???�경 ?�정 ?�인 ?�패")
        return False
    
    # ?�스???�크립트 목록
    tests = [
        ('test_token.py', '?�큰 발급 ?�스??),
        ('test_connection.py', 'API ?�결 ?�스??),
        ('test_strategy.py', '거래 ?�략 ?�스??),
        ('test_order.py', '주문 처리 ?�스??),
        ('test_order_new.py', '?�로??주문 API ?�스??),
    ]
    
    # ?�스???�행
    results = []
    start_time = time.time()
    
    for script_name, description in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"?�스???�작: {description}")
        logger.info(f"{'='*60}")
        
        test_start_time = time.time()
        success = run_test_script(script_name, description)
        test_end_time = time.time()
        
        test_duration = test_end_time - test_start_time
        logger.info(f"?�스???�요 ?�간: {test_duration:.2f}�?)
        
        results.append((description, success, test_duration))
        
        # ?�스??�?간격
        if success:
            logger.info("?�음 ?�스?�로 진행?�니??..")
        else:
            logger.warning("?�스???�패. 계속 진행?��? ?�인?�세??")
            response = input("계속 진행?�시겠습?�까? (y/N): ").strip().lower()
            if response != 'y':
                logger.info("?�스??중단")
                break
    
    # 결과 ?�약
    total_time = time.time() - start_time
    logger.info(f"\n{'='*60}")
    logger.info("?�합 ?�스??결과 ?�약")
    logger.info(f"{'='*60}")
    
    success_count = 0
    total_duration = 0
    
    for description, success, duration in results:
        status = "???�공" if success else "???�패"
        logger.info(f"{description}: {status} ({duration:.2f}�?")
        if success:
            success_count += 1
        total_duration += duration
    
    logger.info(f"\n?�체 ?�스?? {len(results)}�?�?{success_count}�??�공")
    logger.info(f"�??�요 ?�간: {total_time:.2f}�?)
    
    if success_count == len(results):
        logger.success("?�� 모든 ?�스?��? ?�공?�습?�다!")
        logger.success("?��?증권 주식 매매 ?�스?�이 ?�상?�으�??�동?�니??")
        return True
    else:
        logger.warning("?�️ ?��? ?�스?��? ?�패?�습?�다.")
        logger.warning("?�패???�스?��? ?�인?�고 문제�??�결?�주?�요.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
