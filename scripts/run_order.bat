@echo off
echo 키움증권 API 주문 처리 시스템
echo ================================
echo.
echo 1. 환경 설정 확인
echo 2. 토큰 발급
echo 3. 주문 처리
echo 4. 거래량 상위 종목 조회
echo 5. 테스트 실행
echo 6. 종료
echo.
set /p choice="선택하세요 (1-6): "

if "%choice%"=="1" (
    echo.
    echo 환경 설정 확인 중...
    python create_env.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo 토큰 발급 중...
    python issue_token.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo 주문 처리 시스템 시작...
    python place_order.py
    pause
) else if "%choice%"=="4" (
    echo.
    echo 거래량 상위 종목 조회 중...
    python volume_ranking.py
    pause
) else if "%choice%"=="5" (
    echo.
    echo 테스트 실행 중...
    cd test
    python run_all_tests.py
    cd ..
    pause
) else if "%choice%"=="6" (
    echo 종료합니다.
    exit /b 0
) else (
    echo 잘못된 선택입니다.
    pause
) 