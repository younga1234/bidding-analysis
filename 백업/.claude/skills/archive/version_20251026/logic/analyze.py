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

class BiddingAnalyzer:
    def __init__(self, base_amount, agency_rate, data_file):
        self.base_amount = base_amount
        self.agency_rate = agency_rate
        self.data_file = Path(data_file)
        self.variance_range = 0.03  # ±3%
        self.n_simulations = 10000

        # 결과 저장
        self.results = {
            "공고정보": {
                "기초금액": base_amount,
                "발주처투찰률": agency_rate,
                "분석시각": datetime.now().isoformat()
            }
        }

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
        """Phase 2: 과거 1위 데이터 분석"""
        print("\n[Phase 2] 과거 1위 데이터 분석...")

        if not self.data_file.exists():
            print(f"  ⚠️ 데이터 파일 없음: {self.data_file}")
            return None

        df = pd.read_excel(self.data_file)
        df_first = df[df['순위'] == 1].copy()
        rates = df_first['기초대비투찰률'].values

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
        """Phase 3: 경쟁 밀도 히트맵 (전체 유효 업체 분석)"""
        print("\n[Phase 3] 경쟁 밀도 분석 (전체 참여 업체)...")

        # 전체 유효 입찰 데이터 로드 (순위 -1 제외)
        if not self.data_file.exists():
            print(f"  ⚠️ 데이터 파일 없음: {self.data_file}")
            return None, None

        df = pd.read_excel(self.data_file)
        df_valid = df[df['순위'] >= 1].copy()  # 유효 입찰만
        all_rates = df_valid['기초대비투찰률'].values

        print(f"  전체 참여 업체: {len(df)}개")
        print(f"  유효 입찰: {len(df_valid)}개")
        print(f"  탈락 (순위 -1): {len(df[df['순위'] == -1])}개")

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
            if hist[idx] <= 2 and edges[idx] >= 87.0:  # 하한가 이상만
                start = edges[idx]
                end = edges[idx + 1]
                safe_zones.append(f"{start:.2f}~{end:.2f}% ({hist[idx]}개)")

        self.results["경쟁_밀도"] = {
            "분석_대상": f"유효 입찰 {len(df_valid)}개",
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
        """Phase 9: 기대값 최적화 (경쟁 밀도 회피형)"""
        print("\n[Phase 9] 기대값 최적화 (Expectational Evasion Strategy)...")

        # 평균 예정가격 (몬테카를로 결과)
        avg_reserve_price = self.results["몬테카를로_시뮬레이션"]["예정가격_평균"]

        # 스캔 범위: 과거 1위 최소~최대 ±0.5%
        scan_min = max(past_rates.min() - 0.5, 85.0)
        scan_max = min(past_rates.max() + 0.5, 90.0)
        scan_rates = np.arange(scan_min, scan_max, 0.01)

        results = []
        for x in scan_rates:
            # 1. P_floor: 몬테카를로 시뮬레이션에서 낙찰하한가 ≤ x인 비율
            p_floor = np.sum(simulated_rates <= x) / len(simulated_rates)

            # 2. P_compete: 과거 1위가 x 이하인 비율 (CDF)
            p_compete = np.sum(past_rates <= x) / len(past_rates)

            # 3. P_collision: 해당 구간의 경쟁 밀도
            bin_idx = np.searchsorted(edges, x) - 1
            if 0 <= bin_idx < len(hist):
                density = hist[bin_idx]
                p_collision = density / len(all_rates)
            else:
                p_collision = 0

            # 4. P_win: 실제 낙찰 확률
            p_win = p_floor * p_compete * (1 - p_collision)

            # 5. R_profit: 이익률
            bid_amount = self.base_amount * x / 100
            profit = avg_reserve_price - bid_amount
            r_profit = profit / avg_reserve_price if avg_reserve_price > 0 else 0

            # 6. E(x): 기대값 (금액)
            e_value = p_win * profit

            # 7. f(x): 경쟁 밀도 리스크 (금액 단위로 페널티)
            f_risk = p_collision * avg_reserve_price

            # 8. Adjusted E(x): 경쟁 밀도 차감 기대값
            lambda_risk = 0.5  # 리스크 가중치
            adjusted_e = e_value - lambda_risk * f_risk

            results.append({
                'rate': round(x, 3),
                'p_floor': round(p_floor, 4),
                'p_compete': round(p_compete, 4),
                'p_collision': round(p_collision, 4),
                'p_win': round(p_win, 4),
                'r_profit': round(r_profit, 4),
                'e_value': round(e_value, 2),
                'f_risk': round(f_risk, 2),
                'adjusted_e': round(adjusted_e, 2)
            })

        # 최적 지점 찾기
        results_sorted = sorted(results, key=lambda x: x['adjusted_e'], reverse=True)
        optimal = results_sorted[0]

        # 상위 5개
        top5 = results_sorted[:5]

        self.results["기대값_최적화"] = {
            "분석_구간": f"{scan_min:.2f}% ~ {scan_max:.2f}%",
            "최적_입찰률": optimal['rate'],
            "최적_낙찰확률": optimal['p_win'],
            "최적_이익률": optimal['r_profit'],
            "최적_기대값": optimal['adjusted_e'],
            "경쟁_밀도_리스크": optimal['p_collision'],
            "상위5개_후보": [{
                "입찰률": r['rate'],
                "조정_기대값": r['adjusted_e'],
                "낙찰확률": r['p_win']
            } for r in top5]
        }

        print(f"  최적 입찰률: {optimal['rate']}%")
        print(f"  조정 기대값: {optimal['adjusted_e']:,.0f}원")
        print(f"  낙찰 확률: {optimal['p_win']*100:.1f}%")
        print(f"  경쟁 리스크: {optimal['p_collision']*100:.1f}%")

        return {
            'optimal': optimal,
            'all_results': results,
            'top5': top5
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
            # 전략 1: 기대값 최적 (조정 기대값 최대 지점)
            optimal = optimal_result['optimal']
            top5 = optimal_result['top5']

            strategies.append({
                "순위": 1,
                "전략명": "기대값 최적 전략 (Optimal E-f)",
                "입찰률": optimal['rate'],
                "입찰금액": int(self.base_amount * optimal['rate'] / 100),
                "낙찰확률": f"{optimal['p_win']*100:.1f}%",
                "이익률": f"{optimal['r_profit']*100:.1f}%",
                "조정_기대값": f"{optimal['adjusted_e']:,.0f}원",
                "경쟁_리스크": f"{optimal['p_collision']*100:.1f}%",
                "리스크": "균형",
                "이유": "경쟁 밀도를 차감한 기대값이 최대인 지점 (Expectational Evasion)"
            })

            # 전략 2: 확률 중심 (P_win 최대)
            all_results = optimal_result['all_results']
            prob_max = max(all_results, key=lambda x: x['p_win'])

            strategies.append({
                "순위": 2,
                "전략명": "확률 중심 전략 (Max P_win)",
                "입찰률": prob_max['rate'],
                "입찰금액": int(self.base_amount * prob_max['rate'] / 100),
                "낙찰확률": f"{prob_max['p_win']*100:.1f}%",
                "이익률": f"{prob_max['r_profit']*100:.1f}%",
                "조정_기대값": f"{prob_max['adjusted_e']:,.0f}원",
                "경쟁_리스크": f"{prob_max['p_collision']*100:.1f}%",
                "리스크": "낮음 (낙찰 우선)",
                "이유": "낙찰 확률이 최대인 지점 (수익률 희생 가능)"
            })

            # 전략 3: 이익 중심 (R_profit 높으면서 P_win > 30%)
            profit_candidates = [r for r in all_results if r['p_win'] >= 0.3]
            if profit_candidates:
                profit_max = max(profit_candidates, key=lambda x: x['r_profit'])
            else:
                profit_max = max(all_results, key=lambda x: x['r_profit'])

            strategies.append({
                "순위": 3,
                "전략명": "이익 중심 전략 (Max R_profit)",
                "입찰률": profit_max['rate'],
                "입찰금액": int(self.base_amount * profit_max['rate'] / 100),
                "낙찰확률": f"{profit_max['p_win']*100:.1f}%",
                "이익률": f"{profit_max['r_profit']*100:.1f}%",
                "조정_기대값": f"{profit_max['adjusted_e']:,.0f}원",
                "경쟁_리스크": f"{profit_max['p_collision']*100:.1f}%",
                "리스크": "높음 (수익 우선)",
                "이유": "이익률이 최대인 지점 (낙찰 확률 낮을 수 있음)"
            })

        self.results["추천_전략"] = strategies

        for s in strategies:
            print(f"\n  {s['순위']}. {s['전략명']}")
            print(f"     입찰률: {s['입찰률']}%")
            print(f"     입찰금액: {s['입찰금액']:,}원")
            if '낙찰확률' in s:
                print(f"     낙찰확률: {s['낙찰확률']}")
            if '이익률' in s:
                print(f"     이익률: {s['이익률']}")
            if '조정_기대값' in s:
                print(f"     조정 기대값: {s['조정_기대값']}")
            if '경쟁_리스크' in s:
                print(f"     경쟁 리스크: {s['경쟁_리스크']}")
            print(f"     리스크 수준: {s['리스크']}")
            print(f"     이유: {s['이유']}")

        return strategies

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

        # 결과 저장
        output_file = f"/mnt/a/25/data분석/bidding_analysis_{int(self.agency_rate*1000)}.json"
        self.save_results(output_file)

        print("\n" + "="*80)
        print("분석 완료!")
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
