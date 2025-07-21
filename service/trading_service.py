#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 전략 실행 스케줄 관리 서비스
"""

import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from loguru import logger
from kiwoom import OrderHandler, MarketDataAPI
from config.settings import settings

class TradingService:
    """전략 실행 스케줄 관리 서비스"""
    
    def __init__(self):
        self.order_handler = OrderHandler()
        self.market_data = MarketDataAPI()
        self.strategies = {}
        self.is_running = False
        self.scheduler = schedule.Scheduler()
        
    def add_strategy(self, name: str, strategy_func: Callable, 
                    schedule_time: str = "09:00", days: List[str] = None):
        """
        전략 추가
        
        Args:
            name (str): 전략 이름
            strategy_func (Callable): 전략 실행 함수
            schedule_time (str): 실행 시간 (HH:MM)
            days (List[str]): 실행 요일 (['monday', 'tuesday', ...])
        """
        try:
            if days:
                # 특정 요일에 실행
                for day in days:
                    getattr(self.scheduler, day).at(schedule_time).do(strategy_func)
            else:
                # 매일 실행
                self.scheduler.every().day.at(schedule_time).do(strategy_func)
            
            self.strategies[name] = {
                'function': strategy_func,
                'schedule_time': schedule_time,
                'days': days
            }
            logger.info(f"✅ 전략 '{name}' 추가됨 (실행시간: {schedule_time})")
            
        except Exception as e:
            logger.error(f"❌ 전략 추가 실패: {e}")
    
    def remove_strategy(self, name: str):
        """전략 제거"""
        if name in self.strategies:
            # 스케줄러에서 제거
            self.scheduler.clear(name)
            del self.strategies[name]
            logger.info(f"✅ 전략 '{name}' 제거됨")
        else:
            logger.warning(f"⚠️ 전략 '{name}'을 찾을 수 없습니다")
    
    def start(self):
        """스케줄러 시작"""
        if not self.strategies:
            logger.warning("⚠️ 등록된 전략이 없습니다")
            return
        
        self.is_running = True
        logger.info("🚀 전략 스케줄러 시작")
        
        try:
            while self.is_running:
                self.scheduler.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("⏹️ 스케줄러 중단됨")
            self.stop()
        except Exception as e:
            logger.error(f"❌ 스케줄러 오류: {e}")
            self.stop()
    
    def stop(self):
        """스케줄러 중지"""
        self.is_running = False
        logger.info("⏹️ 전략 스케줄러 중지")
    
    def get_strategies(self) -> Dict:
        """등록된 전략 목록 반환"""
        return self.strategies.copy()
    
    def run_strategy_once(self, name: str):
        """전략 즉시 실행"""
        if name in self.strategies:
            try:
                logger.info(f"▶️ 전략 '{name}' 즉시 실행")
                self.strategies[name]['function']()
            except Exception as e:
                logger.error(f"❌ 전략 '{name}' 실행 실패: {e}")
        else:
            logger.warning(f"⚠️ 전략 '{name}'을 찾을 수 없습니다")
    
    def is_market_open(self) -> bool:
        """장 운영 시간 확인"""
        now = datetime.now()
        
        # 주말 체크
        if now.weekday() >= 5:  # 토요일(5), 일요일(6)
            return False
        
        # 장 운영 시간 체크 (09:00-15:30)
        market_start = now.replace(hour=9, minute=0, second=0, microsecond=0)
        market_end = now.replace(hour=15, minute=30, second=0, microsecond=0)
        
        return market_start <= now <= market_end
    
    def wait_for_market_open(self):
        """장 시작까지 대기"""
        while not self.is_market_open():
            logger.info("⏰ 장 시작까지 대기 중...")
            time.sleep(60)  # 1분마다 체크
        
        logger.info("🔔 장이 시작되었습니다!")

# 기본 전략 예제
def sample_strategy():
    """샘플 전략"""
    logger.info("📊 샘플 전략 실행 중...")
    # 여기에 실제 전략 로직 구현
    pass

if __name__ == "__main__":
    # 서비스 테스트
    service = TradingService()
    
    # 샘플 전략 추가
    service.add_strategy("sample", sample_strategy, "09:30")
    
    # 스케줄러 시작
    service.start() 