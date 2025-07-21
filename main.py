#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 REST API 주식 매매 테스트
메인 실행 진입점
"""

import sys
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
    
    args = parser.parse_args()
    
    # 로깅 설정
    setup_logging()
    
    logger.info("키움증권 주식 매매 테스트 시작")
    
    # 설정 확인
    if not check_configuration():
        sys.exit(1)
    
    if args.config_check:
        logger.info("설정 확인 완료")
        return
    
    # 연결 테스트
    if not test_connection():
        logger.error("API 연결 테스트 실패")
        sys.exit(1)
    
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
