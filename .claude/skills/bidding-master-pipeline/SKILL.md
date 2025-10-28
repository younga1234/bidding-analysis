---
name: bidding-master-pipeline
description: "낙찰가분석 전체 파이프라인 자동 실행 (v3.2). 이미지 분석 -> bidding_context.json 생성 -> 3개 skill 병렬 트리거 (logic, bidding-meta-cognition, bidding-advanced-analyzer) -> 3가지 결과 제시. Use when 낙찰가분석, 전체 분석, 파이프라인 실행"
allowed-tools: Read, Write, Bash, Glob, Skill
---

# Bidding Master Pipeline v3.2

## 🎯 목적

**"낙찰가분석"** 한마디로 이미지 분석부터 3가지 분석 결과까지 완전 자동 실행

```
입력: /mnt/a/25/data분석/ (이미지 파일 1개)
     ↓
[자동 실행: 이미지 분석 → 종합 분석 → 시간대별 가중 분석 → 고급 분석]
     ↓
출력: 3가지 분석 결과
      [분석 1] logic 종합 분석
      [분석 2] 시간대별 가중 분석
      [분석 3] 고급 분석 (10가지 심층 분석)
```

## 🔑 핵심 변경사항 (v3.2 ⭐⭐⭐)

### ⭐ 3가지 분석 실행
- **Stage 3**: logic 종합 분석 (COMPREHENSIVE)
- **Stage 4**: 시간대별 가중 분석
- **Stage 5**: 고급 분석 (10가지 심층 분석) ⭐ NEW!
- **결과**: 3가지 분석 결과 제시

### ⭐ logic 종합 분석 (Stage 3)
**모든 요소 통합:**
- 예정가 형성 확률 (몬테카를로)
- 시간 가중 경쟁 밀도
- 상대적 몰림도
- 실제 1위 확률
- 종합 점수 계산

### ⭐ 시간대별 가중 분석 (Stage 4)
**시간 가중치 적용:**
- 1개월: 40%
- 3개월: 30%
- 6개월: 20%
- 1년: 10%
- 가중 평균 계산
- 트렌드 분석

### ⭐ 고급 분석 (Stage 5) ⭐ NEW!
**10가지 심층 분석:**
- Phase 1 (우선): 시간대별 패턴, 발주처별 특성, 2D 상관관계
- Phase 2 (차기): 업체별 패턴, 심리적 앵커, 계절성
- Phase 3 (장기): 순위 간격, 클러스터 탐지, 금액 구간, 고급 몬테카를로
- 시각화 파일 생성 (히트맵, 비교 차트)

═══

## 🔑 트리거 키워드

- **"낙찰가분석"** ⭐ (PRIMARY)
- "낙찰가 분석"
- "입찰 분석"

═══

## 🚀 자동 실행 (Skill Chain)

**이 skill이 호출되면 다음을 순차 트리거:**

1. **Stage 0: 이미지 분석** (이 skill에서 직접 실행)
   - 이미지 파일 감지
   - 공고 정보 추출 (공고번호, 기초금액, 투찰률, 발주처)
   - bidding_context.json 생성

2. **Stage 1: 전처리 파일 확인** (이 skill에서 직접 실행)
   - 전처리 파일 존재 확인
   - 없으면 → data-preprocessing skill 트리거
   - 있으면 → Stage 2 스킵

3. **Stage 2: 분석 트리거** (이 skill에서 직접 실행)
   - logic skill 트리거 (종합 분석)
   - bidding-meta-cognition skill 트리거 (시간대별)
   - bidding-advanced-analyzer skill 트리거 (고급 분석)
   - 3개 skill 병렬 실행

4. **완료!**
   - 각 skill이 자동으로 결과 저장
   - 최종 결과 제시

**중요: Skill 도구로 자동 트리거!**

═══

## ⚡ 실행 로직 (이 섹션을 따라 자동 실행)

**이 skill이 호출되면 아래 단계를 순서대로 실행하세요:**

### Step 1: 이미지 분석 (이 skill에서 직접 실행)

