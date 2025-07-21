#!/bin/bash

# 키움증권 주식 매매 시스템 테스트 실행 스크립트

echo "========================================"
echo "키움증권 주식 매매 시스템 테스트 실행"
echo "========================================"
echo

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수 정의
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}📝 $1${NC}"
}

# 1. 환경 변수 확인
echo "1. 환경 변수 확인..."
if [ ! -f .env ]; then
    print_error ".env 파일이 없습니다."
    print_info "env.example을 복사하여 .env 파일을 생성하고 실제 API 정보를 입력해주세요."
    echo "cp env.example .env"
    exit 1
fi

print_success ".env 파일 확인 완료"
echo

# 2. 의존성 확인
echo "2. 의존성 확인..."
if ! python3 -c "import loguru, requests" 2>/dev/null; then
    print_warning "필요한 패키지가 설치되지 않았습니다."
    print_info "pip install -r requirements.txt 실행 중..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "패키지 설치 실패"
        exit 1
    fi
fi

print_success "의존성 확인 완료"
echo

# 3. 테스트 실행
echo "3. 테스트 실행..."
echo
echo "선택하세요:"
echo "1. 토큰 발급 테스트"
echo "2. API 연결 테스트"
echo "3. 거래 전략 테스트"
echo "4. 주문 처리 테스트"
echo "5. 새로운 주문 API 테스트"
echo "6. 모든 테스트 실행"
echo "7. 종료"
echo

read -p "선택 (1-7): " choice

case $choice in
    1)
        echo
        echo "🚀 토큰 발급 테스트 실행..."
        python3 test_token.py
        ;;
    2)
        echo
        echo "🚀 API 연결 테스트 실행..."
        python3 test_connection.py
        ;;
    3)
        echo
        echo "🚀 거래 전략 테스트 실행..."
        python3 test_strategy.py
        ;;
    4)
        echo
        echo "🚀 주문 처리 테스트 실행..."
        python3 test_order.py
        ;;
    5)
        echo
        echo "🚀 새로운 주문 API 테스트 실행..."
        python3 test_order_new.py
        ;;
    6)
        echo
        echo "🚀 모든 테스트 실행..."
        python3 run_all_tests.py
        ;;
    7)
        echo "종료합니다."
        exit 0
        ;;
    *)
        print_error "잘못된 선택입니다."
        exit 1
        ;;
esac

echo
echo "테스트 완료!" 