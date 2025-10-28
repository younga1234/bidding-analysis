#!/usr/bin/env python3
"""
시간대별 가중 분석
6개 기간 × 가중치 → 최종 최적 입찰률
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import sys

def analyze_temporal_weighted(df, base_rate):
    """
    시간대별 가중 분석

    기간:
    - 1개월: 40%
    - 3개월: 30%
    - 6개월: 20%
    - 1년: 10%
    - 2년: 0%
    - 3년: 0%
    """

    now = datetime.now()

    # 날짜 컬럼 변환
    df['날짜'] = pd.to_datetime(df['투찰일시'])

    # 기간별 정의
    periods = {
        '1개월': (now - timedelta(days=30), 0.40),
        '3개월': (now - timedelta(days=90), 0.30),
        '6개월': (now - timedelta(days=180), 0.20),
        '1년': (now - timedelta(days=365), 0.10),
    }

    results = {}

    for period_name, (cutoff_date, weight) in periods.items():
        # 해당 기간 데이터 필터
        period_df = df[df['날짜'] >= cutoff_date].copy()

        if len(period_df) < 10:
            print(f"⚠️ {period_name}: 데이터 부족 ({len(period_df)}건), 건너뜀")
            continue

        # 경쟁 밀도 히트맵 (0.05% 구간)
        bin_size = 0.05
        min_rate = period_df['기초대비사정률'].min()
        max_rate = period_df['기초대비사정률'].max()

        bins = np.arange(
            np.floor(min_rate / bin_size) * bin_size,
            np.ceil(max_rate / bin_size) * bin_size + bin_size,
            bin_size
        )

        # 구간별 경쟁자 수 계산
        density_map = {}
        for i in range(len(bins) - 1):
            bin_start = bins[i]
            bin_end = bins[i + 1]
            count = len(period_df[
                (period_df['기초대비사정률'] >= bin_start) &
                (period_df['기초대비사정률'] < bin_end)
            ])
            if count > 0:
                density_map[f"{bin_start:.2f}~{bin_end:.2f}"] = count

        # 경쟁 밀도 최소 구간 찾기 (1위 존재 확인)
        winners = period_df[period_df['순위'] == 1]

        min_density = float('inf')
        optimal_rate = None

        for bin_range, count in density_map.items():
            # 이 구간에 과거 1위가 있는지 확인
            bin_start = float(bin_range.split('~')[0])
            bin_end = float(bin_range.split('~')[1])

            has_winner = len(winners[
                (winners['기초대비사정률'] >= bin_start) &
                (winners['기초대비사정률'] < bin_end)
            ]) > 0

            if has_winner and count < min_density:
                min_density = count
                optimal_rate = (bin_start + bin_end) / 2

        if optimal_rate is None:
            # 1위 없으면 단순 최소 밀도 구간
            min_bin = min(density_map, key=density_map.get)
            bin_start = float(min_bin.split('~')[0])
            bin_end = float(min_bin.split('~')[1])
            optimal_rate = (bin_start + bin_end) / 2
            min_density = density_map[min_bin]

        results[period_name] = {
            'data_count': len(period_df),
            'optimal_rate': optimal_rate,
            'min_density': min_density,
            'weight': weight,
            'weighted_value': optimal_rate * weight
        }

        print(f"✅ {period_name}: {optimal_rate:.3f}% (경쟁자 {min_density}명, 가중치 {weight:.0%})")

    # 가중 평균 계산
    weighted_sum = sum(r['weighted_value'] for r in results.values())
    total_weight = sum(r['weight'] for r in results.values())

    if total_weight > 0:
        final_rate = weighted_sum / total_weight
    else:
        final_rate = base_rate if base_rate is not None else 0.0

    # ±1% 범위 제한 (base_rate가 있을 경우만)
    if base_rate is not None:
        min_limit = base_rate - 1.0
        max_limit = base_rate + 1.0

        if final_rate < min_limit:
            final_rate = min_limit
            print(f"⚠️ 하한 제한 적용: {min_limit:.3f}%")
        elif final_rate > max_limit:
            final_rate = max_limit
            print(f"⚠️ 상한 제한 적용: {max_limit:.3f}%")

        range_limit = f"{min_limit:.3f}~{max_limit:.3f}%"
    else:
        range_limit = "제한 없음"

    # 트렌드 분석
    period_rates = [
        (periods[p][0], results[p]['optimal_rate'])
        for p in ['1개월', '3개월', '6개월', '1년']
        if p in results
    ]
    period_rates.sort(key=lambda x: x[0], reverse=True)  # 최신순

    if len(period_rates) >= 2:
        recent = period_rates[0][1]
        old = period_rates[-1][1]
        trend = recent - old
        trend_direction = "상승" if trend > 0.05 else "하락" if trend < -0.05 else "안정"
    else:
        trend = 0
        trend_direction = "데이터 부족"

    return {
        'period_results': results,
        'weighted_average': final_rate,
        'base_rate': base_rate,
        'range_limit': range_limit,
        'trend': trend,
        'trend_direction': trend_direction,
        'total_weight': total_weight
    }

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--data-file', required=True)
    parser.add_argument('--base-rate', type=float, required=False, default=None)
    parser.add_argument('--output', default='data분석/temporal_weighted_result.json')

    args = parser.parse_args()

    print("=" * 80)
    print("시간대별 가중 분석")
    print("=" * 80)

    # 데이터 로드
    df = pd.read_excel(args.data_file)
    print(f"데이터 로드: {len(df)}건")
    if args.base_rate:
        print(f"기준 입찰률: {args.base_rate:.3f}%")
    else:
        print("기준 입찰률: 독립 실행 (제한 없음)")
    print()

    # 분석 실행
    result = analyze_temporal_weighted(df, args.base_rate)

    # 결과 출력
    print()
    print("=" * 80)
    print("최종 결과")
    print("=" * 80)
    print(f"가중 평균: {result['weighted_average']:.3f}%")
    print(f"범위 제한: {result['range_limit']}")
    print(f"트렌드: {result['trend_direction']} ({result['trend']:+.3f}%)")
    print(f"총 가중치: {result['total_weight']:.0%}")
    print()

    # 입찰금액 계산 (임시, 실제로는 기초금액 필요)
    # print(f"💡 최종 추천 입찰률: {result['weighted_average']:.3f}%")

    # JSON 저장
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 결과 저장: {args.output}")
