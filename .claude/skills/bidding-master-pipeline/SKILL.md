---
name: bidding-master-pipeline
description: "Orchestrate the complete bidding analysis pipeline. This skill should be used when running end-to-end bidding analysis from image extraction to generating three parallel analysis results."
allowed-tools: Bash, Read, Write
---

# Bidding Master Pipeline

## Purpose

Automate the entire bidding analysis workflow by coordinating image analysis, context creation, and parallel execution of three analysis skills.

## When to Use

Use this skill when:
- Running complete bidding analysis pipeline
- Processing bidding announcement images
- Need automated workflow from image to analysis results

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

- `scripts/extract_bidding_info.py`
- `scripts/trigger_skills.py`
- `scripts/pipeline_orchestrator.py`

### Integration

This skill integrates with the bidding analysis ecosystem and may be triggered as part of the automated pipeline or run independently for specific analysis needs.
