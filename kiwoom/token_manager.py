#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 API 토큰 관리 클래스
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
from loguru import logger
from dotenv import load_dotenv
from config.settings import settings

# .env 파일 로드
load_dotenv()

class TokenManager:
    """키움증권 API 토큰 관리 클래스"""
    
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.token_type = 'Bearer'
        self.token_expires_at = None
        
        # .env 파일에서 토큰 로드 시도
        self.load_token_from_env()
    
    def issue_access_token(self, save_to_env=False):
        """
        접근 토큰 발급 (샘플 코드 방식)
        Args:
            save_to_env (bool): .env 파일에 저장할지 여부
        Returns:
            Dict: 발급 결과
        """
        import requests
        import json
        from datetime import datetime, timedelta
        try:
            app_key = settings.KIWOOM_APP_KEY
            app_secret = settings.KIWOOM_APP_SECRET
            if not app_key or not app_secret:
                logger.error("APP_KEY와 APP_SECRET이 설정되지 않았습니다.")
                return {'success': False, 'error': 'API 키가 설정되지 않음'}

            host = 'https://api.kiwoom.com'
            endpoint = '/oauth2/token'
            url = host + endpoint
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
            }
            data = {
                'grant_type': 'client_credentials',
                'appkey': app_key,
                'secretkey': app_secret,
            }
            response = requests.post(url, headers=headers, json=data)

            print('Code:', response.status_code)
            print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
            print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))

            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get('token')
                self.refresh_token = result.get('refresh_token')
                self.token_type = result.get('token_type', 'Bearer')
                expires_dt = result.get('expires_dt')
                if expires_dt:
                    try:
                        self.token_expires_at = datetime.strptime(expires_dt, '%Y%m%d%H%M%S')
                    except ValueError:
                        self.token_expires_at = datetime.now() + timedelta(hours=24)
                else:
                    self.token_expires_at = datetime.now() + timedelta(hours=24)
                logger.success(f"✅ 액세스 토큰 발급 성공")
                logger.info(f"토큰 타입: {self.token_type}")
                logger.info(f"만료 시간: {self.token_expires_at}")
                if save_to_env:
                    self.save_token_to_env()
                return {
                    'success': True,
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                    'token_type': self.token_type,
                    'expires_at': self.token_expires_at.isoformat()
                }
            else:
                logger.error(f"❌ 토큰 발급 실패: {response.status_code}")
                logger.error(f"응답 내용: {response.text}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"❌ 토큰 발급 중 예외 발생: {e}")
            return {'success': False, 'error': str(e)}
    
    def is_token_valid(self):
        """
        토큰 유효성 확인
        
        Returns:
            bool: 토큰이 유효한지 여부
        """
        if not self.access_token:
            return False
            
        # 만료 시간이 있으면 시간 기반으로 확인
        if self.token_expires_at:
            # 만료 5분 전부터는 갱신 필요하다고 판단
            refresh_threshold = datetime.now() + timedelta(minutes=5)
            is_valid = self.token_expires_at > refresh_threshold
            if is_valid:
                logger.info("✅ 토큰이 유효합니다 (시간 기반)")
                return True
            else:
                logger.info("⚠️ 토큰이 만료되었습니다 (시간 기반)")
                return False
        
        # 만료 시간이 없으면 API 호출로 유효성을 확인
        logger.info("🔍 만료 시간이 없습니다. 토큰 유효성을 API로 확인합니다.")
        return self._validate_token_with_api()
    
    def _validate_token_with_api(self):
        """
        API 호출로 토큰 유효성 확인
        
        Returns:
            bool: 토큰이 유효한지 여부
        """
        try:
            import requests
            
            # 간단한 API 호출로 토큰 유효성 확인
            url = "https://api.kiwoom.com/api/dostk/acnt"
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'authorization': self.get_authorization_header(),
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            # 401 Unauthorized면 토큰이 만료된 것
            if response.status_code == 401:
                logger.info("❌ 토큰이 만료되었습니다.")
                return False
            elif response.status_code == 200:
                logger.info("✅ 토큰이 유효합니다.")
                return True
            else:
                # 다른 오류는 토큰 문제가 아닐 수 있으므로 유효하다고 가정
                logger.info(f"⚠️ API 응답: {response.status_code}, 토큰은 유효하다고 가정합니다.")
                return True
                
        except Exception as e:
            logger.warning(f"⚠️ 토큰 유효성 확인 중 오류: {e}, 토큰은 유효하다고 가정합니다.")
            return True
    
    def get_access_token(self):
        """
        현재 액세스 토큰 반환
        
        Returns:
            str: 액세스 토큰 (없으면 None)
        """
        return self.access_token
    
    def get_authorization_header(self):
        """
        Authorization 헤더 반환
        
        Returns:
            str: Authorization 헤더 값
        """
        if self.access_token and self.token_type:
            return f"{self.token_type} {self.access_token}"
        return None
    
    def refresh_token_if_needed(self):
        """
        토큰이 만료되었거나 곧 만료될 경우 갱신
        
        Returns:
            bool: 갱신 성공 여부
        """
        if self.is_token_valid():
            logger.info("✅ 토큰이 유효합니다. 갱신이 필요하지 않습니다.")
            return True
        
        logger.info("🔄 토큰 갱신이 필요합니다.")
        
        # 새로운 토큰 발급
        result = self.issue_access_token(save_to_env=True)
        
        if result.get('success'):
            logger.success("✅ 토큰 갱신 성공")
            return True
        else:
            logger.error(f"❌ 토큰 갱신 실패: {result.get('error')}")
            return False
    
    def save_token_to_env(self):
        """토큰을 .env 파일에 저장"""
        try:
            env_file = '.env'
            
            # 기존 .env 파일 읽기
            env_content = {}
            if os.path.exists(env_file):
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            env_content[key] = value
            
            # 토큰 정보 업데이트
            if self.access_token:
                env_content['ACCESS_TOKEN'] = self.access_token
            if self.refresh_token:
                env_content['REFRESH_TOKEN'] = self.refresh_token
            if self.token_expires_at:
                env_content['TOKEN_EXPIRES_AT'] = self.token_expires_at.isoformat()
            
            # .env 파일에 저장
            with open(env_file, 'w', encoding='utf-8') as f:
                for key, value in env_content.items():
                    f.write(f"{key}={value}\n")
            
            logger.info("✅ 토큰이 .env 파일에 저장되었습니다.")
            
        except Exception as e:
            logger.error(f"❌ .env 파일 저장 실패: {e}")
    
    def load_token_from_env(self):
        """환경 변수에서 토큰 로드"""
        try:
            # 환경 변수에서 토큰 로드
            self.access_token = os.getenv('ACCESS_TOKEN')
            self.refresh_token = os.getenv('REFRESH_TOKEN')
            
            # 만료 시간 로드
            expires_at_str = os.getenv('TOKEN_EXPIRES_AT')
            if expires_at_str:
                try:
                    self.token_expires_at = datetime.fromisoformat(expires_at_str)
                except ValueError:
                    logger.warning("⚠️ 토큰 만료 시간 형식이 올바르지 않습니다.")
                    self.token_expires_at = None
            
            if self.access_token:
                logger.info("✅ .env 파일에서 토큰을 로드했습니다.")
                logger.info("🔍 토큰 유효성을 확인하기 위해 API 호출을 시도합니다.")
                # 토큰 유효성 확인
                if self.is_token_valid():
                    logger.info("✅ 로드된 토큰이 유효합니다.")
                else:
                    logger.warning("⚠️ 로드된 토큰이 유효하지 않습니다.")
                    # 토큰이 만료된 경우 자동 갱신 시도
                    if self.refresh_token_if_needed():
                        logger.info("🔄 토큰 자동 갱신 성공")
                    else:
                        logger.error("❌ 토큰 자동 갱신 실패")
            else:
                logger.info("ℹ️ .env 파일에서 토큰을 찾을 수 없습니다.")
                
        except Exception as e:
            logger.error(f"❌ 환경 변수에서 토큰 로드 실패: {e}")
    
    def clear_token(self):
        """토큰 정보 초기화"""
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        logger.info("🗑️ 토큰 정보가 초기화되었습니다.") 
