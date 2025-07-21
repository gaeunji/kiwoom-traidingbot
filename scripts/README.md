# Scripts Directory

키움증권 API 관련 실행 스크립트들이 포함된 디렉토리입니다.

## 파일 목록

### 주문 관련

- `place_order.py` - 주식 매수/매도 주문 실행 스크립트
- `run_order.bat` - Windows 배치 파일 (주문 실행)

### 시장 데이터

- `volume_ranking.py` - 거래량 상위 종목 조회 스크립트

### 토큰 관리

- `issue_token.py` - 접근 토큰 발급 스크립트
- `create_env.py` - 환경 변수 파일 생성 스크립트

## 사용법

```bash
# 주문 실행
python scripts/place_order.py

# 거래량 상위 종목 조회
python scripts/volume_ranking.py

# 토큰 발급
python scripts/issue_token.py

# 환경 변수 파일 생성
python scripts/create_env.py
```

## Windows 배치 파일

```bash
# 주문 실행 (Windows)
scripts/run_order.bat
```
