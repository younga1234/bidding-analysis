---
name: bidding-advanced-analyzer
description: 고급 입찰 분석 실행 (Phase 1: 시간대별, 발주처별, 2D 상관관계). bidding_context.json → advanced_analyze.py → JSON 결과 + PNG 시각화 3개 생성. Use when 고급 분석, 다차원 분석, 시각화 생성, skill 체인 자동 실행
allowed-tools: Bash, Read
---

# 고급 입찰 분석 스킬 (Bidding Advanced Analyzer)

## ⚡ 실행 로직 (이 skill이 트리거되면 자동 실행)

**이 skill이 호출되면 아래 명령을 자동으로 실행하세요:**

### Step 1: bidding_context.json 읽기

```bash
# 작업 디렉토리로 이동
cd /mnt/a/25

# bidding_context.json에서 정보 추출
AGENCY_RATE=$(jq -r '.발주처투찰률' data분석/bidding_context.json)

# 파일명용 변환 (87.745 → 87_745)
AGENCY_RATE_FILE=${AGENCY_RATE//./_}

echo "✅ 정보 읽기 완료:"
echo "  - 발주처투찰률: ${AGENCY_RATE}%"
```

### Step 2: 전처리 파일 경로 생성

```bash
DATA_FILE="data전처리완료/투찰률_${AGENCY_RATE_FILE}%_데이터.xlsx"

# 파일 존재 확인
if [ ! -f "$DATA_FILE" ]; then
  echo "❌ 오류: 전처리 파일이 없습니다: $DATA_FILE"
  exit 1
fi

echo "✅ 전처리 파일 확인: $DATA_FILE"
```

### Step 3: advanced_analyze.py 자동 실행

```bash
# venv 활성화
source venv/bin/activate

# advanced_analyze.py 실행 (Phase 1 모듈)
echo "🔄 고급 입찰 분석 시작..."

python .claude/skills/bidding-advanced-analyzer/advanced_analyze.py \
  --data-file "$DATA_FILE" \
  --agency-rate $AGENCY_RATE \
  --modules temporal,agency,2d

# 실행 결과 확인
if [ $? -eq 0 ]; then
  echo "✅ 고급 입찰 분석 완료"
  echo "📄 결과: data분석/bidding_analysis_advanced_${AGENCY_RATE_FILE}.json"
  echo "📊 시각화: data분석/*_${AGENCY_RATE_FILE}.png"
else
  echo "❌ 오류: advanced_analyze.py 실행 실패"
  exit 1
fi
```

### Step 4: 완료

```
- 결과 파일: data분석/bidding_analysis_advanced_{투찰률}.json 생성됨
- 시각화 파일: PNG 파일 3개 생성됨
- 다음 skill로 자동 진행 (bidding-master-pipeline이 관리)
```

═══

# 고급 입찰 분석 스킬 (Bidding Advanced Analyzer)

## 🎯 목적

기존 `logic` 스킬의 기본 분석을 보완하여 **1위 확률을 1~2% 추가 개선**하는 고급 분석 수행.

**핵심 철학**: "단일 차원 → 다차원 분석"으로 진화
- 시간 차원 (최근 트렌드 가중)
- 발주처 차원 (발주처별 특성)
- 2D 공간 (사정률 × 투찰률 조합)
- 업체 패턴 (반복 행동)
- 심리적 요인 (앵커 포인트)

═══

## 📊 10가지 분석 모듈

### Phase 1: 핵심 분석 (우선 구현 ⭐⭐⭐⭐⭐)

#### 1. 시간대별 패턴 분석 (`temporal_analysis.py`)
**문제**: 2023년 데이터와 2025년 데이터의 패턴이 다를 수 있음 (AI 도구 확산)

**분석 내용**:
- 데이터를 3개월/6개월/12개월 단위로 분리
- 최근 3개월 데이터 70%, 과거 데이터 30% 가중치
- 시간에 따른 경쟁 밀도 변화 추적
- 트렌드 감지 (특정 구간의 밀도 증가/감소)

