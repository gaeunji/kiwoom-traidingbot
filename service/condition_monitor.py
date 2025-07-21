#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 조건 검색 매수 감시 서비스
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from loguru import logger
from kiwoom import OrderHandler, MarketDataAPI
from config.settings import settings

class ConditionMonitor:
    """조건 검색 매수 감시 서비스"""
    
    def __init__(self):
        self.order_handler = OrderHandler()
        self.market_data = MarketDataAPI()
        self.is_running = False
        self.conditions = {}
        self.monitored_stocks = set()
        self.condition_results = {}
        
    def add_condition(self, name: str, condition_func: Callable, 
                     check_interval: int = 60, auto_buy: bool = False,
                     buy_quantity: int = 1, max_buy_amount: int = 1000000):
        """
        조건 추가
        
        Args:
            name (str): 조건 이름
            condition_func (Callable): 조건 검사 함수
            check_interval (int): 검사 간격 (초)
            auto_buy (bool): 자동 매수 여부
            buy_quantity (int): 매수 수량
            max_buy_amount (int): 최대 매수 금액
        """
        self.conditions[name] = {
            'function': condition_func,
            'check_interval': check_interval,
            'auto_buy': auto_buy,
            'buy_quantity': buy_quantity,
            'max_buy_amount': max_buy_amount,
            'last_check': None,
            'triggered_stocks': set()
        }
        logger.info(f"✅ 조건 '{name}' 추가됨 (검사간격: {check_interval}초, 자동매수: {auto_buy})")
    
    def remove_condition(self, name: str):
        """조건 제거"""
        if name in self.conditions:
            del self.conditions[name]
            logger.info(f"✅ 조건 '{name}' 제거됨")
        else:
            logger.warning(f"⚠️ 조건 '{name}'을 찾을 수 없습니다")
    
    def add_stock_to_monitor(self, stock_code: str, stock_name: str = ""):
        """감시 종목 추가"""
        self.monitored_stocks.add(stock_code)
        logger.info(f"✅ 감시 종목 추가: {stock_code} {stock_name}")
    
    def remove_stock_from_monitor(self, stock_code: str):
        """감시 종목 제거"""
        if stock_code in self.monitored_stocks:
            self.monitored_stocks.remove(stock_code)
            logger.info(f"✅ 감시 종목 제거: {stock_code}")
        else:
            logger.warning(f"⚠️ 감시 종목 '{stock_code}'을 찾을 수 없습니다")
    
    def check_condition(self, condition_name: str, stock_code: str) -> bool:
        """조건 검사"""
        if condition_name not in self.conditions:
            return False
        
        condition = self.conditions[condition_name]
        try:
            result = condition['function'](stock_code)
            return result
        except Exception as e:
            logger.error(f"❌ 조건 검사 오류 ({condition_name}, {stock_code}): {e}")
            return False
    
    def execute_auto_buy(self, condition_name: str, stock_code: str):
        """자동 매수 실행"""
        if condition_name not in self.conditions:
            return
        
        condition = self.conditions[condition_name]
        if not condition['auto_buy']:
            return
        
        try:
            # 현재가 조회
            price_info = self.market_data.get_market_price(stock_code)
            if not price_info:
                logger.warning(f"⚠️ 현재가 조회 실패: {stock_code}")
                return
            
            current_price = float(price_info.get('prpr', 0))
            if current_price <= 0:
                logger.warning(f"⚠️ 유효하지 않은 현재가: {current_price}")
                return
            
            # 매수 금액 계산
            buy_quantity = condition['buy_quantity']
            buy_amount = current_price * buy_quantity
            
            # 최대 매수 금액 체크
            if buy_amount > condition['max_buy_amount']:
                logger.warning(f"⚠️ 매수 금액 초과: {buy_amount:,}원 > {condition['max_buy_amount']:,}원")
                return
            
            # 매수 주문 실행
            success, message = self.order_handler.place_buy_order(
                stock_code=stock_code,
                quantity=buy_quantity,
                price=int(current_price),
                trade_type='6'  # 최유리지정가
            )
            
            if success:
                logger.info(f"✅ 자동 매수 성공: {stock_code} {buy_quantity}주 @ {current_price:,}원")
                condition['triggered_stocks'].add(stock_code)
            else:
                logger.error(f"❌ 자동 매수 실패: {stock_code} - {message}")
                
        except Exception as e:
            logger.error(f"❌ 자동 매수 실행 오류: {e}")
    
    def monitor_conditions(self):
        """조건 감시 실행"""
        if not self.conditions or not self.monitored_stocks:
            logger.warning("⚠️ 감시할 조건이나 종목이 없습니다")
            return
        
        self.is_running = True
        logger.info(f"🚀 조건 감시 시작 (조건: {len(self.conditions)}개, 종목: {len(self.monitored_stocks)}개)")
        
        try:
            while self.is_running:
                current_time = datetime.now()
                
                for condition_name, condition in self.conditions.items():
                    # 검사 간격 체크
                    if (condition['last_check'] and 
                        (current_time - condition['last_check']).seconds < condition['check_interval']):
                        continue
                    
                    condition['last_check'] = current_time
                    
                    # 모든 감시 종목에 대해 조건 검사
                    for stock_code in self.monitored_stocks:
                        if self.check_condition(condition_name, stock_code):
                            logger.info(f"🎯 조건 '{condition_name}' 만족: {stock_code}")
                            
                            # 자동 매수 실행
                            if condition['auto_buy']:
                                self.execute_auto_buy(condition_name, stock_code)
                            
                            # 결과 저장
                            if condition_name not in self.condition_results:
                                self.condition_results[condition_name] = []
                            
                            self.condition_results[condition_name].append({
                                'stock_code': stock_code,
                                'timestamp': current_time.isoformat(),
                                'auto_buy': condition['auto_buy']
                            })
                
                time.sleep(1)  # 1초 대기
                
        except KeyboardInterrupt:
            logger.info("⏹️ 조건 감시 중단됨")
            self.stop()
        except Exception as e:
            logger.error(f"❌ 조건 감시 오류: {e}")
            self.stop()
    
    def stop(self):
        """조건 감시 중지"""
        self.is_running = False
        logger.info("⏹️ 조건 감시 중지")
    
    def get_condition_results(self, condition_name: str = None) -> Dict:
        """조건 검사 결과 반환"""
        if condition_name:
            return self.condition_results.get(condition_name, [])
        return self.condition_results.copy()
    
    def clear_condition_results(self, condition_name: str = None):
        """조건 검사 결과 초기화"""
        if condition_name:
            if condition_name in self.condition_results:
                self.condition_results[condition_name] = []
        else:
            self.condition_results.clear()
        logger.info("✅ 조건 검사 결과 초기화")