```
1. Glob 도구로 data분석/*.png 파일 찾기
2. Read 도구로 이미지 읽기
3. 이미지에서 추출:
   - 공고번호
   - 기초금액
   - 투찰률 (발주처투찰률)
   - 발주기관 (발주처)
4. Bash 도구로 bidding_context.json 생성
```

### Step 2: 전처리 파일 확인 (이 skill에서 직접 실행)

```bash
AGENCY_RATE=$(jq -r '.발주처투찰률' data분석/bidding_context.json)
AGENCY_RATE_FILE=${AGENCY_RATE//./_}

# 전처리 파일 확인
if [ -f "data전처리완료/투찰률_${AGENCY_RATE_FILE}%_데이터.xlsx" ]; then
  echo "✅ 전처리 파일 존재 - Stage 2 스킵"
else
  echo "⚠️ 전처리 파일 없음 - data-preprocessing skill 트리거 필요"
  # data-preprocessing skill 트리거는 현재 미구현 (전처리는 수동)
fi
```

### Step 3: 분석 Skills 트리거 (병렬 실행)

**⭐ Skill 도구를 사용하여 3개 skill을 병렬로 트리거:**

**실행 방법:**
- 단일 응답 메시지에서 3개의 Skill 도구를 동시에 호출
- 각 skill은 독립적으로 bidding_context.json을 읽어 자동 실행
- 각 skill이 자체 실행 로직에 따라 분석 수행

**Skill 호출 (이 skill이 트리거되면 아래 3개 skill을 호출하세요):**

1. `Skill("logic")`
   → logic/SKILL.md의 "⚡ 실행 로직" 섹션 자동 실행
   → 결과: data분석/bidding_analysis_comprehensive_{투찰률}.json

2. `Skill("bidding-meta-cognition")`
   → bidding-meta-cognition/SKILL.md의 "⚡ 실행 로직" 섹션 자동 실행
   → 결과: data분석/temporal_weighted_{투찰률}.json

3. `Skill("bidding-advanced-analyzer")`
   → bidding-advanced-analyzer/SKILL.md의 "⚡ 실행 로직" 섹션 자동 실행
   → 결과: data분석/bidding_analysis_advanced_{투찰률}.json + PNG 파일들

**중요:**
- 3개 Skill을 한 번에 호출 (병렬 실행)
- 각 skill은 bidding_context.json을 독립적으로 읽음
- 각 skill의 SKILL.md에 정의된 실행 로직이 자동으로 실행됨

### Step 4: 결과 확인 및 제시

```
생성된 파일 확인:
- data분석/bidding_analysis_comprehensive_{투찰률}.json
- data분석/temporal_weighted_{투찰률}.json
- data분석/bidding_analysis_advanced_{투찰률}.json
- data분석/*.png (시각화 파일들)

사용자에게 3가지 분석 결과 요약 제시
```

═══

## 📋 전체 실행 단계 (v3.0)

### Stage 0: 이미지 감지 및 정보 추출 ⭐

**목적:** 이미지에서 입찰 정보 추출

**입력:** `/mnt/a/25/data분석/*.png`

**처리:**
1. Glob으로 이미지 파일 감지
2. Read로 이미지 읽기 (Claude Vision)
3. 정보 추출:
   - **공고번호**: {공고 이미지에서 추출}
   - **기초금액**: {공고 이미지에서 추출}
   - **투찰률** (이미지 필드 "투찰률" = 시스템 "발주처투찰률"): {공고 이미지에서 추출}
   - **발주기관** (이미지 필드 "발주기관" → 시스템 "발주처"로 저장): {공고 이미지에서 추출}

**출력 형식:**
```json
{
  "공고번호": "{공고에서 추출}",
  "기초금액": {공고에서 추출},
  "발주처투찰률": {공고에서 추출},
  "발주처": "{공고에서 추출}"
}
```
→ `data분석/bidding_context.json` 저장

