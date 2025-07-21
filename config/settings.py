#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 API 설정
"""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings(BaseSettings):
    """키움증권 API 설정 클래스"""
    
    # API 키 설정
    KIWOOM_APP_KEY: str = os.getenv('KIWOOM_APP_KEY', '')
    KIWOOM_APP_SECRET: str = os.getenv('KIWOOM_APP_SECRET', '')
    KIWOOM_ACCESS_TOKEN: str = os.getenv('KIWOOM_ACCESS_TOKEN', '')
    
    # 계좌 정보
    ACCOUNT_NUMBER: str = os.getenv('ACCOUNT_NUMBER', '')
    
    # API 엔드포인트
    KIWOOM_BASE_URL: str = os.getenv('KIWOOM_BASE_URL', 'https://api.kiwoom.com')
    KIWOOM_TOKEN_URL: str = os.getenv('KIWOOM_TOKEN_URL', 'https://api.kiwoom.com/oauth2/token')
    
    # 토큰 설정
    ACCESS_TOKEN: str = os.getenv('ACCESS_TOKEN', '')
    REFRESH_TOKEN: str = os.getenv('REFRESH_TOKEN', '')
    TOKEN_EXPIRES_AT: str = os.getenv('TOKEN_EXPIRES_AT', '')
    
    # 거래 설정
    MAX_POSITION_SIZE: float = float(os.getenv('MAX_POSITION_SIZE', '1000000'))
    STOP_LOSS_RATIO: float = float(os.getenv('STOP_LOSS_RATIO', '0.02'))
    TAKE_PROFIT_RATIO: float = float(os.getenv('TAKE_PROFIT_RATIO', '0.05'))
    
    # 로깅 설정
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'trading.log')
    
    # 데이터베이스 설정
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./trading.db')
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # 추가 필드 무시

# 설정 인스턴스 생성
settings = Settings() 
