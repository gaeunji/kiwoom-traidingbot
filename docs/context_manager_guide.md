# TradingStrategy Context Manager 가이드

## 개요

`TradingStrategy` 객체의 연결 → 실행 → 종료 패턴을 간소화하기 위한 Context Manager를 제공합니다.

## 주요 기능

### 1. `with_strategy()` Context Manager

자동으로 `TradingStrategy` 객체를 생성하고, 연결/해제를 관리합니다.

```python
from utils import with_strategy

# 기본 사용법
with with_strategy() as strategy:
    strategy.add_to_watchlist('005930')
    strategy.run_strategy_on_watchlist()
```

### 2. `run_with_strategy()` 헬퍼 함수

함수를 `TradingStrategy`와 함께 실행하는 헬퍼 함수입니다.

```python
from utils import run_with_strategy

def my_strategy(strategy):
    strategy.add_to_watchlist('005930')
    strategy.run_strategy_on_watchlist()

# 헬퍼 함수 사용
run_with_strategy(my_strategy)
```

## 사용 예제

### 예제 1: 기본 Context Manager 사용

```python
from utils import with_strategy

try:
    with with_strategy() as strategy:
        # 관심종목 추가
        strategy.add_to_watchlist('005930')  # 삼성전자
        strategy.add_to_watchlist('000660')  # SK하이닉스

        # 현재가 조회
        prices = strategy.get_watchlist_prices()
        for code, price in prices.items():
            print(f"{code}: {price:,}원")

        # 포트폴리오 요약
        summary = strategy.get_portfolio_summary()
        print(f"포트폴리오: {summary}")

except Exception as e:
    print(f"오류 발생: {e}")
```

### 예제 2: 헬퍼 함수 사용

```python
from utils import run_with_strategy

def my_strategy(strategy):
    """사용자 정의 전략"""
    # 관심종목 설정
    watchlist = ['005930', '000660', '035420']
    for stock in watchlist:
        strategy.add_to_watchlist(stock)

    # 전략 실행
    strategy.run_strategy_on_watchlist()

    # 결과 출력
    summary = strategy.get_portfolio_summary()
    print(f"전략 실행 결과: {summary}")

def error_handler(error):
    """오류 처리 함수"""
    print(f"전략 실행 중 오류 발생: {error}")

# 헬퍼 함수로 전략 실행
run_with_strategy(my_strategy, error_handler)
```

### 예제 3: 여러 전략 순차 실행

```python
from utils import run_with_strategy

def strategy_1(strategy):
    """전략 1: 삼성전자만 관심종목에 추가"""
    strategy.add_to_watchlist('005930')
    prices = strategy.get_watchlist_prices()
    print(f"전략 1 결과: {prices}")

def strategy_2(strategy):
    """전략 2: SK하이닉스만 관심종목에 추가"""
    strategy.add_to_watchlist('000660')
    prices = strategy.get_watchlist_prices()
    print(f"전략 2 결과: {prices}")

# 여러 전략 순차 실행
strategies = [strategy_1, strategy_2]

for i, strategy_func in enumerate(strategies, 1):
    print(f"전략 {i} 실행 중...")
    try:
        run_with_strategy(strategy_func)
    except Exception as e:
        print(f"전략 {i} 실행 실패: {e}")
```

## 기존 코드와 비교

### Before (기존 방식)

```python
from strategy.trading_strategy import TradingStrategy

def run_old_way():
    strategy = TradingStrategy()
    if not strategy.connect():
        print("API 연결 실패")
        return

    try:
        strategy.add_to_watchlist('005930')
        strategy.run_strategy_on_watchlist()
    except Exception as e:
        print(f"오류: {e}")
    finally:
        strategy.disconnect()
```

### After (Context Manager 사용)

```python
from utils import with_strategy

def run_new_way():
    try:
        with with_strategy() as strategy:
            strategy.add_to_watchlist('005930')
            strategy.run_strategy_on_watchlist()
    except Exception as e:
        print(f"오류: {e}")
```

## 장점

### 1. 코드 간소화

- 연결/해제 로직 제거
- 중복 코드 제거
- 더 깔끔한 코드 구조

### 2. 자동 리소스 관리

- 자동 연결 해제
- 예외 발생 시에도 안전한 정리
- 메모리 누수 방지

### 3. 오류 처리 개선

- 일관된 오류 처리
- 자동 로깅
- 디버깅 용이성

### 4. 재사용성 향상

- 여러 곳에서 동일한 패턴 사용
- 테스트 코드 간소화
- 유지보수성 향상

## 주의사항

### 1. 연결 실패 시

Context Manager는 연결 실패 시 `ConnectionError`를 발생시킵니다.

```python
try:
    with with_strategy() as strategy:
        # 연결 성공 시에만 실행
        pass
except ConnectionError:
    print("API 연결에 실패했습니다.")
```

### 2. 예외 처리

Context Manager 내부에서 발생한 예외는 자동으로 전파됩니다.

```python
try:
    with with_strategy() as strategy:
        strategy.non_existent_method()  # AttributeError 발생
except AttributeError:
    print("메서드가 존재하지 않습니다.")
```

### 3. 독립 실행

각 Context Manager는 독립적으로 실행되므로, 여러 번 사용할 수 있습니다.

```python
# 첫 번째 실행
with with_strategy() as strategy1:
    strategy1.add_to_watchlist('005930')

# 두 번째 실행
with with_strategy() as strategy2:
    strategy2.add_to_watchlist('000660')
```

## 실행 예제

```bash
# 예제 실행
python examples/strategy_examples.py

# 개별 스크립트 실행
python scripts/interactive_runner.py
python scripts/automated_runner.py
```

## 관련 파일

- `utils/strategy_manager.py`: Context Manager 구현
- `utils/__init__.py`: 모듈 export
- `scripts/interactive_runner.py`: 리팩토링된 대화형 모드
- `scripts/automated_runner.py`: 리팩토링된 자동화 모드
- `examples/strategy_examples.py`: 사용 예제
