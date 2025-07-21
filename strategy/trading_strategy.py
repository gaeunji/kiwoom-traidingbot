# -*- coding: utf-8 -*-
from typing import Dict, List, Optional
from loguru import logger
from config.settings import settings
from kiwoom import KiwoomConnector, OrderHandler

class TradingStrategy:
    """거래 전략 관리 클래스"""
    
    def __init__(self):
        self.api = KiwoomConnector()
        self.order_handler = OrderHandler()
        self.positions: Dict[str, Dict] = {}  # 보유 포지션
        self.watchlist: List[str] = []  # 관심종목 리스트
        
    def connect(self) -> bool:
        """API 연결"""
        return self.api.connect()
    
    def disconnect(self):
        """API 연결 해제"""
        self.api.disconnect()
        
    def add_to_watchlist(self, stock_code: str):
        """관심종목에 추가"""
        if stock_code not in self.watchlist:
            self.watchlist.append(stock_code)
            logger.info(f"관심종목 추가: {stock_code}")
    
    def remove_from_watchlist(self, stock_code: str):
        """관심종목에서 제거"""
        if stock_code in self.watchlist:
            self.watchlist.remove(stock_code)
            logger.info(f"관심종목 제거: {stock_code}")
    
    def get_current_price(self, stock_code: str) -> Optional[float]:
        """현재가 조회"""
        try:
            # MarketDataAPI를 사용하여 현재가 조회
            from kiwoom import MarketDataAPI
            market_api = MarketDataAPI()
            price_data = market_api.get_market_price(stock_code)
            
            if price_data and isinstance(price_data, dict):
                # 키움 API 응답 구조에 따라 현재가 필드 확인
                current_price = price_data.get('stck_prpr', 0)
                if current_price:
                    try:
                        return float(current_price)
                    except (ValueError, TypeError):
                        logger.warning(f"현재가 변환 실패: {current_price}")
                        return None
                else:
                    logger.warning(f"현재가 데이터 없음: {stock_code}")
                    return None
            else:
                logger.warning(f"가격 데이터 조회 실패: {stock_code}")
                return None
                
        except Exception as e:
            logger.error(f"현재가 조회 중 오류: {stock_code}, {e}")
            return None
    
    def calculate_position_size(self, stock_code: str, price: float) -> int:
        """포지션 크기 계산"""
        available_cash = self.get_available_cash()
        max_position_value = min(settings.MAX_POSITION_SIZE, available_cash)
        quantity = int(max_position_value / price)
        return max(1, quantity)  # 최소 1주
    
    def get_available_cash(self) -> float:
        """사용 가능한 현금 조회"""
        # 계좌평가잔고내역요청 API 사용
        account_balance = self.api.get_account_balance()
        
        if account_balance:
            # 키움 API 응답 구조에 따라 현금 잔고 추출
            # prsm_dpst_aset_amt: 예수금자산금액 (현금 잔고)
            cash_balance = account_balance.get('prsm_dpst_aset_amt', '0')
            logger.info(f"현금 잔고 (prsm_dpst_aset_amt): {cash_balance}")
            
            # 문자열을 정수로 변환 (키움 API는 0으로 패딩된 문자열 반환)
            try:
                return float(int(cash_balance))
            except (ValueError, TypeError):
                logger.warning(f"현금 잔고 변환 실패: {cash_balance}")
                return 0.0
        
        # API 호출 실패 시 기본값 반환
        logger.warning("계좌 잔고 조회 실패, 기본값 사용")
        return 10000000.0  # 1천만원
    
    def get_account_summary(self) -> Optional[Dict]:
        """계좌 요약 정보 조회"""
        # 계좌평가잔고내역요청 API 사용
        account_balance = self.api.get_account_balance()
        
        if account_balance:
            # 키움 API 응답 구조에 따라 데이터 추출
            summary = {
                'cash_bal': float(int(account_balance.get('prsm_dpst_aset_amt', '0'))),  # 예수금자산금액
                'total_value': float(int(account_balance.get('tot_evlt_amt', '0'))),     # 총평가금액
                'total_pnl': float(int(account_balance.get('tot_evlt_pl', '0'))),        # 총평가손익
                'total_profit_rate': float(account_balance.get('tot_prft_rt', '0')),     # 총수익률
                'positions': account_balance.get('acnt_evlt_remn_indv_tot', []),         # 보유 종목
                'total_purchase_amount': float(int(account_balance.get('tot_pur_amt', '0'))),  # 총매입금액
                'total_loan_amount': float(int(account_balance.get('tot_loan_amt', '0'))),     # 총대출금액
            }
            # 개선된 출력 로그
            logger.info("\n[계좌 요약 정보]")
            logger.info(f"  예수금자산금액: {summary['cash_bal']:,.0f}원")
            logger.info(f"  총평가금액: {summary['total_value']:,.0f}원")
            logger.info(f"  총평가손익: {summary['total_pnl']:,.0f}원")
            logger.info(f"  총수익률: {summary['total_profit_rate']:.2f}%")
            logger.info(f"  총매입금액: {summary['total_purchase_amount']:,.0f}원")
            logger.info(f"  총대출금액: {summary['total_loan_amount']:,.0f}원")
            logger.info(f"  보유 종목 수: {len(summary['positions'])}개")
            if summary['positions']:
                logger.info("  [상위 5개 보유 종목]")
                for i, position in enumerate(summary['positions'][:5]):
                    stk_nm = position.get('stk_nm', '-')
                    stk_cd = position.get('stk_cd', '-')
                    rmnd_qty = int(position.get('rmnd_qty', 0))
                    cur_prc = int(position.get('cur_prc', 0))
                    evltv_prft = int(position.get('evltv_prft', 0))
                    prft_rt = position.get('prft_rt', '-')
                    logger.info(f"    {i+1}. {stk_nm} ({stk_cd}) | 보유수량: {rmnd_qty}주 | 현재가: {cur_prc:,}원 | 평가손익: {evltv_prft:,}원 ({prft_rt}%)")
                if len(summary['positions']) > 5:
                    logger.info(f"    ... 외 {len(summary['positions']) - 5}개 종목")
            return summary
        
        # API 호출 실패 시 기본값 반환
        logger.warning("계좌 잔고 조회 실패, 기본값 사용")
        return {
            'cash_bal': 10000000.0,
            'total_value': 10000000.0,
            'total_pnl': 0.0,
            'total_profit_rate': 0.0,
            'positions': [],
            'total_purchase_amount': 0.0,
            'total_loan_amount': 0.0,
        }
    
    def simple_moving_average_strategy(self, stock_code: str, short_period: int = 5, long_period: int = 20) -> Optional[str]:
        """단순 이동평균 전략"""
        # 실제 구현에서는 과거 데이터를 수집해야 함
        # 현재는 간단한 시뮬레이션 구현
        current_price = self.get_current_price(stock_code)
        if not current_price:
            return None
        
        # 매수 신호: 단기 이동평균이 장기 이동평균을 상향 돌파
        # 매도 신호: 단기 이동평균이 장기 이동평균을 하향 돌파
        # 실제로는 과거 데이터 기반으로 계산해야 함
        
        if stock_code in self.positions:
            # 보유 중인 경우 매도 조건 확인
            entry_price = self.positions[stock_code]['entry_price']
            if current_price <= entry_price * (1 - settings.STOP_LOSS_RATIO):
                return 'sell'  # 손절
            elif current_price >= entry_price * (1 + settings.TAKE_PROFIT_RATIO):
                return 'sell'  # 익절
        else:
            # 미보유 중인 경우 매수 조건 확인
            # 실제로는 더 복잡한 조건이 필요
            return 'buy'
        
        return None
    
    def execute_strategy(self, stock_code: str):
        """전략 실행"""
        try:
            signal = self.simple_moving_average_strategy(stock_code)
            
            if signal == 'buy' and stock_code not in self.positions:
                current_price = self.get_current_price(stock_code)
                if current_price:
                    quantity = self.calculate_position_size(stock_code, current_price)
                    success, message = self.order_handler.place_order(stock_code, 'buy', quantity, int(current_price))
                    if success:
                        self.positions[stock_code] = {
                            'entry_price': current_price,
                            'quantity': quantity,
                            'entry_time': 'now'  # 실제로는 datetime 사용
                        }
                        logger.info(f"매수 주문 실행: {stock_code} {quantity}주 @ {current_price}")
                    else:
                        logger.error(f"매수 주문 실패: {message}")
            
            elif signal == 'sell' and stock_code in self.positions:
                position = self.positions[stock_code]
                success, message = self.order_handler.place_order(stock_code, 'sell', position['quantity'])
                if success:
                    logger.info(f"매도 주문 실행: {stock_code} {position['quantity']}주")
                    del self.positions[stock_code]
                else:
                    logger.error(f"매도 주문 실패: {message}")
                    
        except Exception as e:
            logger.error(f"전략 실행 중 오류: {e}")
    
    def run_strategy_on_watchlist(self):
        """관심종목 전체에 전략 실행"""
        for stock_code in self.watchlist:
            self.execute_strategy(stock_code)
    
    def get_portfolio_summary(self) -> Dict:
        """포트폴리오 요약"""
        total_value = 0.0
        total_pnl = 0.0
        
        for stock_code, position in self.positions.items():
            current_price = self.get_current_price(stock_code)
            if current_price:
                position_value = current_price * position['quantity']
                position_pnl = (current_price - position['entry_price']) * position['quantity']
                total_value += position_value
                total_pnl += position_pnl
        
        return {
            'total_value': total_value,
            'total_pnl': total_pnl,
            'positions': len(self.positions),
            'available_cash': self.get_available_cash()
        }
    
    def get_watchlist_prices(self) -> Dict[str, float]:
        """관심종목 현재가 조회"""
        prices = {}
        for stock_code in self.watchlist:
            try:
                price = self.get_current_price(stock_code)
                if price and price > 0:
                    prices[stock_code] = price
                else:
                    logger.warning(f"유효하지 않은 현재가: {stock_code} = {price}")
            except Exception as e:
                logger.error(f"현재가 조회 중 오류: {stock_code}, {e}")
                continue
        return prices
    
    def get_connection_status(self) -> Dict:
        """연결 상태 조회"""
        return self.api.get_connection_status() 
