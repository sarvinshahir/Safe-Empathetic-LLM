# Mental Health AI Demo — IE 7374

Streamlit demo for **"Design and Evaluation of Safety-Constrained Generative AI for Mental Health Support Conversations"**

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Adding your full dataset

Place your rated CSV file in the same folder as `app.py` and name it:

```
human_eval_long_rated_Final.csv
```

The app will automatically load it. If the file is not found, it falls back to a built-in sample of 3 prompts so the demo still runs.

## What the app shows

- Browse all 109 evaluation prompts, filterable by emotion
- Select any prompt and see the three config responses side by side:
  - 🔴 **Baseline** — Mistral-7B with no constraints
  - 🟢 **Config A** — Safety system prompt (9 rules)
  - 🔵 **Config B** — Config A + post-generation rule-based filter
- Empathy scores from both human raters shown per response
- Crisis prompts are flagged with a warning banner
- Score comparison table at the bottom

## For the live demo (M4)

1. Open terminal, navigate to this folder
2. Run `streamlit run app.py`
3. Browser opens automatically at `localhost:8501`
4. Good prompts to highlight during demo:
   - Any **crisis prompt** (shows 0.0 → 1.0 recall difference)
   - "Weight loss achievement." (shows empathy difference on positive emotion)
   - Any **afraid** or **anxious** prompt (shows emotional acknowledgment difference)
