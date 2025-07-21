@echo off
chcp 65001 >nul
echo ========================================
echo 키움증권 주식 매매 시스템 테스트 실행
echo ========================================
echo.

echo 1. 환경 변수 확인...
if not exist .env (
    echo ❌ .env 파일이 없습니다.
    echo 📝 env.example을 복사하여 .env 파일을 생성하고 실제 API 정보를 입력해주세요.
    pause
    exit /b 1
)

echo ✅ .env 파일 확인 완료
echo.

echo 2. 의존성 확인...
python -c "import loguru, requests" 2>nul
if errorlevel 1 (
    echo ❌ 필요한 패키지가 설치되지 않았습니다.
    echo 📦 pip install -r requirements.txt 실행 중...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 패키지 설치 실패
        pause
        exit /b 1
    )
)

echo ✅ 의존성 확인 완료
echo.

echo 3. 테스트 실행...
echo.
echo 선택하세요:
echo 1. 토큰 발급 테스트
echo 2. API 연결 테스트
echo 3. 거래 전략 테스트
echo 4. 주문 처리 테스트
echo 5. 새로운 주문 API 테스트
echo 6. 모든 테스트 실행
echo 7. 종료
echo.

set /p choice="선택 (1-7): "

if "%choice%"=="1" (
    echo.
    echo 🚀 토큰 발급 테스트 실행...
    python test_token.py
) else if "%choice%"=="2" (
    echo.
    echo 🚀 API 연결 테스트 실행...
    python test_connection.py
) else if "%choice%"=="3" (
    echo.
    echo 🚀 거래 전략 테스트 실행...
    python test_strategy.py
) else if "%choice%"=="4" (
    echo.
    echo 🚀 주문 처리 테스트 실행...
    python test_order.py
) else if "%choice%"=="5" (
    echo.
    echo 🚀 새로운 주문 API 테스트 실행...
    python test_order_new.py
) else if "%choice%"=="6" (
    echo.
    echo 🚀 모든 테스트 실행...
    python run_all_tests.py
) else if "%choice%"=="7" (
    echo 종료합니다.
    exit /b 0
) else (
    echo 잘못된 선택입니다.
    pause
    exit /b 1
)

echo.
echo 테스트 완료!
pause 