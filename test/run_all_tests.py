#!/usr/bin/env python
"""
통합 테스트 실행 스크립트
모든 테스트를 순차적으로 실행합니다.
"""

import sys
import os
import subprocess
import time
from loguru import logger

def setup_logging():
    """로깅 설정"""
    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

def run_test_script(script_name, description):
    """개별 테스트 스크립트 실행"""
    logger.info(f"\n{'='*60}")
    logger.info(f"테스트 실행: {description}")
    logger.info(f"스크립트: {script_name}")
    logger.info(f"{'='*60}")
    
    try:
        # Python 스크립트 실행
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5분 초과시 종료
        )
        
        if result.returncode == 0:
            logger.success(f"✅ {description} 테스트 성공")
            if result.stdout:
                logger.info("출력:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        logger.info(f"  {line}")
            return True
        else:
            logger.error(f"❌ {description} 테스트 실패 (종료 코드: {result.returncode})")
            if result.stderr:
                logger.error("에러 출력:")
                for line in result.stderr.strip().split('\n'):
                    if line.strip():
                        logger.error(f"  {line}")
            if result.stdout:
                logger.info("표준 출력:")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        logger.info(f"  {line}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"❌ {description} 테스트 타임아웃(5분 초과)")
        return False
    except FileNotFoundError:
        logger.error(f"❌ 테스트 스크립트를 찾을 수 없습니다: {script_name}")
        return False
    except Exception as e:
        logger.error(f"❌ {description} 테스트 실행 오류: {e}")
        return False

def check_environment():
    """환경 설정 확인"""
    logger.info("필수 환경 설정 확인")
    
    # 필수 환경 변수 확인
    required_vars = ['KIWOOM_APP_KEY', 'KIWOOM_APP_SECRET', 'ACCOUNT_NUMBER']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ 필수 환경 변수가 설정되어 있지 않습니다: {', '.join(missing_vars)}")
        logger.error("반드시 .env 파일을 생성하고 내용을 입력해 주세요.")
        return False
    
    logger.success("✅ 환경 변수 설정 확인 완료")
    
    # 필수 파일 확인
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
        logger.error(f"❌ 필수 테스트 파일이 없습니다: {', '.join(missing_files)}")
        return False
    
    logger.success("✅ 테스트 파일 확인 완료")
    
    return True

def main():
    """메인 함수"""
    setup_logging()
    
    logger.info("🔎 키움증권 주식 매매 테스트 통합 테스트 시작")
    
    # 환경 설정 확인
    if not check_environment():
        logger.error("❌ 환경 설정 확인 실패")
        return False
    
    # 테스트 스크립트 목록
    tests = [
        ('test_token.py', '토큰 발급 테스트'),
        ('test_connection.py', 'API 연결 테스트'),
        ('test_strategy.py', '거래 전략 테스트'),
        ('test_order.py', '주문 처리 테스트'),
        ('test_order_new.py', '신규주문 API 테스트'),
    ]
    
    # 테스트 실행
    results = []
    start_time = time.time()
    
    for script_name, description in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"테스트 시작: {description}")
        logger.info(f"{'='*60}")
        
        test_start_time = time.time()
        success = run_test_script(script_name, description)
        test_end_time = time.time()
        
        test_duration = test_end_time - test_start_time
        logger.info(f"테스트 소요 시간: {test_duration:.2f}초")
        
        results.append((description, success, test_duration))
        
        # 테스트 간 간격
        if success:
            logger.info("다음 테스트로 진행합니다..")
        else:
            logger.warning("테스트 실패. 계속 진행할지 확인하세요.")
            response = input("계속 진행하시겠습니까? (y/N): ").strip().lower()
            if response != 'y':
                logger.info("테스트 중단")
                break
    
    # 결과 요약
    total_time = time.time() - start_time
    logger.info(f"\n{'='*60}")
    logger.info("통합 테스트 결과 요약")
    logger.info(f"{'='*60}")
    
    success_count = 0
    total_duration = 0
    
    for description, success, duration in results:
        status = "✅ 성공" if success else "❌ 실패"
        logger.info(f"{description}: {status} ({duration:.2f}초)")
        if success:
            success_count += 1
        total_duration += duration
    
    logger.info(f"\n전체 테스트 {len(results)}개 중 {success_count}개 성공")
    logger.info(f"총 소요 시간: {total_time:.2f}초")
    
    if success_count == len(results):
        logger.success("🎉 모든 테스트가 성공했습니다!")
        logger.success("키움증권 주식 매매 시스템이 정상적으로 동작합니다.")
        return True
    else:
        logger.warning("⚠️ 일부 테스트가 실패했습니다.")
        logger.warning("실패한 테스트를 확인하고 문제를 해결해 주세요.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 