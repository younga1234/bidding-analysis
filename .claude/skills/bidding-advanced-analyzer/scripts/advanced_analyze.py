#!/usr/bin/env python3
"""
고급 입찰 분석 - 메인 실행 스크립트

10가지 고급 분석 모듈 통합 실행:
- Phase 1: 시간대별, 발주처별, 2D 상관관계
- Phase 2: 업체 패턴, 심리적 앵커, 계절성
- Phase 3: 순위 간격, 클러스터, 금액 구간, 몬테카를로
"""

import argparse
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Phase 1 모듈 (우선 구현)
try:
    from modules.temporal_analysis import analyze_temporal_patterns, visualize_temporal_heatmap
    from modules.agency_analysis import analyze_agency_patterns, visualize_agency_comparison
    from modules.correlation_2d import analyze_2d_correlation, visualize_2d_heatmap
    PHASE1_AVAILABLE = True
except ImportError as e:
    PHASE1_AVAILABLE = False
    print(f"⚠️ Phase 1 모듈 로드 실패: {e}")

# Phase 2 모듈 (차기 구현)
try:
    from modules.company_patterns import analyze_company_patterns
    from modules.psychological import analyze_psychological_anchors
    from modules.seasonality import analyze_seasonality
    PHASE2_AVAILABLE = True
except ImportError:
    PHASE2_AVAILABLE = False

# Phase 3 모듈 (장기 구현)
try:
    from modules.rank_gap import analyze_rank_gaps
    from modules.cluster_detect import detect_clusters
    from modules.amount_range import analyze_amount_ranges
    from modules.monte_carlo_plus import run_advanced_monte_carlo
    PHASE3_AVAILABLE = True
except ImportError:
    PHASE3_AVAILABLE = False