**조건 분기:**
```
IF 이미지 없음:
  → 사용자에게 이미지 업로드 요청 후 종료
ELSE:
  → Stage 1로 이동
```

═══

### Stage 1: 전처리 파일 확인

**목적:** 해당 발주처투찰률 그룹 데이터 확인

**확인 대상:**
```bash
# 발주처투찰률은 공고 이미지에서 추출된 값 사용
/mnt/a/25/data전처리완료/투찰률_{공고의_투찰률}%_데이터.xlsx
```

**조건 분기:**
```
IF 파일 존재:
  → Stage 2 스킵
  → Stage 3로 바로 이동 ✅
ELSE:
  → Stage 2 실행 (데이터 준비)
```

═══

### Stage 2: 데이터 준비 (조건부 실행)

**⚠️ Stage 1에서 전처리 파일이 없을 때만 실행**

**처리:**
1. Excel 파일 생성
2. 참여업체 목록 확인
3. 데이터 전처리 실행

**출력:** `data전처리완료/투찰률_{공고의_투찰률}%_데이터.xlsx`

═══

### Stage 3: 종합 분석 (COMPREHENSIVE) ⭐

**실행 스킬:** `.claude/skills/logic/analyze.py`

**실행 명령:**
```bash
cd /mnt/a/25
source venv/bin/activate

AGENCY_RATE=$(jq -r '.발주처투찰률' data분석/bidding_context.json)
BASE_AMOUNT=$(jq -r '.기초금액' data분석/bidding_context.json)
AGENCY_RATE_FILE=${AGENCY_RATE//./_}

python .claude/skills/logic/analyze.py \
  --base-amount $BASE_AMOUNT \
  --agency-rate $AGENCY_RATE \
  --data-file "data전처리완료/투찰률_${AGENCY_RATE_FILE}%_데이터.xlsx"
```

**예시:** (값은 공고마다 다름)
```bash
python .claude/skills/logic/analyze.py \
  --base-amount {공고의_기초금액} \
  --agency-rate {공고의_투찰률} \
  --data-file "data전처리완료/투찰률_{공고의_투찰률}%_데이터.xlsx"
```

**종합 분석 내용:**
1. [1/5] 몬테카를로 시뮬레이션 (예정가 형성 확률)
2. [2/5] 전체 경쟁 밀도 분석 (0.001% 단위, 1,755개 구간)
3. [3/5] 평균 경쟁 밀도 계산 (상대적 몰림도 기준)
4. [4/5] 각 구간별 종합 분석 (4가지 요소 통합)
5. [5/5] 종합 점수 정렬 (Top 10 추출)

**종합 점수 공식:**
```
점수 = 예정가형성확률 × 실제1위확률 × (1/시간가중밀도) × (1/상대적몰림)
```

**출력:**
```
data분석/bidding_analysis_comprehensive_{공고의_투찰률}.json
```

**결과 형식:** (실제 값은 공고 분석 후 계산됨)
```
1. 기초대비투찰률: {분석 결과}%
   기초대비사정률: {분석 결과}%
   입찰금액: {분석 결과}원
   실제 1위 확률: {분석 결과}% (n명 / m명)
   예정가 형성 확률: {분석 결과}%
   시간 가중 밀도: {분석 결과}명
   상대적 몰림: {분석 결과}배
   종합 점수: {분석 결과}
```

═══

### Stage 4: 시간대별 가중 분석 ⭐ NEW!

**실행 스킬:** `.claude/skills/bidding-meta-cognition/temporal_weighted_analysis.py`

**목적:** logic 분석 결과를 시간대별 가중치로 보정

**실행 명령:**
```bash
cd /mnt/a/25
source venv/bin/activate

AGENCY_RATE=$(jq -r '.발주처투찰률' data분석/bidding_context.json)
AGENCY_RATE_FILE=${AGENCY_RATE//./_}
BASE_RATE=$(jq -r '.최종_추천.bin_mid' data분석/bidding_analysis_comprehensive_${AGENCY_RATE_FILE}.json)

python .claude/skills/bidding-meta-cognition/temporal_weighted_analysis.py \
  --data-file "data전처리완료/투찰률_${AGENCY_RATE_FILE}%_데이터.xlsx" \
  --base-rate $BASE_RATE \
  --output "data분석/temporal_weighted_${AGENCY_RATE_FILE}.json"
```

