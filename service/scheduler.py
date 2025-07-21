#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
키움증권 장 시작/종료 자동 트리거 스케줄러
"""

import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from loguru import logger
from kiwoom import OrderHandler, MarketDataAPI
from config.settings import settings

class MarketScheduler:
    """장 시작/종료 자동 트리거 스케줄러"""
    
    def __init__(self):
        self.order_handler = OrderHandler()
        self.market_data = MarketDataAPI()
        self.is_running = False
        self.scheduler = schedule.Scheduler()
        
        # 장 운영 시간 설정
        self.market_open_time = "09:00"
        self.market_close_time = "15:30"
        self.lunch_start_time = "11:30"
        self.lunch_end_time = "13:00"
        
        # 이벤트 핸들러
        self.event_handlers = {
            'market_open': [],
            'market_close': [],
            'lunch_start': [],
            'lunch_end': [],
            'pre_market': [],
            'post_market': []
        }
    
    def add_event_handler(self, event_type: str, handler: Callable):
        """
        이벤트 핸들러 추가
        
        Args:
            event_type (str): 이벤트 타입
            handler (Callable): 핸들러 함수
        """
        if event_type in self.event_handlers:
            self.event_handlers[event_type].append(handler)
            logger.info(f"✅ 이벤트 핸들러 추가: {event_type}")
        else:
            logger.error(f"❌ 알 수 없는 이벤트 타입: {event_type}")
    
    def remove_event_handler(self, event_type: str, handler: Callable):
        """이벤트 핸들러 제거"""
        if event_type in self.event_handlers and handler in self.event_handlers[event_type]:
            self.event_handlers[event_type].remove(handler)
            logger.info(f"✅ 이벤트 핸들러 제거: {event_type}")
    
    def setup_schedule(self):
        """스케줄 설정"""
        # 장 시작 (09:00)
        self.scheduler.every().monday.at(self.market_open_time).do(self._market_open)
        self.scheduler.every().tuesday.at(self.market_open_time).do(self._market_open)
        self.scheduler.every().wednesday.at(self.market_open_time).do(self._market_open)
        self.scheduler.every().thursday.at(self.market_open_time).do(self._market_open)
        self.scheduler.every().friday.at(self.market_open_time).do(self._market_open)
        
        # 장 종료 (15:30)
        self.scheduler.every().monday.at(self.market_close_time).do(self._market_close)
        self.scheduler.every().tuesday.at(self.market_close_time).do(self._market_close)
        self.scheduler.every().wednesday.at(self.market_close_time).do(self._market_close)
        self.scheduler.every().thursday.at(self.market_close_time).do(self._market_close)
        self.scheduler.every().friday.at(self.market_close_time).do(self._market_close)
        
        # 점심시간 시작 (11:30)
        self.scheduler.every().monday.at(self.lunch_start_time).do(self._lunch_start)
        self.scheduler.every().tuesday.at(self.lunch_start_time).do(self._lunch_start)
        self.scheduler.every().wednesday.at(self.lunch_start_time).do(self._lunch_start)
        self.scheduler.every().thursday.at(self.lunch_start_time).do(self._lunch_start)
        self.scheduler.every().friday.at(self.lunch_start_time).do(self._lunch_start)
        
        # 점심시간 종료 (13:00)
        self.scheduler.every().monday.at(self.lunch_end_time).do(self._lunch_end)
        self.scheduler.every().tuesday.at(self.lunch_end_time).do(self._lunch_end)
        self.scheduler.every().wednesday.at(self.lunch_end_time).do(self._lunch_end)
        self.scheduler.every().thursday.at(self.lunch_end_time).do(self._lunch_end)
        self.scheduler.every().friday.at(self.lunch_end_time).do(self._lunch_end)
        
        # 장 시작 전 (08:50)
        self.scheduler.every().monday.at("08:50").do(self._pre_market)
        self.scheduler.every().tuesday.at("08:50").do(self._pre_market)
        self.scheduler.every().wednesday.at("08:50").do(self._pre_market)
        self.scheduler.every().thursday.at("08:50").do(self._pre_market)
        self.scheduler.every().friday.at("08:50").do(self._pre_market)
        
        # 장 종료 후 (15:40)
        self.scheduler.every().monday.at("15:40").do(self._post_market)
        self.scheduler.every().tuesday.at("15:40").do(self._post_market)
        self.scheduler.every().wednesday.at("15:40").do(self._post_market)
        self.scheduler.every().thursday.at("15:40").do(self._post_market)
        self.scheduler.every().friday.at("15:40").do(self._post_market)
        
        logger.info("✅ 장 스케줄 설정 완료")
    
    def _market_open(self):
        """장 시작 이벤트"""
        logger.info("🔔 장이 시작되었습니다!")
        for handler in self.event_handlers['market_open']:
            try:
                handler()
            except Exception as e:
                logger.error(f"❌ 장 시작 핸들러 오류: {e}")
    
    def _market_close(self):
        """장 종료 이벤트"""
        logger.info("🔔 장이 종료되었습니다!")
        for handler in self.event_handlers['market_close']:
            try:
                handler()
            except Exception as e:
                logger.error(f"❌ 장 종료 핸들러 오류: {e}")
    
    def _lunch_start(self):
        """점심시간 시작 이벤트"""
        logger.info("🍽️ 점심시간이 시작되었습니다!")
        for handler in self.event_handlers['lunch_start']:
            try:
                handler()
            except Exception as e:
                logger.error(f"❌ 점심시간 시작 핸들러 오류: {e}")
    
    def _lunch_end(self):
        """점심시간 종료 이벤트"""
        logger.info("🍽️ 점심시간이 종료되었습니다!")
        for handler in self.event_handlers['lunch_end']:
            try:
                handler()
            except Exception as e:
                logger.error(f"❌ 점심시간 종료 핸들러 오류: {e}")
    
    def _pre_market(self):
        """장 시작 전 이벤트"""
        logger.info("⏰ 장 시작 10분 전입니다!")
        for handler in self.event_handlers['pre_market']:
            try:
                handler()
            except Exception as e:
                logger.error(f"❌ 장 시작 전 핸들러 오류: {e}")
    
    def _post_market(self):
        """장 종료 후 이벤트"""
        logger.info("📊 장이 종료되었습니다. 정리 작업을 시작합니다!")
        for handler in self.event_handlers['post_market']:
            try:
                handler()
            except Exception as e:
                logger.error(f"❌ 장 종료 후 핸들러 오류: {e}")
    
    def start(self):
        """스케줄러 시작"""
        self.setup_schedule()
        self.is_running = True
        logger.info("🚀 장 스케줄러 시작")
        
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
        logger.info("⏹️ 장 스케줄러 중지")
    
    def is_market_open(self) -> bool:
        """현재 장 운영 여부 확인"""
        now = datetime.now()
        
        # 주말 체크
        if now.weekday() >= 5:
            return False
        
        # 점심시간 체크
        lunch_start = now.replace(hour=11, minute=30, second=0, microsecond=0)
        lunch_end = now.replace(hour=13, minute=0, second=0, microsecond=0)
        
        if lunch_start <= now <= lunch_end:
            return False
        
        # 장 운영시간 체크
        market_start = now.replace(hour=9, minute=0, second=0, microsecond=0)
        market_end = now.replace(hour=15, minute=30, second=0, microsecond=0)
        
        return market_start <= now <= market_end
    
    def get_next_market_open(self) -> datetime:
        """다음 장 시작 시간 계산"""
        now = datetime.now()
        
        # 오늘이 주말이면 다음 월요일
        if now.weekday() >= 5:
            days_ahead = 7 - now.weekday()
            next_monday = now + timedelta(days=days_ahead)
            return next_monday.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # 오늘이 평일이면
        if now.hour < 9:
            # 오늘 장 시작
            return now.replace(hour=9, minute=0, second=0, microsecond=0)
        else:
            # 다음 평일 장 시작
            days_ahead = 1
            while (now + timedelta(days=days_ahead)).weekday() >= 5:
                days_ahead += 1
            next_day = now + timedelta(days=days_ahead)
            return next_day.replace(hour=9, minute=0, second=0, microsecond=0)

# 기본 이벤트 핸들러 예제
def market_open_handler():
    """장 시작 시 실행할 작업"""
    logger.info("📈 장 시작 - 거래 준비 완료")

def market_close_handler():
    """장 종료 시 실행할 작업"""
    logger.info("📉 장 종료 - 포지션 정리")

if __name__ == "__main__":
    # 스케줄러 테스트
    scheduler = MarketScheduler()
    
    # 이벤트 핸들러 등록
    scheduler.add_event_handler('market_open', market_open_handler)
    scheduler.add_event_handler('market_close', market_close_handler)
    
    # 스케줄러 시작
    scheduler.start() 