class AdvancedBiddingAnalyzer:
    """고급 입찰 분석기"""

    def __init__(self, data_file, agency_rate, modules=None):
        """
        초기화

        Args:
            data_file (str): 전처리된 데이터 파일 경로
            agency_rate (float): 발주처투찰률 (예: 82.995)
            modules (list): 실행할 모듈 리스트 (None = 모두 실행)
        """
        self.data_file = data_file
        self.agency_rate = agency_rate
        self.modules = modules or ['all']
        self.df = None
        self.results = {
            "메타정보": {
                "분석시각": datetime.now().isoformat(),
                "데이터파일": data_file,
                "발주처투찰률": agency_rate,
                "실행모듈": self.modules
            }
        }

    def load_data(self):
        """데이터 로드"""
        print(f"\n{'='*80}")
        print("고급 입찰 분석 시작")
        print(f"{'='*80}")
        print(f"\n[데이터 로드] {self.data_file}")

        self.df = pd.read_excel(self.data_file)
        print(f"  ✅ 데이터 로드 완료: {len(self.df):,}건")

        # 필수 컬럼 확인
        required_cols = ['기초대비사정률', '기초대비투찰률', '순위']
        missing = [col for col in required_cols if col not in self.df.columns]
        if missing:
            raise ValueError(f"필수 컬럼 누락: {missing}")

        return self.df

    def run_phase1(self):
        """Phase 1: 핵심 분석 (시간대별, 발주처별, 2D)"""
        if not PHASE1_AVAILABLE:
            print("\n⚠️ Phase 1 모듈 미설치 - 건너뜀")
            return

        print(f"\n{'='*80}")
        print("Phase 1: 핵심 분석")
        print(f"{'='*80}")

        # 1. 시간대별 패턴
        if 'all' in self.modules or 'temporal' in self.modules:
            print("\n[1/3] 시간대별 패턴 분석...")
            try:
                temporal_result = analyze_temporal_patterns(
                    df=self.df,
                    recent_months=3,
                    weight_recent=0.7
                )
                self.results["시간대별_패턴"] = temporal_result

                # 시각화
                viz_path = f"/mnt/a/25/data분석/temporal_heatmap_{int(self.agency_rate*1000)}.png"
                visualize_temporal_heatmap(self.df, viz_path, recent_months=3)

                print("  ✅ 완료")
            except Exception as e:
                print(f"  ❌ 오류: {e}")

        # 2. 발주처별 특성
        if 'all' in self.modules or 'agency' in self.modules:
            print("\n[2/3] 발주처별 특성 분석...")
            try:
                agency_result = analyze_agency_patterns(df=self.df)
                self.results["발주처별_특성"] = agency_result

                # 시각화
                viz_path = f"/mnt/a/25/data분석/agency_comparison_{int(self.agency_rate*1000)}.png"
                visualize_agency_comparison(self.df, viz_path)

                print("  ✅ 완료")
            except Exception as e:
                print(f"  ❌ 오류: {e}")

        # 3. 2D 상관관계
        if 'all' in self.modules or '2d' in self.modules:
            print("\n[3/3] 2D 상관관계 분석...")
            try:
                correlation_result = analyze_2d_correlation(df=self.df)
                self.results["2D_상관관계"] = correlation_result

                # 시각화
                viz_path = f"/mnt/a/25/data분석/2d_correlation_{int(self.agency_rate*1000)}.png"
                visualize_2d_heatmap(self.df, viz_path)

                print("  ✅ 완료")
            except Exception as e:
                print(f"  ❌ 오류: {e}")

    def run_phase2(self):
        """Phase 2: 전략 고도화"""
        if not PHASE2_AVAILABLE:
            print("\n⚠️ Phase 2 모듈 미구현 - 건너뜀")
            return

        print(f"\n{'='*80}")
        print("Phase 2: 전략 고도화")
        print(f"{'='*80}")
        print("  (업체 패턴, 심리적 앵커, 계절성)")
        print("  ⚠️ 추후 구현 예정")

    def run_phase3(self):
        """Phase 3: 고급 분석"""
        if not PHASE3_AVAILABLE:
            print("\n⚠️ Phase 3 모듈 미구현 - 건너뜀")
            return

        print(f"\n{'='*80}")
        print("Phase 3: 고급 분석")
        print(f"{'='*80}")
        print("  (순위 간격, 클러스터, 금액 구간, 몬테카를로)")
        print("  ⚠️ 추후 구현 예정")

    def save_results(self):
        """결과 저장"""
        output_file = f"/mnt/a/25/data분석/bidding_analysis_advanced_{int(self.agency_rate*1000)}.json"
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*80}")
        print("분석 완료!")
        print(f"{'='*80}")
        print(f"결과 파일: {output_file}")
        print(f"총 {len(self.results)-1}개 분석 수행")

        return output_file

    def run_full_analysis(self):
        """전체 분석 실행"""
        # 데이터 로드
        self.load_data()

        # Phase별 실행
        self.run_phase1()
        self.run_phase2()
        self.run_phase3()

        # 결과 저장
        output_file = self.save_results()

        return self.results


def main():
    """CLI 진입점"""
    parser = argparse.ArgumentParser(
        description='고급 입찰 분석 - 10가지 심층 분석'
    )
    parser.add_argument(
        '--data-file',
        type=str,
        required=True,
        help='전처리된 데이터 파일 경로'
    )
    parser.add_argument(
        '--agency-rate',
        type=float,
        required=True,
        help='발주처투찰률 (예: 82.995)'
    )
    parser.add_argument(
        '--modules',
        type=str,
        default='all',
        help='실행할 모듈 (쉼표 구분, 예: temporal,agency,2d)'
    )

    args = parser.parse_args()

    # 모듈 리스트 파싱
    if args.modules == 'all':
        modules = ['all']
    else:
        modules = [m.strip() for m in args.modules.split(',')]

    # 분석기 생성 및 실행
    analyzer = AdvancedBiddingAnalyzer(
        data_file=args.data_file,
        agency_rate=args.agency_rate,
        modules=modules
    )

    analyzer.run_full_analysis()


if __name__ == '__main__':
    main()
