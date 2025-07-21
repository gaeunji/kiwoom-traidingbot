#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
설정 확인 유틸리티
"""

from loguru import logger
from config.settings import settings

def check_configuration():
    """설정 확인"""
    logger.info("설정 확인 중..")
    
    required_settings = [
        ('KIWOOM_APP_KEY', settings.KIWOOM_APP_KEY),
        ('KIWOOM_APP_SECRET', settings.KIWOOM_APP_SECRET),
        ('ACCOUNT_NUMBER', settings.ACCOUNT_NUMBER)
    ]
    
    missing_settings = []
    for name, value in required_settings:
        if not value:
            missing_settings.append(name)
    
    if missing_settings:
        logger.error(f"필수 설정이 누락되었습니다: {', '.join(missing_settings)}")
        logger.error("config/settings.py 또는 .env 파일을 확인해주세요.")
        return False
    
    logger.info("설정 확인 완료")
    return True 