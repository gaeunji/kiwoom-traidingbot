#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 API 접근 토큰 발급 스크립트
사용자가 제공한 코드를 기반으로 작성
"""

import requests
import json
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def fn_au10001(data):
    """
    접근토큰 발급 (au10001)
    
    Args:
        data (dict): 요청 데이터 (grant_type, appkey, secretkey)
    """
    # 1. 요청할 API URL
    # host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/oauth2/token'
    url = host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력
    
    return response

def main():
    """메인 실행 함수"""
    print("키움증권 API 접근 토큰 발급")
    print("=" * 50)
    
    # 환경 변수에서 앱키와 시크릿키 가져오기
    app_key = os.getenv('KIWOOM_APP_KEY')
    secret_key = os.getenv('KIWOOM_APP_SECRET')
    
    if not app_key or not secret_key:
        print("❌ 환경 변수에서 앱키 또는 시크릿키를 찾을 수 없습니다.")
        print("📝 .env 파일에 다음을 추가해주세요:")
        print("KIWOOM_APP_KEY=your_actual_app_key")
        print("KIWOOM_APP_SECRET=your_actual_secret_key")
        return
    
    print(f"앱키: {app_key[:10]}...")
    print(f"시크릿키: {secret_key[:10]}...")
    print()
    
    # 1. 요청 데이터
    params = {
        'grant_type': 'client_credentials',  # grant_type
        'appkey': app_key,  # 앱키
        'secretkey': secret_key,  # 시크릿키
    }

    # 2. API 실행
    try:
        response = fn_au10001(data=params)
        
        if response.status_code == 200:
            print("\n✅ 토큰 발급 성공")
            
            # 토큰 정보 추출 (키움 API 응답 구조에 맞게 수정)
            response_data = response.json()
            access_token = response_data.get('token')  # 키움 API는 'token' 필드 사용
            token_type = response_data.get('token_type', 'Bearer')
            expires_dt = response_data.get('expires_dt', '')
            
            print(f"\n발급된 토큰 정보:")
            print(f"  액세스 토큰: {access_token[:20]}...")
            print(f"  토큰 타입: {token_type}")
            print(f"  만료 시간: {expires_dt}")
            
            # Authorization 헤더 표시
            auth_header = f"{token_type} {access_token}"
            print(f"  Authorization 헤더: {auth_header[:30]}...")
            
            # 자동으로 .env 파일에 토큰 저장
            try:
                import sys
                # 프로젝트 루트 디렉토리를 Python 경로에 추가
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                sys.path.insert(0, project_root)
                
                from kiwoom import TokenManager
                token_manager = TokenManager()
                token_manager.access_token = access_token
                token_manager.save_token_to_env()
                print("✅ 토큰이 .env 파일에 자동 저장되었습니다.")
            except Exception as e:
                print(f"❌ .env 파일 저장 실패: {e}")
                print("📝 수동으로 .env 파일에 다음을 추가해주세요:")
                print(f"ACCESS_TOKEN={access_token}")
            
        else:
            print(f"\n❌ 토큰 발급 실패: {response.status_code}")
            print("📝 응답 내용을 확인해주세요.")
            
    except Exception as e:
        print(f"\n❌ 토큰 발급 중 오류 발생: {e}")

if __name__ == '__main__':
    main() 
