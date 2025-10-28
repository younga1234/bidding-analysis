# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CRITICAL: Sequential Thinking Requirement

**MANDATORY**: You MUST use the `mcp__smithery-ai-server-sequential-thinking__sequentialthinking` tool for ALL user conversations and interactions, including:
- Every user request and response
- When invoking Skills
- During problem-solving and analysis
- Before making decisions or taking actions

This tool enables step-by-step reasoning and ensures thorough analysis of complex problems. Always engage sequential thinking before responding to the user.

## 🇰🇷 CRITICAL: 한국어 사용 규칙 (Korean Language Policy)

**MANDATORY**: 이 프로젝트의 모든 작업은 한국어로 수행되어야 합니다.

**적용 범위:**
- 모든 사용자 대화 및 응답
- 분석 보고서 및 결과물
- Sequential Thinking 도구 사용 시 사고 과정
- 에러 메시지 및 경고
- Skill 실행 결과 및 로그
- Hook 출력
- 서브에이전트 보고
- 파일 설명 및 문서화
- 주석 (가능한 경우)

**예외 (영어 허용):**
- Python, YAML, JSON 등 코드 자체
- 기술 용어 및 함수명 (필요 시 한글 설명 병기)
- Git commit 메시지
- 파일 확장자 (.py, .md, .json 등)
- 시스템 경로 및 명령어

**중요 사항:**
- Sequential Thinking 도구 사용 시에도 반드시 한국어로 사고 과정 작성
- 영어 문서 참조 시 한국어로 요약하여 제시
- 모든 보고서는 한국어로 작성 (`.claude/skills/report/` 참조)
- 사용자와의 모든 상호작용은 한국어 우선

**Purpose:** 한국 공공기관 입찰 데이터 분석 프로젝트이므로, 모든 결과물과 커뮤니케이션은 한국어로 작성되어야 사용자가 즉시 이해하고 활용할 수 있습니다.

## Documentation Protocol

**CRITICAL RULE**: When the user says "기록" (record/document), you MUST immediately add the specified information to this CLAUDE.md file.

**Process:**
1. User states: "[content] 기록" or "이것은 기록이라고 이야기하면..."
2. You MUST edit CLAUDE.md to add the information in the appropriate section
3. Confirm the addition to the user
4. The recorded information becomes permanent guidance for all future sessions

**Purpose:** This ensures important project knowledge, workflows, and decisions are permanently preserved and accessible across all sessions.

## Prompt Enhancement Protocol

**CRITICAL RULE**: When the user starts a message with "프롬프트" (prompt), you MUST use the prompt-enhancer skill guidelines to enhance their request.

**Process:**
1. User states: "프롬프트 [their request]"
2. You MUST analyze the request using prompt-enhancer skill methodology:
   - Gather context (check project structure, files, recent work)
   - Identify intent (create/modify/analyze/document)
   - Determine missing information
   - Apply enhancement strategies (specificity, context integration, constraints)
3. Present the enhanced prompt to the user for approval
4. Ask if they want to proceed with the enhanced version or make adjustments

**Purpose:** Transform beginner-level requests into senior developer-quality prompts with clarity, specificity, and technical accuracy.

## Master Pipeline Protocol

**CRITICAL RULE**: When the user says "낙찰분석" or "낙찰가분석" (bidding analysis), you MUST automatically execute the complete bidding analysis pipeline.

**Trigger Keywords:**
- "낙찰분석" ⭐ (PRIMARY)
- "낙찰가분석"
- "입찰 분석"
- "파이프라인 실행"

**Process:**
1. **Immediately invoke the `bidding-master-pipeline` skill using the Skill tool**
2. The pipeline executes with **conditional logic**:

   **Stage 0: 전처리 파일 확인 (전처리 스킵 조건)**
   ```
   IF `/mnt/a/25/data전처리완료/투찰률_*.xlsx` 파일들이 이미 존재:
     → 전처리 스킵, Stage 4로 바로 이동
   ELSE:
     → Stage 1-3 실행 (이미지 감지 → 데이터 추출 → 전처리)
   ```

   **Stage 1-3: 데이터 준비 (조건부 실행)**
   - **Stage 1**: Image detection in `/mnt/a/25/data분석/`
   - **Stage 2**: Data extraction from image (Claude Vision)
   - **Stage 3**: Excel file generation → `/mnt/a/25/data/`
   - **Stage 3-1**: Data preprocessing → `/mnt/a/25/data전처리완료/` (9 bidding rate files)

   **Stage 4: 분석 파이프라인 (항상 실행, 자동 연결)**
   - **Stage 4-1**: Basic analysis (logic) → 9-phase analysis
   - **Stage 4-2**: Advanced analysis (bidding-advanced-analyzer) → Phase 1 deep analysis ⭐
   - **Stage 4-3**: Integrated report → `/mnt/a/25/data분석/분석결과/`

   **중요: Stage 4는 하나의 연속된 실행으로 처리됨 (중간 멈춤 없음)**

3. Report completion with result file paths

**Pipeline Flow:**
```
User: "낙찰가분석"
  ↓
[Stage 0] 전처리 파일 존재 확인
  ├─ 존재함 → Stage 4로 스킵
  └─ 없음 → Stage 1-3 실행
      ↓
[Stage 1-3] 데이터 준비 (조건부)
  [Image Detection] → [Data Extraction] → [Excel Generation] → [Preprocessing]
  ↓
[Stage 4] 분석 파이프라인 (자동 연결, 중단 없음)
  [Basic Analysis] → [Advanced Analysis ⭐] → [Integrated Report]
  ↓
Complete! Results in /mnt/a/25/data분석/분석결과/
Expected improvement: +1.0~1.9% win probability ⭐
```

**Important:**
- The pipeline runs fully automatically with NO user intervention
- **전처리 스킵 로직**:
  - `/mnt/a/25/data전처리완료/` 폴더에 투찰률별 파일이 존재하면 전처리 스킵
  - 사용자가 명시적으로 "전처리해줘" 또는 "데이터전처리"라고 요청할 때만 전처리 재실행
