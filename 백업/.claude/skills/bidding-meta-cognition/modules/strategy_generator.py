#!/usr/bin/env python3
"""
다중 전략 생성 모듈

하나의 "최적해"가 아니라 여러 전략 제시:
- 보수적: 경쟁 밀도 최소화
- 공격적: 수익률 최대화
- 균형: 기대값 최적화
- 맞춤: 검증된 요인 반영
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from .data_utils import filter_valid_range


class StrategyGenerator:
    """다중 전략 생성기"""

    def __init__(self, df: pd.DataFrame, base_amount: float, agency_rate: float):
        """
        Args:
            df: 전체 데이터
            base_amount: 기초금액
            agency_rate: 발주처투찰률
        """
        self.df = filter_valid_range(df)  # ✅ 필터링 추가
        self.base_amount = base_amount
        self.agency_rate = agency_rate
        self.strategies = []

    def generate_all(self,
                     basic_result: Optional[Dict] = None,
                     validated_factors: Optional[List[Dict]] = None,
                     context: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        모든 전략 생성

        Args:
            basic_result: 기본 분석 결과
            validated_factors: 검증된 영향 요인
            context: 현재 상황 (발주처, 월, 금액 등)

        Returns:
            전략 리스트
        """
        print("\n[다중 전략 생성 시작]")

        self.strategies = []

        # 경쟁 밀도 계산
        density_map = self._calculate_density_map()

        # 1. 보수적 전략 (경쟁 밀도 최소)
        self._generate_conservative(density_map)

        # 2. 공격적 전략 (수익률 최대)
        self._generate_aggressive(density_map)

        # 3. 균형 전략 (기대값 최적)
        if basic_result:
            self._generate_balanced(basic_result, density_map)

        # 4. 맞춤 전략 (요인 반영)
        if validated_factors and context:
            self._generate_contextual(validated_factors, context, density_map)

        print(f"  ✅ 총 {len(self.strategies)}개 전략 생성")

        return self.strategies

    def _calculate_density_map(self) -> Dict[float, int]:
        """경쟁 밀도 맵 계산 (0.05% 구간별)"""
        # 기초대비사정률 기준
        rates = self.df['기초대비사정률'].dropna()

        # 98~102% 범위로 제한
        rates = rates[(rates >= 98.0) & (rates <= 102.0)]

        # 0.05% 구간별로 카운트
        bins = np.arange(98.0, 102.05, 0.05)
        density_map = {}

        for i in range(len(bins) - 1):
            bin_start = bins[i]
            bin_end = bins[i + 1]
            count = len(rates[(rates >= bin_start) & (rates < bin_end)])
            # 구간 중앙값을 키로 사용
            key = round((bin_start + bin_end) / 2, 3)
            density_map[key] = count

        return density_map

    def _generate_conservative(self, density_map: Dict[float, int]):
        """보수적 전략: 경쟁 밀도 최소화"""
        # 밀도가 가장 낮은 구간 찾기
        min_density_rate = min(density_map.items(), key=lambda x: x[1])
        rate = min_density_rate[0]
        competitors = min_density_rate[1]

        # 입찰금액 계산
        bid_amount = int(self.base_amount * rate / 100)

        # 1위 확률 추정 (단순 역수)
        win_prob = 1 / (competitors + 1) if competitors > 0 else 0.5

        # 이익률
        profit_rate = (100 - rate) / 100

        strategy = {
            '전략명': '보수적',
            '설명': '경쟁 밀도 최소 구간 선택',
            '입찰률': round(rate, 3),
            '입찰금액': bid_amount,
            '예상_경쟁자': competitors,
            '예상_1위확률': f"{win_prob * 100:.2f}%",
            '이익률': f"{profit_rate * 100:.1f}%",
            '리스크': '낮음',
            '근거': f"경쟁자 {competitors}명으로 최소 (전체 평균 대비 {self._compare_to_avg(competitors):.1f}%)"
        }

        self.strategies.append(strategy)
        print(f"  ✅ 보수적 전략: {rate:.3f}% (경쟁자 {competitors}명)")

    def _generate_aggressive(self, density_map: Dict[float, int]):
        """공격적 전략: 수익률 최대화"""
        # 과거 1위 데이터의 하위 10% 지점 (낮은 입찰률)
        winners = self.df[self.df['순위'] == 1]['기초대비사정률'].dropna()

        if len(winners) < 10:
            print("  ⚠️ 공격적 전략: 1위 데이터 부족")
            return

        # 하위 10% 지점
        rate = np.percentile(winners, 10)

        # 해당 구간의 경쟁 밀도
        bin_key = round(rate / 0.05) * 0.05
        competitors = density_map.get(bin_key, 0)

        # 입찰금액
        bid_amount = int(self.base_amount * rate / 100)

        # 1위 확률 (낮음)
        win_prob = 1 / (competitors + 1) if competitors > 0 else 0.1

        # 이익률 (높음)
        profit_rate = (100 - rate) / 100

        strategy = {
            '전략명': '공격적',
            '설명': '수익률 최대화, 경쟁 감수',
            '입찰률': round(rate, 3),
            '입찰금액': bid_amount,
            '예상_경쟁자': competitors,
            '예상_1위확률': f"{win_prob * 100:.2f}%",
            '이익률': f"{profit_rate * 100:.1f}%",
            '리스크': '높음',
            '근거': f"과거 1위의 하위 10% 지점, 높은 수익률 추구"
        }

        self.strategies.append(strategy)
        print(f"  ✅ 공격적 전략: {rate:.3f}% (이익률 {profit_rate*100:.1f}%)")

    def _generate_balanced(self, basic_result: Dict, density_map: Dict[float, int]):
        """균형 전략: 기대값 최적화 (기본 분석 결과 활용)"""
        # 기본 분석의 최적 입찰률 사용
        if '최종_전략' not in basic_result:
            return

        strategies = basic_result['최종_전략']
        optimal_strategy = None

        # "기대 효용 최적" 전략 찾기
        for s in strategies:
            if '기대' in s.get('전략명', '') or '최적' in s.get('전략명', ''):
                optimal_strategy = s
                break

        if not optimal_strategy:
            optimal_strategy = strategies[0]  # 첫 번째 전략 사용

        rate = optimal_strategy.get('입찰률', 100.0)
        bid_amount = int(self.base_amount * rate / 100)

        # 경쟁 밀도
        bin_key = round(rate / 0.05) * 0.05
        competitors = density_map.get(bin_key, 0)

        # 1위 확률
        win_prob = 1 / (competitors + 1) if competitors > 0 else 0.3

        # 이익률
        profit_rate = (100 - rate) / 100

        strategy = {
            '전략명': '균형',
            '설명': '기대값 최적화 (확률 × 수익)',
            '입찰률': round(rate, 3),
            '입찰금액': bid_amount,
            '예상_경쟁자': competitors,
            '예상_1위확률': f"{win_prob * 100:.2f}%",
            '이익률': f"{profit_rate * 100:.1f}%",
            '리스크': '중간',
            '근거': '조건부 확률 최적화 결과 (기본 분석)'
        }

        self.strategies.append(strategy)
        print(f"  ✅ 균형 전략: {rate:.3f}% (기대값 최적)")

    def _generate_contextual(self,
                            validated_factors: List[Dict],
                            context: Dict,
                            density_map: Dict[float, int]):
        """맞춤 전략: 검증된 요인 반영"""
        # 기준 입찰률 (전체 평균)
        base_rate = self.df[self.df['순위'] == 1]['기초대비사정률'].mean()

        adjustments = []
        adjusted_rate = base_rate

        # 유의미한 요인만 반영
        for factor_result in validated_factors:
            if not factor_result.get('유의미', False):
                continue

            factor = factor_result['요인']

            # 발주처 요인
            if factor == '발주처' and '발주처' in context:
                current_agency = context['발주처']
                agency_stats = factor_result.get('발주처별_통계', [])
                for stat in agency_stats:
                    if stat['발주처'] == current_agency:
                        agency_avg = stat['평균']
                        adjustment = agency_avg - base_rate
                        adjusted_rate += adjustment
                        adjustments.append(f"발주처({current_agency}): {adjustment:+.3f}%p")
                        break

            # 월 요인
            elif factor == '월' and '월' in context:
                current_month = context['월']
                month_stats = factor_result.get('월별_통계', [])
                for stat in month_stats:
                    if stat['월'] == current_month:
                        month_avg = stat['평균']
                        adjustment = month_avg - base_rate
                        adjusted_rate += adjustment
                        adjustments.append(f"월({current_month}월): {adjustment:+.3f}%p")
                        break

            # 금액 요인
            elif factor == '금액' and '기초금액' in context:
                corr = factor_result.get('상관계수', 0)
                if abs(corr) > 0.3:  # 중간 이상 상관
                    # 금액이 평균보다 크면/작으면 조정
                    avg_amount = self.df['기초금액'].mean()
                    current_amount = context['기초금액']
                    amount_ratio = (current_amount - avg_amount) / avg_amount

                    # 상관계수 방향으로 조정
                    adjustment = amount_ratio * corr * 0.5  # 완화 계수
                    adjusted_rate += adjustment
                    adjustments.append(f"금액(상관 {corr:.2f}): {adjustment:+.3f}%p")

        # 조정 후 입찰률
        adjusted_rate = max(98.0, min(102.0, adjusted_rate))  # 범위 제한

        bid_amount = int(self.base_amount * adjusted_rate / 100)

        # 경쟁 밀도
        bin_key = round(adjusted_rate / 0.05) * 0.05
        competitors = density_map.get(bin_key, 0)

        # 1위 확률
        win_prob = 1 / (competitors + 1) if competitors > 0 else 0.3

        # 이익률
        profit_rate = (100 - adjusted_rate) / 100

        adjustment_text = " + ".join(adjustments) if adjustments else "조정 없음"

        strategy = {
            '전략명': '상황맞춤',
            '설명': '검증된 요인 반영한 조정',
            '입찰률': round(adjusted_rate, 3),
            '입찰금액': bid_amount,
            '예상_경쟁자': competitors,
            '예상_1위확률': f"{win_prob * 100:.2f}%",
            '이익률': f"{profit_rate * 100:.1f}%",
            '리스크': '중간',
            '근거': f"기준({base_rate:.3f}%) {adjustment_text}",
            '적용된_조정': adjustments
        }

        self.strategies.append(strategy)
        print(f"  ✅ 맞춤 전략: {adjusted_rate:.3f}% (요인 {len(adjustments)}개 반영)")

    def _compare_to_avg(self, competitors: int) -> float:
        """평균 대비 경쟁자 비율"""
        avg_competitors = len(self.df) / 80  # 대략적 평균
        return (competitors / avg_competitors - 1) * 100 if avg_competitors > 0 else 0


def generate_strategies(df: pd.DataFrame,
                       base_amount: float,
                       agency_rate: float,
                       basic_result: Optional[Dict] = None,
                       validated_factors: Optional[List[Dict]] = None,
                       context: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    다중 전략 생성

    Args:
        df: 전체 데이터
        base_amount: 기초금액
        agency_rate: 발주처투찰률
        basic_result: 기본 분석 결과
        validated_factors: 검증된 영향 요인
        context: 현재 상황

    Returns:
        전략 리스트
    """
    generator = StrategyGenerator(df, base_amount, agency_rate)
    return generator.generate_all(basic_result, validated_factors, context)
