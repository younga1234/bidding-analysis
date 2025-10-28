#!/usr/bin/env python3
"""
입찰 메타 인지 분석 - 메인 실행 스크립트

AI가 먼저 생각하고 검증하고 발견하는 단계
- 요인별 통계 검증
- 다중 전략 생성
- 능동적 패턴 발견
- 신뢰도 평가
"""

import argparse
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# 모듈 임포트
try:
    from modules.factor_validator import validate_factors
    from modules.strategy_generator import generate_strategies
    from modules.insight_finder import find_insights
    from modules.data_utils import filter_valid_range
    MODULE_AVAILABLE = True
except ImportError as e:
    MODULE_AVAILABLE = False
    print(f"⚠️ 모듈 로드 실패: {e}")


class MetaCognitionAnalyzer:
    """메타 인지 분석기"""

    def __init__(self,
                 data_file: str,
                 basic_result_file: Optional[str] = None,
                 advanced_result_file: Optional[str] = None,
                 context: Optional[Dict] = None):
        """
        초기화

        Args:
            data_file: 전처리된 데이터 파일
            basic_result_file: 기본 분석 결과 JSON
            advanced_result_file: 고급 분석 결과 JSON
            context: 현재 상황 (발주처, 월, 금액 등)
        """
        self.data_file = data_file
        self.basic_result_file = basic_result_file
        self.advanced_result_file = advanced_result_file
        self.context = context or {}

        self.df = None
        self.basic_result = None
        self.advanced_result = None
        self.meta_result = {
            "메타정보": {
                "분석시각": datetime.now().isoformat(),
                "데이터파일": data_file,
                "컨텍스트": self.context
            }
        }

    def load_data(self):
        """데이터 로드"""
        print(f"\n{'='*80}")
        print("메타 인지 분석 시작")
        print(f"{'='*80}")
        print(f"\n[데이터 로드] {self.data_file}")

        self.df = pd.read_excel(self.data_file)
        self.df = filter_valid_range(self.df)  # ✅ 필터링 추가
        print(f"  ✅ 데이터 로드 완료: {len(self.df):,}건")

        # 기본 분석 결과 로드
        if self.basic_result_file and Path(self.basic_result_file).exists():
            with open(self.basic_result_file, 'r', encoding='utf-8') as f:
                self.basic_result = json.load(f)
            print(f"  ✅ 기본 분석 결과 로드")

        # 고급 분석 결과 로드
        if self.advanced_result_file and Path(self.advanced_result_file).exists():
            with open(self.advanced_result_file, 'r', encoding='utf-8') as f:
                self.advanced_result = json.load(f)
            print(f"  ✅ 고급 분석 결과 로드")

    def run_factor_validation(self):
        """요인별 통계 검증"""
        print(f"\n{'='*80}")
        print("Step 1: 요인별 통계 검증")
        print(f"{'='*80}")

        try:
            validated_factors = validate_factors(self.df)
            self.meta_result["검증된_영향요인"] = validated_factors

            # 유의미한 요인 개수
            significant_count = sum(1 for f in validated_factors if f.get('유의미', False))
            print(f"\n  ✅ 검증 완료: 총 {len(validated_factors)}개 요인, {significant_count}개 유의미")

            return validated_factors

        except Exception as e:
            print(f"  ❌ 오류: {e}")
            return []

    def run_strategy_generation(self, validated_factors):
        """다중 전략 생성"""
        print(f"\n{'='*80}")
        print("Step 2: 다중 전략 생성")
        print(f"{'='*80}")

        # 기초금액, 발주처투찰률 추출
        base_amount = self.context.get('기초금액', self.df['기초금액'].median())
        agency_rate = self.context.get('발주처투찰률', 87.745)

        try:
            strategies = generate_strategies(
                df=self.df,
                base_amount=base_amount,
                agency_rate=agency_rate,
                basic_result=self.basic_result,
                validated_factors=validated_factors,
                context=self.context
            )
            self.meta_result["생성된_전략"] = strategies

            print(f"\n  ✅ 전략 생성 완료: {len(strategies)}개")

            return strategies

        except Exception as e:
            print(f"  ❌ 오류: {e}")
            return []

    def run_insight_discovery(self):
        """능동적 패턴 발견"""
        print(f"\n{'='*80}")
        print("Step 3: 능동적 패턴 발견")
        print(f"{'='*80}")

        try:
            insights = find_insights(self.df)
            self.meta_result["능동적_발견"] = insights

            print(f"\n  ✅ 패턴 발견 완료: {len(insights)}개")

            return insights

        except Exception as e:
            print(f"  ❌ 오류: {e}")
            return []

    def run_confidence_assessment(self, validated_factors, strategies):
        """신뢰도 평가"""
        print(f"\n{'='*80}")
        print("Step 4: 신뢰도 평가")
        print(f"{'='*80}")

        try:
            # 1. 데이터 충분성
            winners = self.df[self.df['순위'] == 1]
            data_sufficiency = min(len(winners) / 100, 1.0)  # 100건 이상이면 1.0

            # 2. 컨텍스트 매칭
            context_match = self._calculate_context_match()

            # 3. 시간적 유효성
            temporal_validity = self._calculate_temporal_validity()

            # 4. 이상치 여부
            is_outlier = self._check_outlier()

            # 전체 신뢰도 (가중 평균)
            overall_confidence = (
                data_sufficiency * 0.3 +
                context_match * 0.4 +
                temporal_validity * 0.3
            )

            # 이상치면 신뢰도 감소
            if is_outlier:
                overall_confidence *= 0.7

            # 평가
            if overall_confidence >= 0.7:
                assessment = "높음"
                recommendation = "과거 패턴을 높은 신뢰도로 참고 가능"
            elif overall_confidence >= 0.5:
                assessment = "보통"
                recommendation = "과거 패턴 참고 가능하나, 현재 상황 특성 고려 필요"
            else:
                assessment = "낮음"
                recommendation = "과거 데이터와 현재 상황이 다름, 신중한 판단 필요"

            confidence_result = {
                "전체_신뢰도": round(overall_confidence, 2),
                "평가": assessment,
                "근거": {
                    "데이터_충분성": round(data_sufficiency, 2),
                    "컨텍스트_매칭": round(context_match, 2),
                    "시간적_유효성": round(temporal_validity, 2),
                    "이상치_여부": is_outlier
                },
                "권장사항": recommendation
            }

            self.meta_result["신뢰도_평가"] = confidence_result

            print(f"  ✅ 신뢰도 평가: {overall_confidence:.2f} ({assessment})")
            print(f"     - 데이터 충분성: {data_sufficiency:.2f}")
            print(f"     - 컨텍스트 매칭: {context_match:.2f}")
            print(f"     - 시간적 유효성: {temporal_validity:.2f}")
            print(f"     - 이상치 여부: {is_outlier}")

            # 최종 추천
            self._generate_final_recommendation(strategies, confidence_result, validated_factors)

            return confidence_result

        except Exception as e:
            print(f"  ❌ 오류: {e}")
            return {}

    def _calculate_context_match(self) -> float:
        """컨텍스트 매칭 점수 계산"""
        if not self.context:
            return 0.5  # 컨텍스트 없으면 중간값

        match_score = 0.0
        factors = 0

        # 발주처 매칭
        if '발주처' in self.context and '발주처' in self.df.columns:
            current_agency = self.context['발주처']
            if current_agency in self.df['발주처'].values:
                agency_count = len(self.df[self.df['발주처'] == current_agency])
                match_score += min(agency_count / 50, 1.0)  # 50건 이상이면 1.0
            factors += 1

        # 금액 매칭 (평균과의 차이)
        if '기초금액' in self.context:
            current_amount = self.context['기초금액']
            avg_amount = self.df['기초금액'].mean()
            std_amount = self.df['기초금액'].std()

            # Z-score 계산
            z_score = abs(current_amount - avg_amount) / std_amount if std_amount > 0 else 0
            # Z-score가 클수록 매칭 낮음
            amount_match = max(1.0 - z_score / 3, 0.0)  # 3σ 이상이면 0
            match_score += amount_match
            factors += 1

        # 월 매칭
        if '월' in self.context and '월' in self.df.columns:
            current_month = self.context['월']
            if current_month in self.df['월'].values:
                month_count = len(self.df[self.df['월'] == current_month])
                match_score += min(month_count / 30, 1.0)  # 30건 이상이면 1.0
            factors += 1

        return match_score / factors if factors > 0 else 0.5

    def _calculate_temporal_validity(self) -> float:
        """시간적 유효성 계산"""
        if '입찰일시' not in self.df.columns:
            return 0.5

        try:
            self.df['입찰일시_parsed'] = pd.to_datetime(self.df['입찰일시'], errors='coerce')
            valid_df = self.df.dropna(subset=['입찰일시_parsed'])

            if len(valid_df) == 0:
                return 0.5

            # 최근 6개월 데이터 비중
            six_months_ago = datetime.now() - pd.Timedelta(days=180)
            recent_count = len(valid_df[valid_df['입찰일시_parsed'] >= six_months_ago])
            total_count = len(valid_df)

            return recent_count / total_count

        except:
            return 0.5

    def _check_outlier(self) -> bool:
        """현재 상황이 이상치인지 확인"""
        if '기초금액' not in self.context:
            return False

        current_amount = self.context['기초금액']
        mean_amount = self.df['기초금액'].mean()
        std_amount = self.df['기초금액'].std()

        if std_amount == 0:
            return False

        z_score = abs(current_amount - mean_amount) / std_amount

        # Z-score > 3이면 이상치
        return z_score > 3

    def _generate_final_recommendation(self, strategies, confidence, validated_factors):
        """최종 추천 생성"""
        if not strategies:
            return

        # 신뢰도에 따라 전략 선택
        if confidence['전체_신뢰도'] >= 0.7:
            # 높은 신뢰도: 맞춤 전략 우선, 없으면 균형
            recommended = next((s for s in strategies if s['전략명'] == '상황맞춤'), None)
            if not recommended:
                recommended = next((s for s in strategies if s['전략명'] == '균형'), strategies[0])
            reason = "높은 신뢰도, 맞춤 전략 추천"

        elif confidence['전체_신뢰도'] >= 0.5:
            # 중간 신뢰도: 균형 전략
            recommended = next((s for s in strategies if s['전략명'] == '균형'), strategies[0])
            reason = "중간 신뢰도, 균형 전략 추천"

        else:
            # 낮은 신뢰도: 보수적 전략
            recommended = next((s for s in strategies if s['전략명'] == '보수적'), strategies[0])
            reason = "낮은 신뢰도, 보수적 전략 추천"

        # 유의미한 요인 반영 여부
        significant_factors = [f['요인'] for f in validated_factors if f.get('유의미', False)]
        if significant_factors:
            reason += f" (반영 요인: {', '.join(significant_factors)})"

        self.meta_result["최종_추천"] = {
            "전략": recommended['전략명'],
            "입찰률": recommended['입찰률'],
            "입찰금액": recommended['입찰금액'],
            "신뢰도": confidence['전체_신뢰도'],
            "이유": reason
        }

    def _convert_to_python_types(self, obj):
        """numpy 타입을 Python 네이티브 타입으로 변환"""
        if isinstance(obj, dict):
            return {key: self._convert_to_python_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_python_types(item) for item in obj]
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj

    def save_results(self):
        """결과 저장"""
        # 투찰률 추출 (파일명에서)
        filename = Path(self.data_file).stem
        if '_' in filename:
            rate_part = filename.split('_')[1]  # "87"
            rate_int = int(rate_part.replace('%', ''))
        else:
            rate_int = 87745

        output_file = f"/mnt/a/25/data분석/meta_analysis_{rate_int}.json"
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # numpy 타입 변환
        converted_result = self._convert_to_python_types(self.meta_result)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(converted_result, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*80}")
        print("메타 분석 완료!")
        print(f"{'='*80}")
        print(f"결과 파일: {output_file}")

        # 요약 출력
        if "최종_추천" in self.meta_result:
            rec = self.meta_result["최종_추천"]
            print(f"\n📊 최종 추천:")
            print(f"   전략: {rec['전략']}")
            print(f"   입찰률: {rec['입찰률']}%")
            print(f"   입찰금액: {rec['입찰금액']:,}원")
            print(f"   신뢰도: {rec['신뢰도']}")
            print(f"   이유: {rec['이유']}")

        return output_file

    def run_full_analysis(self):
        """전체 분석 실행"""
        # 데이터 로드
        self.load_data()

        # Step 1: 요인 검증
        validated_factors = self.run_factor_validation()

        # Step 2: 전략 생성
        strategies = self.run_strategy_generation(validated_factors)

        # Step 3: 인사이트 발견
        insights = self.run_insight_discovery()

        # Step 4: 신뢰도 평가
        confidence = self.run_confidence_assessment(validated_factors, strategies)

        # 결과 저장
        output_file = self.save_results()

        return self.meta_result


def main():
    """CLI 진입점"""
    parser = argparse.ArgumentParser(
        description='입찰 메타 인지 분석 - AI가 먼저 생각하고 검증하고 발견'
    )
    parser.add_argument(
        '--data-file',
        type=str,
        required=True,
        help='전처리된 데이터 파일 경로'
    )
    parser.add_argument(
        '--basic-result',
        type=str,
        help='기본 분석 결과 JSON 파일'
    )
    parser.add_argument(
        '--advanced-result',
        type=str,
        help='고급 분석 결과 JSON 파일'
    )
    parser.add_argument(
        '--context',
        type=str,
        help='현재 상황 (JSON 문자열, 예: \'{"발주처": "국가유산청", "월": 12}\')'
    )

    args = parser.parse_args()

    # 컨텍스트 파싱
    context = None
    if args.context:
        try:
            context = json.loads(args.context)
        except:
            print(f"⚠️ 컨텍스트 파싱 실패: {args.context}")

    # 분석기 생성 및 실행
    analyzer = MetaCognitionAnalyzer(
        data_file=args.data_file,
        basic_result_file=args.basic_result,
        advanced_result_file=args.advanced_result,
        context=context
    )

    analyzer.run_full_analysis()


if __name__ == '__main__':
    main()
