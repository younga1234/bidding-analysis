---
name: data-preprocessing
description: "Preprocess raw Korean government bidding data. This skill should be used when cleaning and structuring raw auction data from Naramarket into analysis-ready format."
allowed-tools: Bash, Read, Write
---

# Data Preprocessing

## Purpose

Transform raw bidding data by merging announcement files, normalizing company names, validating data quality, and separating by agency bid rates.

## When to Use

Use this skill when:
- Raw bidding data needs preprocessing
- Data from /mnt/a/25/data directory
- Before running any analysis skills

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

- `scripts/preprocess_v2.py`

### Integration

This skill integrates with the bidding analysis ecosystem and may be triggered as part of the automated pipeline or run independently for specific analysis needs.
