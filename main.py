#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 REST API 주식 매매 테스트
메인 실행 진입점
"""

import sys
import time
import argparse
from loguru import logger

# 유틸리티 모듈 import
from utils.logging_setup import setup_logging
from utils.config_check import check_configuration
from utils.connection_test import test_connection

# 실행 모듈 import
from scripts.interactive_runner import run_interactive_mode
from scripts.automated_runner import run_automated_mode

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='키움증권 주식 매매 테스트')
    parser.add_argument('--mode', choices=['interactive', 'automated', 'test'], 
                       default='interactive', help='실행 모드')
    parser.add_argument('--config-check', action='store_true', 
                       help='설정 확인만 실행')
    parser.add_argument('--skip-test-connection', action='store_true',
                       help='API 연결 테스트를 건너뜁니다')
    
    args = parser.parse_args()
    
    # 1. 로깅 설정 시간 측정
    start = time.time()
    setup_logging()
    logger.info(f"로깅 설정 완료: {time.time() - start:.2f}초")
    
    logger.info("키움증권 주식 매매 테스트 시작")
    
    # 2. 설정 확인 시간 측정
    start = time.time()
    if not check_configuration():
        logger.error(f"설정 확인 실패: {time.time() - start:.2f}초")
        sys.exit(1)
    logger.info(f"설정 확인 완료: {time.time() - start:.2f}초")
    
    if args.config_check:
        logger.info("설정 확인만 실행 후 종료")
        return
    
    # 3. 연결 테스트 시간 측정 (옵션)
    if not args.skip_test_connection:
        start = time.time()
        if not test_connection():
            logger.error(f"API 연결 테스트 실패: {time.time() - start:.2f}초")
            sys.exit(1)
        logger.info(f"연결 테스트 완료: {time.time() - start:.2f}초")
    else:
        logger.info("API 연결 테스트를 건너뜁니다.")
    
    # 모드별 실행
    if args.mode == 'interactive':
        run_interactive_mode()
    elif args.mode == 'automated':
        run_automated_mode()
    elif args.mode == 'test':
        logger.info("테스트 모드 완료")
    
    logger.info("프로그램 종료")

if __name__ == "__main__":
    main()
