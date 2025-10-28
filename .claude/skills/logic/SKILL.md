---
name: logic
description: "복수예가입찰 종합 분석 실행. bidding_context.json 읽기 -> analyze.py 자동 실행 -> 최적 입찰값 계산 (시간가중 경쟁밀도, 몰림도, 1위확률 통합). Use when 입찰 분석, 종합 분석, 최적 입찰값 계산, skill 체인 자동 실행"
allowed-tools: Bash, Read
---

# 복수예가입찰 종합 분석 (COMPREHENSIVE)

## 🎯 목적

**모든 요소를 통합한 종합 분석으로 최적 입찰값 계산**

입력: 기초금액, 발주처투찰률, 전처리 데이터
     ↓
[종합 분석: 시간가중 + 몰림도 + 실제1위확률]
     ↓
출력: 기초대비투찰률, 기초대비사정률, 입찰금액

═══

## ⚡ 실행 로직 (이 skill이 트리거되면 자동 실행)

**이 skill이 호출되면 아래 명령을 자동으로 실행하세요:**

### Step 1: bidding_context.json 읽기

```bash
# 작업 디렉토리로 이동
cd /mnt/a/25

# bidding_context.json에서 정보 추출
AGENCY_RATE=$(jq -r '.발주처투찰률' data분석/bidding_context.json)
BASE_AMOUNT=$(jq -r '.기초금액' data분석/bidding_context.json)

# 파일명용 변환 (87.745 → 87_745)
AGENCY_RATE_FILE=${AGENCY_RATE//./_}

echo "✅ 정보 읽기 완료:"
echo "  - 발주처투찰률: ${AGENCY_RATE}%"
echo "  - 기초금액: ${BASE_AMOUNT}원"
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

### Step 3: analyze.py 자동 실행

```bash
# venv 활성화
source venv/bin/activate

# analyze.py 실행
echo "🔄 logic 종합 분석 시작..."

python .claude/skills/logic/analyze.py \
  --base-amount $BASE_AMOUNT \
  --agency-rate $AGENCY_RATE \
  --data-file "$DATA_FILE"

# 실행 결과 확인
if [ $? -eq 0 ]; then
  echo "✅ logic 종합 분석 완료"
  echo "📄 결과: data분석/bidding_analysis_comprehensive_${AGENCY_RATE_FILE}.json"
else
  echo "❌ 오류: analyze.py 실행 실패"
  exit 1
fi
```

### Step 4: 완료

```
- 결과 파일: data분석/bidding_analysis_comprehensive_{투찰률}.json 생성됨
- 다음 skill로 자동 진행 (bidding-master-pipeline이 관리)
```

═══

## 🔑 핵심 원칙

### 1. 전체 데이터 사용
- 해당 발주처투찰률 그룹의 모든 데이터 분석
- 최소 샘플 크기 제한 없음
- 과거 1위가 있는 모든 구간 분석

### 2. 0.001% 단위 분석
- 세밀한 경쟁 밀도 분석
- 데이터 범위에 따라 구간 수 자동 계산

### 3. 종합 점수 계산
```
점수 = 실제1위확률 × (1/시간가중밀도) × (1/상대적몰림)
```

═══

## 📊 분석 단계 (4단계)

### [1/4] 전체 경쟁 밀도 분석
**목적**: 0.001% 단위 구간 생성

**처리**:
- 기초대비투찰률 최소~최대 범위 (데이터 기반)
- 0.001% 단위로 구간 분할
- 데이터 범위에 따라 구간 자동 생성

**출력**:
- 분석 구간: 데이터 기반 계산

═══

### [2/4] 평균 경쟁 밀도 계산
**목적**: 상대적 몰림도 계산 기준

**처리**:
- 전체 업체: 데이터에서 계산
- 구간 수: 데이터 범위 기반
- 평균 밀도 = 전체 업체 / 구간 수

**출력**:
- 평균 밀도: 데이터 기반 계산

═══

### [3/4] 각 구간별 종합 분석
**목적**: 모든 요소 통합 점수 계산

**처리**:
1. **시간 가중 경쟁 밀도** (weighted_density)
   - 1개월: 40% 가중치
   - 3개월: 30% 가중치
   - 6개월: 20% 가중치
   - 1년: 10% 가중치
   - 최근 데이터 우선

2. **상대적 몰림도** (relative_crowding)
   - 이 구간 밀도 / 평균 밀도
   - 1.0 = 평균 수준
   - 2.0 = 평균의 2배 몰림

3. **실제 1위 확률** (actual_win_prob)
   - 과거 1위 수 / 전체 경쟁자 수
   - 1위가 없는 구간은 제외

4. **종합 점수**
```python
score = (
    actual_win_prob
    * (1 / (weighted_density + 1))
    * (1 / (relative_crowding + 0.1))
)
```

**필터링**:
- 데이터 없는 구간: 제외
- 1위 없는 구간: 제외

**출력**:
- 유효 구간: 데이터 기반 계산
- 각 구간의 종합 점수

═══

### [4/4] 종합 점수 정렬
**목적**: 최적 입찰값 Top 10 추출

**처리**:
- 종합 점수 내림차순 정렬
- Top 10 추출

**출력 형식**: (실제 값은 분석 후 계산됨)
```
1. 기초대비투찰률: {분석_결과}%
   기초대비사정률: {분석_결과}%
   입찰금액: {분석_결과}원
   실제 1위 확률: {분석_결과}% (n명 / m명)
   예정가 형성 확률: {분석_결과}%
   시간 가중 밀도: {분석_결과}명
   상대적 몰림: {분석_결과}배
   종합 점수: {분석_결과}
