#!/usr/bin/env python3
"""
요인별 통계 검증 모듈

실제 데이터로 발주처/월/금액/지역별 영향도를 통계적으로 검증
가정이나 임의값 없이 오직 p-value와 effect size만 사용
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any
from .data_utils import filter_valid_range


class FactorValidator:
    """요인별 통계 검증기"""

    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df: 전체 데이터 (전처리 완료된 데이터)
        """
        self.df = filter_valid_range(df)  # ✅ 필터링 추가
        self.results = []

    def validate_all(self) -> List[Dict[str, Any]]:
        """모든 요인 검증"""
        print("\n[요인별 통계 검증 시작]")

        # 1위 데이터만 추출
        winners = self.df[self.df['순위'] == 1].copy()

        if len(winners) < 10:
            print(f"  ⚠️ 1위 데이터 부족: {len(winners)}건 (최소 10건 필요)")
            return []

        print(f"  1위 데이터: {len(winners)}건")

        # 각 요인 검증
        self.results = []

        # 1. 발주처별 차이
        self._validate_agency(winners)

        # 2. 월별 차이
        self._validate_month(winners)

        # 3. 금액별 상관관계
        self._validate_amount(winners)

        # 4. 지역별 차이
        self._validate_region(winners)

        return self.results

    def _validate_agency(self, winners: pd.DataFrame):
        """발주처별 차이 검증 (ANOVA)"""
        if '발주처' not in winners.columns:
            return

        # 발주처별 그룹화
        groups = winners.groupby('발주처')['기초대비사정률']

        # 발주처가 2개 이상이어야 검증 가능
        if len(groups) < 2:
            return

        # 각 발주처별 샘플 수 확인
        group_sizes = groups.count()
        valid_agencies = group_sizes[group_sizes >= 5].index.tolist()

        if len(valid_agencies) < 2:
            print("  ⚠️ 발주처별 분석: 샘플 부족 (각 발주처당 최소 5건 필요)")
            return

        # 유효한 발주처만 필터링
        filtered_winners = winners[winners['발주처'].isin(valid_agencies)]
        groups = [group for name, group in filtered_winners.groupby('발주처')['기초대비사정률']]

        # ANOVA 검정
        try:
            f_stat, p_value = stats.f_oneway(*groups)

            # 효과 크기 계산 (최대 - 최소)
            group_means = filtered_winners.groupby('발주처')['기초대비사정률'].mean()
            effect_size = group_means.max() - group_means.min()

            # 발주처별 평균
            agency_stats = []
            for agency in valid_agencies:
                agency_data = filtered_winners[filtered_winners['발주처'] == agency]['기초대비사정률']
                agency_stats.append({
                    '발주처': agency,
                    '평균': round(agency_data.mean(), 3),
                    '표준편차': round(agency_data.std(), 3),
                    '샘플수': len(agency_data)
                })

            result = {
                '요인': '발주처',
                '통계_검정': 'ANOVA',
                'p_value': round(p_value, 4),
                '유의미': p_value < 0.05,
                '효과크기': f"{effect_size:.3f}%p",
                '발주처별_통계': agency_stats
            }

            # 인사이트 생성
            if p_value < 0.05:
                max_agency = group_means.idxmax()
                min_agency = group_means.idxmin()
                result['인사이트'] = (
                    f"{max_agency}가 평균 대비 가장 높고 ({group_means[max_agency]:.2f}%), "
                    f"{min_agency}가 가장 낮음 ({group_means[min_agency]:.2f}%)"
                )
            else:
                result['인사이트'] = "발주처별 차이 통계적으로 유의미하지 않음"

            self.results.append(result)
            print(f"  ✅ 발주처별 분석: p={p_value:.4f} {'(유의미)' if p_value < 0.05 else '(유의미하지 않음)'}")

        except Exception as e:
            print(f"  ❌ 발주처별 분석 오류: {e}")

    def _validate_month(self, winners: pd.DataFrame):
        """월별 차이 검증 (Kruskal-Wallis)"""
        if '월' not in winners.columns:
            return

        # 월별 그룹화
        groups = winners.groupby('월')['기초대비사정률']

        # 월이 3개 이상이어야 검증 가능
        if len(groups) < 3:
            return

        # 각 월별 샘플 수 확인
        group_sizes = groups.count()
        valid_months = group_sizes[group_sizes >= 3].index.tolist()

        if len(valid_months) < 3:
            print("  ⚠️ 월별 분석: 샘플 부족 (각 월당 최소 3건 필요)")
            return

        # 유효한 월만 필터링
        filtered_winners = winners[winners['월'].isin(valid_months)]
        groups = [group for name, group in filtered_winners.groupby('월')['기초대비사정률']]

        # Kruskal-Wallis 검정 (비모수)
        try:
            h_stat, p_value = stats.kruskal(*groups)

            # 효과 크기 계산
            group_means = filtered_winners.groupby('월')['기초대비사정률'].mean()
            effect_size = group_means.max() - group_means.min()

            # 월별 평균
            month_stats = []
            for month in sorted(valid_months):
                month_data = filtered_winners[filtered_winners['월'] == month]['기초대비사정률']
                month_stats.append({
                    '월': int(month),
                    '평균': round(month_data.mean(), 3),
                    '표준편차': round(month_data.std(), 3),
                    '샘플수': len(month_data)
                })

            result = {
                '요인': '월',
                '통계_검정': 'Kruskal-Wallis',
                'p_value': round(p_value, 4),
                '유의미': p_value < 0.05,
                '효과크기': f"{effect_size:.3f}%p",
                '월별_통계': month_stats
            }

            # 인사이트 생성
            if p_value < 0.05:
                max_month = group_means.idxmax()
                min_month = group_means.idxmin()
                result['인사이트'] = (
                    f"{int(max_month)}월이 평균 대비 가장 높고 ({group_means[max_month]:.2f}%), "
                    f"{int(min_month)}월이 가장 낮음 ({group_means[min_month]:.2f}%)"
                )
            else:
                result['인사이트'] = "월별 차이 통계적으로 유의미하지 않음"

            self.results.append(result)
            print(f"  ✅ 월별 분석: p={p_value:.4f} {'(유의미)' if p_value < 0.05 else '(유의미하지 않음)'}")

        except Exception as e:
            print(f"  ❌ 월별 분석 오류: {e}")

    def _validate_amount(self, winners: pd.DataFrame):
        """금액별 상관관계 검증 (Pearson Correlation)"""
        if '기초금액' not in winners.columns:
            return

        # 결측치 제거
        valid_data = winners[['기초금액', '기초대비사정률']].dropna()

        if len(valid_data) < 10:
            print("  ⚠️ 금액별 분석: 샘플 부족")
            return

        try:
            # Pearson 상관계수
            corr, p_value = stats.pearsonr(valid_data['기초금액'], valid_data['기초대비사정률'])

            # 상관 강도 해석
            if abs(corr) < 0.1:
                strength = "무시할 수 있음"
            elif abs(corr) < 0.3:
                strength = "약함"
            elif abs(corr) < 0.5:
                strength = "중간"
            elif abs(corr) < 0.7:
                strength = "강함"
            else:
                strength = "매우 강함"

            # 금액 구간별 평균 (참고용)
            valid_data_copy = valid_data.copy()
            valid_data_copy['금액구간'] = pd.qcut(valid_data_copy['기초금액'],
                                                  q=4,
                                                  labels=['최소', '하위', '상위', '최대'],
                                                  duplicates='drop')
            amount_stats = []
            for label in ['최소', '하위', '상위', '최대']:
                if label in valid_data_copy['금액구간'].values:
                    group_data = valid_data_copy[valid_data_copy['금액구간'] == label]
                    amount_stats.append({
                        '구간': label,
                        '평균금액': int(group_data['기초금액'].mean()),
                        '평균입찰률': round(group_data['기초대비사정률'].mean(), 3),
                        '샘플수': len(group_data)
                    })

            result = {
                '요인': '금액',
                '통계_검정': 'Pearson Correlation',
                'p_value': round(p_value, 4),
                '유의미': p_value < 0.05,
                '상관계수': round(corr, 3),
                '상관_강도': strength,
                '금액구간별_통계': amount_stats
            }

            # 인사이트 생성
            if p_value < 0.05:
                if corr > 0:
                    result['인사이트'] = f"금액이 클수록 입찰률 높아지는 경향 (r={corr:.3f})"
                else:
                    result['인사이트'] = f"금액이 클수록 입찰률 낮아지는 경향 (r={corr:.3f})"
            else:
                result['인사이트'] = "금액과 입찰률 사이 유의미한 상관관계 없음"

            self.results.append(result)
            print(f"  ✅ 금액별 분석: r={corr:.3f}, p={p_value:.4f} {'(유의미)' if p_value < 0.05 else '(유의미하지 않음)'}")

        except Exception as e:
            print(f"  ❌ 금액별 분석 오류: {e}")

    def _validate_region(self, winners: pd.DataFrame):
        """지역별 차이 검증"""
        if '지역' not in winners.columns:
            print("  ⚠️ 지역별 분석: 지역 컬럼 없음")
            return

        # 지역별 그룹화
        groups = winners.groupby('지역')['기초대비사정률']

        if len(groups) < 2:
            print("  ⚠️ 지역별 분석: 지역 종류 부족")
            return

        # 각 지역별 샘플 수 확인
        group_sizes = groups.count()
        valid_regions = group_sizes[group_sizes >= 5].index.tolist()

        if len(valid_regions) < 2:
            print("  ⚠️ 지역별 분석: 샘플 부족")
            return

        # 유효한 지역만 필터링
        filtered_winners = winners[winners['지역'].isin(valid_regions)]
        groups = [group for name, group in filtered_winners.groupby('지역')['기초대비사정률']]

        try:
            f_stat, p_value = stats.f_oneway(*groups)

            group_means = filtered_winners.groupby('지역')['기초대비사정률'].mean()
            effect_size = group_means.max() - group_means.min()

            result = {
                '요인': '지역',
                '통계_검정': 'ANOVA',
                'p_value': round(p_value, 4),
                '유의미': p_value < 0.05,
                '효과크기': f"{effect_size:.3f}%p"
            }

            if p_value < 0.05:
                max_region = group_means.idxmax()
                min_region = group_means.idxmin()
                result['인사이트'] = (
                    f"{max_region}이 평균 대비 가장 높고 ({group_means[max_region]:.2f}%), "
                    f"{min_region}이 가장 낮음 ({group_means[min_region]:.2f}%)"
                )
            else:
                result['인사이트'] = "지역별 차이 통계적으로 유의미하지 않음"

            self.results.append(result)
            print(f"  ✅ 지역별 분석: p={p_value:.4f} {'(유의미)' if p_value < 0.05 else '(유의미하지 않음)'}")

        except Exception as e:
            print(f"  ❌ 지역별 분석 오류: {e}")


def validate_factors(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    요인별 통계 검증 실행

    Args:
        df: 전체 데이터

    Returns:
        검증 결과 리스트
    """
    validator = FactorValidator(df)
    return validator.validate_all()