**예시:** (값은 공고 분석 결과에 따라 다름)
```bash
python .claude/skills/bidding-meta-cognition/temporal_weighted_analysis.py \
  --data-file "data전처리완료/투찰률_{공고의_투찰률}%_데이터.xlsx" \
  --base-rate {logic_분석_결과값} \
  --output "data분석/temporal_weighted_{공고의_투찰률}.json"
```

**시간대별 가중치:**
- 1개월: 40%
- 3개월: 30%
- 6개월: 20%
- 1년: 10%

**처리:**
1. 각 기간별 경쟁 밀도 최소 구간 찾기
2. 1위 존재 구간만 선택
3. 가중 평균 계산
4. ±1% 범위 제한
5. 트렌드 분석

**출력:**
```
data분석/temporal_weighted_{공고의_투찰률}.json
```

**결과 형식:** (실제 값은 시간대별 분석 후 계산됨)
```
✅ 1개월: {분석 결과}% (경쟁자 n명, 가중치 40%)
✅ 3개월: {분석 결과}% (경쟁자 n명, 가중치 30%)
✅ 6개월: {분석 결과}% (경쟁자 n명, 가중치 20%)
✅ 1년: {분석 결과}% (경쟁자 n명, 가중치 10%)

가중 평균: {분석 결과}%
트렌드: {분석 결과} (±x.xxx%)
```

═══

### Stage 5: 고급 분석 (10가지 심층 분석) ⭐ NEW!

**실행 스킬:** `.claude/skills/bidding-advanced-analyzer/advanced_analyze.py`

**목적:** 다차원 분석으로 1위 확률 1~2% 추가 개선

**실행 명령:**
```bash
cd /mnt/a/25
source venv/bin/activate

AGENCY_RATE=$(jq -r '.발주처투찰률' data분석/bidding_context.json)
AGENCY_RATE_FILE=${AGENCY_RATE//./_}

python .claude/skills/bidding-advanced-analyzer/advanced_analyze.py \
  --data-file "data전처리완료/투찰률_${AGENCY_RATE_FILE}%_데이터.xlsx" \
  --agency-rate $AGENCY_RATE \
  --modules all
```

**10가지 분석 모듈:**

**Phase 1 (핵심):**
1. 시간대별 패턴 분석 - 최근 3개월 70% 가중
2. 발주처별 특성 분석 - 발주처별 최적 전략
3. 2D 상관관계 분석 - 사정률×투찰률 저밀도 구간

**Phase 2 (전략):**
4. 업체별 반복 패턴 - 패턴 업체 회피
5. 심리적 앵커 포인트 - 예쁜 숫자 회피
6. 계절성/월별 패턴 - 월별 최적 전략

**Phase 3 (고급):**
7. 순위 간격 분석 - 안전 간격 계산
8. 담합/클러스터 탐지 - 비정상 밀집 회피
9. 기초금액 구간별 분석 - 규모별 전략
10. 고급 몬테카를로 시뮬레이션 - 동적 시뮬레이션

**출력:**
```
data분석/bidding_analysis_advanced_{투찰률}.json
data분석/temporal_heatmap_{투찰률}.png
data분석/agency_comparison_{투찰률}.png
data분석/2d_correlation_{투찰률}.png
```

═══

## 🔄 전체 실행 플로우 (v3.2 병렬 실행)

