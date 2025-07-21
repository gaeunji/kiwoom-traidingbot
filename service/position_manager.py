#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 잔고/포지션 관리 서비스
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from loguru import logger
from kiwoom import OrderHandler, MarketDataAPI
from config.settings import settings

class PositionManager:
    """잔고/포지션 관리 서비스"""
    
    def __init__(self):
        self.order_handler = OrderHandler()
        self.market_data = MarketDataAPI()
        self.positions = {}
        self.position_history = []
        self.risk_limits = {
            'max_position_value': 10000000,  # 최대 포지션 가치
            'max_single_stock_value': 2000000,  # 단일 종목 최대 가치
            'max_daily_loss': 500000,  # 일일 최대 손실
            'stop_loss_rate': 0.05,  # 손절 비율 (5%)
            'take_profit_rate': 0.10  # 익절 비율 (10%)
        }
        
    def get_account_balance(self) -> Optional[Dict]:
        """계좌 잔고 조회"""
        try:
            # 실제 API 호출로 계좌 잔고 조회
            # 여기서는 예시 데이터 반환
            balance = {
                'total_balance': 50000000,  # 총 잔고
                'available_balance': 30000000,  # 사용 가능 잔고
                'invested_amount': 20000000,  # 투자 금액
                'unrealized_pnl': 500000,  # 평가 손익
                'realized_pnl': 1000000,  # 실현 손익
                'last_updated': datetime.now().isoformat()
            }
            return balance
        except Exception as e:
            logger.error(f"❌ 계좌 잔고 조회 오류: {e}")
            return None
    
    def get_positions(self) -> Dict:
        """현재 포지션 조회"""
        try:
            # 실제 API 호출로 포지션 조회
            # 여기서는 예시 데이터 반환
            positions = {
                '005930': {  # 삼성전자
                    'stock_code': '005930',
                    'stock_name': '삼성전자',
                    'quantity': 100,
                    'avg_price': 65000,
                    'current_price': 68000,
                    'market_value': 6800000,
                    'unrealized_pnl': 300000,
                    'unrealized_pnl_rate': 0.046,
                    'last_updated': datetime.now().isoformat()
                },
                '000660': {  # SK하이닉스
                    'stock_code': '000660',
                    'stock_name': 'SK하이닉스',
                    'quantity': 50,
                    'avg_price': 120000,
                    'current_price': 115000,
                    'market_value': 5750000,
                    'unrealized_pnl': -250000,
                    'unrealized_pnl_rate': -0.042,
                    'last_updated': datetime.now().isoformat()
                }
            }
            self.positions = positions
            return positions
        except Exception as e:
            logger.error(f"❌ 포지션 조회 오류: {e}")
            return {}
    
    def add_position(self, stock_code: str, quantity: int, price: int):
        """포지션 추가"""
        try:
            # 현재가 조회
            price_info = self.market_data.get_market_price(stock_code)
            if not price_info:
                logger.error(f"❌ 현재가 조회 실패: {stock_code}")
                return False
            
            current_price = float(price_info.get('prpr', 0))
            stock_name = price_info.get('hts_kor_isnm', '')
            
            # 기존 포지션 확인
            if stock_code in self.positions:
                existing = self.positions[stock_code]
                # 평균 매수가 계산
                total_quantity = existing['quantity'] + quantity
                total_cost = (existing['avg_price'] * existing['quantity']) + (price * quantity)
                avg_price = total_cost / total_quantity
                
                self.positions[stock_code] = {
                    'stock_code': stock_code,
                    'stock_name': stock_name,
                    'quantity': total_quantity,
                    'avg_price': avg_price,
                    'current_price': current_price,
                    'market_value': current_price * total_quantity,
                    'unrealized_pnl': (current_price - avg_price) * total_quantity,
                    'unrealized_pnl_rate': (current_price - avg_price) / avg_price,
                    'last_updated': datetime.now().isoformat()
                }
            else:
                # 새로운 포지션
                self.positions[stock_code] = {
                    'stock_code': stock_code,
                    'stock_name': stock_name,
                    'quantity': quantity,
                    'avg_price': price,
                    'current_price': current_price,
                    'market_value': current_price * quantity,
                    'unrealized_pnl': (current_price - price) * quantity,
                    'unrealized_pnl_rate': (current_price - price) / price,
                    'last_updated': datetime.now().isoformat()
                }
            
            # 포지션 히스토리 추가
            self.position_history.append({
                'action': 'buy',
                'stock_code': stock_code,
                'quantity': quantity,
                'price': price,
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info(f"✅ 포지션 추가: {stock_code} {quantity}주 @ {price:,}원")
            return True
            
        except Exception as e:
            logger.error(f"❌ 포지션 추가 오류: {e}")
            return False
    
    def reduce_position(self, stock_code: str, quantity: int, price: int):
        """포지션 감소"""
        try:
            if stock_code not in self.positions:
                logger.error(f"❌ 포지션이 없습니다: {stock_code}")
                return False
            
            position = self.positions[stock_code]
            if position['quantity'] < quantity:
                logger.error(f"❌ 보유 수량 부족: {position['quantity']} < {quantity}")
                return False
            
            # 포지션 업데이트
            remaining_quantity = position['quantity'] - quantity
            if remaining_quantity == 0:
                # 포지션 완전 청산
                del self.positions[stock_code]
            else:
                # 포지션 부분 청산
                position['quantity'] = remaining_quantity
                position['market_value'] = position['current_price'] * remaining_quantity
                position['unrealized_pnl'] = (position['current_price'] - position['avg_price']) * remaining_quantity
                position['unrealized_pnl_rate'] = (position['current_price'] - position['avg_price']) / position['avg_price']
                position['last_updated'] = datetime.now().isoformat()
            
            # 포지션 히스토리 추가
            self.position_history.append({
                'action': 'sell',
                'stock_code': stock_code,
                'quantity': quantity,
                'price': price,
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info(f"✅ 포지션 감소: {stock_code} {quantity}주 @ {price:,}원")
            return True
            
        except Exception as e:
            logger.error(f"❌ 포지션 감소 오류: {e}")
            return False
    
    def check_risk_limits(self) -> List[str]:
        """리스크 한도 체크"""
        violations = []
        
        try:
            # 포지션 업데이트
            self.get_positions()
            
            total_position_value = 0
            daily_pnl = 0
            
            for stock_code, position in self.positions.items():
                position_value = position['market_value']
                total_position_value += position_value
                daily_pnl += position['unrealized_pnl']
                
                # 단일 종목 한도 체크
                if position_value > self.risk_limits['max_single_stock_value']:
                    violations.append(f"단일종목한도초과: {stock_code} ({position_value:,}원)")
                
                # 손절 체크
                if position['unrealized_pnl_rate'] <= -self.risk_limits['stop_loss_rate']:
                    violations.append(f"손절도달: {stock_code} ({position['unrealized_pnl_rate']:.2%})")
                
                # 익절 체크
                if position['unrealized_pnl_rate'] >= self.risk_limits['take_profit_rate']:
                    violations.append(f"익절도달: {stock_code} ({position['unrealized_pnl_rate']:.2%})")
            
            # 총 포지션 한도 체크
            if total_position_value > self.risk_limits['max_position_value']:
                violations.append(f"총포지션한도초과: {total_position_value:,}원")
            
            # 일일 손실 한도 체크
            if daily_pnl < -self.risk_limits['max_daily_loss']:
                violations.append(f"일일손실한도초과: {daily_pnl:,}원")
            
            return violations
            
        except Exception as e:
            logger.error(f"❌ 리스크 한도 체크 오류: {e}")
            return ["리스크체크오류"]
    
    def execute_risk_management(self):
        """리스크 관리 실행"""
        violations = self.check_risk_limits()
        
        if not violations:
            logger.info("✅ 리스크 한도 정상")
            return
        
        logger.warning(f"⚠️ 리스크 한도 위반: {len(violations)}건")
        
        for violation in violations:
            logger.warning(f"⚠️ {violation}")
            
            # 손절 실행
            if "손절도달" in violation:
                stock_code = violation.split(": ")[1].split(" ")[0]
                self.execute_stop_loss(stock_code)
            
            # 익절 실행
            elif "익절도달" in violation:
                stock_code = violation.split(": ")[1].split(" ")[0]
                self.execute_take_profit(stock_code)
    
    def execute_stop_loss(self, stock_code: str):
        """손절 실행"""
        try:
            if stock_code not in self.positions:
                return
            
            position = self.positions[stock_code]
            current_price = position['current_price']
            
            # 시장가 매도 주문
            success, message = self.order_handler.place_sell_order(
                stock_code=stock_code,
                quantity=position['quantity'],
                price=0,  # 시장가
                trade_type='3'  # 시장가
            )
            
            if success:
                logger.info(f"🛑 손절 실행: {stock_code} {position['quantity']}주 @ 시장가")
                # 포지션에서 제거
                del self.positions[stock_code]
            else:
                logger.error(f"❌ 손절 실행 실패: {stock_code} - {message}")
                
        except Exception as e:
            logger.error(f"❌ 손절 실행 오류: {e}")
    
    def execute_take_profit(self, stock_code: str):
        """익절 실행"""
        try:
            if stock_code not in self.positions:
                return
            
            position = self.positions[stock_code]
            current_price = position['current_price']
            
            # 시장가 매도 주문
            success, message = self.order_handler.place_sell_order(
                stock_code=stock_code,
                quantity=position['quantity'],
                price=0,  # 시장가
                trade_type='3'  # 시장가
            )
            
            if success:
                logger.info(f"💰 익절 실행: {stock_code} {position['quantity']}주 @ 시장가")
                # 포지션에서 제거
                del self.positions[stock_code]
            else:
                logger.error(f"❌ 익절 실행 실패: {stock_code} - {message}")
                
        except Exception as e:
            logger.error(f"❌ 익절 실행 오류: {e}")
    
    def get_position_summary(self) -> Dict:
        """포지션 요약 정보"""
        try:
            self.get_positions()
            
            total_value = 0
            total_pnl = 0
            total_quantity = 0
            
            for position in self.positions.values():
                total_value += position['market_value']
                total_pnl += position['unrealized_pnl']
                total_quantity += position['quantity']
            
            return {
                'total_positions': len(self.positions),
                'total_value': total_value,
                'total_pnl': total_pnl,
                'total_quantity': total_quantity,
                'avg_pnl_rate': total_pnl / total_value if total_value > 0 else 0,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ 포지션 요약 조회 오류: {e}")
            return {}
    
    def set_risk_limits(self, limits: Dict):
        """리스크 한도 설정"""
        self.risk_limits.update(limits)
        logger.info(f"✅ 리스크 한도 업데이트: {limits}")
    
    def get_position_history(self, stock_code: str = None) -> List[Dict]:
        """포지션 히스토리 조회"""
        if stock_code:
            return [h for h in self.position_history if h['stock_code'] == stock_code]
        return self.position_history.copy()

if __name__ == "__main__":
    # 포지션 관리 테스트
    manager = PositionManager()
    
    # 계좌 잔고 조회
    balance = manager.get_account_balance()
    print(f"계좌 잔고: {balance}")
    
    # 포지션 조회
    positions = manager.get_positions()
    print(f"포지션: {positions}")
    
    # 리스크 체크
    violations = manager.check_risk_limits()
    print(f"리스크 위반: {violations}")
    
    # 포지션 요약
    summary = manager.get_position_summary()
    print(f"포지션 요약: {summary}") 