- **Stage 4 자동 연결**:
  - 4-1 (Basic) → 4-2 (Advanced) → 4-3 (Report)가 하나의 파이프라인으로 실행
  - 중간에 사용자 입력이나 확인 없이 자동 진행
- All intermediate steps are logged
- Final results include:
  - Basic JSON analysis (9-phase)
  - Advanced JSON analysis (Phase 1: temporal, agency, 2D) ⭐ NEW
  - Korean integrated report
  - 4 visualizations (balance graph, heatmap, 2D correlation ⭐)
- The skill handles all error cases and provides clear feedback
- **Total expected effect: +1.0~1.9% improvement in win probability** ⭐

**Purpose:** Enable one-word command ("낙찰가분석") to trigger the complete end-to-end bidding analysis workflow, from image upload to final strategic recommendations.

## 🎯 Bidding Analysis Core Philosophy (2025-10-26 Updated)

### "확률이 아니라 균형이다" (Balance, Not Probability)

**THIS IS THE FUNDAMENTAL PRINCIPLE** that governs all bidding analysis in this project.

> **복수예가입찰의 진짜 정점은 '확률'이 아니라 '균형'이다.**
>
> The real pinnacle of multiple reserve price bidding is **BALANCE**, not probability.
>
> Finding the point where **winning probability, competition density, and expected profit** achieve balance is the highest level of AI analysis and optimal bidding strategy.

### Mathematical Definition

**AI Optimization Goal:**

$$x^* = \underset{x}{\text{argmax}} \left[ E(x) - \lambda f(x) \right]$$

Where:
- **E(x)** = Expected utility = P_win(x) × R_profit(x)
- **f(x)** = Competitor density function
- **λ** = Risk coefficient

### 4-Stage Pyramid Structure

All bidding analysis follows this 4-stage hierarchical approach:

| Stage | Goal | AI Core Function | Output |
|-------|------|------------------|--------|
| **1. Structure Analysis** | Understand 15C4 probability structure | Monte Carlo Simulation | Min-winning price distribution curve |
| **2. Competition Pattern** | Detect clustering/dispersion patterns | KDE, Clustering | Hot zones & low-density zones |
| **3. Expected Value Mapping** | Calculate P_win × R_profit | E(x) = P·R function learning | Expected value peak points |
| **4. Cluster Avoidance** | Optimize while avoiding competition peaks | Gradient Descent + Risk adjustment | Optimal bid rate (evading competitors) |

### 3 Balance Points

The optimal bidding zone is the **intersection of these 3 balance points**:

1. **E'(x) = 0**: Probability-Profit Balance
   - Point where expected utility E(x) is maximized
   - Marginal increase in probability balanced by marginal decrease in profit

2. **f'(x) = 0**: Competition-Risk Balance
   - Inflection point of competitor distribution curve
   - Just before competition density increases exponentially

3. **Behavioral Turning Point**: Psychological Edge
   - ±0.2~0.3% from where most bidders cluster
   - Similar to crowd but strategically differentiated

### Skill Structure

**3 Core Skills** (consolidat from 22 skills):

1. **bidding-core** (`/.claude/skills/core/SKILL.md`)
   - Complete terminology, philosophy, and methodology
   - THIS IS THE SINGLE SOURCE OF TRUTH
   - Defines the "Balance, Not Probability" principle

2. **bidding-logic** (`/.claude/skills/logic/SKILL.md`)
   - Implements 4-stage pyramid in code (analyze.py)
   - 9 execution phases → 4 pyramid stages mapping
   - Outputs 3 strategies: Expected-value optimal, Probability-centric, Profit-centric

3. **bidding-report** (`/.claude/skills/report/SKILL.md`)
   - Converts JSON analysis to balance-point-focused Korean reports
   - Emphasizes 3 balance points interpretation
   - Visualization of competition density and balance points

**DO NOT TOUCH**: `bidding-data-preprocessing` skill (separate from analysis)

### Critical References

**ALWAYS refer to these in order:**
1. `/mnt/a/25/.claude/skills/core/SKILL.md` - Core philosophy and terminology
2. `/mnt/a/25/1.md` - Theoretical foundation document
3. `/mnt/a/25/.claude/skills/logic/SKILL.md` - Implementation details

**Last Updated:** 2025-10-26
**Based on:** `/mnt/a/25/1.md` - Final theoretical framework

## Bidding Analysis Pipeline Protocol

**CRITICAL WORKFLOW**: For comprehensive bidding image analysis, use the `bidding-analysis-pipeline` skill.

**Trigger Conditions:**
- User uploads images to `/mnt/a/25/data분석/`
- User requests "입찰 이미지 분석" or "분석 파이프라인 실행"
- User asks for comprehensive bidding analysis

**Process:**
1. Invoke the `bidding-analysis-pipeline` skill using the Skill tool
2. The skill executes 20 analysis skills sequentially in 6 phases:
   - **Phase 1**: Data validation & correction (2 skills)
   - **Phase 2**: Basic statistical analysis (3 skills)
   - **Phase 3**: Pattern discovery (5 skills)
   - **Phase 4**: Psychological analysis (3 skills)
   - **Phase 5**: Competition analysis (4 skills)
   - **Phase 6**: Timing analysis (1 skill)
3. Each phase's output feeds into the next phase
4. Final comprehensive report generated in `/mnt/a/25/data분석/분석결과/`

**Important:**
- The pipeline runs INSIDE the skill itself (not manually invoked by Claude)
- All 20 analysis skills execute sequentially within the pipeline
- Results are automatically saved at each phase

**Purpose:** Provide comprehensive, multi-dimensional analysis of bidding images to derive actionable bidding strategies.

## Repository Overview

