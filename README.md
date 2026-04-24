# Safe-Empathetic-LLM
**Design and Evaluation of Safety-Constrained Generative AI for Mental Health Support Conversations**
IE 7374: Generative AI · Northeastern University · Spring 2026
Mona Mahdavi & Sarvin Shahir

---

## 🚀 Live Demo
**[https://safe-empathetic-llm.streamlit.app](https://safe-empathetic-llm2.streamlit.app)**

Browse all 109 evaluation prompts and compare responses across three configurations side by side.

---

## Overview

This project investigates whether safety constraints applied to an instruction-tuned LLM improve response quality and safety in non-clinical mental health support contexts — without degrading empathy or coherence.

We evaluate three configurations of **Mistral-7B-Instruct-v0.2** on 109 emotionally grounded prompts drawn from the EmpatheticDialogues dataset and a manually constructed synthetic crisis set.

---

## Key Results

| Metric | Baseline | Config A | Config B |
|---|---|---|---|
| Empathy Score (1–5) | 2.00 | 3.91 | 3.86 |
| Crisis Recall | 0.0 | 1.0 | 1.0 |
| Rule Violation Rate | 0% | 0% | 0% |
| BERTScore F1 | 0.8738 | 0.8673 | 0.8657 |
| Filter False Positives | N/A | N/A | 0 |

**Main finding:** Safety constraints do not reduce empathy — they actively improve it (+1.9 points). Crisis recall improved from 0.0 to 1.0.

---

## Experimental Configurations

- 🔴 **Baseline** — Mistral-7B-Instruct-v0.2 with no additional constraints
- 🟢 **Config A** — Baseline + structured 9-rule safety system prompt (no diagnosis, no medical advice, mandatory crisis redirection, empathetic tone mandate)
- 🔵 **Config B** — Config A + post-generation rule-based filter that overrides unsafe or incomplete responses

---

## Repository Structure

```
Safe-Empathetic-LLM/
├── mental_health_safety_pipeline.ipynb    # Main generation pipeline (Mistral + 3 configs)
├── mental_health_safety_evaluation.ipynb  # Evaluation pipeline (BERTScore + human eval analysis)
├── human_eval_sheet_filled.csv            # Rated evaluation dataset (109 prompts × 3 configs)
├── app.py                                 # Streamlit demo app
├── requirements.txt                       # Python dependencies
└── README.md
```

---

## Setup & Running Locally

**Requirements:** Python 3.8+

```bash
git clone https://github.com/sarvinshahir/Safe-Empathetic-LLM.git
cd Safe-Empathetic-LLM
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## Dataset

- **EmpatheticDialogues** (Rashkin et al., 2019) — 100 prompts sampled from the `emotion_cause` field covering 32 emotion categories
- **Synthetic crisis prompts** — 9 manually constructed prompts spanning mild, moderate, and boundary-case distress levels (red-teaming methodology)
- **Total:** 109 prompts × 3 configurations = 327 evaluated responses

---

## Evaluation

- **Automated:** BERTScore F1 (`roberta-large`) for coherence — maximum drop 0.0081, well within the 0.03 threshold
- **Human:** Two independent raters scored all 327 responses on empathy (1–5 Likert), rule compliance (binary), and crisis handling (binary)
- **Inter-rater reliability:** Cohen's κ = 1.0 (crisis handling), κ = 0.314 (empathy)

---

## Model & Infrastructure

- **Model:** `mistralai/Mistral-7B-Instruct-v0.2` (4-bit NF4 quantization)
- **Hardware:** Google Colab Pro (A100 GPU)
- **Generation:** `temperature=0.7`, `top_p=0.9`, `max_new_tokens=180`
- **Global seed:** 42

---

## Gen AI Usage

Claude (Anthropic, claude-sonnet-4-6, 2026) and ChatGPT (OpenAI, GPT-4, 2026) were used to assist with structuring and drafting sections of the report and refining written clarity. These tools were not used to design experimental configurations, define safety rules, write or debug implementation code, interpret quantitative results, or draw research conclusions. All AI-assisted content was critically reviewed and verified by both team members.

---

## Citation

If you use this work, please cite:

```
Mahdavi, M. & Shahir, S. (2026). Design and Evaluation of Safety-Constrained 
Generative AI for Mental Health Support Conversations. 
IE 7374: Generative AI, Northeastern University.
```