```
사용자: "낙찰가분석"
  ↓
┌────────────────────────────────────────────────────────┐
│ [Stage 0] 이미지 감지 및 정보 추출                      │
│  - Glob: data분석/*.png                                │
│  - Read: 이미지 Vision 분석                            │
│  - 추출: 공고번호, 기초금액, 투찰율(=발주처투찰률), 발주처│
│  - 저장: bidding_context.json                         │
└────────────────────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────────────────────┐
│ [Stage 1] 전처리 파일 확인                             │
│  - 확인: 투찰률_{공고의_투찰률}%_데이터.xlsx           │
│  - 결과: ✅ 존재 → Stage 2 스킵                        │
└────────────────────────────────────────────────────────┘
  ↓ (파일 없는 경우만)
┌────────────────────────────────────────────────────────┐
│ [Stage 2] 데이터 준비 (조건부)                         │
│  - Excel 파일 생성                                     │
│  - 참여업체 목록 확인                                   │
│  - 데이터 전처리                                       │
└────────────────────────────────────────────────────────┘
  ↓
┌────────────────────────────────────────────────────────┐
│ [Stage 3, 4, 5] 병렬 실행 ⭐⭐⭐                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │ Stage 3:         │  │ Stage 4:         │          │
│  │ logic 종합 분석   │  │ 시간대별 가중    │          │
│  │                  │  │ (독립 실행)      │          │
│  │ • 예정가 형성    │  │ • 1개월 40%     │          │
│  │ • 경쟁 밀도      │  │ • 3개월 30%     │          │
│  │ • 실제 1위 확률  │  │ • 6개월 20%     │          │
│  │ • 종합 점수      │  │ • 1년 10%       │          │
│  └──────────────────┘  └──────────────────┘          │
│                                                        │
│  ┌──────────────────────────────────────┐             │
│  │ Stage 5: 고급 분석 (10가지)          │             │
│  │                                      │             │
│  │ Phase 1:                             │             │
│  │ • 시간대별 패턴                       │             │
│  │ • 발주처별 특성                       │             │
│  │ • 2D 상관관계                        │             │
│  │                                      │             │
│  │ Phase 2 & 3:                         │             │
│  │ • 업체 패턴, 심리적 앵커, 계절성      │             │
│  │ • 순위 간격, 클러스터, 몬테카를로     │             │
│  └──────────────────────────────────────┘             │
│                                                        │
└────────────────────────────────────────────────────────┘
  ↓
✅ 완료!
  - bidding_analysis_comprehensive_{투찰률}.json
  - temporal_weighted_{투찰률}.json
  - bidding_analysis_advanced_{투찰률}.json
  - 시각화 파일들 (PNG)
```

═══

## 📊 최종 출력 파일

### 📝 JSON 분석 결과
```
data분석/
├── bidding_context.json                              (이미지 정보)
├── bidding_analysis_comprehensive_{투찰률}.json      (종합 분석)
├── temporal_weighted_{투찰률}.json                   (시간대별 가중 분석)
└── bidding_analysis_advanced_{투찰률}.json           (고급 분석) ⭐ NEW!
```

### 📊 시각화 파일 (PNG) ⭐ NEW!
```
data분석/
├── temporal_heatmap_{투찰률}.png                     (시간대별 히트맵)
├── agency_comparison_{투찰률}.png                    (발주처 비교)
└── 2d_correlation_{투찰률}.png                       (2D 상관관계)
```

### JSON 결과 구조

#### 1. bidding_analysis_comprehensive_{투찰률}.json
```json
{
  "기초금액": {공고에서_추출},
  "발주처투찰률": {공고에서_추출},
  "전체_데이터": {분석된_데이터_건수},
  "최종_추천": {
    "bin_mid": {분석_결과},
    "reserve_rate": {분석_결과},
    "amount": {분석_결과},
    "actual_win_prob": {분석_결과},
    "p_reserve": {분석_결과},
    "weighted_density": {분석_결과},
    "relative_crowding": {분석_결과},
    "score": {분석_결과}
  },
  "상위10개": [...]
}
```