**출력**:
```json
{
  "temporal_weights": {
    "recent_3m": 0.7,
    "past_9m": 0.3
  },
  "trend": "구간별 경쟁 밀도 추세 (데이터 기반)",
  "adjusted_optimal": "시간 가중 적용된 최적 구간"
}
```

═══

#### 2. 발주처별 특성 분석 (`agency_analysis.py`)
**문제**: 발주처마다 다른 발주처투찰률과 경쟁 환경

**분석 내용**:
- 데이터에서 발주처 추출 (공고번호 패턴 or 별도 컬럼)
- 발주처별 경쟁 밀도 히트맵 생성
- 발주처별 과거 1위 분포
- 발주처별 최적 입찰률

**출력**:
```json
{
  "agency_specific": {
    "발주처명": {
      "optimal_rate": "데이터 기반 계산값",
      "competition_density": "실제 경쟁자 수",
      "past_winners_median": "실제 1위 중앙값"
    }
  }
}
```

═══

#### 3. 2D 상관관계 분석 (`correlation_2d.py`)
**문제**: 사정률과 투찰률을 독립적으로 보면 숨겨진 패턴을 놓침

**분석 내용**:
- X축: 기초대비사정률 (98-102%)
- Y축: 기초대비투찰률 (86-90%)
- 2D 히트맵 생성 (각 셀의 경쟁자 수)
- 상관계수 계산 (Pearson, Spearman)
- 저밀도 2D 셀 추출

**출력**:
```json
{
  "correlation_coefficient": "실제 상관계수",
  "low_density_zones": "데이터 기반 저경쟁 구간",
  "visualization": "2d_correlation.png"
}
```

═══

### Phase 2: 전략 고도화 (차기 구현 ⭐⭐⭐⭐)

#### 4. 업체별 반복 패턴 (`company_patterns.py`)
- 특정 업체가 항상 비슷한 전략을 쓰는지 분석
- 표준편차 < 0.1% = 패턴 업체
- 예측 가능한 경쟁자 회피

#### 5. 심리적 앵커 포인트 (`psychological.py`)
- 과거 1위 중앙값 ± 0.05% 구간 회피
- 반복 숫자 회피 (777, 888, 000)
- "예쁜 숫자" 위험도 평가

#### 6. 계절성/월별 패턴 (`seasonality.py`)
- 12월(연말) vs 1월(연초) 경쟁 강도 비교
- 휴일 전후 패턴 분석
- 월별 최적 전략

═══

### Phase 3: 고급 분석 (장기 프로젝트 ⭐⭐⭐)

#### 7. 순위 간격 분석 (`rank_gap.py`)
- 1위-2위 간격 분포 분석
- 최소 안전 간격 계산
- 동률 회피 전략

#### 8. 담합/클러스터 탐지 (`cluster_detect.py`)
- DBSCAN 클러스터링
- 0.01% 범위 내 3개 이상 = 의심
- 비정상 밀집 구간 회피

#### 9. 기초금액 구간별 분석 (`amount_range.py`)
- 4구간 분리 (< 5천, 5천-1억, 1-3억, 3억+)
- 규모별 경쟁 특성
- 대형/소형 프로젝트 전략 차별화

#### 10. 고급 몬테카를로 시뮬레이션 (`monte_carlo_plus.py`)
- 예정가 형성 + 경쟁자 시뮬레이션
- 80개 업체의 입찰률 랜덤 생성 (과거 분포 기반)
- 10,000회 동적 시뮬레이션
- 진짜 1위 확률 계산

═══

## 🚀 사용법

### 자동 실행 (마스터 파이프라인 통합)

```python
# 사용자 명령: "낙찰분석"

[bidding-master-pipeline]
  ↓
[logic] → 기본 분석
  ↓
[bidding-advanced-analyzer] → 고급 분석 (자동)
  ↓
[report] → 통합 보고서
```

### 수동 실행

```bash
source /mnt/a/25/venv/bin/activate
python3 /mnt/a/25/.claude/skills/bidding-advanced-analyzer/advanced_analyze.py \
  --data-file "/mnt/a/25/data전처리완료/투찰률_{공고의_투찰률}%_데이터.xlsx" \
  --agency-rate {공고의_투찰률} \
  --modules temporal,agency,2d  # 선택적 모듈 지정
```

