#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 API 연결 관리 클래스
"""

import requests
import json
import time
from typing import Dict, Optional
from loguru import logger
from config.settings import settings
from .token_manager import TokenManager

class KiwoomConnector:
    """키움증권 API 연결 관리 클래스"""
    
    def __init__(self):
        self.app_key = settings.KIWOOM_APP_KEY
        self.app_secret = settings.KIWOOM_APP_SECRET
        self.base_url = settings.KIWOOM_BASE_URL
        self.session = requests.Session()
        self.is_connected = False
        
        # 토큰 관리자 초기화
        self.token_manager = TokenManager()
        
        # 기본 헤더 설정
        self.session.headers.update({
            'Content-Type': 'application/json',
            'appKey': self.app_key,
            'appSecret': self.app_secret
        })
    
    def connect(self) -> bool:
        """API 연결 및 인증"""
        try:
            if not self.app_key or not self.app_secret:
                logger.error("APP_KEY와 APP_SECRET이 설정되지 않았습니다.")
                return False
            
            # 액세스 토큰 발급
            if self.get_access_token():
                self.is_connected = True
                logger.info("키움증권 API 연결 성공")
                return True
            else:
                logger.error("키움증권 API 연결 실패")
                return False
                
        except Exception as e:
            logger.error(f"연결 중 오류 발생: {e}")
            return False
    
    def get_access_token(self) -> bool:
        """액세스 토큰 발급"""
        try:
            # 토큰 관리자를 통해 토큰 발급
            result = self.token_manager.issue_access_token()
            
            if result and result.get('success'):
                # 헤더 업데이트
                auth_header = self.token_manager.get_authorization_header()
                if auth_header:
                    self.session.headers.update({
                        'authorization': auth_header
                    })
                logger.info("액세스 토큰 발급 성공")
                return True
            else:
                logger.error("액세스 토큰 발급 실패")
                if result:
                    logger.error(f"오류: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"액세스 토큰 발급 중 오류: {e}")
            return False
    
    def refresh_token(self) -> bool:
        """토큰 갱신"""
        return self.token_manager.refresh_token_if_needed()
    
    def disconnect(self):
        """연결 해제"""
        self.is_connected = False
        self.session.close()
        logger.info("키움증권 API 연결 해제")
    
    def is_token_valid(self) -> bool:
        """토큰 유효성 검사"""
        return self.token_manager.is_token_valid()
    
    def get_connection_status(self) -> Dict:
        """연결 상태 정보 반환"""
        return {
            'is_connected': self.is_connected,
            'has_token': bool(self.token_manager.access_token),
            'token_valid': self.is_token_valid(),
            'app_key_configured': bool(self.app_key),
            'app_secret_configured': bool(self.app_secret),
            'account_configured': bool(settings.ACCOUNT_NUMBER)
        }
    
    def get_account_balance(self, qry_tp: str = '1', dmst_stex_tp: str = 'KRX', cont_yn: str = 'N', next_key: str = '') -> Optional[Dict]:
        """
        계좌평가잔고내역요청 (kt00018) - 키움증권 샘플코드 방식
        
        Args:
            qry_tp: 조회구분 1:합산, 2:개별
            dmst_stex_tp: 국내거래소구분 KRX:한국거래소
            cont_yn: 연속조회여부 N:조회, Y:연속조회
            next_key: 연속조회키
            
        Returns:
            API 응답 데이터 또는 None
        """
        try:
            if not self.token_manager.is_token_valid():
                if not self.token_manager.refresh_token_if_needed():
                    return None
            
            token = self.token_manager.access_token
            host = 'https://api.kiwoom.com'  # 실전투자
            endpoint = '/api/dostk/acnt'
            url = host + endpoint
            
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'authorization': f'Bearer {token}',
                'cont-yn': cont_yn,
                'next-key': next_key,
                'api-id': 'kt00018',
            }
            
            data = {
                'qry_tp': qry_tp,  # 조회구분 1:합산, 2:개별
                'dmst_stex_tp': dmst_stex_tp,  # 국내거래소구분 KRX:한국거래소
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            logger.info(f"계좌평가잔고내역요청 - Status: {response.status_code}")
            logger.info(f"Response Headers: {json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False)}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Response Body: {json.dumps(result, indent=4, ensure_ascii=False)}")
                return result
            else:
                logger.error(f"계좌평가잔고내역요청 실패: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"계좌평가잔고내역요청 중 오류 발생: {e}")
            return None
