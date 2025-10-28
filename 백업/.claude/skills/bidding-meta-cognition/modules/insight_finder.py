#!/usr/bin/env python3
"""
능동적 패턴 발견 모듈

사용자가 묻기 전에 먼저 발견:
- 이상 패턴: 최근 추세 변화
- 숨은 상관: 예상 못한 관계
- 위험 구간: 경쟁 밀도 급증
- 기회 영역: 저경쟁 구간
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta
from .data_utils import filter_valid_range


class InsightFinder:
    """능동적 패턴 발견기"""

    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df: 전체 데이터
        """
        self.df = filter_valid_range(df)  # ✅ 필터링 추가
        self.insights = []

    def find_all(self) -> List[Dict[str, Any]]:
        """모든 패턴 발견"""
        print("\n[능동적 패턴 발견 시작]")

        self.insights = []

        # 1. 이상 패턴 탐지
        self._find_anomalies()

        # 2. 경쟁 밀도 급증 구간
        self._find_risk_zones()

        # 3. 기회 영역 (저경쟁)
        self._find_opportunity_zones()

        # 4. 숨겨진 상관관계
        self._find_hidden_correlations()

        print(f"  ✅ 총 {len(self.insights)}개 인사이트 발견")

        return self.insights

    def _find_anomalies(self):
        """이상 패턴 탐지 (시간별 추세 변화)"""
        if '입찰일시' not in self.df.columns:
            return

        try:
            # 날짜 파싱
            self.df['입찰일시_parsed'] = pd.to_datetime(self.df['입찰일시'], errors='coerce')
            recent_df = self.df.dropna(subset=['입찰일시_parsed'])

            if len(recent_df) < 50:
                return

            # 최근 3개월
            three_months_ago = datetime.now() - timedelta(days=90)
            recent = recent_df[recent_df['입찰일시_parsed'] >= three_months_ago]
            old = recent_df[recent_df['입찰일시_parsed'] < three_months_ago]

            if len(recent) < 20 or len(old) < 20:
                return

            # 1위 입찰률 비교
            recent_winners = recent[recent['순위'] == 1]['기초대비사정률'].mean()
            old_winners = old[old['순위'] == 1]['기초대비사정률'].mean()

            diff = recent_winners - old_winners

            if abs(diff) > 0.2:  # 0.2%p 이상 변화
                insight = {
                    '카테고리': '이상_패턴',
                    '내용': f"최근 3개월 1위 입찰률 {diff:+.3f}%p {'상승' if diff > 0 else '하락'} (이전: {old_winners:.3f}%, 최근: {recent_winners:.3f}%)",
                    '중요도': '높음' if abs(diff) > 0.3 else '중간',
                    '해석': '시장 환경 변화 가능성, 최근 데이터 가중 필요' if abs(diff) > 0.3 else '소폭 추세 변화 관찰'
                }
                self.insights.append(insight)
                print(f"  🔍 이상 패턴 발견: 최근 입찰률 {diff:+.3f}%p 변화")

        except Exception as e:
            print(f"  ⚠️ 이상 패턴 탐지 오류: {e}")

    def _find_risk_zones(self):
        """위험 구간: 경쟁 밀도 급증 구간"""
        # 기초대비사정률 분포
        rates = self.df['기초대비사정률'].dropna()
        rates = rates[(rates >= 98.0) & (rates <= 102.0)]

        if len(rates) < 100:
            return

        # 0.05% 구간별 카운트
        bins = np.arange(98.0, 102.05, 0.05)
        counts, bin_edges = np.histogram(rates, bins=bins)

        # 평균 대비 2배 이상인 구간
        avg_count = np.mean(counts)
        high_density_zones = []

        for i, count in enumerate(counts):
            if count > avg_count * 2:
                bin_start = bin_edges[i]
                bin_end = bin_edges[i + 1]
                high_density_zones.append({
                    '구간': f"{bin_start:.2f}~{bin_end:.2f}%",
                    '경쟁자': int(count),
                    '평균대비': f"{count / avg_count:.1f}배"
                })

        if high_density_zones:
            # 가장 밀집된 구간 TOP 3
            top_zones = sorted(high_density_zones, key=lambda x: x['경쟁자'], reverse=True)[:3]

            zone_text = ", ".join([z['구간'] for z in top_zones])

            insight = {
                '카테고리': '위험_구간',
                '내용': f"경쟁 밀도 급증 구간: {zone_text}",
                '상세': top_zones,
                '중요도': '높음',
                '해석': '이 구간들은 절대 회피 권장 (경쟁자 평균 대비 2배 이상)'
            }
            self.insights.append(insight)
            print(f"  🔍 위험 구간 발견: {len(top_zones)}개 구간")

    def _find_opportunity_zones(self):
        """기회 영역: 저경쟁 구간"""
        # 기초대비사정률 분포
        rates = self.df['기초대비사정률'].dropna()
        rates = rates[(rates >= 98.0) & (rates <= 102.0)]

        if len(rates) < 100:
            return

        # 0.05% 구간별 카운트
        bins = np.arange(98.0, 102.05, 0.05)
        counts, bin_edges = np.histogram(rates, bins=bins)

        # 평균 대비 50% 이하인 구간 (저경쟁)
        avg_count = np.mean(counts)
        low_density_zones = []

        for i, count in enumerate(counts):
            if count < avg_count * 0.5 and count > 0:
                bin_start = bin_edges[i]
                bin_end = bin_edges[i + 1]

                # 1위 데이터가 이 구간에 있는지 확인
                winners_in_zone = self.df[
                    (self.df['순위'] == 1) &
                    (self.df['기초대비사정률'] >= bin_start) &
                    (self.df['기초대비사정률'] < bin_end)
                ]

                low_density_zones.append({
                    '구간': f"{bin_start:.2f}~{bin_end:.2f}%",
                    '경쟁자': int(count),
                    '평균대비': f"{count / avg_count:.1%}",
                    '과거_1위': len(winners_in_zone)
                })

        if low_density_zones:
            # 1위가 있었던 저경쟁 구간만 필터
            viable_zones = [z for z in low_density_zones if z['과거_1위'] > 0]

            if viable_zones:
                # 경쟁자가 가장 적은 TOP 3
                top_zones = sorted(viable_zones, key=lambda x: x['경쟁자'])[:3]

                zone_text = ", ".join([z['구간'] for z in top_zones])

                insight = {
                    '카테고리': '기회_영역',
                    '내용': f"저경쟁 구간 (과거 1위 존재): {zone_text}",
                    '상세': top_zones,
                    '중요도': '중간',
                    '해석': '경쟁 밀도 낮으면서도 낙찰 가능성 있는 구간'
                }
                self.insights.append(insight)
                print(f"  🔍 기회 영역 발견: {len(top_zones)}개 구간")

    def _find_hidden_correlations(self):
        """숨겨진 상관관계 발견"""
        # 1위 데이터만
        winners = self.df[self.df['순위'] == 1].copy()

        if len(winners) < 30:
            return

        correlations = []

        # 기초금액 vs 기초대비사정률
        if '기초금액' in winners.columns:
            valid = winners[['기초금액', '기초대비사정률']].dropna()
            if len(valid) >= 20:
                corr = valid['기초금액'].corr(valid['기초대비사정률'])
                if abs(corr) > 0.3:
                    correlations.append({
                        '변수1': '기초금액',
                        '변수2': '1위_입찰률',
                        '상관계수': round(corr, 3),
                        '방향': '양의 상관' if corr > 0 else '음의 상관',
                        '해석': f"금액이 {'클수록 입찰률도 높아짐' if corr > 0 else '클수록 입찰률은 낮아짐'}"
                    })

        # 발주처 vs 경쟁 밀도
        if '발주처' in self.df.columns:
            try:
                agency_density = self.df.groupby('발주처').size()
                if len(agency_density) >= 2:
                    max_agency = agency_density.idxmax()
                    min_agency = agency_density.idxmin()
                    ratio = agency_density[max_agency] / agency_density[min_agency]

                    if ratio > 2:
                        correlations.append({
                            '변수1': '발주처',
                            '변수2': '참여업체수',
                            '상관계수': None,
                            '방향': '편차 큼',
                            '해석': f"{max_agency}가 {min_agency} 대비 {ratio:.1f}배 많은 참여"
                        })
            except:
                pass

        if correlations:
            insight = {
                '카테고리': '숨은_상관',
                '내용': f"예상 못한 상관관계 {len(correlations)}개 발견",
                '상세': correlations,
                '중요도': '중간',
                '해석': '전략 수립 시 고려 필요'
            }
            self.insights.append(insight)
            print(f"  🔍 숨은 상관 발견: {len(correlations)}개")


def find_insights(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    능동적 패턴 발견 실행

    Args:
        df: 전체 데이터

    Returns:
        발견된 인사이트 리스트
    """
    finder = InsightFinder(df)
    return finder.find_all()
