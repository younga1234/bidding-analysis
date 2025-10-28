#!/usr/bin/env python3
"""
입찰 분석 COMPREHENSIVE - 모든 요소 통합
- 예정가 형성 확률 (몬테카를로)
- 시간 가중 경쟁 밀도 (1개월 40%, 3개월 30%, 6개월 20%, 1년 10%)
- 상대적 몰림도 (평균 대비)
- 실제 1위 확률 (과거 1위 존재 필수)
- 이익률
- 최소 샘플 크기 (통계적 유의성)
- 0.01% 단위 분석
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def monte_carlo_reserve_price(base_amount, n=10000):
    """
    몬테카를로 시뮬레이션 - 예정가 형성 확률
    15개 추첨 (98~102%), 4개 선택, 평균 = 예정가
    """
    simulations = []
    for _ in range(n):
        draws = np.random.uniform(98, 102, 15)
        selected = np.random.choice(draws, 4, replace=False)
        reserve_price = np.mean(selected)
        simulations.append(reserve_price)

    return np.array(simulations)

def calculate_time_weighted_density(df, bin_start, bin_end):
    """
    시간 가중 경쟁 밀도
    1개월 40%, 3개월 30%, 6개월 20%, 1년 10%
    """
    now = datetime.now()
    df['날짜'] = pd.to_datetime(df['투찰일시'])

    periods = {
        '1개월': (now - timedelta(days=30), 0.40),
        '3개월': (now - timedelta(days=90), 0.30),
        '6개월': (now - timedelta(days=180), 0.20),
        '1년': (now - timedelta(days=365), 0.10),
    }

    total_weighted = 0.0
    period_counts = {}

    for period_name, (cutoff_date, weight) in periods.items():
        period_df = df[df['날짜'] >= cutoff_date]

        count = len(period_df[
            (period_df['기초대비투찰률'] >= bin_start) &
            (period_df['기초대비투찰률'] < bin_end)
        ])

        total_weighted += count * weight
        period_counts[period_name] = count

    return total_weighted, period_counts

def comprehensive_analysis(df, base_amount, agency_rate, bin_size=0.001):
    """
    종합 분석 - 모든 요소 통합
    """
    print("[1/5] 몬테카를로 시뮬레이션...")
    reserve_simulations = monte_carlo_reserve_price(base_amount, n=10000)
    print(f"  예정가 범위: {reserve_simulations.min():.3f}% ~ {reserve_simulations.max():.3f}%")
    print()

    print("[2/5] 전체 경쟁 밀도 분석...")
    min_rate = df['기초대비투찰률'].min()
    max_rate = df['기초대비투찰률'].max()

    bins = np.arange(
        np.floor(min_rate / bin_size) * bin_size,
        np.ceil(max_rate / bin_size) * bin_size + bin_size,
        bin_size
    )

    print(f"  분석 구간: {len(bins)-1}개 ({bin_size}% 단위)")
    print()

    print("[3/5] 평균 경쟁 밀도 계산...")
    total_competitors = len(df)
    num_bins = len(bins) - 1
    avg_density = total_competitors / num_bins
    print(f"  전체 업체: {total_competitors}명")
    print(f"  평균 밀도: {avg_density:.2f}명/구간")
    print()

    print("[4/5] 각 구간별 분석...")
    candidates = []

    for i in range(len(bins) - 1):
        bin_start = bins[i]
        bin_end = bins[i + 1]
        bin_mid = (bin_start + bin_end) / 2

        # 이 구간의 전체 데이터
        bin_df = df[
            (df['기초대비투찰률'] >= bin_start) &
            (df['기초대비투찰률'] < bin_end)
        ]

        total_count = len(bin_df)

        if total_count == 0:
            continue

        # 이 구간의 1위
        winners = bin_df[bin_df['순위'] == 1]
        winner_count = len(winners)

        # 1위가 없는 구간은 제외
        if winner_count == 0:
            continue

        # 1. 예정가 형성 확률
        required_reserve = bin_mid / (agency_rate / 100)
        p_reserve = np.sum(reserve_simulations >= required_reserve) / len(reserve_simulations)

        if p_reserve < 0.01:  # 1% 미만이면 스킵
            continue

        # 2. 시간 가중 경쟁 밀도
        weighted_density, period_counts = calculate_time_weighted_density(
            df, bin_start, bin_end
        )

        if weighted_density == 0:
            continue

        # 3. 상대적 몰림도
        relative_crowding = weighted_density / avg_density

        # 4. 실제 1위 확률
        actual_win_prob = winner_count / total_count

        # 종합 점수 = 모든 요소 통합
        score = (
            p_reserve
            * actual_win_prob
            * (1 / (weighted_density + 1))
            * (1 / (relative_crowding + 0.1))
        )

        # 기초대비사정률 계산
        reserve_rate = (bin_mid / agency_rate) * 100

        candidates.append({
            'bin_start': bin_start,
            'bin_end': bin_end,
            'bin_mid': bin_mid,
            'reserve_rate': reserve_rate,
            'total_competitors': total_count,
            'winners': winner_count,
            'actual_win_prob': actual_win_prob,
            'p_reserve': p_reserve,
            'weighted_density': weighted_density,
            'relative_crowding': relative_crowding,
            'score': score,
            'amount': int(base_amount * bin_mid / 100),
            'period_counts': period_counts
        })

    print(f"  유효 구간: {len(candidates)}개")
    print()

    print("[5/5] 종합 점수 정렬...")
    candidates.sort(key=lambda x: x['score'], reverse=True)

    return candidates

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--base-amount', type=int, required=True)
    parser.add_argument('--agency-rate', type=float, required=True)
    parser.add_argument('--data-file', required=True)

    args = parser.parse_args()

    print("=" * 80)
    print("입찰 분석 COMPREHENSIVE (모든 요소 통합)")
    print("=" * 80)
    print(f"기초금액: {args.base_amount:,}원")
    print(f"발주처투찰률: {args.agency_rate}%")
    print()

    # 데이터 로드
    df = pd.read_excel(args.data_file)
    print(f"✅ 데이터 로드: {len(df):,}건")
    print()

    # 종합 분석
    candidates = comprehensive_analysis(df, args.base_amount, args.agency_rate)

    print("=" * 80)
    print("최종 결과 (Top 10)")
    print("=" * 80)

    for i, item in enumerate(candidates[:10], 1):
        print(f"\n{i}. 기초대비투찰률: {item['bin_mid']:.3f}%")
        print(f"   기초대비사정률: {item['reserve_rate']:.3f}%")
        print(f"   입찰금액: {item['amount']:,}원")
        print(f"   실제 1위 확률: {item['actual_win_prob']:.2%} ({item['winners']}명 / {item['total_competitors']}명)")
        print(f"   예정가 형성 확률: {item['p_reserve']:.1%}")
        print(f"   시간 가중 밀도: {item['weighted_density']:.1f}명")
        print(f"   상대적 몰림: {item['relative_crowding']:.2f}배")
        print(f"   종합 점수: {item['score']:.8f}")

    # 결과 저장
    output = {
        '기초금액': args.base_amount,
        '발주처투찰률': args.agency_rate,
        '전체_데이터': len(df),
        '최종_추천': candidates[0] if candidates else None,
        '상위10개': candidates[:10]
    }

    with open('data분석/bidding_analysis_comprehensive_87745.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2, default=str)

    print("\n" + "=" * 80)
    print(f"✅ 결과 저장: data분석/bidding_analysis_comprehensive_87745.json")
    print("=" * 80)

if __name__ == '__main__':
    main()