#### 2. temporal_weighted_{투찰률}.json ⭐ NEW!
```json
{
  "weighted_average": {분석_결과},
  "base_rate": {logic_분석_결과},
  "range_limit": "{base_rate-1}~{base_rate+1}%",
  "trend": {분석_결과},
  "trend_direction": "{상승/안정/하락}",
  "total_weight": 1.0,
  "period_results": {
    "1개월": {
      "optimal_rate": {분석_결과},
      "min_density": {분석_결과},
      "weight": 0.4,
      "weighted_value": {분석_결과}
    },
    "3개월": {
      "optimal_rate": {분석_결과},
      "min_density": {분석_결과},
      "weight": 0.3,
      "weighted_value": {분석_결과}
    },
    "6개월": {...},
    "1년": {...}
  }
}
```

═══

## 📊 분석 결과 출력

**2가지 분석 결과 제시:**

### [분석 1] logic 종합 분석
- 예정가 형성 확률
- 시간 가중 경쟁 밀도
- 상대적 몰림도
- 실제 1위 확률
- 종합 점수 계산

**출력:**
- bidding_analysis_comprehensive_87745.json
- 상위 10개 구간 제시

### [분석 2] 시간대별 가중 분석
- 1개월 데이터 (40% 가중치)
- 3개월 데이터 (30% 가중치)
- 6개월 데이터 (20% 가중치)
- 1년 데이터 (10% 가중치)
- 가중 평균 계산
- ±1% 범위 제한
- 트렌드 분석

**출력:**
- temporal_weighted_87745.json
- 가중 평균 및 트렌드 제시

⚠️ **모든 값은 실제 분석 실행 후 계산됩니다. 공고마다 다릅니다!**

═══

## 🎯 핵심 원칙 (v3.1)

### 1. 이미지 우선 원칙
**모든 분석은 이미지 기반:**
- 투찰율(=발주처투찰률): 이미지 필드 "투찰률"에서 읽음
- 기초금액: 이미지에서 읽음
- 발주처: 이미지 필드 "발주기관"에서 읽음
- 공고번호: 이미지에서 읽음

### 2. 발주처투찰률별 분석 (핵심 원칙)
**⚠️ 모든 분석은 발주처투찰률별로 완전 분리:**
```
이미지 투찰율 = 87.745% (발주처투찰률)
  ↓
87.745% 그룹만 분석
  ↓
87.745% 데이터만 사용
  ↓
결과 1개 생성
```

**중요:** 발주처투찰률이 다르면 완전히 다른 데이터, 다른 분석, 다른 결과

### 3. 종합 분석 통합
**모든 분석이 logic skill 안에 통합:**
- 예정가 형성 확률
- 시간 가중 경쟁 밀도
- 상대적 몰림도
- 실제 1위 확률

### 4. 4단계 완료
**Stage 0 → 1 → 3 → 4 = 끝:**
- 중간 멈춤 없음
- 사용자 입력 불필요
- 완전 자동화
- 2가지 추천값 제공

═══

## 🚨 에러 핸들링

### Stage 0: 이미지 없음
```
→ "data분석/ 폴더에 입찰 공고 이미지를 업로드해주세요."
→ 파이프라인 중단
```

### Stage 0: 이미지 정보 추출 실패
```
→ "이미지에서 투찰율을 읽을 수 없습니다. 올바른 입찰 공고 이미지인지 확인해주세요."
→ 파이프라인 중단
```

### Stage 1: 전처리 파일 없음
```
→ Stage 2 실행
→ 전처리 완료 후 Stage 3 진행
```

### Stage 3: 분석 실패
```
→ 에러 로그 출력
→ 디버깅 정보 제공
```

═══

## 📝 로깅

모든 실행 단계는 `data분석/pipeline_log.txt`에 기록:

