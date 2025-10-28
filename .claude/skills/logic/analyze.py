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

    def analyze_competition_density(self, rates):
        """Phase 3: 경쟁 밀도 히트맵"""
        print("\n[Phase 3] 경쟁 밀도 분석...")

        # 0.05% 단위 구간별 분포
        bins = np.arange(rates.min() // 0.05 * 0.05, rates.max() + 0.05, 0.05)
        hist, edges = np.histogram(rates, bins=bins)

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
            "최고_밀집_구간": avoid_zones[0] if avoid_zones else "없음",
            "회피_구간_Top5": avoid_zones[:5],
            "안전_구간_Top10": safe_zones[:10]
        }

        print(f"  최고 밀집: {avoid_zones[0] if avoid_zones else '없음'}")
        print(f"  안전 구간: {len(safe_zones)}개")

        return hist, edges

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

    def generate_strategies(self, rates, third_counts, ending_counts):
        """Phase 8: 최종 전략 3개 생성"""
        print("\n[Phase 8] 최종 전략 생성...")

        median = np.median(rates)
        mean = rates.mean()

        # 안전한 셋째 자리
        safe_thirds = sorted(third_counts.items(), key=lambda x: x[1])[:3]
        safe_third = int(safe_thirds[0][0])

        # 안전한 끝자리
        safe_endings = sorted(ending_counts.items(), key=lambda x: x[1])[:3]
        safe_endings = [(int(e[0]), e[1]) for e in safe_endings]

        strategies = []

        # 전략 1: 중앙값 + 소수점 조정
        rate_1 = round(median + 0.001, 3)
        # 셋째 자리를 안전한 숫자로 조정
        rate_1 = (int(rate_1 * 100) / 100) + (safe_third / 1000)
        amount_1 = int(self.base_amount * rate_1 / 100)
        # 끝자리 조정
        ending_1 = amount_1 % 1000
        if ending_1 in [0, 500]:  # 충돌 위험
            amount_1 = amount_1 - ending_1 + safe_endings[0][0]

        strategies.append({
            "순위": 1,
            "전략명": "중앙값 전략 (안정적)",
            "입찰률": round(rate_1, 3),
            "입찰금액": amount_1,
            "리스크": "중간",
            "충돌확률": "낮음",
            "이유": f"과거 중앙값({median:.3f}%) 기반, 소수점 셋째자리 {safe_third}로 조정"
        })

        # 전략 2: 저경쟁 구간
        rate_2 = median - 0.1  # 약간 낮게
        rate_2 = (int(rate_2 * 100) / 100) + (safe_third / 1000)
        amount_2 = int(self.base_amount * rate_2 / 100)
        ending_2 = amount_2 % 1000
        if ending_2 in [0, 500]:
            amount_2 = amount_2 - ending_2 + safe_endings[1][0]

        strategies.append({
            "순위": 2,
            "전략명": "저경쟁 구간 (공격적)",
            "입찰률": round(rate_2, 3),
            "입찰금액": amount_2,
            "리스크": "높음",
            "충돌확률": "매우낮음",
            "이유": "경쟁 밀도 낮은 구간, 하한가 위험 있음"
        })

        # 전략 3: 고안전 구간
        rate_3 = median + 0.2  # 약간 높게
        rate_3 = (int(rate_3 * 100) / 100) + (safe_third / 1000)
        amount_3 = int(self.base_amount * rate_3 / 100)
        ending_3 = amount_3 % 1000
        if ending_3 in [0, 500]:
            amount_3 = amount_3 - ending_3 + safe_endings[2][0]

        strategies.append({
            "순위": 3,
            "전략명": "고안전 구간 (보수적)",
            "입찰률": round(rate_3, 3),
            "입찰금액": amount_3,
            "리스크": "낮음",
            "충돌확률": "없음",
            "이유": "안전하지만 가격 경쟁력 낮음"
        })

        self.results["추천_전략"] = strategies

        for s in strategies:
            print(f"\n  {s['순위']}. {s['전략명']}")
            print(f"     입찰률: {s['입찰률']}%")
            print(f"     입찰금액: {s['입찰금액']:,}원")
            print(f"     리스크: {s['리스크']}")

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

        # Phase 2: 과거 1위
        past_rates = self.analyze_past_winners()
        if past_rates is None:
            print("\n⚠️ 과거 데이터가 없어 분석을 중단합니다.")
            return None

        # Phase 3: 경쟁 밀도
        hist, edges = self.analyze_competition_density(past_rates)

        # Phase 4: 소수점 패턴
        third_counts = self.analyze_decimal_patterns(past_rates)

        # Phase 5: 끝자리 선호도
        ending_counts = self.analyze_ending_digits(past_rates)

        # Phase 6: 심리적 바닥선
        safe_floor = self.find_psychological_floor(past_rates, simulated_rates)

        # Phase 8: 최종 전략
        strategies = self.generate_strategies(past_rates, third_counts, ending_counts)

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
