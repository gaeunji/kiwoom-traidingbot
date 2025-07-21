#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 API 주문 처리 클래스
"""

import requests
import json
from typing import Dict, Optional, Tuple, List
from loguru import logger
from config.settings import settings
from .token_manager import TokenManager
from .connector import KiwoomConnector

class OrderHandler:
    """키움증권 API 주문 처리 클래스"""
    
    def __init__(self):
        self.connector = KiwoomConnector()
        self.token_manager = self.connector.token_manager
        self.base_url = settings.KIWOOM_BASE_URL
        self.account_number = settings.ACCOUNT_NUMBER
        
    def connect(self) -> bool:
        """API 연결"""
        return self.connector.connect()
    
    def disconnect(self):
        """API 연결 해제"""
        self.connector.disconnect()
    
    def get_connection_status(self) -> Dict:
        """연결 상태 확인"""
        return self.connector.get_connection_status()
    
    def place_buy_order(self, stock_code: str, quantity: int, price: int = 0, trade_type: str = '6') -> Tuple[bool, str]:
        """매수 주문 (키움증권 샘플코드 방식)"""
        import json
        try:
            # 토큰 유효성 확인 및 갱신
            if not self.token_manager.is_token_valid():
                if not self.token_manager.refresh_token_if_needed():
                    return False, "토큰 갱신 실패"
            
            token = self.token_manager.access_token
            url = 'https://api.kiwoom.com/api/dostk/ordr'
            
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'authorization': f'Bearer {token}',
                'cont-yn': 'N',
                'next-key': '',
                'api-id': 'kt10000',
            }
            
            # 주문 데이터 준비 (키움 샘플코드와 동일)
            order_data = {
                'dmst_stex_tp': 'KRX',
                'stk_cd': stock_code,
                'ord_qty': str(quantity),
                'ord_uv': str(price) if price > 0 else '',
                'trde_tp': trade_type,  # 6: 최유리지정가 (키움 샘플코드 기준)
                'cond_uv': '',
            }
            
            response = requests.post(url, headers=headers, json=order_data)
            print('Code:', response.status_code)
            print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
            print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status_code') == '0000':
                    logger.info(f"매수 주문 성공: {stock_code}, {quantity}주")
                    return True, "매수 주문 성공"
                else:
                    error_msg = result.get('message', '알 수 없는 오류')
                    logger.error(f"매수 주문 실패: {error_msg}")
                    return False, f"매수 주문 실패: {error_msg}"
            else:
                logger.error(f"매수 주문 API 호출 실패: {response.status_code}")
                return False, f"API 호출 실패: {response.status_code}"
                
        except Exception as e:
            logger.error(f"매수 주문 중 오류 발생: {e}")
            return False, f"주문 처리 오류: {str(e)}"
    
    def place_sell_order(self, stock_code: str, quantity: int, price: int = 0, trade_type: str = '6') -> Tuple[bool, str]:
        """매도 주문 (키움증권 샘플코드 방식)"""
        import json
        try:
            # 토큰 유효성 확인 및 갱신
            if not self.token_manager.is_token_valid():
                if not self.token_manager.refresh_token_if_needed():
                    return False, "토큰 갱신 실패"
            
            token = self.token_manager.access_token
            url = 'https://api.kiwoom.com/api/dostk/ordr'
            
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'authorization': f'Bearer {token}',
                'cont-yn': 'N',
                'next-key': '',
                'api-id': 'kt10001',
            }
            
            # 주문 데이터 준비 (키움 샘플코드 사용)
            order_data = {
                'dmst_stex_tp': 'KRX',
                'stk_cd': stock_code,
                'ord_qty': str(quantity),
                'ord_uv': str(price) if price > 0 else '',
                'trde_tp': trade_type,  # 6: 최유리지정가 (키움 샘플코드 기준)
                'cond_uv': '',
            }
            
            response = requests.post(url, headers=headers, json=order_data)
            print('Code:', response.status_code)
            print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
            print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status_code') == '0000':
                    logger.info(f"매도 주문 성공: {stock_code}, {quantity}주")
                    return True, "매도 주문 성공"
                else:
                    error_msg = result.get('message', '알 수 없는 오류')
                    logger.error(f"매도 주문 실패: {error_msg}")
                    return False, f"매도 주문 실패: {error_msg}"
            else:
                logger.error(f"매도 주문 API 호출 실패: {response.status_code}")
                return False, f"API 호출 실패: {response.status_code}"
                
        except Exception as e:
            logger.error(f"매도 주문 중 오류 발생: {e}")
            return False, f"주문 처리 오류: {str(e)}"
    
    def place_order(self, stock_code: str, quantity: int, price: int = 0, trade_type: str = '6', order_type: str = '1') -> Tuple[bool, str]:
        """일반 주문 처리 (매수/매도 통합) - 키움증권 샘플코드 방식"""
        if order_type == '1':  # 매수
            return self.place_buy_order(stock_code, quantity, price, trade_type)
        elif order_type == '2':  # 매도
            return self.place_sell_order(stock_code, quantity, price, trade_type)
        else:
            return False, "잘못된 주문 타입"
    
    def get_order_history(self) -> Optional[List[Dict]]:
        """주문 내역 조회"""
        try:
            if not self.connector.is_connected:
                logger.error("API가 연결되지 않았습니다.")
                return None
            
            url = f"{self.base_url}/api/dostk/ordr"
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'authorization': self.token_manager.get_authorization_header(),
                'api-id': 'kt10002',  # 주문 내역 조회 API ID
            }
            
            data = {
                'dmst_stex_tp': 'KRX',
                'cont_yn': 'N',
                'next_key': ''
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status_code') == '0000':
                    return result.get('data')
                else:
                    logger.error(f"주문 내역 조회 실패: {result.get('message')}")
                    return None
            else:
                logger.error(f"주문 내역 조회 API 호출 실패: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"주문 내역 조회 중 오류 발생: {e}")
            return None
    
    def get_order_status(self, order_id: str) -> Optional[Dict]:
        """주문 상태 조회"""
        try:
            if not self.connector.is_connected:
                logger.error("API가 연결되지 않았습니다.")
                return None
            
            # 주문 내역에서 해당 주문 ID 검색
            order_history = self.get_order_history()
            if order_history:
                for order in order_history:
                    if order.get('ODNO') == order_id:
                        return order
            
            return None
            
        except Exception as e:
            logger.error(f"주문 상태 조회 중 오류 발생: {e}")
            return None
    
    def cancel_order(self, order_id: str) -> Tuple[bool, str]:
        """주문 취소"""
        try:
            if not self.connector.is_connected:
                logger.error("API가 연결되지 않았습니다.")
                return False, "API 연결 실패"
            
            url = f"{self.base_url}/uapi/domestic-stock/v1/trading/order-cash"
            
            data = {
                'CANO': self.account_number,
                'ACNT_PRDT_CD': '01',
                'OVRS_EXCG_CD': 'KRX',
                'PDNO': '',
                'ORD_DVSN': '00',
                'ORD_QTY': '0',
                'OVRS_ORD_UNPR': '0',
                'CTAC_TLNO': '',
                'MGCO_APTM_ODNO': order_id,
                'ORD_APLC_CNT': '1',
                'OVRS_RSVN_ORD_YN': 'N'
            }
            
            response = self.connector.session.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get('rt_cd') == '0':
                logger.info(f"주문 취소 성공: {order_id}")
                return True, "주문 취소 성공"
            else:
                error_msg = result.get('msg1', '알 수 없는 오류')
                logger.error(f"주문 취소 실패: {error_msg}")
                return False, f"주문 취소 실패: {error_msg}"
                
        except Exception as e:
            logger.error(f"주문 취소 중 오류 발생: {e}")
            return False, str(e)