# 기본 조건 함수 예제
def volume_spike_condition(stock_code: str) -> bool:
    """거래량 급증 조건"""
    try:
        # 거래량 상위 종목 조회
        volume_stocks = MarketDataAPI().get_top_volume_stocks(limit=50)
        if not volume_stocks:
            return False
        
        # 해당 종목이 상위 50위 안에 있는지 확인
        for stock in volume_stocks:
            if stock.get('stock_code') == stock_code:
                return True
        
        return False
    except Exception as e:
        logger.error(f"❌ 거래량 급증 조건 검사 오류: {e}")
        return False

def price_breakout_condition(stock_code: str) -> bool:
    """가격 돌파 조건"""
    try:
        # 현재가 조회
        price_info = MarketDataAPI().get_market_price(stock_code)
        if not price_info:
            return False
        
        current_price = float(price_info.get('prpr', 0))
        change_rate = float(price_info.get('prdy_ctrt', 0))
        
        # 등락률 5% 이상 조건
        return change_rate >= 5.0
        
    except Exception as e:
        logger.error(f"❌ 가격 돌파 조건 검사 오류: {e}")
        return False

if __name__ == "__main__":
    # 조건 감시 테스트
    monitor = ConditionMonitor()
    
    # 조건 추가
    monitor.add_condition("거래량급증", volume_spike_condition, 
                         check_interval=30, auto_buy=False)
    monitor.add_condition("가격돌파", price_breakout_condition, 
                         check_interval=60, auto_buy=True, buy_quantity=1)
    
    # 감시 종목 추가
    monitor.add_stock_to_monitor("005930", "삼성전자")
    monitor.add_stock_to_monitor("000660", "SK하이닉스")
    
    # 조건 감시 시작
    monitor.monitor_conditions() 