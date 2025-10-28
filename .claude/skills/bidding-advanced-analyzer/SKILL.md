---
name: bidding-advanced-analyzer
description: "Perform advanced multi-dimensional bidding analysis. This skill should be used when deep analysis is needed including temporal patterns, agency characteristics, and 2D correlations."
allowed-tools: Bash, Read, Write
---

# Bidding Advanced Analyzer

## Purpose

Execute Phase 1 advanced analysis with three modules: temporal analysis, agency analysis, and 2D correlation analysis.

## When to Use

Use this skill when:
- Advanced multi-dimensional analysis needed
- Visual izations required (PNG charts)
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

- `scripts/advanced_analyze.py`

### Integration

This skill integrates with the bidding analysis ecosystem and may be triggered as part of the automated pipeline or run independently for specific analysis needs.
