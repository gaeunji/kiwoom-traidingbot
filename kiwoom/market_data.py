#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 시장 데이터 API 클래스
"""

import requests
import json
import time
from typing import Dict, Optional, List
from loguru import logger
from config.settings import settings
from .token_manager import TokenManager

class MarketDataAPI:
    """키움증권 시장 데이터 API"""
    
    def __init__(self):
        self.base_url = settings.KIWOOM_BASE_URL
        self.token_manager = TokenManager()
        
    def get_market_price(self, stock_code: str, cont_yn='N', next_key='') -> dict | None:
        """
        시장가 조회 (ka10095)
        Args:
            stock_code (str): 종목코드
            cont_yn (str): 연속조회 여부
            next_key (str): 다음 페이지 키
        Returns:
            dict or None: 응답 데이터
        """
        try:
            if not self.token_manager.is_token_valid():
                if not self.token_manager.refresh_token_if_needed():
                    return None

            token = self.token_manager.access_token
            host = 'https://api.kiwoom.com'
            endpoint = '/api/dostk/stkinfo'
            url = host + endpoint

            data = {'stk_cd': stock_code}
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'authorization': f'Bearer {token}',
                'cont-yn': cont_yn,
                'next-key': next_key,
                'api-id': 'ka10095',
            }

            response = requests.post(url, headers=headers, json=data)
            logger.debug(f"시장가 조회(ka10095) 응답코드: {response.status_code}")
            logger.debug(f"응답 헤더: {json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, ensure_ascii=False)}")
            try:
                body = response.json()
                logger.debug(f"응답 바디: {json.dumps(body, indent=2, ensure_ascii=False)}")
            except Exception as e:
                logger.error(f"JSON 파싱 오류: {e}")
                body = response.text
                logger.error(f"응답 텍스트: {body}")

            if response.status_code == 200:
                return body
            else:
                logger.error(f"시장가 조회(ka10095) API 호출 실패: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"시장가 조회(ka10095) 호출 중 오류: {e}")
            import traceback
            logger.error(f"상세 오류: {traceback.format_exc()}")
            return None
    
    def get_top_volume_stocks(self, limit: int = 20, market_type: str = '000', cont_yn: str = 'N', next_key: str = '') -> Optional[List[Dict]]:
        """
        당일거래량상위요청 (ka10030) - 키움증권 샘플코드 방식
        """
        import json
        try:
            if not self.token_manager.is_token_valid():
                if not self.token_manager.refresh_token_if_needed():
                    return None

            token = self.token_manager.access_token
            url = 'https://api.kiwoom.com/api/dostk/rkinfo'
            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'authorization': f'Bearer {token}',
                'cont-yn': cont_yn,
                'next-key': next_key,
                'api-id': 'ka10030',
            }
            data = {
                'mrkt_tp': market_type,
                'sort_tp': '1',
                'mang_stk_incls': '0',
                'crd_tp': '0',
                'trde_qty_tp': '0',
                'pric_tp': '0',
                'trde_prica_tp': '0',
                'mrkt_open_tp': '0',
                'stex_tp': '3',
            }
            response = requests.post(url, headers=headers, json=data)
            print('Code:', response.status_code)
            print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
            
            if response.status_code == 200:
                result = response.json()
                
                # 데이터 필드 확인 (키움 API 응답 구조에 맞게 수정)
                if 'tdy_trde_qty_upper' in result:
                    if result['tdy_trde_qty_upper']:
                        print(f"조회된 종목 수: {len(result['tdy_trde_qty_upper'])}개")
                        stocks = result['tdy_trde_qty_upper']
                        processed_stocks = self._process_volume_stocks(stocks)
                        if limit > 0:
                            processed_stocks = processed_stocks[:limit]
                        return processed_stocks
                    else:
                        print("tdy_trde_qty_upper 필드는 있지만 비어있습니다.")
                        logger.error("❌ 거래량 상위 종목 조회 실패: 데이터 없음")
                        return None
                else:
                    print("응답에 'tdy_trde_qty_upper' 필드가 없습니다.")
                    print(f"응답 키들: {list(result.keys())}")
                    logger.error("❌ 거래량 상위 종목 조회 실패: 데이터 없음")
                    return None
            else:
                logger.error(f"❌ 거래량상위요청 API 호출 실패: {response.status_code}")
                logger.error(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            logger.error(f"❌ 거래량 상위 종목 조회 중 예외 발생: {e}")
            return None
    
    def get_top_volume_stocks_all(self, limit: int = 100, market_type: str = '000') -> Optional[List[Dict]]:
        """
        전체 거래량 상위 종목 조회 (연속조회 포함)
        
        Args:
            limit (int): 조회할 종목 수
            market_type (str): 시장구분
            
        Returns:
            List[Dict]: 전체 거래량 상위 종목 리스트
        """
        try:
            all_stocks = []
            cont_yn = 'N'
            next_key = ''
            
            while True:
                stocks = self.get_top_volume_stocks(
                    limit=0,  # limit=0으로 설정하여 모든 데이터 조회
                    market_type=market_type,
                    cont_yn=cont_yn,
                    next_key=next_key
                )
                
                if not stocks:
                    break
                
                all_stocks.extend(stocks)
                
                # 연속조회 여부 확인
                cont_yn = 'N'  # 실제 응답 헤더에서 확인 필요
                next_key = ''   # 실제 응답 헤더에서 확인 필요
                
                # 연속조회 중단 조건 설정
                if len(stocks) < 50:  # 한번에 조회하는 최대 개수
                    break
                
                # 연속조회 간격 조절
                time.sleep(0.1)
            
            # limit 적용
            if limit > 0:
                all_stocks = all_stocks[:limit]
            
            logger.info(f"✅ 전체 거래량 상위 종목 조회 완료: {len(all_stocks)}개")
            return all_stocks
            
        except Exception as e:
            logger.error(f"❌ 전체 거래량 상위 종목 조회 중 오류: {e}")
            return None
    
    def _process_volume_stocks(self, raw_stocks: List[Dict]) -> List[Dict]:
        """
        거래량 상위 종목 데이터 처리 (키움 API 필드명에 맞게 수정)
        
        Args:
            raw_stocks (List[Dict]): 원본 종목 데이터
            
        Returns:
            List[Dict]: 처리된 종목 데이터
        """
        processed_stocks = []
        
        for stock in raw_stocks:
            try:
                processed_stock = {
                    'stock_code': stock.get('stk_cd', ''),  # 종목코드
                    'stock_name': stock.get('stk_nm', ''),  # 종목명
                    'current_price': float(stock.get('cur_prc', 0)),  # 현재가
                    'volume': int(stock.get('trde_qty', 0)),  # 거래량
                    'change_amount': float(stock.get('pred_pre', 0)),  # 전일대비
                    'change_rate': float(stock.get('flu_rt', 0)),  # 등락률
                    'trade_amount': int(stock.get('trde_amt', 0)),  # 거래대금
                    'turnover_ratio': float(stock.get('trde_tern_rt', 0)),  # 거래대비율
                    'timestamp': time.time()
                }
                processed_stocks.append(processed_stock)
            except Exception as e:
                logger.warning(f"종목 데이터 처리 중 오류: {e}, 데이터: {stock}")
                continue
        
        return processed_stocks
    
    def get_market_summary(self) -> Optional[Dict]:
        """시장 요약 정보 조회"""
        try:
            if not self.token_manager.is_token_valid():
                if not self.token_manager.refresh_token_if_needed():
                    return None
            
            url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-price"
            params = {
                'FID_COND_MRKT_DIV_CODE': 'J',
                'FID_INPUT_ISCD': '000001'  # KOSPI 지수
            }
            headers = self.token_manager.get_authorization_header()
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('rt_cd') == '0':
                    return result.get('output')
                else:
                    logger.error(f"시장 요약 조회 실패: {result.get('msg1')}")
                    return None
            else:
                logger.error(f"시장 요약 조회 API 호출 실패: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"시장 요약 조회 중 오류 발생: {e}")
            return None 

    def get_watchlist_info(self, stock_codes, cont_yn='N', next_key=''):
        """
        관심종목정보요청 (ka10095)
        Args:
            stock_codes (list[str] or str): 종목코드 리스트 또는 단일 코드
            cont_yn (str): 연속조회 여부
            next_key (str): 다음 페이지 키
        Returns:
            dict or None: 응답 데이터
        """
        try:
            if not self.token_manager.is_token_valid():
                if not self.token_manager.refresh_token_if_needed():
                    return None

            token = self.token_manager.access_token
            host = 'https://api.kiwoom.com'
            endpoint = '/api/dostk/stkinfo'
            url = host + endpoint

            # 단일 코드도 리스트로 변환
            if isinstance(stock_codes, str):
                stock_codes = [stock_codes]

            # 요청 데이터: 여러 종목 지원 (API 문서에 따라 수정)
            # 예시: {'stk_cd': '005930'} 또는 {'stk_cd_list': ['005930', '000660']}
            if len(stock_codes) == 1:
                data = {'stk_cd': stock_codes[0]}
            else:
                data = {'stk_cd_list': stock_codes}

            headers = {
                'Content-Type': 'application/json;charset=UTF-8',
                'authorization': f'Bearer {token}',
                'cont-yn': cont_yn,
                'next-key': next_key,
                'api-id': 'ka10095',
            }

            response = requests.post(url, headers=headers, json=data)
            logger.debug(f"관심종목정보요청 응답코드: {response.status_code}")
            logger.debug(f"응답 헤더: {json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, ensure_ascii=False)}")
            try:
                body = response.json()
                logger.debug(f"응답 바디: {json.dumps(body, indent=2, ensure_ascii=False)}")
            except Exception as e:
                logger.error(f"JSON 파싱 오류: {e}")
                body = response.text
                logger.error(f"응답 텍스트: {body}")

            if response.status_code == 200:
                return body
            else:
                logger.error(f"관심종목정보요청 API 호출 실패: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"관심종목정보요청(ka10095) 호출 중 오류: {e}")
            import traceback
            logger.error(f"상세 오류: {traceback.format_exc()}")
            return None 
