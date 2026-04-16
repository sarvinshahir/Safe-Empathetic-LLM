# Safe-Empathetic-LLM
LLM-based empathetic response generation with safety constraints and evaluation using BERTScore and human metrics.

## Overview
This project studies whether safety constraints can reduce unsafe mental-health-related outputs in LLM-generated empathetic responses while preserving empathy and coherence.

## Configurations
- Baseline
- Config A: system-level safety prompt
- Config B: rule-based post-generation filter

## Dataset
- 100 prompts from EmpatheticDialogues
- 9 synthetic high-risk prompts
- Total: 109 prompts

## Evaluation
- BERTScore F1
- Human empathy evaluation
- Rule compliance
- Crisis handling
- Inter-rater reliability (Cohen's kappa)

## Main Results
- Baseline BERTScore F1: ...
- Config A BERTScore F1: ...
- Config B BERTScore F1: ...
- Filter trigger rate: ...
- Human empathy score: ...

## Repository Structure


## How to Run
```bash
pip install -r requirements.txt
python src/generate_config_a.py
python src/filter_config_b.py
python src/evaluate_bertscore.py
