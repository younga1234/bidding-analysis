---
name: bidding-meta-cognition
description: "Execute temporal weighted analysis with time-based prioritization. This skill should be used when analyzing bidding patterns with emphasis on recent data over historical trends."
allowed-tools: Bash, Read, Write
---

# Bidding Meta Cognition

## Purpose

Calculate optimal bid rates using temporal weighting (1mo: 40%, 3mo: 30%, 6mo: 20%, 1yr: 10%) to prioritize recent bidding patterns.

## When to Use

Use this skill when:
- Temporal weighted analysis needed
- Recent data should be prioritized
- Part of parallel skill chain execution

## How to Use

### Input Requirements

This skill reads from `bidding_context.json` which contains:
- `공고번호`: Announcement number
- `기초금액`: Base amount
- `발주처투찰률`: Agency bid rate
- `발주처`: Procuring agency

### Execution Process

1. **Read Context**: Extract information from `data분석/bidding_context.json`
2. **Locate Data**: Find preprocessed data file
3. **Execute Script**: Run the analysis script from scripts directory
4. **Generate Output**: Create JSON results and visualizations

### Scripts

- `scripts/temporal_weighted_analysis.py`

### Integration

This skill integrates with the bidding analysis ecosystem and may be triggered as part of the automated pipeline or run independently for specific analysis needs.
