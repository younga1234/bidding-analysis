#!/usr/bin/env python3
"""
입찰 분석 로직 - 통합 실행 스크립트

모든 분석을 하나로 통합:
1. 몬테카를로 시뮬레이션
2. 과거 1위 분포 분석
3. 경쟁 밀도 히트맵
4. 소수점 패턴 분석
5. 끝자리 선호도
6. 심리적 바닥선
7. 안전 구간 식별
8. 최종 추천 전략 3개
"""

import numpy as np
import pandas as pd
import json
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.font_manager as fm


def get_korean_font():
    """
    시스템에 설치된 한국어 폰트를 자동으로 감지하여 반환

    Returns:
        str: 사용 가능한 한국어 폰트 이름
    """
    # 우선순위대로 검색할 폰트 목록
    preferred_fonts = [
        'Noto Sans KR',
        'NotoSansKR',
        'Noto Sans CJK KR',
        'Noto Sans CJK JP',  # CJK 공통 폰트 (한글 포함)
        'NanumGothic',
        'NanumBarunGothic',
        'Malgun Gothic',
        'DejaVu Sans'  # fallback
    ]

    # 시스템에 설치된 모든 폰트 이름 수집
    available_fonts = {f.name for f in fm.fontManager.ttflist}

    # 우선순위대로 확인
    for font in preferred_fonts:
        if font in available_fonts:
            return font

    # 아무것도 없으면 DejaVu Sans (기본값)
    return 'DejaVu Sans'


