# Service Directory

키움증권 API 기반 자동화 서비스들이 포함된 디렉토리입니다.

## 📋 서비스 목록

### 1. **trading_service.py** - 전략 실행 스케줄 관리

- 전략 등록 및 스케줄링
- 장 운영 시간 확인
- 전략 즉시 실행 기능
- 장 시작 대기 기능

### 2. **scheduler.py** - 장 시작/종료 자동 트리거

- 장 시작/종료 이벤트 핸들러
- 점심시간 관리
- 장 시작 전/후 작업
- 다음 장 시작 시간 계산

### 3. **condition_monitor.py** - 조건 검색 매수 감시

- 사용자 정의 조건 등록
- 실시간 조건 감시
- 자동 매수 실행
- 조건 검사 결과 관리

### 4. **position_manager.py** - 잔고/포지션 관리

- 계좌 잔고 조회
- 포지션 추가/감소
- 리스크 한도 관리
- 손절/익절 자동 실행

## 🚀 사용법

### 전략 실행 서비스

```python
from service.trading_service import TradingService

# 서비스 초기화
service = TradingService()

# 전략 추가
def my_strategy():
    print("내 전략 실행")

service.add_strategy("my_strategy", my_strategy, "09:30")

# 스케줄러 시작
service.start()
```

### 장 스케줄러

```python
from service.scheduler import MarketScheduler

# 스케줄러 초기화
scheduler = MarketScheduler()

# 이벤트 핸들러 등록
def market_open_handler():
    print("장 시작!")

scheduler.add_event_handler('market_open', market_open_handler)

# 스케줄러 시작
scheduler.start()
```

### 조건 감시

```python
from service.condition_monitor import ConditionMonitor

# 감시 서비스 초기화
monitor = ConditionMonitor()

# 조건 함수 정의
def volume_condition(stock_code):
    # 거래량 급증 조건 로직
    return True

# 조건 등록
monitor.add_condition("거래량급증", volume_condition,
                     check_interval=30, auto_buy=True)

# 감시 종목 추가
monitor.add_stock_to_monitor("005930", "삼성전자")

# 감시 시작
monitor.monitor_conditions()
```

### 포지션 관리

```python
from service.position_manager import PositionManager

# 포지션 관리자 초기화
manager = PositionManager()

# 계좌 잔고 조회
balance = manager.get_account_balance()

# 포지션 조회
positions = manager.get_positions()

# 리스크 관리 실행
manager.execute_risk_management()
```

## ⚙️ 설정

### 리스크 한도 설정

```python
# 포지션 관리자에서 리스크 한도 설정
risk_limits = {
    'max_position_value': 10000000,      # 최대 포지션 가치
    'max_single_stock_value': 2000000,   # 단일 종목 최대 가치
    'max_daily_loss': 500000,            # 일일 최대 손실
    'stop_loss_rate': 0.05,              # 손절 비율 (5%)
    'take_profit_rate': 0.10             # 익절 비율 (10%)
}

manager.set_risk_limits(risk_limits)
```

## 📊 모니터링

### 포지션 요약 조회

```python
summary = manager.get_position_summary()
print(f"총 포지션: {summary['total_positions']}개")
print(f"총 가치: {summary['total_value']:,}원")
print(f"총 손익: {summary['total_pnl']:,}원")
```

### 조건 검사 결과

```python
results = monitor.get_condition_results("거래량급증")
for result in results:
    print(f"조건 만족: {result['stock_code']} at {result['timestamp']}")
```

## 🔧 의존성

- `schedule`: 스케줄링 기능
- `loguru`: 로깅
- `kiwoom`: 키움증권 API 모듈
- `config.settings`: 설정 관리
