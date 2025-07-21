# Test Directory

키움증권 API 테스트 파일들이 포함된 디렉토리입니다.

## 📋 테스트 파일 목록

### 1. **test_token.py** - 토큰 발급 테스트

- 접근 토큰 발급 테스트
- 토큰 유효성 확인 테스트
- Authorization 헤더 생성 테스트
- 토큰 갱신 및 초기화 테스트

### 2. **test_connection.py** - API 연결 테스트

- 기본 연결 및 인증 테스트
- 계좌 정보 조회 테스트
- 주식 현재가 조회 테스트
- 시장 데이터 API 테스트

### 3. **test_strategy.py** - 거래 전략 테스트

- 거래 전략 기능 테스트
- 종목 랭킹 테스트
- 캐시 관리 테스트

### 4. **test_order.py** - 주문 처리 테스트

- 주문 처리 기능 테스트
- 주문 유효성 검사 테스트

### 5. **test_order_new.py** - 새로운 주문 API 테스트

- 새로운 kt10000/kt10001 API 테스트
- 매수/매도 주문 파라미터 테스트
- 토큰 기반 인증 테스트

### 6. **run_all_tests.py** - 통합 테스트

- 모든 테스트를 순차적으로 실행

## 🚀 테스트 실행 방법

### 개별 테스트 실행

```bash
# 토큰 발급 테스트
python test/test_token.py

# API 연결 테스트
python test/test_connection.py

# 거래 전략 테스트
python test/test_strategy.py

# 주문 처리 테스트
python test/test_order.py

# 새로운 주문 API 테스트
python test/test_order_new.py

# 모든 테스트 실행
python test/run_all_tests.py
```

### Windows 배치 파일 실행

```bash
# Windows에서 모든 테스트 실행
test/run_tests.bat
```

### Linux/Mac 스크립트 실행

```bash
# Linux/Mac에서 모든 테스트 실행
bash test/run_tests.sh
```

## 📋 테스트 목적

- API 연결 상태 확인
- 주문 데이터 검증
- 토큰 유효성 확인
- 실제 주문 없이 시스템 검증
- 거래 전략 검증
- 새로운 API 기능 테스트

## ⚠️ 주의사항

- 이 디렉토리의 테스트는 실제 주문을 실행하지 않습니다
- 개발 및 디버깅 목적으로만 사용하세요
- 테스트 실행 전 환경 변수 설정을 확인하세요
- 상세한 테스트 가이드는 `TEST_GUIDE.md`를 참조하세요