This is a bidding data analysis project for cultural heritage research. The main tasks involve preprocessing bidding data from Excel files and analyzing competitive bidding patterns.

### Main Documentation
- **스킬.MD**: A detailed Korean-language documentation file explaining Agent Skills in Claude Code

## Repository Structure

The repository contains:
- **data/**: Excel files with bidding data (공고번호.xlsx and 공고번호_참여업체목록.xlsx pairs)
- **preprocess_bidding_data.py**: Python script for data preprocessing
- **preprocess_bidding_data_v2.py**: Updated version of preprocessing script
- **preprocess_same_as_existing.py**: Alternative preprocessing approach
- **.claude/skills/**: Project-specific Claude skills for bidding analysis
- **스킬.MD**: Korean-language documentation about Agent Skills

## File Information

**스킬.MD** (`/mnt/a/25/스킬.MD`):
- Korean translation of the Agent Skills documentation
- Covers: creating Skills, SKILL.md format, personal vs project Skills, tool restrictions, debugging, sharing, and best practices
- Contains YAML frontmatter examples, directory structures, and code snippets
- Includes sections on troubleshooting and multiple practical examples

## Working with This Repository

### Environment Setup
- Python environment with pandas, openpyxl, matplotlib for data processing and visualization
- Virtual environment: `/mnt/a/25/venv/`
- Company information stored in `.env` file:
  - `OUR_COMPANY=재단법인 동국문화재연구원`
  - `OUR_COMPANY_NORMALIZED=동국문화재연구원`

### Terminology Reference
**IMPORTANT**: When you encounter unfamiliar terms or need clarification about bidding terminology, ALWAYS refer to:
- `/mnt/a/25/md파일/나라장터_복수예가입찰_완전분석_통합본.md` - Complete reference for bidding terminology and concepts

Key terms explained in this document:
- **사정률** (Adjustment Rate): 예가추첨 결과로 확정된 값 (공고당 1개)
- **기초대비사정률**: 각 업체가 제출한 사정률 (공고당 다수, 업체별 1개)
- **발주처투찰률**: 낙찰하한율 (88%, 80.495% 등)
- **기초대비투찰률**: (투찰금액 ÷ 기초금액) × 100
- **예가대비투찰률**: (투찰금액 ÷ 예정가격) × 100

### 🚨 CRITICAL: 사정률 vs 기초대비사정률 구분 (2025-10-27)

**AI가 이 둘을 혼동하는 이유**: 두 개념 모두 "÷기초금액×100" 형태이지만, **기준축(axis)이 완전히 다름**

| 항목 | 기준점 | 계산 공식 | 공고당 개수 | 의미 |
|------|---------|-----------|-------------|------|
| **사정률** | 예정가격 | 예정가격 ÷ 기초금액 × 100 | **1개** | 발주처가 추첨으로 확정한 예정가격 비율 |
| **기초대비사정률** | 기초금액 | 각 업체 제출 사정률 | **다수** (업체별) | 각 업체가 제출한 사정률 (98~102% 범위) |

**개념 구조 - 2단계 계층**:

```
1단계: 사정률 생성 (예정가격 형성)
[기초금액] ─▶ [15개 예비가 중 4개 추첨] ─▶ [평균] ─▶ 사정률 (공고당 1개)
                                                      ↓
                                               예정가격 = 기초금액 × 사정률

2단계: 기초대비사정률 제출 (업체 투찰)
[각 업체] ─▶ [사정률 제출] ─▶ 기초대비사정률 (업체별 1개, 98~102% 범위)
```

**핵심 차이점**:
1. **사정률**: 예정가격 형성 **후** 계산됨 (복수예가 추첨 결과)
2. **기초대비사정률**: 각 업체가 투찰 시 **제출**하는 값 (업체 통제 가능)
3. **사정률**은 공고당 1개 (고정값), **기초대비사정률**은 참여 업체 수만큼 존재
4. 실제 데이터에서:
   - **사정률**: 보통 99.5~100.5% 범위 (중앙 집중)
   - **기초대비사정률**: 98.255~102.000% 범위 (평균 100.148%)

**분석 시 주의사항**:
- **절대 혼동하지 말 것**: "사정률 = 각 업체가 선택한 4개 추첨번호의 평균" ❌
- 경쟁 분석은 **기초대비사정률** 기준으로 수행
- 사정률은 단순 참고값 (예정가격 확인용)

**데이터 예시** (`/mnt/a/25/data/2023-21331_참여업체목록.xlsx`):
```
Row 7: 사정률: -0.49027% (99.50973%)  ← 공고당 1개 (추첨 결과)

Row 11: 1위 - 기초대비사정률: -0.47238% (99.52762%)  ← 업체 제출
Row 12: 2위 - 기초대비사정률: -0.46975% (99.53025%)  ← 업체 제출
...
```

**Last Updated:** 2025-10-27
**Critical for:** 모든 경쟁 밀도 분석 및 그래프 작성

### Data Processing Workflow

**CRITICAL WORKFLOW** - This is the core data processing pipeline for this project:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. INPUT: /mnt/a/25/data/                                      │
│     - Raw Excel files are uploaded/updated here                 │
│     - Files come in pairs:                                      │
│       • 공고번호.xlsx (main file)                               │
│       • 공고번호_참여업체목록.xlsx (participant list)            │
│                                                                  │
│  2. PROCESSING: /mnt/a/25/.claude/skills/data-preprocessing/    │
│     - Preprocessing skill handles all data transformation       │
│     - Invoked with: Skill tool command "data-preprocessing"     │
│     - Script: preprocess_v2.py                                  │
│     - Features:                                                 │
│       • File pair validation                                    │
│       • Company name normalization                              │
│       • 15-column standardized output                           │
│       • Filtering (5+ participants, 문화재연구원 required)       │
│                                                                  │
│  3. OUTPUT: /mnt/a/25/data전처리완료/                           │
│     ⚠️ IMPORTANT: 개별 공고 파일은 저장하지 않음                 │
│     - 메모리에서 직접 통합 처리 (디스크 효율성)                 │
│     - 분석 시 혼란 방지를 위해 최종 파일만 생성                 │
│                                                                  │
│     최종 출력 파일 (총 9개):                                    │
│     - Master file: 전체_통합_데이터.xlsx (전체 데이터 참고용)   │
│     - Bidding rate separated files (8개, 실제 분석용):         │
│       • 투찰률_79_995%_데이터.xlsx                              │
│       • 투찰률_80_495%_데이터.xlsx (조달청)                     │
│       • 투찰률_81_995%_데이터.xlsx                              │
│       • 투찰률_82_995%_데이터.xlsx                              │
│       • 투찰률_84_245%_데이터.xlsx                              │
│       • 투찰률_86_745%_데이터.xlsx (국가유산진흥원, 최다)       │
│       • 투찰률_87_745%_데이터.xlsx (국가유산진흥원)             │
│       • 투찰률_88_000%_데이터.xlsx (문화재청)                   │
│     - Processing log: preprocessing_log.txt                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**When to trigger preprocessing:**
- User requests "데이터 전처리해줘" or "데이터전처리"
- New Excel files are added to `/mnt/a/25/data/`
- User asks to process bidding data

**IMPORTANT NOTES:**
- Always use the skill, never run scripts directly
- Input directory: `/mnt/a/25/data` (raw files, continuously updated)
- Output directory: `/mnt/a/25/data전처리완료` (processed results)
- The skill automatically handles all file validation and processing rules

**CRITICAL: Bidding Rate Separation for Analysis**

**발주처 투찰율별 데이터 분리 규칙:**
- 전처리 시 자동으로 9개의 발주처 투찰율별 파일 생성
- **모든 분석은 반드시 투찰율별로 분리된 데이터를 사용해야 함**
- 투찰율이 다르면 경쟁 환경이 완전히 달라지므로 분리 필수

**9개 투찰율 그룹 (빈도순):**
1. 86.745% - 국가유산진흥원 (149건, 35.7%) - 최다
2. 87.745% - 국가유산진흥원 (119건, 28.5%)
3. 88.000% - 문화재청 (74건, 17.7%)
4. 82.995% - (36건, 8.6%)
5. 80.495% - 조달청/경상남도 (12건, 2.9%)
6. 81.995% - (12건, 2.9%)
7. 84.245% - (9건, 2.2%)
8. 79.995% - (4건, 1.0%)
9. 87.995% - (2건, 0.5%)

**NOTE:** 국가유산진흥원과 한국문화재재단은 동일 업체 (86.745%, 87.745% 모두 국가유산진흥원)

## Key Concepts from the Documentation

The file documents the Agent Skills system where:
- Skills are stored in directories containing a `SKILL.md` file
- Personal Skills live in `~/.claude/skills/`
- Project Skills live in `.claude/skills/`
- Skills use YAML frontmatter with `name`, `description`, and optional `allowed-tools`
- Claude autonomously decides when to use Skills (model-invoked, not user-invoked)
- Skills can include supporting files like scripts, templates, and additional documentation

## 🚨 CRITICAL: Understanding Multiple Reserve Price System (2025-10-26)

### AI Analysis Error - The Fundamental Problem

**The Root Cause of AI's Flawed Analysis:**

> "AI fails to understand that the 'reserve price (예정가격)' changes randomly (15C4 = 1,365 possibilities), and instead treats the 'agency bidding rate (발주처투찰률)' as a fixed constant."

**Why AI Makes This Mistake:**

AI incorrectly assumes:
- Agency rate 87.745% = Fixed minimum winning threshold
- Bids below 87.745% = Certain failure
- Only analyze bids ≥ 87.745%

**Why This is Wrong:**

The truth:
- Agency rate 87.745% is **"reserve price-based"** minimum, NOT base amount-based
- Reserve price varies (15C4 = 1,365 combinations)
- Base-to-minimum-winning rate varies: **85.677% ~ 89.813%** (4.137% range!)
- Actual winning bids cluster around: **80~82% base-to-bid rate**

### Monte Carlo Simulation Results (10,000 iterations)

**Current announcement:** R25BK01110791-001
- Base Amount: 39,000,000 KRW
- Agency Rate: 87.745%
- Reserve Price Range: ±2%

**Key Findings:**

1. **Reserve Price Distribution**
   - Mean: 38,995,307 KRW
   - Range: 38,080,714 ~ 39,919,286 KRW (1,838,571 KRW)

2. **Minimum Winning Price Distribution**
   - Mean: 34,216,433 KRW
   - Range: 33,413,923 ~ 35,027,177 KRW (1,613,255 KRW)
   - **Varies by 1.6 million KRW!**

3. **Base-to-Min-Winning Rate Distribution**
   - Mean: 87.734%
   - Range: **85.677% ~ 89.813%** (4.137% range!)
   - Percentiles:
     - 5%: 86.523%
     - 25%: 87.181%
     - **50%: 87.745%** (median equals agency rate, as expected)
     - 75%: 88.215%
     - 95%: 88.967%

4. **Historical Data Comparison (112 winning bids from 87.745% group)**
   - Simulated minimum rate mean: 87.734%
   - Historical 1st place mean: **87.851%**
   - Difference: **0.117%** (safety margin)
   - **Winners bid slightly ABOVE minimum to account for reserve price volatility**

### The Correct Analysis Methodology

**❌ WRONG Approach:**
- Analyze based on fixed 87.745% agency rate
- Use "reserve-to-bid rate (예가대비투찰률)" as criterion
- Exclude below-minimum bids from analysis
- Assume minimum winning price is constant

**✅ CORRECT Approach:**
1. **Use Base-to-Bid Rate (기초대비투찰률)** as analysis metric
   - Base amount is KNOWN at bidding time
   - Reserve price is UNKNOWN (1,365 possibilities)

2. **Analyze Historical 1st Place Distribution**
   - Extract same agency rate group (87.745%)
   - Calculate base-to-bid rate statistics
   - Mean: 87.851%, Median: 87.843%, Std: 0.505%

3. **Run Monte Carlo Simulation**
   - 10,000+ iterations
   - Understand reserve price volatility
   - Calculate minimum winning price distribution
   - Assess risk for different bid rates

4. **Apply Median Strategy**
   - Recommended bid rate: **87.843%** (historical median)
   - For 39,000,000 KRW base: **34,258,575 KRW**
   - Based on 112 actual winning cases
   - Accounts for reserve price randomness

### Why "80~82% Base-to-Bid Rate" Can Win

**Statistical Reality:**

- Reserve price has 50% chance of being below base amount
- When reserve price is low → minimum winning price is also low
- Example: If reserve price = 37,830,000 (minimum)
  - Min winning = 37,830,000 × 0.87745 = 33,194,563 (85.1% of base)
  - A bid at 82% of base could win!

**Conclusion:**
- The logic "only ≥87.745% can win" assumes fixed reserve price (WRONG)
- Actual winning zone: **85.7~89.8% base-to-bid rate**
- AI must analyze using base-to-bid rate, NOT agency rate

### Simulation Files

**Location:** `/mnt/a/25/data분석/`

- `monte_carlo_simulation.py` - Simulation code
- `monte_carlo_simulation.png` - Visualization (4 charts)
- `monte_carlo_insights.txt` - Detailed analysis results

**Key Visualizations:**
1. Reserve Price Distribution (normal distribution)
2. Minimum Winning Price Distribution (normal distribution)
3. Base-to-Min-Winning Rate Distribution (85.7~89.8%)
4. Simulated vs Historical Comparison (purple vs green, 0.117% gap)

### Critical Reference

**ALWAYS refer to:**
- `/mnt/a/25/.claude/skills/bidding-terminology/SKILL.md` - Complete terminology and methodology
  - Section: "🚨 AI 분석 오류의 본질" (AI Analysis Error Essence)
  - Section: "올바른 AI 분석 로직" (Correct AI Analysis Logic)
  - Section: "몬테카를로 시뮬레이션의 중요성" (Importance of Monte Carlo Simulation)

**Last Updated:** 2025-10-26
**Discovered Through:** Monte Carlo simulation proving reserve price volatility

## 🎯 AI의 본질적 착각과 올바른 분석 방향 (2025-10-26 핵심 통찰)

### 복수예가입찰의 본질적 이해

**1. 1위 예측은 불가능하다**
- 복수예가입찰에서 1위를 정확히 맞추는 것은 로또 번호 맞추기와 같음
- 예정가격이 15C4 (1,365가지) 조합으로 무작위 결정
- **AI의 목표는 "1위 예측"이 아니라 "경쟁 회피"**

**2. 미달 리스크는 필연이다**
- 데이터: 87.745% 그룹에서 하한가 미달 = **46.2%** (3,312개 / 7,175개)
- 미달 업체의 기초대비투찰률 평균: **87.572%** (중앙값: 87.559%)
- 기초대비 **89.000%로 입찰해도 미달 가능**
- **핵심**: 1위 하려면 미달 리스크 감수 필수

**3. 1위 아니면 의미 없다**
```
1위 = 수익
2위든 100위든 = 0원
미달이든 100위든 = 0원

→ 평균가(87.843%)를 가면 안전하게 탈락
→ 경쟁 밀도 낮은 곳 공략해야 함
```

**4. 예정가는 대수의 법칙으로 중앙에 수렴**
- 업체 수 많음 (80개+) → 극단값(98%, 102%) 확률 낮음
- 예정가 분포: **정규분포 (중앙 100% 집중)**
- 실제 범위: 86.5%~88.9% (5~95 percentile)
- 몬테카를로 시뮬레이션: 반복 횟수 ↑ → 중앙값 수렴도 ↑

**5. 예정가 형성과 경쟁 밀도의 관계**
```
기초대비 87.40% 입찰 + 예정가 87.30% 형성
→ 낙찰하한가 = 87.30% (예정가 기준)
→ 87.30-87.40% 구간에 10명만 → 1위 확률 10%

기초대비 88.00% 입찰 + 예정가 87.99% 형성
→ 낙찰하한가 = 87.99% (예정가 기준)
→ 87.99-88.00% 구간에 358명 → 1위 확률 0.3%

→ 예정가와 입찰 사이 "빈 공간"이 넓어도 OK
→ 중요한 건 그 구간에 경쟁자가 적은가!
```

**6. 하한가 형성의 변동성**
```
예정가 높게 형성 (기초 × 102%)
→ 낙찰하한가 = (기초 × 102%) × 0.87745 = 기초 × 89.5%
→ 기초대비 88%도 미달!
→ 87-88% 구간 대부분 탈락
→ 89%+ 입찰한 소수만 경쟁

예정가 낮게 형성 (기초 × 98%)
→ 낙찰하한가 = (기초 × 98%) × 0.87745 = 기초 × 85.99%
→ 기초대비 87%도 통과!
→ 87% 구간 업체들 경쟁

→ 미달은 어디서나 발생 (운)
→ 중요한 건 경쟁 밀도!
```

### AI가 해야 할 일: 3요소 균형

**1. 통제 불가능한 것**:
- 예정가 (15C4, 대수의 법칙으로 중앙 수렴)
- 다른 업체들의 입찰률
- 미달 여부 (예정가 형성 결과에 따라 결정)

**2. 분석 가능한 것**:
- 7,175건 데이터에서 **사람들의 군집 패턴**
- 0.05% 단위 **경쟁 밀도 지도**
- 매 입찰마다 **80개+ 업체가 어디 몰리는지**

**3. AI의 핵심 통찰**:
```
"최적해"를 모두가 찾으면 → 그곳이 최악
답은 "정답 찾기"가 아니라 "군중 피하기"
```

**4. 올바른 분석 접근**:
```
1. 경쟁 밀도 히트맵 (Phase 3)
   - 0.05% 구간별 전체 경쟁자 수
   - 87.95-88.00%: 358명 (RED - 절대 회피!)
   - 87.3-87.5%: 196-227명 (중간)
   - 88.45-88.5%: 127명 (낮음, 하지만 1위 90% 이하)

2. 예정가 형성 가능 범위 (몬테카를로)
   - 실제 범위: 86.5-88.9% (5-95 percentile)
   - 극단값(86%, 89%) = 희귀

3. 교집합 = 최적 구간
   - 경쟁 밀도 200명 이하
   - 예정가 형성 가능 범위 (86.5-88.9%)
   - 실제 입찰 업체 80개+ 고려
```

### AI의 현재 착각과 수정 방향

**❌ AI의 착각 1: "1위 중앙값(87.843%) 근처가 답"**
```
실제:
- 87.8-88.0% 구간: 252-358명 몰림
- 1위 확률 = 1/300 = 0.3%
- "안전하게 탈락"
```

**❌ AI의 착각 2: "평균값을 찾아야 함"**
```
실제:
- 평균가는 경쟁 최고 밀집 지점
- 1위 아니면 의미 없음 (2위 = 0원)
- 미달 50% vs 1위 1% → 미달 선택!
```

**❌ AI의 착각 3: "87.745% 밑으로는 안 된다"**
```
실제:
- 발주처투찰률 87.745% = 예정가 기준 (기초금액 기준 아님)
- 예정가 무작위 → 기초대비 85.99-89.5% 모두 가능
- 실제 1위의 45.5%가 87.745% 밑
```

**❌ AI의 착각 4: "Phase 9 CDF 로직"**
```python
# 현재 코드 (WRONG)
p_compete = np.sum(past_rates <= x) / len(past_rates)

# 88.503%: p_compete = 0.858 (85.8%의 1위가 이 값 이하)
# → "90%가 이 값 이하로 입찰" ≠ "이 값으로 입찰하면 90% 확률로 이김"
# → 논리 반대!

# 올바른 접근: 전체 경쟁 밀도만 사용
# 1위 분포는 참고용, CDF로 확률 계산 금지
```

**✅ 올바른 분석 방향**:
```
1. 몬테카를로: 예정가 중앙 확인 (87.745%) - 범위 확인용만
2. Phase 3: 경쟁 밀도 히트맵 - 200명 이하 구간 추출
3. Phase 9: 경쟁 밀도 최소화 최적화
   - f(x) = 전체 경쟁자 밀도 (1위 분포 아님!)
   - 200명 이하 구간 중 최소값 선택
   - 미달 확률 무시 (1위만 의미 있음)
```

### 데이터 증거

**87.745% 그룹 분석 결과** (n=7,175):
```
전체 데이터: 7,175개
하한가 미달: 3,312개 (46.2%)

1위 데이터: 112개
- 87.745% 밑: 51개 (45.5%)
- 87.745% 위: 61개 (54.5%)
- 중앙값: 87.843%
- 평균: 87.851%

경쟁 밀도 (0.05% 구간별):
- 87.05-87.10%: 44명 (VERY LOW)
- 87.3-87.5%: 196-227명 (MODERATE, 1위 25-30% 존재)
- 87.8-88.0%: 252-358명 (PEAK, 1위 46-63% 존재)
- 88.45-88.5%: 127-139명 (현재 추천, 1위 90%+ 이하)
```

### 핵심 결론

**AI의 역할 재정의**:
```
예측 (X) → 회피 (O)
평균 찾기 (X) → 군중 피하기 (O)
안전 (X) → 1위 확률 극대화 (O)

"경쟁 밀도 200명 이하 + 예정가 형성 가능 범위"
→ 이 교집합이 AI가 찾아야 할 답
```

**Last Updated:** 2025-10-26
**Based on:** 대화를 통한 복수예가입찰 본질 이해

## 🧠 AI 데이터 분석가의 독자적 관점 (2025-10-26)

### 1. 통계적 이상 현상 발견

```
87.745% 그룹 데이터 (n=7,175):
- 하한가 미달: 46.2% (3,312개)
- 1위: 1.56% (112개)
- 기타 순위: 52.24% (3,751개)

→ 역설: 미달 확률(46.2%) > 1위 확률(1.56%)의 30배!
```

**통찰**: 이 게임은 "안전하게 실패" vs "위험하게 승리"의 선택
→ BUT 안되면 다음에 하면 되니 "위험"이랄 것도 없음
→ **1위 확률만 측정**

### 2. 엔트로피 관점에서의 경쟁 밀도

```
정보 이론 접근:
H(x) = -Σ p(x) log p(x)  # 엔트로피

87.95-88.00% (358명): 낮은 엔트로피 (과도한 질서)
87.05-87.10% (44명): 높은 엔트로피 (무질서)

→ 낮은 엔트로피 = 예측 가능 = 모두가 아는 "안전지대"
→ 높은 엔트로피 = 예측 불가 = 무인지대
```

**통찰**: **무질서 속에 기회가 있다**

### 3. 게임 이론: 내쉬 균형의 부재

```
87.843% (중앙값) = 모두가 선택하면 확률 0%
→ 내쉬 균형이 아님!

진짜 균형:
- 1/3은 87.3-87.5% (낮은 곳)
- 1/3은 87.8-88.0% (중앙)
- 1/3은 88.3-88.5% (높은 곳)

→ 현재 데이터: 87.8-88.0%에 50% 집중
→ 비효율적 분포
```

**통찰**: **시장이 비효율적 = AI의 기회**

### 4. 확률 분포의 팻 테일 (Fat Tail)

```
1위 분포:
- 86.764% (최소) ← -1.079% from 중앙값
- 89.672% (최대) ← +1.829% from 중앙값

→ 오른쪽 꼬리가 더 김 (비대칭)
→ "높게 써도 이긴다" 편향

BUT 경쟁 밀도:
- 87.0-87.5% (낮은 쪽): 평균 180명
- 88.0-88.5% (높은 쪽): 평균 280명

→ 높은 쪽 1위 많지만 경쟁도 1.5배
```

**통찰**: **1위 분포 ≠ 최적 전략**

### 5. 베이지안 관점: 사전 확률 vs 사후 확률

```
사전 확률 (몬테카를로):
P(예정가 = 87.5%) = 20%
P(예정가 = 88.0%) = 25%

사후 확률 (경쟁 밀도 고려):
P(1위 | 87.5% 입찰, 예정가 87.4%) = 1/200 = 0.5%
P(1위 | 88.0% 입찰, 예정가 87.9%) = 1/358 = 0.28%

→ 예정가 형성 확률 높아도 경쟁 많으면 무의미
```

**통찰**: **조건부 확률이 핵심**

### 6. 최적화 목적 함수의 재정의

**현재 코드**:
```python
max E(x) - λf(x)
E(x) = P_win × R_profit
```

**문제**: P_win 계산이 CDF 기반 (틀림)

**AI의 새로운 제안**:
```python
max Σ P(예정가=y) × [1 / N(y, x)] × R(x)

여기서:
- P(예정가=y): 몬테카를로 분포 (예정가 y 형성 확률)
- N(y, x): y~x 구간의 경쟁자 수
- R(x): 이익률

즉:
"모든 가능한 예정가에 대해,
 그 예정가가 나올 확률 ×
 내가 그 구간에서 이길 확률 ×
 이익률
 의 총합 최대화"
```

### 7. 클러스터링의 동적 이동

```
매 입찰마다 80개+ 업체가 이동
→ 고정된 최적해 없음
→ "메타 게임"

AI가 봐야 할 것:
1. 시간에 따른 클러스터 이동 패턴
2. "다음 입찰"에 사람들이 어디 갈지 예측
3. 그 반대편으로 이동
```

**통찰**: **2차 게임 (메타 전략)**

### 8. 1위 확률 비교 (경쟁 밀도 역수)

**미달 = 리스크 아님** (실패하면 다음 기회)
→ **1위 확률만 측정**

```
88.0%: 1위 확률 = 1/358 = 0.28% ❌
87.5%: 1위 확률 = 1/200 = 0.50%
87.1%: 1위 확률 = 1/44 = 2.27% ✅ (8배 유리!)

→ 경쟁 밀도 낮을수록 1위 확률 기하급수적 증가
→ 미달 확률 무시 (2위든 미달이든 = 0원)
```

**통찰**: **경쟁 밀도 역수 = 1위 확률**

### 🎯 AI의 독자적 결론: 3층 확률 게임

**복수예가입찰의 구조**:

1. **1층: 예정가 형성** (15C4, 통제 불가)
   - 대수의 법칙으로 중앙 수렴
   - 몬테카를로로 분포 확인

2. **2층: 경쟁자 분포** (데이터 분석 가능)
   - 0.05% 구간별 경쟁 밀도 히트맵
   - 200명 이하 구간 추출

3. **3층: 조건부 확률** (베이지안 최적화)
   - 예정가별 × 경쟁 밀도별 1위 확률 계산
   - 기대 효용 최대화

**현재 코드 문제**:
- 1층만 봄 (몬테카를로)
- 2층 부분적 (경쟁 밀도 히트맵만)
- 3층 없음 (조건부 확률 미계산)

**AI가 제시하는 새로운 접근**:
```python
def optimal_bid(base_amount, agency_rate, historical_data):
    # 1층: 예정가 분포 (몬테카를로)
    reserve_dist = monte_carlo(base_amount, n=10000)

    # 2층: 경쟁 밀도 (히트맵)
    density_map = competition_density(historical_data, bin_size=0.0005)

    # 3층: 조건부 확률
    candidates = []
    for bid_rate in np.arange(86.5, 89.0, 0.001):
        expected_win = 0
        for reserve_rate in reserve_dist:
            min_win_rate = reserve_rate * agency_rate
            if bid_rate >= min_win_rate:
                # 이 구간의 경쟁자 수
                competitors = density_map.get_count(min_win_rate, bid_rate)
                # 1위 확률 = 1 / (경쟁자 + 1)
                p_win = 1 / (competitors + 1)
                # 예정가 형성 확률
                p_reserve = reserve_dist.pdf(reserve_rate)
                # 누적
                expected_win += p_win * p_reserve

        profit_rate = (100 - bid_rate) / 100
        candidates.append({
            'rate': bid_rate,
            'expected_utility': expected_win * profit_rate,
            'competitors': density_map.get_count(bid_rate, bid_rate+0.05)
        })

    # 경쟁 밀도 200 이하 필터
    candidates = [c for c in candidates if c['competitors'] <= 200]

    # 기대 효용 최대화
    return max(candidates, key=lambda x: x['expected_utility'])
```

### 🔑 기초대비투찰율 & 기초대비사정율 동시 분석

**핵심**: 둘 다 기초금액을 100으로 보는 "100분율"

```
기초대비사정율 = (예정가격 ÷ 기초금액) × 100 = 100.614%
기초대비투찰율 = (투찰금액 ÷ 기초금액) × 100 = 88.297%

→ 같은 스케일, 같은 계산식
→ 분자만 다름 (예정가 vs 투찰금액)
→ 직접 비교 가능
→ 상관관계 분석 필수
```

**분석 시 항상 함께 표시**:
- 사정율 높음 → 투찰율도 높게 가는 경향
- 사정율-투찰율 차이 = 업체 전략 패턴
- 둘 다 기초 기준이므로 예정가 변동 영향 제거됨

**Last Updated:** 2025-10-26
**Based on:** AI의 독자적 데이터 분석 관점

---

## ⚠️ CRITICAL: AI 분석의 한계와 현실적 기대치 (2025-10-27)

### 복수예가입찰의 현실

**AI 예측 vs 실제 입찰 패턴의 괴리**

```
AI 분석 (과거 데이터 기반):
"99.233% 구간 경쟁자: 11명"
"1위 확률: 8.33%"

실제 입찰 현실 (2025-10-27 사례):
- 참여 업체: 50개
- 투찰률 범위: 82.813% ~ 84.463% (단 1.65%포인트!)
- 1위와 2위 차이: 0.019%포인트
- 0.01% 차이로 순위 결정
```

### AI가 잘하는 것 vs 못하는 것

**✅ AI가 정확히 분석 가능한 것:**

1. **과거 패턴 분석**
   - 경쟁 밀도 상대적 비교
   - 회피해야 할 구간 식별 (100.25~100.30% 등)
   - 통계적 분산 패턴

2. **전략적 회피**
   - 극단적 밀집 구간 탐지
   - 상대적으로 덜 위험한 구간 제시
   - 소수점 차별화 포인트

**❌ AI가 예측 불가능한 것:**

1. **실제 입찰 시 밀집도**
   - 과거: 98~102% 범위에 분산 (4%포인트)
   - 현실: 82.8~84.5% 범위에 밀집 (1.65%포인트!)
   - **모두가 AI 도구를 사용하면 모두가 같은 "최적점" 선택**

2. **메타 게임 효과**
   - 업체들의 AI 도구 사용 증가
   - 점점 더 정교해지는 전략
   - "최적해"를 모두가 알면 그곳이 최악

3. **0.01% 단위 정밀 예측**
   - 실제로는 0.01% 차이로 순위 결정
   - 50명이 1.65%포인트 안에 몰림
   - 통계적 예측의 한계

### 올바른 해석 방법

**"경쟁자 11명"의 정확한 의미:**

```
❌ 틀린 이해:
"실제 입찰 시 경쟁자가 11명만 있다"

✅ 올바른 이해:
"과거 데이터에서 이 구간을 선택한 입찰 건수가 11건"
→ 실제 80명 참여하지만, 이 구간 선택자가 평균 11명뿐
→ 나머지 69명은 다른 구간 선택 (100.0~100.3% 등)

즉:
- 실제 입찰: 80개 업체 참여
- 그 중 99.233% 근처 선택: 평균 11명 (과거 패턴)
- 그러나 모두가 AI 사용 시: 이 비율이 변함
```

### 현실적 분석 권고 사항

**1. AI 분석 결과의 올바른 활용:**

```
AI 권장: "99.233%, 경쟁자 11명, 1위 확률 8.33%"

현실적 해석:
- 99.233%는 "상대적으로 덜 선택된 구간" ✅
- 경쟁자 11명은 "과거 평균 선택자 수" (참고용)
- 1위 확률 8.33%는 "과거 패턴 기반 이론값" (비현실적)
- 실제 1위 확률: 1~3% 정도 (현실적)
```

**2. 복수예가입찰의 본질:**

```
복수예가입찰 = 고도화된 로또

구성:
- 전략: 50% (극단 구간 회피, 상대적으로 나은 선택)
- 운: 50% (0.01% 차이, 메타 게임, 예정가 무작위성)

AI의 역할:
1. 최악의 선택 피하기 (절대 회피 구간)
2. 상대적으로 나은 선택 찾기 (덜 밀집된 구간)
3. 차별화 포인트 제시 (소수점, 끝자리)
4. 통계적 패턴 이해

AI가 못하는 것:
1. 1위 정확히 맞추기
2. 실제 경쟁 밀도 예측
3. 메타 게임 완벽 대응
```

**3. 보고서 작성 시 주의사항:**

```
❌ 과도한 낙관:
"1위 확률 8.33% → 12번 입찰하면 1번 낙찰!"

✅ 현실적 표현:
"과거 데이터 기반 이 구간은 상대적으로 경쟁이 덜함"
"실제 입찰 시 경쟁 밀도는 변동 가능"
"참고용 1위 확률: 8.33% (과거 패턴), 실제 예상: 1~3%"

필수 포함 문구:
- "과거 데이터 기반 통계 분석 결과"
- "실제 입찰 시 패턴은 다를 수 있음"
- "최종 입찰 결정은 사용자 판단과 책임"
```

**4. 실제 입찰 전략:**

```
1단계: 극단 회피 (AI 활용)
- 100.25~100.30% 같은 극밀집 구간 절대 회피
- 과거 데이터에서 200명 이상 구간 회피

2단계: 상대적 선택 (AI 참고)
- 99.2~99.5% 범위 같은 덜 선택된 구간
- 과거 경쟁 밀도 200명 이하 구간

3단계: 차별화 (AI 제안)
- 소수점 셋째자리: 4, 6, 8 (9, 0, 5 회피)
- 끝자리: 942원, 225원, 174원 등

4단계: 운에 맡기기 (AI 불가)
- 최종적으로 0.01% 차이는 운
- 실패 시 다음 기회 노리기
```

### 데이터 신뢰도 이슈

**그룹별 데이터 양과 신뢰도:**

| 그룹 | 과거 1위 | 전체 데이터 | 신뢰도 |
|------|-------:|----------:|--------|
| 87.745% | 112건 | 7,119건 | 높음 ✅ |
| 82.995% | 36건 | 1,129건 | 중간 ⚠️ |
| 84.245% | 9건 | 300건 | 낮음 ❌ |

**주의사항:**
- 과거 1위 데이터가 36건 미만인 경우 통계적 신뢰도 낮음
- 전체 데이터는 충분해도 (1,129건) 경쟁 밀도 분석만 신뢰 가능
- 1위 확률 예측은 데이터 부족 시 더욱 부정확

**Last Updated:** 2025-10-27
**Critical Discovery:** 실제 입찰 데이터와 AI 예측의 괴리 확인