### 모듈별 실행

```python
from modules.temporal_analysis import analyze_temporal_patterns

result = analyze_temporal_patterns(
    df=df,
    recent_months=3,
    weight_recent=0.7
)
```

═══

## 📁 출력 파일

### JSON 결과
```
/mnt/a/25/data분석/bidding_analysis_advanced_{투찰률}.json
```

### 시각화 파일
```
/mnt/a/25/data분석/temporal_heatmap_{투찰률}.png     # 시간대별 히트맵
/mnt/a/25/data분석/2d_correlation_{투찰률}.png       # 2D 상관관계
/mnt/a/25/data분석/agency_comparison_{투찰률}.png    # 발주처 비교
```

═══

## 🔧 기술 스택

- **Python 3.8+**
- **pandas**: 데이터 처리
- **numpy**: 수치 계산
- **matplotlib/seaborn**: 시각화
- **scikit-learn**: 클러스터링, 상관분석
- **scipy**: 통계 분석

═══

## 📊 분석 모듈 우선순위

| 모듈 | 우선순위 | 비고 |
|------|---------|------|
| 시간대별 패턴 | ⭐⭐⭐⭐⭐ | 최신 트렌드 반영 |
| 발주처별 특성 | ⭐⭐⭐⭐⭐ | 발주처 맞춤 전략 |
| 2D 상관관계 | ⭐⭐⭐⭐⭐ | 다차원 저경쟁 구간 발견 |
| 업체별 패턴 | ⭐⭐⭐⭐ | 패턴 업체 회피 |
| 심리적 앵커 | ⭐⭐⭐⭐ | 심리적 숫자 회피 |
| 계절성 | ⭐⭐⭐ | 월별 특성 |
| 순위 간격 | ⭐⭐⭐ | 안전 간격 |
| 클러스터 탐지 | ⭐⭐ | 비정상 밀집 |
| 기초금액 구간 | ⭐⭐ | 규모별 차별화 |
| 고급 몬테카를로 | ⭐⭐⭐⭐ | 동적 시뮬레이션 |

═══

## ⚠️ 현실적 한계

**솔직한 평가**:
```
현재 1위 확률: 공고마다 다름 (데이터 분석 후 계산)
고급 분석 적용: 기본 대비 +1~2% 개선
실제 입찰 현실: 다수 업체가 좁은 구간에 몰림 → 작은 차이로 결정

→ 복수예가입찰 = 전략 + 운의 조합
→ 고급 분석은 확률 개선, 보장 불가
```

**고급 분석의 진짜 가치**:
- "최악의 선택" 회피 → 1위 확률 +1~2%
- "상대적으로 나은 선택" 제시
- 메타 게임 대응 (모두가 아는 최적점 피하기)
- 발주처별 특화 전략

═══

## 🔗 관련 스킬

- `logic`: 기본 분석 (9단계, 경쟁 밀도, 몬테카를로)
- `data-preprocessing`: 데이터 전처리
- `report`: 보고서 생성
- `core`: 용어 정의 및 철학

═══

## 📝 업데이트 로그

- **2025-10-27**: 스킬 생성, Phase 1 모듈 3개 구현 계획
- **Phase 1 완료 예정**: 시간대별, 발주처별, 2D 상관관계
- **Phase 2 예정**: 업체 패턴, 심리적 앵커, 계절성
- **Phase 3 예정**: 순위 간격, 클러스터, 금액 구간, 몬테카를로

═══

## 💡 개발 원칙

1. **모듈화**: 각 분석은 독립적으로 실행 가능
2. **한국어 우선**: 모든 출력, 주석, 로그는 한국어
3. **데이터 기반**: 가설이 아닌 실제 데이터 패턴
4. **점진적 개선**: Phase별로 단계적 구현
5. **현실 인정**: AI의 한계를 명확히 문서화

═══

**Last Updated**: 2025-10-27
**Status**: Phase 1 구현 시작
