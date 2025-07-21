# Examples Directory

키움증권 API 사용 예제 파일들이 포함된 디렉토리입니다.

## 파일 목록

### 환경 설정

- `env.example.env` - 환경 변수 설정 예제 파일

## 사용법

### 환경 변수 설정

1. `env.example.env` 파일을 `.env`로 복사:

```bash
cp examples/env.example.env .env
```

2. `.env` 파일을 편집하여 실제 값으로 수정:

```env
# 키움증권 API 설정
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_APP_SECRET=your_app_secret_here
KIWOOM_BASE_URL=https://api.kiwoom.com

# 계좌 정보
ACCOUNT_NUMBER=your_account_number_here

# 토큰 정보 (자동 생성됨)
ACCESS_TOKEN=your_access_token_here
REFRESH_TOKEN=your_refresh_token_here
TOKEN_EXPIRES_AT=your_token_expires_at_here
```

## 주의사항

- 실제 API 키와 시크릿은 안전하게 보관하세요
- `.env` 파일은 절대 Git에 커밋하지 마세요
- 예제 파일은 참고용으로만 사용하세요