```
[2025-10-28 16:00:00] 파이프라인 시작 (v3.0 COMPREHENSIVE)
[2025-10-28 16:00:01] Stage 0: 이미지 감지 - 발견
[2025-10-28 16:00:02] Stage 0: 정보 추출 완료
  - 투찰율: {공고값}%
  - 기초금액: {공고값}원
  - 발주처: {공고값}
[2025-10-28 16:00:03] Stage 1: 전처리 파일 확인 - 존재 (Stage 2 스킵)
[2025-10-28 16:00:04] Stage 3: 종합 분석 시작
[2025-10-28 16:00:45] Stage 3: 종합 분석 완료 (41초)
  - 최종 추천: 87.106% (99.271%)
  - 입찰금액: 33,305,658원
[2025-10-28 16:00:46] Stage 4: 시간대별 가중 분석 시작
[2025-10-28 16:00:52] Stage 4: 시간대별 가중 분석 완료 (6초)
  - 가중 평균: 87.105%
  - 트렌드: 안정 (+0.050%)
[2025-10-28 16:00:53] 파이프라인 종료 (총 실행시간: 53초)
```

═══

## 🔗 관련 스킬

| 스킬 | Stage | 역할 |
|------|:-----:|------|
| `data-preprocessing` | 2 | 데이터 전처리 (조건부) |
| `logic` | 3 | 종합 분석 (COMPREHENSIVE) |
| `bidding-meta-cognition` | 4 | 시간대별 가중 분석 (독립 실행) |
| `bidding-advanced-analyzer` | 5 | 고급 분석 (10가지 심층 분석) ⭐ NEW! |

═══

## 📅 업데이트 이력

- **2025-10-28 v3.2**: 고급 분석 추가 + 병렬 실행 ⭐⭐⭐⭐⭐
  - Stage 5 추가: bidding-advanced-analyzer (10가지 심층 분석)
  - 병렬 실행 구조: Stage 3, 4, 5 동시 실행
  - 3가지 분석 실행: logic + 시간대별 + 고급 분석
  - 3가지 결과 제시: 종합 점수 + 시간가중 평균 + 고급 분석
  - 시각화 파일 생성: 히트맵, 비교 차트, 2D 상관관계
  - 시간대별 가중 분석을 독립 실행으로 수정 (base_rate optional)
  - 5단계로 확장 (0 → 1 → [3+4+5 병렬])

- **2025-10-28 v3.1**: 시간대별 가중 분석 추가 ⭐⭐⭐
  - Stage 4 추가: temporal_weighted_analysis
  - 2가지 분석 실행: logic 종합 분석 + 시간대별 가중 분석
  - 2가지 결과 제시: 종합 점수 + 시간가중 평균
  - 4단계로 확장 (0 → 1 → 3 → 4)
  - 시간대별 가중치: 1개월 40%, 3개월 30%, 6개월 20%, 1년 10%
  - ±1% 범위 제한
  - 트렌드 분석 추가
  - 결정 없이 결과만 제시

- **2025-10-28 v3.0**: 종합 분석 통합 (COMPREHENSIVE)
  - 모든 분석을 logic skill에 통합
  - Stage 5-2 (고급 분석) 제거
  - Stage 5-3 (메타 인지) 일부 제거
  - 3단계로 단순화 (0 → 1 → 3)
  - 종합 점수 공식:
    - 예정가형성확률 × 실제1위확률 × (1/시간가중밀도) × (1/상대적몰림)
  - 0.001% 단위 분석
  - 전체 데이터 사용 (최소 샘플 제한 없음)
  - 기초대비사정률 자동 계산

- **2025-10-28 v2.1**: 최종 입찰 결과값 추가
  - 용어 매핑 명확화
  - 최종 입찰값 섹션 추가

- **2025-10-28 v2.0**: 전면 재설계
  - 이미지 우선 원칙
  - 메타 인지 통합

═══

**⚠️ v3.2 핵심 변경:**
1. **병렬 실행**: Stage 3, 4, 5 동시 실행 → 속도 향상
2. **3가지 분석**: logic + 시간대별 + 고급 분석 (10가지)
3. **3가지 결과**: 종합 점수 + 시간가중 평균 + 고급 분석
4. **시각화**: 히트맵, 비교 차트, 2D 상관관계 PNG 생성
5. **독립 실행**: 시간대별 가중 분석이 logic 없이 독립 실행 가능
6. **다차원 분석**: 시간대별, 발주처별, 2D 공간 분석으로 1~2% 개선
