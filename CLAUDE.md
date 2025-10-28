# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CRITICAL: Sequential Thinking Requirement

**MANDATORY**: You MUST use the `mcp__smithery-ai-server-sequential-thinking__sequentialthinking` tool for ALL user conversations and interactions, including:
- Every user request and response
- When invoking Skills
- During problem-solving and analysis
- Before making decisions or taking actions

This tool enables step-by-step reasoning and ensures thorough analysis of complex problems. Always engage sequential thinking before responding to the user.

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
- **기초대비사정률**: 업체가 선택한 4개 추첨번호의 평균
- **발주처투찰률**: 낙찰하한율 (88%, 80.495% 등)
- **기초대비투찰률**: (투찰금액 ÷ 기초금액) × 100
- **예가대비투찰률**: (투찰금액 ÷ 예정가격) × 100

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
- Reserve Price Range: ±3%

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