```

═══

## 🚀 실행 방법

### 명령어 형식
```bash
source venv/bin/activate

python3 /mnt/a/25/.claude/skills/logic/analyze.py \
  --base-amount {공고의_기초금액} \
  --agency-rate {공고의_발주처투찰률} \
  --data-file "data전처리완료/투찰률_{공고의_투찰률}%_데이터.xlsx"
```

### 파라미터
```
필수:
  --base-amount: 기초금액 (원) - 공고에서 추출
  --agency-rate: 발주처투찰률 (%) - 공고에서 추출
  --data-file: 전처리된 데이터 경로 - 공고의 투찰률에 해당하는 파일

출력:
  data분석/bidding_analysis_comprehensive_{투찰률}.json
```

═══

## 📁 출력 파일

### JSON 결과 형식 (실제 값은 분석 후 계산됨)
```json
{
  "기초금액": {공고에서_추출},
  "발주처투찰률": {공고에서_추출},
  "전체_데이터": {데이터_건수},
  "최종_추천": {
    "bin_mid": {분석_결과},
    "reserve_rate": {분석_결과},
    "amount": {분석_결과},
    "actual_win_prob": {분석_결과},
    "weighted_density": {분석_결과},
    "relative_crowding": {분석_결과},
    "score": {분석_결과}
  },
  "상위10개": [...]
}
```

═══

## 🔧 핵심 원칙 (2025-10-28)

### ⭐ 설계 원칙
1. **이익률 제거**
   - 낙찰이 목표, 이익률 최적화 아님

2. **0.001% 단위**
   - 세밀한 경쟁 밀도 분석

3. **전체 데이터 사용**
   - 최소 샘플 제한 제거
   - 해당 발주처투찰률 그룹의 모든 데이터 분석

4. **종합 점수**
   - 3가지 요소 통합
   - 1위확률 × (1/밀도) × (1/몰림)

5. **기초대비사정률 추가**
   - 기초대비투찰률과 함께 출력
   - 사정률 = (투찰률 / 발주처투찰률) × 100

═══

## 🔗 관련 파일

- `analyze.py` (메인 스크립트)
- `analyze_old_backup.py` (이전 버전 백업)

═══

**Last Updated**: 2025-10-28
**Algorithm**: 종합 분석 (시간가중 + 몰림도 + 실제1위확률)
**Status**: Production Ready ✅
**Note**: 모든 값은 공고 데이터에서 추출하여 계산됨
