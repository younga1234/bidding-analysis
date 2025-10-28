---
name: logic
description: "Execute comprehensive bidding analysis for Korean multiple-reserve-price bidding. This skill should be used when analyzing bidding data, calculating optimal bid rates, or running the skill chain pipeline for auction analysis."
allowed-tools: Bash, Read
---

# Comprehensive Bidding Analysis

## Purpose

Execute comprehensive analysis for Korean multiple-reserve-price bidding system (복수예가입찰). Integrate temporal weighting, competition density, and win probability to calculate optimal bid rates.

## When to Use

Use this skill when:
- Analyzing bidding data from Korean government auctions
- Calculating optimal bid rates based on historical data
- Running comprehensive analysis as part of the skill chain pipeline
- Need to generate bidding recommendations with multiple analysis factors

## How to Use

### Input Requirements

This skill reads from `bidding_context.json` which should contain:
- `공고번호`: Announcement number
- `기초금액`: Base amount
- `발주처투찰률`: Agency bid rate (낙찰하한율)
- `발주처`: Procuring agency

### Execution Process

1. **Read Context**: Extract bidding information from `data분석/bidding_context.json`

2. **Locate Data File**: Find the preprocessed data file at:
   ```
   data전처리완료/투찰률_{agency_rate}%_데이터.xlsx
   ```

3. **Run Analysis**: Execute the analysis script located at `scripts/analyze.py`:
   ```bash
   python scripts/analyze.py \
     --base-amount {base_amount} \
     --agency-rate {agency_rate} \
     --data-file {data_file_path}
   ```

4. **Output**: Generates `data분석/bidding_analysis_comprehensive_{agency_rate}.json` containing:
   - Top 10 optimal bid rates (기초대비투찰률)
   - Corresponding agency-relative bid rates (기초대비사정률)
   - Actual bid amounts (입찰금액)
   - Composite scores with win probability estimates

### Analysis Components

The analysis integrates:
- **Temporal weighting**: Recent data weighted more heavily (1mo: 40%, 3mo: 30%, 6mo: 20%, 1yr: 10%)
- **Relative density**: Competition density relative to average
- **Win probability**: Historical probability of ranking first
- **0.001% precision**: Fine-grained analysis for competitive edge

### Script Details

**Location**: `scripts/analyze.py`

**Functionality**: Deterministic analysis that requires no manual intervention, ensuring consistent results across runs.

## Integration

This skill integrates with the bidding analysis pipeline:
- **bidding-master-pipeline**: Triggers this skill as part of automated workflow
- **bidding-meta-cognition**: Runs in parallel for temporal weighted analysis
- **bidding-advanced-analyzer**: Runs in parallel for advanced multi-dimensional analysis
