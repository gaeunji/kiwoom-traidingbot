from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """모든 거래 전략의 공통 인터페이스"""

    @abstractmethod
    def connect(self) -> bool:
        """API 또는 데이터 연결"""
        pass

    @abstractmethod
    def run(self):
        """전략 실행 메인 엔트리포인트"""
        pass

    @abstractmethod
    def disconnect(self):
        """연결 해제 및 리소스 정리"""
        pass 