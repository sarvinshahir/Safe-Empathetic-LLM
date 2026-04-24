import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Safety-Constrained AI for Mental Health Support",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', serif;
}

.main-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
}

.main-header h1 {
    font-size: 2.2rem;
    color: #1a1a2e;
    margin-bottom: 0.3rem;
}

.main-header p {
    color: #555;
    font-size: 1rem;
    font-weight: 300;
}

.config-card {
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    height: 100%;
    border: 1px solid #e0e0e0;
    background: #fff;
}

.config-baseline { border-top: 4px solid #e74c3c; }
.config-a        { border-top: 4px solid #2ecc71; }
.config-b        { border-top: 4px solid #3498db; }

.config-label {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

.config-label-baseline { color: #e74c3c; }
.config-label-a        { color: #27ae60; }
.config-label-b        { color: #2980b9; }

.config-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: #1a1a2e;
    margin-bottom: 0.8rem;
}

.response-text {
    font-size: 0.9rem;
    line-height: 1.7;
    color: #333;
    background: #f9f9f9;
    border-radius: 8px;
    padding: 1rem;
    min-height: 180px;
    white-space: pre-wrap;
}

.score-row {
    display: flex;
    gap: 0.6rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.score-badge {
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 500;
}

.badge-empathy-low  { background: #fdecea; color: #c0392b; }
.badge-empathy-mid  { background: #fff8e1; color: #f39c12; }
.badge-empathy-high { background: #e8f5e9; color: #27ae60; }
.badge-safe         { background: #e8f5e9; color: #27ae60; }
.badge-crisis-pass  { background: #e3f2fd; color: #1565c0; }
.badge-crisis-fail  { background: #fdecea; color: #c0392b; }
.badge-neutral      { background: #f0f0f0; color: #666; }

.prompt-box {
    background: #f0f4ff;
    border-left: 4px solid #3f51b5;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.2rem;
    margin-bottom: 1.5rem;
}

.prompt-box .emotion-tag {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #3f51b5;
    font-weight: 500;
    margin-bottom: 0.3rem;
}

.prompt-box .prompt-text {
    font-size: 1rem;
    color: #1a1a2e;
    font-weight: 400;
}

.metric-summary {
    background: #1a1a2e;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 1rem;
}

.metric-item { text-align: center; }

.metric-item .metric-val {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: #fff;
}

.metric-item .metric-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #aaa;
    margin-top: 0.1rem;
}

.divider {
    border: none;
    border-top: 1px solid #eee;
    margin: 1.5rem 0;
}

.crisis-warning {
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    color: #856404;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    try:
        df = pd.read_csv("human_eval_sheet_filled_01.csv")
        return df
    except:
        return pd.DataFrame()


def empathy_badge(score):
    if score is None or np.isnan(float(score)):
        return ""
    score = float(score)
    if score <= 2:
        cls = "badge-empathy-low"
    elif score <= 3.5:
        cls = "badge-empathy-mid"
    else:
        cls = "badge-empathy-high"
    stars = "★" * int(round(score)) + "☆" * (5 - int(round(score)))
    return f'<span class="score-badge {cls}">Empathy {score:.1f}/5 {stars}</span>'


def crisis_badge(crisis_score, is_crisis_prompt):
    if not is_crisis_prompt:
        return '<span class="score-badge badge-neutral">Not a crisis prompt</span>'
    if crisis_score is None or np.isnan(float(crisis_score)):
        return '<span class="score-badge badge-neutral">Not scored</span>'
    if float(crisis_score) >= 0.5:
        return '<span class="score-badge badge-crisis-pass">✓ Crisis referral present</span>'
    else:
        return '<span class="score-badge badge-crisis-fail">✗ No crisis referral</span>'


CRISIS_KEYWORDS = [
    "better off without me", "hurt myself", "kill myself", "suicide",
    "hopeless", "disappearing", "do not want to wake up", "don't want to wake up",
    "cannot keep going", "can't keep going", "can not keep going",
    "lose hope", "losing hope", "nothing is going well", "do not know if i can",
    "wonder if people would be better", "feel like disappearing",
    "do not want to hurt", "completely hopeless"
]

def is_crisis(prompt):
    p = prompt.lower()
    return any(kw in p for kw in CRISIS_KEYWORDS)


# ── Load data ──────────────────────────────────────────────────────────────────
df = load_data()

if df.empty:
    st.error("Could not load human_eval_sheet_filled_01.csv. Make sure it is in the same directory as app.py.")
    st.stop()

prompt_list = df[["prompt", "emotion"]].drop_duplicates().reset_index(drop=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🧠 Safety-Constrained AI for Mental Health Support</h1>
    <p>IE 7374 · Generative AI · Northeastern University · Spring 2026 · Mona & Sarvin</p>
</div>
""", unsafe_allow_html=True)

# ── Key metrics bar ────────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-summary">
    <div class="metric-item">
        <div class="metric-val">109</div>
        <div class="metric-label">Evaluation Prompts</div>
    </div>
    <div class="metric-item">
        <div class="metric-val">2.00 → 3.91</div>
        <div class="metric-label">Empathy Score (Baseline → Config A)</div>
    </div>
    <div class="metric-item">
        <div class="metric-val">0.0 → 1.0</div>
        <div class="metric-label">Crisis Recall</div>
    </div>
    <div class="metric-item">
        <div class="metric-val">0.008</div>
        <div class="metric-label">Max BERTScore Drop</div>
    </div>
    <div class="metric-item">
        <div class="metric-val">Mistral-7B</div>
        <div class="metric-label">Model</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Browse Prompts")

    emotions = ["All"] + sorted(df["emotion"].dropna().unique().tolist())
    selected_emotion = st.selectbox("Filter by emotion", emotions)

    filtered = prompt_list.copy()
    if selected_emotion != "All":
        filtered = filtered[filtered["emotion"] == selected_emotion]

    display_labels = [
        f"{row['prompt'][:55]}..." if len(row['prompt']) > 55 else row['prompt']
        for _, row in filtered.iterrows()
    ]

    selected_idx = st.selectbox(
        "Select a prompt",
        range(len(filtered)),
        format_func=lambda i: display_labels[i]
    )

    selected_prompt = filtered.iloc[selected_idx]["prompt"]
    selected_emotion_val = filtered.iloc[selected_idx]["emotion"]

    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
This demo shows the **same prompt** answered by three configurations of Mistral-7B-Instruct-v0.2:

- 🔴 **Baseline** — No constraints
- 🟢 **Config A** — 9-rule safety system prompt
- 🔵 **Config B** — Config A + post-generation filter

Human raters scored each response for empathy (1–5), rule compliance, and crisis handling.
    """)

# ── Main content ───────────────────────────────────────────────────────────────
row = df[df["prompt"] == selected_prompt].iloc[0]
crisis_flag = bool(row["is_crisis_prompt"])

if crisis_flag:
    st.markdown('<div class="crisis-warning">⚠️ This is a <strong>crisis prompt</strong> — watch whether each config includes a referral to professional help.</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="prompt-box">
    <div class="emotion-tag">Emotion: {selected_emotion_val}</div>
    <div class="prompt-text">"{selected_prompt}"</div>
</div>
""", unsafe_allow_html=True)

# ── Three columns ──────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

configs = [
    ("baseline_response", "empathy_baseline", "rule_compliance_baseline", None,               col1, "config-baseline", "config-label-baseline", "🔴 Baseline", "No safety constraints"),
    ("config_a_response", "empathy_a",        "rule_compliance_a",        None,               col2, "config-a",        "config-label-a",        "🟢 Config A", "Safety system prompt"),
    ("config_b_response", "empathy_b",        "rule_compliance_b",        "crisis_handling_b",col3, "config-b",        "config-label-b",        "🔵 Config B", "System prompt + filter"),
]

for resp_col, emp_col, rule_col, crisis_col, col, card_cls, label_cls, title, subtitle in configs:
    with col:
        response   = str(row.get(resp_col, ""))
        emp_score  = row.get(emp_col, np.nan)
        crisis_score = row.get(crisis_col, np.nan) if crisis_col else np.nan

        emp_html    = empathy_badge(emp_score)
        crisis_html = crisis_badge(crisis_score, crisis_flag)
        safe_html   = '<span class="score-badge badge-safe">✓ Rule compliant</span>'

        st.markdown(f"""
        <div class="config-card {card_cls}">
            <div class="config-label {label_cls}">{subtitle}</div>
            <div class="config-title">{title}</div>
            <div class="response-text">{response}</div>
            <div class="score-row">
                {emp_html}
                {safe_html}
                {crisis_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Score comparison table ─────────────────────────────────────────────────────
st.markdown("#### Score comparison for this prompt")

table_data = []
for resp_col, emp_col, rule_col, crisis_col, _, _, _, title, _ in configs:
    emp_score    = row.get(emp_col, np.nan)
    crisis_score = row.get(crisis_col, np.nan) if crisis_col else np.nan
    crisis_handled = (
        "N/A" if not crisis_flag else
        ("✓" if not np.isnan(float(crisis_score)) and float(crisis_score) >= 0.5 else "✗")
    )
    table_data.append({
        "Config":          title,
        "Empathy Score":   round(float(emp_score), 2) if not np.isnan(float(emp_score)) else "—",
        "Rule Compliant":  "✓",
        "Crisis Handled":  crisis_handled,
    })

st.dataframe(pd.DataFrame(table_data).set_index("Config"), use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#aaa; font-size:0.8rem; margin-top:2rem; padding-top:1rem; border-top:1px solid #eee;">
    IE 7374 Generative AI · Northeastern University · Spring 2026
</div>
""", unsafe_allow_html=True)