class BiddingAnalyzer:
    def __init__(self, base_amount, agency_rate, data_file):
        self.base_amount = base_amount
        self.agency_rate = agency_rate
        self.data_file = Path(data_file)
        self.variance_range = 0.02  # ±2%
        self.n_simulations = 10000

        # 결과 저장
        self.results = {
            "공고정보": {
                "기초금액": base_amount,
                "발주처투찰률": agency_rate,
                "분석시각": datetime.now().isoformat()
            }
        }

    def _filter_valid_range(self, df):
        """
        기초대비사정률 유효 범위 필터링 (99~101%)

        Args:
            df: 원본 데이터프레임

        Returns:
            필터링된 데이터프레임
        """
        if '기초대비사정률' in df.columns:
            original_count = len(df)
            df = df[
                (df['기초대비사정률'] >= 99.0) &
                (df['기초대비사정률'] <= 101.0)
            ].copy()
            filtered_count = original_count - len(df)
            if filtered_count > 0:
                print(f"  ⚠️ 범위 외 데이터 제거: {filtered_count}건 (99~101% 범위 외)")
        return df

    def run_monte_carlo(self):
        """Phase 1: 몬테카를로 시뮬레이션"""
        print("\n[Phase 1] 몬테카를로 시뮬레이션 (10,000회)...")

        # 15개 예비가격
        min_price = self.base_amount * (1 - self.variance_range)
        max_price = self.base_amount * (1 + self.variance_range)
        prelim_prices = np.linspace(min_price, max_price, 15)

        # 10,000회 시뮬레이션
        np.random.seed(42)
        reserve_prices = []
        min_winning_prices = []
        base_to_min_rates = []

        for _ in range(self.n_simulations):
            selected = np.random.choice(prelim_prices, 4, replace=False)
            reserve_price = np.mean(selected)
            min_winning_price = reserve_price * (self.agency_rate / 100)
            base_to_min_rate = (min_winning_price / self.base_amount) * 100

            reserve_prices.append(reserve_price)
            min_winning_prices.append(min_winning_price)
            base_to_min_rates.append(base_to_min_rate)

        reserve_prices = np.array(reserve_prices)
        min_winning_prices = np.array(min_winning_prices)
        base_to_min_rates = np.array(base_to_min_rates)

        self.results["몬테카를로_시뮬레이션"] = {
            "예정가격_평균": float(reserve_prices.mean()),
            "예정가격_변동폭": float(reserve_prices.max() - reserve_prices.min()),
            "낙찰하한가_평균": float(min_winning_prices.mean()),
            "낙찰하한가_변동폭": float(min_winning_prices.max() - min_winning_prices.min()),
            "기초대비_낙찰하한율_평균": round(base_to_min_rates.mean(), 3),
            "기초대비_낙찰하한율_범위": [round(base_to_min_rates.min(), 3), round(base_to_min_rates.max(), 3)],
            "기초대비_낙찰하한율_변동폭": round(base_to_min_rates.max() - base_to_min_rates.min(), 3)
        }

        print(f"  예정가격 변동폭: {reserve_prices.max() - reserve_prices.min():,.0f}원")
        print(f"  낙찰하한가 변동폭: {min_winning_prices.max() - min_winning_prices.min():,.0f}원")
        print(f"  기초대비 낙찰하한율: {base_to_min_rates.min():.3f}% ~ {base_to_min_rates.max():.3f}%")

        return base_to_min_rates

    def analyze_past_winners(self):
        """Phase 2: 과거 1위 데이터 분석 - 기초대비사정률 기준"""
        print("\n[Phase 2] 과거 1위 데이터 분석 (기초대비사정률)...")

        if not self.data_file.exists():
            print(f"  ⚠️ 데이터 파일 없음: {self.data_file}")
            return None

        df = pd.read_excel(self.data_file)
        df = self._filter_valid_range(df)  # ✅ 필터링 추가
        df_first = df[df['순위'] == 1].copy()
        rates = df_first['기초대비사정률'].dropna().values

        self.results["과거_1위_분석"] = {
            "데이터_개수": len(df_first),
            "평균": round(rates.mean(), 3),
            "중앙값": round(np.median(rates), 3),
            "표준편차": round(rates.std(), 3),
            "최소": round(rates.min(), 3),
            "최대": round(rates.max(), 3),
            "백분위수": {
                "5%": round(np.percentile(rates, 5), 3),
                "25%": round(np.percentile(rates, 25), 3),
                "50%": round(np.percentile(rates, 50), 3),
                "75%": round(np.percentile(rates, 75), 3),
                "95%": round(np.percentile(rates, 95), 3)
            }
        }

        print(f"  데이터: {len(df_first)}개")
        print(f"  평균: {rates.mean():.3f}%")
        print(f"  중앙값: {np.median(rates):.3f}%")

        return rates

    def analyze_competition_density(self):
        """Phase 3: 경쟁 밀도 히트맵 (전체 업체 분석 - 모든 순위 포함) - 기초대비사정률 기준"""
        print("\n[Phase 3] 경쟁 밀도 분석 (전체 참여 업체)...")

        # 전체 입찰 데이터 로드 (모든 순위 포함)
        if not self.data_file.exists():
            print(f"  ⚠️ 데이터 파일 없음: {self.data_file}")
            return None, None, None

        df = pd.read_excel(self.data_file)
        df = self._filter_valid_range(df)  # ✅ 필터링 추가

        # 🔥 CRITICAL: 모든 순위 포함 (순위 -1도 경쟁자!)
        df_all = df.copy()

        # 이상치 제거 (IQR 방법) - 기초대비사정률 기준
        Q1 = df_all['기초대비사정률'].quantile(0.25)
        Q3 = df_all['기초대비사정률'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        before_count = len(df_all)
        df_all = df_all[(df_all['기초대비사정률'] >= lower_bound) &
                        (df_all['기초대비사정률'] <= upper_bound)].copy()
        outliers_removed = before_count - len(df_all)

        all_rates = df_all['기초대비사정률'].values

        print(f"  전체 참여 업체: {len(df)}개")
        print(f"  이상치 제거: {outliers_removed}개 (범위: {lower_bound:.2f}% ~ {upper_bound:.2f}%)")
        print(f"  분석 대상: {len(df_all)}개")
        print(f"    - 순위 -1 (탈락): {len(df_all[df_all['순위'] == -1])}개")
        print(f"    - 순위 1~N (유효): {len(df_all[df_all['순위'] >= 1])}개")

        # 0.05% 단위 구간별 분포
        bins = np.arange(all_rates.min() // 0.05 * 0.05, all_rates.max() + 0.05, 0.05)
        hist, edges = np.histogram(all_rates, bins=bins)

        # 상위 10개 (회피 구간)
        top_indices = np.argsort(hist)[-10:][::-1]
        avoid_zones = []
        for idx in top_indices:
            if hist[idx] > 3:  # 3개 이상은 회피
                start = edges[idx]
                end = edges[idx + 1]
                avoid_zones.append(f"{start:.2f}~{end:.2f}% ({hist[idx]}개)")

        # 안전 구간 (0~2개)
        safe_zones = []
        for idx in range(len(hist)):
            if hist[idx] <= 2 and edges[idx] >= 98.0:  # 기초대비사정률 최소값 이상만
                start = edges[idx]
                end = edges[idx + 1]
                safe_zones.append(f"{start:.2f}~{end:.2f}% ({hist[idx]}개)")

        self.results["경쟁_밀도"] = {
            "분석_대상": f"유효 입찰 {len(df_all)}개",
            "최고_밀집_구간": avoid_zones[0] if avoid_zones else "없음",
            "회피_구간_Top5": avoid_zones[:5],
            "안전_구간_Top10": safe_zones[:10]
        }

        print(f"  최고 밀집: {avoid_zones[0] if avoid_zones else '없음'}")
        print(f"  안전 구간: {len(safe_zones)}개")

        return all_rates, hist, edges

    def analyze_decimal_patterns(self, rates):
        """Phase 4: 소수점 패턴 분석"""
        print("\n[Phase 4] 소수점 패턴 분석...")

        # 첫째 자리
        first = ((rates * 10) % 10).astype(int)
        first_counts = Counter(first)

        # 둘째 자리
        second = ((rates * 100) % 10).astype(int)
        second_counts = Counter(second)

        # 셋째 자리
        third = ((rates * 1000) % 10).astype(int)
        third_counts = Counter(third)

        # 가장 많은 것 (회피)
        avoid_third = sorted(third_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        # 가장 적은 것 (안전)
        safe_third = sorted(third_counts.items(), key=lambda x: x[1])[:3]

        self.results["소수점_패턴"] = {
            "첫째자리_분포": {str(k): int(v) for k, v in sorted(first_counts.items())},
            "둘째자리_분포": {str(k): int(v) for k, v in sorted(second_counts.items())},
            "셋째자리_분포": {str(k): int(v) for k, v in sorted(third_counts.items())},
            "회피_셋째자리": [int(d[0]) for d in avoid_third],
            "안전_셋째자리": [int(d[0]) for d in safe_third]
        }

        print(f"  셋째자리 회피: {[d[0] for d in avoid_third]}")
        print(f"  셋째자리 안전: {[d[0] for d in safe_third]}")

        return third_counts

    def analyze_ending_digits(self, rates):
        """Phase 5: 끝자리 선호도"""
        print("\n[Phase 5] 끝자리 선호도 분석...")

        amounts = self.base_amount * rates / 100
        endings = (amounts % 1000).astype(int)
        ending_counts = Counter(endings)

        # 가장 많은 끝자리 (회피)
        avoid_endings = sorted(ending_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        # 가장 적은 끝자리 (안전)
        safe_endings = sorted(ending_counts.items(), key=lambda x: x[1])[:5]

        self.results["끝자리_선호도"] = {
            "회피_끝자리": [{"끝자리": int(e[0]), "개수": int(e[1])} for e in avoid_endings],
            "안전_끝자리": [{"끝자리": int(e[0]), "개수": int(e[1])} for e in safe_endings]
        }

        print(f"  회피 끝자리: {[e[0] for e in avoid_endings[:3]]}")
        print(f"  안전 끝자리: {[e[0] for e in safe_endings[:3]]}")

        return ending_counts

    def find_psychological_floor(self, rates, simulated_min):
        """Phase 6: 심리적 바닥선 탐지"""
        print("\n[Phase 6] 심리적 바닥선 탐지...")

        # 실제 최소값
        actual_min = rates.min()
        # 시뮬레이션 5% 백분위
        sim_5pct = np.percentile(simulated_min, 5)

        # 안전 하한선
        safe_floor = max(actual_min - 0.1, sim_5pct)

        self.results["심리적_바닥선"] = {
            "실제_최소": round(actual_min, 3),
            "시뮬_5%백분위": round(sim_5pct, 3),
            "안전_하한선": round(safe_floor, 3),
            "권장_최소입찰률": round(safe_floor + 0.05, 3)
        }

        print(f"  안전 하한선: {safe_floor:.3f}%")
        print(f"  권장 최소: {safe_floor + 0.05:.3f}%")

        return safe_floor

    def optimize_expected_value(self, past_rates, all_rates, hist, edges, simulated_rates):
        """Phase 9: 조건부 확률 최적화 - 기초대비사정률 기준 (NEW - 2025-10-26)"""
        print("\n[Phase 9] 조건부 확률 최적화 (기초대비사정률)...")

        # 스캔 범위: IQR ± 0.3% (기초대비사정률 범위: 98-102%)
        Q1 = np.percentile(past_rates, 25)
        Q3 = np.percentile(past_rates, 75)
        scan_min = max(Q1 - 0.3, 98.0)  # 기초대비사정률 최소값
        scan_max = min(Q3 + 0.3, 102.0)  # 기초대비사정률 최대값
        scan_rates = np.arange(scan_min, scan_max, 0.001)  # 0.001% 단위

        print(f"  스캔 범위: {scan_min:.3f}% ~ {scan_max:.3f}%")

        results = []
        for bid_rate in scan_rates:
            expected_utility = 0.0
            avg_p_win = 0.0
            valid_scenarios = 0

            # 모든 예정가 시나리오에 대해
            for reserve_rate in simulated_rates:
                # 이 예정가에서의 낙찰하한가
                min_win_rate = reserve_rate * (self.agency_rate / 100)

                # 내 입찰이 하한가 이상인가?
                if bid_rate >= min_win_rate:
                    # 이 구간의 경쟁자 수 계산
                    competitors = np.sum((all_rates >= min_win_rate) & (all_rates <= bid_rate))

                    # 1위 확률 = 1 / (경쟁자 + 1)
                    p_win = 1.0 / (competitors + 1)

                    # 이익률
                    profit_rate = (100 - bid_rate) / 100

                    # 누적
                    expected_utility += p_win * profit_rate
                    avg_p_win += p_win
                    valid_scenarios += 1

            # 평균화
            if valid_scenarios > 0:
                expected_utility /= len(simulated_rates)
                avg_p_win /= valid_scenarios
            else:
                expected_utility = 0
                avg_p_win = 0

            # 내 구간의 경쟁 밀도
            bin_idx = np.searchsorted(edges, bid_rate) - 1
            if 0 <= bin_idx < len(hist):
                my_competitors = hist[bin_idx]
            else:
                my_competitors = 0

            results.append({
                'rate': round(bid_rate, 3),
                'expected_utility': round(expected_utility, 6),
                'avg_p_win': round(avg_p_win, 6),
                'competitors': int(my_competitors),
                'profit_rate': round((100 - bid_rate) / 100, 4)
            })

        # 경쟁 밀도 200명 이하 필터
        filtered = [r for r in results if r['competitors'] <= 200]

        if not filtered:
            print("  ⚠️ 경쟁 200명 이하 구간 없음, 전체에서 선택")
            filtered = results

        # 최적 지점: expected_utility 최대
        optimal = max(filtered, key=lambda x: x['expected_utility'])

        # 상위 3개
        top3 = sorted(filtered, key=lambda x: x['expected_utility'], reverse=True)[:3]

        self.results["기대값_최적화"] = {
            "알고리즘": "조건부 확률 (NEW)",
            "분석_구간": f"{scan_min:.3f}% ~ {scan_max:.3f}%",
            "최적_입찰률": optimal['rate'],
            "기대_효용": optimal['expected_utility'],
            "평균_1위확률": optimal['avg_p_win'],
            "경쟁자_수": optimal['competitors'],
            "이익률": optimal['profit_rate'],
            "상위3개_후보": [{
                "입찰률": r['rate'],
                "기대효용": r['expected_utility'],
                "1위확률": r['avg_p_win'],
                "경쟁자": r['competitors']
            } for r in top3]
        }

        print(f"  최적 입찰률: {optimal['rate']:.3f}%")
        print(f"  기대 효용: {optimal['expected_utility']:.6f}")
        print(f"  평균 1위 확률: {optimal['avg_p_win']*100:.2f}%")
        print(f"  경쟁자 수: {optimal['competitors']}명")

        return {
            'optimal': optimal,
            'all_results': results,
            'top3': top3
        }

    def generate_strategies(self, rates, third_counts, ending_counts, optimal_result=None):
        """Phase 8: 최종 전략 3개 생성 (경쟁 밀도 회피형)"""
        print("\n[Phase 8] 최종 전략 생성 (Evasion Strategy)...")

        strategies = []

        if optimal_result is None:
            print("  ⚠️ 기대값 최적화 결과 없음, 기본 전략 사용")
            median = np.median(rates)
            safe_thirds = sorted(third_counts.items(), key=lambda x: x[1])[:3]
            safe_third = int(safe_thirds[0][0])

            rate_1 = round(median + 0.001, 3)
            strategies.append({
                "순위": 1,
                "전략명": "중앙값 기본 전략",
                "입찰률": rate_1,
                "입찰금액": int(self.base_amount * rate_1 / 100),
                "리스크": "중간",
                "충돌확률": "불명",
                "이유": "기대값 최적화 실패로 기본 전략 사용"
            })
        else:
            # NEW 알고리즘 (조건부 확률)
            optimal = optimal_result['optimal']
            top3 = optimal_result['top3']

            # 전략 1: 기대 효용 최적 (expected_utility 최대)
            strategies.append({
                "순위": 1,
                "전략명": "기대 효용 최적 (조건부 확률)",
                "입찰률": optimal['rate'],
                "입찰금액": int(self.base_amount * optimal['rate'] / 100),
                "1위확률": f"{optimal['avg_p_win']*100:.2f}%",
                "이익률": f"{optimal['profit_rate']*100:.1f}%",
                "기대효용": f"{optimal['expected_utility']:.6f}",
                "경쟁자수": optimal['competitors'],
                "리스크": "균형",
                "이유": "조건부 확률 × 이익률 최대화"
            })

            # 전략 2: 경쟁 회피 (competitors 최소)
            all_results = optimal_result['all_results']
            low_comp_candidates = [r for r in all_results if r['competitors'] <= 150]
            if low_comp_candidates:
                low_comp = min(low_comp_candidates, key=lambda x: x['competitors'])
            else:
                low_comp = min(all_results, key=lambda x: x['competitors'])

            strategies.append({
                "순위": 2,
                "전략명": "경쟁 회피 (1위 확률 최대)",
                "입찰률": low_comp['rate'],
                "입찰금액": int(self.base_amount * low_comp['rate'] / 100),
                "1위확률": f"{low_comp['avg_p_win']*100:.2f}%",
                "이익률": f"{low_comp['profit_rate']*100:.1f}%",
                "기대효용": f"{low_comp['expected_utility']:.6f}",
                "경쟁자수": low_comp['competitors'],
                "리스크": "낮음 (경쟁 최소)",
                "이유": "경쟁 밀도 최소 구간 선택"
            })

            # 전략 3: 이익 최대 (profit_rate 최대, 경쟁자 200명 이하)
            profit_candidates = [r for r in all_results if r['competitors'] <= 200]
            if profit_candidates:
                profit_max = max(profit_candidates, key=lambda x: x['profit_rate'])
            else:
                profit_max = max(all_results, key=lambda x: x['profit_rate'])

            strategies.append({
                "순위": 3,
                "전략명": "이익 최대 (수익 우선)",
                "입찰률": profit_max['rate'],
                "입찰금액": int(self.base_amount * profit_max['rate'] / 100),
                "1위확률": f"{profit_max['avg_p_win']*100:.2f}%",
                "이익률": f"{profit_max['profit_rate']*100:.1f}%",
                "기대효용": f"{profit_max['expected_utility']:.6f}",
                "경쟁자수": profit_max['competitors'],
                "리스크": "중간 (수익 우선)",
                "이유": "이익률 최대화 (낙찰률 감수)"
            })

        self.results["추천_전략"] = strategies

        for s in strategies:
            print(f"\n  {s['순위']}. {s['전략명']}")
            print(f"     입찰률: {s['입찰률']}%")
            print(f"     입찰금액: {s['입찰금액']:,}원")
            if '1위확률' in s:
                print(f"     1위 확률: {s['1위확률']}")
            if '경쟁자수' in s:
                print(f"     경쟁자: {s['경쟁자수']}명")
            if '이익률' in s:
                print(f"     이익률: {s['이익률']}")
            if '기대효용' in s:
                print(f"     기대 효용: {s['기대효용']}")
            print(f"     리스크: {s['리스크']}")
            print(f"     이유: {s['이유']}")

        return strategies

    def create_balance_graph(self, hist, edges, optimal_result):
        """
        균형점 분석 그래프 생성 (그래프.md 사양) - 기초대비사정률 기준

        - X축: 기초대비사정률 (98-102% 범위)
        - Y축 왼쪽: 경쟁자 밀도 (막대)
        - Y축 오른쪽: 기대효용 & 1위확률 (선)
        - 최적점: 노란 별★ 표시
        - 소수점 3자리 표시 (%.3f%%)
        """
        print("\n[그래프] 균형점 분석 그래프 생성 (기초대비사정률)...")

        # 한글 폰트 자동 감지 및 설정
        korean_font = get_korean_font()
        plt.rcParams['font.family'] = korean_font
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 12
        print(f"  폰트: {korean_font}")

        # 그래프 크기 (그래프.md 사양: 14×9인치, 300DPI)
        fig, ax1 = plt.subplots(figsize=(14, 9), dpi=300)

        # X축 범위: 기초대비사정률 범위 (98-102%)
        x_min = 98.0
        x_max = 102.0

        # 데이터 필터링
        mask = (edges[:-1] >= x_min) & (edges[:-1] <= x_max)
        x_data = edges[:-1][mask]
        y_density = hist[mask]

        # Y축 왼쪽: 경쟁자 밀도 (막대그래프)
        bars = ax1.bar(x_data, y_density, width=0.05,
                       color='#AED6F1', edgecolor='#2E86DE',
                       alpha=0.7, label='경쟁자 밀도')
        ax1.set_xlabel('기초대비 사정률 (%)', fontsize=13, weight='bold')
        ax1.set_ylabel('경쟁자 수 (명)', fontsize=13, weight='bold', color='#2E86DE')
        ax1.tick_params(axis='y', labelcolor='#2E86DE')
        ax1.set_xlim(x_min, x_max)

        # X축 포맷: 소수점 3자리
        ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f%%'))

        # Y축 오른쪽: 기대효용 & 1위확률
        ax2 = ax1.twinx()

        # optimal_result의 all_results에서 그래프 데이터 추출
        all_results = optimal_result['all_results']
        rates = [r['rate'] for r in all_results if x_min <= r['rate'] <= x_max]
        utilities = [r['expected_utility'] * 100 for r in all_results if x_min <= r['rate'] <= x_max]
        p_wins = [r['avg_p_win'] * 100 for r in all_results if x_min <= r['rate'] <= x_max]

        # 기대효용 선 (빨간색)
        line1 = ax2.plot(rates, utilities, color='#E74C3C', linewidth=3,
                        label='기대효용 (%)', zorder=5)

        # 1위확률 선 (초록색)
        line2 = ax2.plot(rates, p_wins, color='#28B463', linewidth=2.5,
                        label='평균 1위확률 (%)', zorder=5)

        ax2.set_ylabel('기대효용 / 1위확률 (%)', fontsize=13, weight='bold', color='#E74C3C')
        ax2.tick_params(axis='y', labelcolor='#E74C3C')

        # 최적 균형점 표시 (노란 별)
        optimal_rate = optimal_result['optimal']['rate']
        optimal_util = optimal_result['optimal']['expected_utility'] * 100
        ax2.plot(optimal_rate, optimal_util, marker='*', markersize=25,
                color='#FFD700', markeredgecolor='black', markeredgewidth=1.5,
                zorder=10, label='최적 균형점')

        # 최적점 주석
        ax2.annotate(f'최적균형점\n{optimal_rate:.3f}%\n경쟁자: {optimal_result["optimal"]["competitors"]}명',
                    xy=(optimal_rate, optimal_util),
                    xytext=(optimal_rate + 0.3, optimal_util + 0.5),
                    fontsize=11, weight='bold', color='#FFD700',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#FFD700', linewidth=2),
                    arrowprops=dict(arrowstyle='->', color='#FFD700', linewidth=2))

        # 경쟁 과밀 구간 음영 (200명 이상)
        for i, (x, density) in enumerate(zip(x_data, y_density)):
            if density >= 200:
                ax1.axvspan(x - 0.025, x + 0.025, color='#FADBD8', alpha=0.4, zorder=1)

        # 안전 구간 음영 (100명 이하)
        for i, (x, density) in enumerate(zip(x_data, y_density)):
            if density <= 100:
                ax1.axvspan(x - 0.025, x + 0.025, color='#D5F4E6', alpha=0.3, zorder=1)

        # 중앙 기준선 (100%)
        ax1.axvline(x=100.0, color='black', linestyle=':', linewidth=2,
                   label=f'기초금액 (100.000%)', zorder=3)

        # 격자
        ax1.grid(True, linestyle=':', alpha=0.5, color='#D5D8DC')

        # 범례 통합
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2,
                  loc='upper right', fontsize=11, framealpha=0.95)

        # 제목
        plt.title('복수예가입찰 균형점 분석 전략 (기초대비사정률)\n(경쟁밀도 · 기대효용 · 1위확률 통합)',
                 fontsize=16, weight='bold', pad=20)

        # 저장
        output_file = f"/mnt/a/25/data분석/balance_graph_{int(self.agency_rate*1000)}.png"
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✅ 그래프 저장: {output_file}")
        return output_file

    def create_competition_heatmap(self, hist, edges, optimal_result):
        """
        경쟁 밀도 히트맵 생성

        - X축: 기초대비사정률 (98-102%)
        - Y축: 단일 행 (히트맵 바 형태)
        - 색상: 경쟁자 밀도 (RdYlGn_r - 빨강=위험, 초록=안전)
        - 최적점: 노란 별★ 표시
        """
        print("\n[히트맵] 경쟁 밀도 히트맵 생성...")

        # 한글 폰트 설정
        korean_font = get_korean_font()
        plt.rcParams['font.family'] = korean_font
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 12

        # 그래프 크기
        fig, ax = plt.subplots(figsize=(16, 4), dpi=300)

        # X축 범위
        x_min = 98.0
        x_max = 102.0

        # 데이터 필터링
        mask = (edges[:-1] >= x_min) & (edges[:-1] <= x_max)
        x_data = edges[:-1][mask]
        y_density = hist[mask]

        # 히트맵 데이터 준비 (1행 히트맵)
        heatmap_data = y_density.reshape(1, -1)

        # 히트맵 그리기 (RdYlGn_r: 빨강=높음, 노랑=중간, 초록=낮음)
        im = ax.imshow(heatmap_data, cmap='RdYlGn_r', aspect='auto',
                      extent=[x_min, x_max, 0, 1], interpolation='nearest')

        # 컬러바
        cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.02)
        cbar.set_label('경쟁자 수 (명)', fontsize=13, weight='bold')

        # X축 설정
        ax.set_xlabel('기초대비 사정률 (%)', fontsize=13, weight='bold')
        ax.set_xlim(x_min, x_max)

        # X축 눈금 (0.5% 간격)
        x_ticks = np.arange(x_min, x_max + 0.1, 0.5)
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([f'{x:.1f}%' for x in x_ticks])

        # Y축 제거 (단일 행이므로)
        ax.set_yticks([])
        ax.set_ylabel('')

        # 최적점 표시 (노란 별)
        optimal_rate = optimal_result['optimal']['rate']
        ax.plot(optimal_rate, 0.5, marker='*', markersize=30,
               color='#FFD700', markeredgecolor='black', markeredgewidth=2,
               zorder=10)

        # 최적점 주석
        ax.annotate(f'최적점: {optimal_rate:.3f}%\n경쟁자: {optimal_result["optimal"]["competitors"]}명',
                   xy=(optimal_rate, 0.5),
                   xytext=(optimal_rate, 1.5),
                   fontsize=11, weight='bold', color='black',
                   ha='center',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                            edgecolor='#FFD700', linewidth=2),
                   arrowprops=dict(arrowstyle='->', color='#FFD700', linewidth=2))

        # 중앙 기준선 (100%)
        ax.axvline(x=100.0, color='blue', linestyle='--', linewidth=2,
                  alpha=0.7, label='기초금액 (100%)')

        # 범례
        ax.legend(loc='upper left', fontsize=11, framealpha=0.95)

        # 제목
        plt.title('경쟁 밀도 히트맵 (기초대비사정률)\n빨강=고위험 구간, 초록=안전 구간',
                 fontsize=16, weight='bold', pad=20)

        # 저장
        output_file = f"/mnt/a/25/data분석/heatmap_{int(self.agency_rate*1000)}.png"
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"  ✅ 히트맵 저장: {output_file}")
        return output_file

    def save_results(self, output_file):
        """결과를 JSON 파일로 저장"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 결과 저장: {output_path}")

    def run_full_analysis(self):
        """전체 분석 실행"""
        print("="*80)
        print("입찰 분석 로직 - 통합 실행")
        print("="*80)
        print(f"기초금액: {self.base_amount:,}원")
        print(f"발주처투찰률: {self.agency_rate}%")

        # Phase 1: 몬테카를로
        simulated_rates = self.run_monte_carlo()

        # Phase 2: 과거 1위 (낙찰 가능 범위 파악)
        past_rates = self.analyze_past_winners()
        if past_rates is None:
            print("\n⚠️ 과거 데이터가 없어 분석을 중단합니다.")
            return None

        # Phase 3: 경쟁 밀도 (전체 유효 업체 분포)
        all_rates, hist, edges = self.analyze_competition_density()
        if all_rates is None:
            print("\n⚠️ 경쟁 밀도 분석 실패.")
            return None

        # Phase 4: 소수점 패턴 (전체 업체 기준)
        third_counts = self.analyze_decimal_patterns(all_rates)

        # Phase 5: 끝자리 선호도 (전체 업체 기준)
        ending_counts = self.analyze_ending_digits(all_rates)

        # Phase 6: 심리적 바닥선
        safe_floor = self.find_psychological_floor(past_rates, simulated_rates)

        # Phase 9: 기대값 최적화 (경쟁 밀도 회피형)
        optimal_result = self.optimize_expected_value(past_rates, all_rates, hist, edges, simulated_rates)

        # Phase 8: 최종 전략
        strategies = self.generate_strategies(past_rates, third_counts, ending_counts, optimal_result)

        # 그래프 생성
        graph_file = self.create_balance_graph(hist, edges, optimal_result)
        heatmap_file = self.create_competition_heatmap(hist, edges, optimal_result)

        # 결과 저장
        output_file = f"/mnt/a/25/data분석/bidding_analysis_{int(self.agency_rate*1000)}.json"
        self.save_results(output_file)

        print("\n" + "="*80)
        print("분석 완료!")
        print(f"JSON: {output_file}")
        print(f"균형점 그래프: {graph_file}")
        print(f"경쟁 밀도 히트맵: {heatmap_file}")
        print("="*80)

        return self.results

def main():
    parser = argparse.ArgumentParser(description='입찰 분석 로직')
    parser.add_argument('--base-amount', type=int, required=True, help='기초금액')
    parser.add_argument('--agency-rate', type=float, required=True, help='발주처투찰률')
    parser.add_argument('--data-file', type=str, required=True, help='데이터 파일 경로')

    args = parser.parse_args()

    analyzer = BiddingAnalyzer(
        base_amount=args.base_amount,
        agency_rate=args.agency_rate,
        data_file=args.data_file
    )

    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()
