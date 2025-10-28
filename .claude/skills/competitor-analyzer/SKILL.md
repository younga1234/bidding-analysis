---
name: competitor-analyzer
description: "Analyze competitor bidding patterns and detect AI tool usage. This skill should be used when investigating whether competitors use automated bidding analysis tools."
allowed-tools: Bash, Read, Write
---

# Competitor Analyzer

## Purpose

Detect AI tool usage through five indicators: entropy analysis, decimal patterns, company variance, temporal trends, and outlier detection.

## When to Use

Use this skill when:
- Competitor pattern analysis needed
- AI tool usage detection required
- Pattern analysis across agency bid rates

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

- `scripts/competitor_analysis.py`

### Integration

This skill integrates with the bidding analysis ecosystem and may be triggered as part of the automated pipeline or run independently for specific analysis needs.
