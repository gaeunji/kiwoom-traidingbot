# 키움증권 REST API 주식 매매 시스템

키움증권의 REST API를 사용하여 자동 주식 매매 시스템을 구현한 프로젝트입니다.

## 주요 기능

- 키움증권 REST API 연결 및 인증
- 실시간 주식 가격 조회
- 자동 주식 매매 전략 실행
- 포트폴리오 관리
- 대화형 및 자동화 모드 지원

## 프로젝트 구조

```
kiwoom-trading/
├── main.py                 # 메인 실행 진입점
├── requirements.txt        # 필요한 패키지 목록
├── README.md              # 프로젝트 설명서
├── config/                # 설정 파일
│   └── settings.py        # 설정 관리
├── kiwoom/                # 핵심 API 모듈
│   ├── __init__.py        # 패키지 초기화
│   ├── connector.py       # API 연결 관리
│   ├── token_manager.py   # 토큰 관리
│   ├── order_handler.py   # 주문 처리
│   └── market_data.py     # 시장 데이터
├── scripts/               # 실행 스크립트
│   ├── place_order.py     # 주문 실행
│   ├── volume_ranking.py  # 거래량 상위 조회
│   ├── issue_token.py     # 토큰 발급
│   ├── create_env.py      # 환경 변수 생성
│   └── run_order.bat      # Windows 배치 파일
├── test/                  # 테스트 파일
│   ├── test_token.py      # 토큰 발급 테스트
│   ├── test_connection.py # API 연결 테스트
│   ├── test_strategy.py   # 거래 전략 테스트
│   ├── test_order.py      # 주문 처리 테스트
│   ├── test_order_new.py  # 새로운 주문 API 테스트
│   ├── run_all_tests.py   # 통합 테스트
│   └── TEST_GUIDE.md      # 상세 테스트 가이드
├── examples/              # 예제 파일
│   └── env.example.env    # 환경 변수 예제
├── docs/                  # 문서
├── data/                  # 데이터 저장소
├── service/               # 자동화 서비스
│   ├── trading_service.py # 전략 실행 스케줄 관리
│   ├── scheduler.py       # 장 시작/종료 자동 트리거
│   ├── condition_monitor.py # 조건 검색 매수 감시
│   ├── position_manager.py # 잔고/포지션 관리
│   └── README.md          # 서비스 사용법
└── strategy/              # 거래 전략
```

## 설치 및 설정

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`examples/env.example.env` 파일을 복사하여 `.env` 파일을 생성하고 필요한 정보를 입력하세요:

```bash
cp examples/env.example.env .env
```

`.env` 파일에서 다음 정보를 설정해야 합니다:

- `KIWOOM_APP_KEY`: 키움증권 API 앱 키
- `KIWOOM_APP_SECRET`: 키움증권 API 앱 시크릿
- `ACCOUNT_NUMBER`: 계좌번호

### 3. 키움증권 API 설정

1. [키움증권 Open API](https://www.kiwoom.com/h/customer/download/VOpenApiInfoView)에서 API 신청
2. 앱 키와 앱 시크릿 발급
3. 계좌번호 확인

## 사용법

### 메인 실행

```bash
python main.py
```

### 개별 스크립트 실행

#### 주문 실행

```bash
python scripts/place_order.py
```

#### 거래량 상위 종목 조회

```bash
python scripts/volume_ranking.py
```

#### 토큰 발급

```bash
python scripts/issue_token.py
```

#### 환경 변수 생성

```bash
python scripts/create_env.py
```

#### Windows 배치 파일

```bash
scripts/run_order.bat
```

### 테스트 실행

```bash
# 개별 테스트
python test/test_token.py
python test/test_connection.py
python test/test_strategy.py
python test/test_order.py
python test/test_order_new.py

# 모든 테스트 실행
python test/run_all_tests.py

# Windows 배치 파일
test/run_tests.bat

# Linux/Mac 스크립트
bash test/run_tests.sh
```

### 자동화 서비스 실행

```bash
# 전략 실행 서비스
python service/trading_service.py

# 장 스케줄러
python service/scheduler.py

# 조건 감시 서비스
python service/condition_monitor.py

# 포지션 관리 서비스
python service/position_manager.py
```

## 주요 클래스

### KiwoomConnector

- API 연결 및 인증 관리
- 토큰 발급 및 갱신
- 연결 상태 모니터링

### KiwoomAPI

- REST API 호출 관리
- 주식 가격 조회
- 주문 처리
- 계좌 정보 조회

### TradingStrategy

- 거래 전략 구현
- 포트폴리오 관리
- 관심 종목 관리
- 자동 매매 실행

## 거래 전략

현재 구현된 전략:

- 단순 이동평균 전략 (기본)
- 손절/익절 관리
- 포지션 크기 자동 계산

## 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제작되었습니다.

## 기여

버그 리포트나 기능 제안은 이슈를 통해 제출해주세요.

## 연락처

프로젝트 관련 문의사항이 있으시면 이슈를 통해 연락해주세요.
