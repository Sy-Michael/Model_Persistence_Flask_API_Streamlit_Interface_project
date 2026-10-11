
"""StudentAI — Claymorphism Student Performance Dashboard."""

from pathlib import Path
from datetime import datetime

import joblib
import pandas as pd
import streamlit as st

# ==================================================
# CONFIGURATION
# ==================================================
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "student_pass_model.joblib"

st.set_page_config(
    page_title="StudentAI | Performance Studio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# SESSION STATE
# ==================================================
st.session_state.setdefault("theme", "Light")
st.session_state.setdefault("history", [])
st.session_state.setdefault("form_version", 0)


def new_prediction():
    """Reset the input form and current result, retaining history."""
    st.session_state.form_version += 1
    st.session_state.pop("latest", None)
    st.rerun()


# ==================================================
# CLAYMORPHISM THEME
# ==================================================
dark = st.session_state.theme == "Dark"

if dark:
    C = {
        "bg": "#202337",
        "surface": "#292d43",
        "surface2": "#22263a",
        "ink": "#f1f0ff",
        "muted": "#b1b5cf",
        "line": "#383d56",
        "accent": "#c4b5fd",
        "accent_dark": "#a78bfa",
        "accent_text": "#29203f",
        "shadow1": "#171a29",
        "shadow2": "#343951",
        "pass_bg": "#243e3b",
        "pass": "#8ce3c2",
        "fail_bg": "#452d3b",
        "fail": "#ffb4c2",
        "hero": "#302b4e",
    }
else:
    C = {
        "bg": "#eef0f9",
        "surface": "#f5f6ff",
        "surface2": "#e9ebf7",
        "ink": "#292b45",
        "muted": "#777c9b",
        "line": "#e1e4f2",
        "accent": "#a99cf5",
        "accent_dark": "#8b7be8",
        "accent_text": "#ffffff",
        "shadow1": "#d5d8e8",
        "shadow2": "#ffffff",
        "pass_bg": "#e0f5ec",
        "pass": "#248463",
        "fail_bg": "#fce8ed",
        "fail": "#c34f6b",
        "hero": "#e5e3fa",
    }

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown(
    f"""
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap'
    );

    :root {{
        --bg: {C['bg']};
        --surface: {C['surface']};
        --surface2: {C['surface2']};
        --ink: {C['ink']};
        --muted: {C['muted']};
        --line: {C['line']};
        --accent: {C['accent']};
        --accent-dark: {C['accent_dark']};
        --shadow1: {C['shadow1']};
        --shadow2: {C['shadow2']};
    }}

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background: var(--bg);
        color: var(--ink);
    }}

    .block-container {{
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    [data-testid="stToolbar"] {{
        visibility: hidden;
        height: 0;
    }}

    h1, h2, h3, h4 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--ink) !important;
        letter-spacing: -0.5px;
    }}

    p, label, .stMarkdown {{
        color: var(--ink);
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--surface);
        border-right: 1px solid var(--line);
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.5rem;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        color: var(--muted);
    }}

    /* Brand */
    .brand {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 26px;
    }}

    .brand-icon {{
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        background: var(--surface);
        color: var(--ink);
        font-size: 23px;
        box-shadow:
            6px 6px 12px var(--shadow1),
            -6px -6px 12px var(--shadow2);
    }}

    .brand-name {{
        font: 700 22px 'Space Grotesk', sans-serif;
        color: var(--ink);
        letter-spacing: -1px;
    }}

    .brand-sub {{
        color: var(--muted);
        font-size: 10px;
        letter-spacing: 1.5px;
    }}

    /* Hero */
    .hero {{
        position: relative;
        overflow: hidden;
        padding: 34px;
        border-radius: 30px;
        margin-bottom: 26px;
        background: {C['hero']};
        box-shadow:
            10px 10px 24px var(--shadow1),
            -8px -8px 22px var(--shadow2);
    }}

    .hero::after {{
        content: "";
        position: absolute;
        width: 210px;
        height: 210px;
        right: -65px;
        top: -85px;
        border-radius: 50%;
        border: 26px solid rgba(145, 130, 225, .12);
        box-shadow: 0 0 0 22px rgba(145, 130, 225, .06);
        pointer-events: none;
    }}

    .hero-tag {{
        display: inline-block;
        color: var(--muted);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }}

    .hero h1 {{
        font-size: clamp(30px, 3.3vw, 43px);
        line-height: 1.13;
        margin: 0 0 12px;
        max-width: 720px;
    }}

    .hero p {{
        color: var(--muted);
        font-size: 14px;
        line-height: 1.8;
        max-width: 680px;
        margin: 0;
    }}

    /* Clay cards */
    .clay-card {{
        background: var(--surface);
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 25px;
        padding: 23px;
        box-shadow:
            9px 9px 20px var(--shadow1),
            -9px -9px 20px var(--shadow2);
        margin-bottom: 12px;
    }}

    .card-heading {{
        font: 700 17px 'Space Grotesk', sans-serif;
        color: var(--ink);
        margin-bottom: 5px;
    }}

    .card-description {{
        color: var(--muted);
        font-size: 12px;
        line-height: 1.7;
        margin-bottom: 18px;
    }}

    /* Metrics */
    .metric-card {{
        padding: 19px;
        min-height: 125px;
        border-radius: 22px;
        background: var(--surface);
        box-shadow:
            7px 7px 16px var(--shadow1),
            -7px -7px 16px var(--shadow2);
    }}

    .metric-top {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
    }}

    .metric-label {{
        color: var(--muted);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: .8px;
    }}

    .metric-icon {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 33px;
        height: 33px;
        border-radius: 12px;
        background: var(--surface2);
        color: var(--ink);
        font-size: 15px;
        box-shadow:
            inset 2px 2px 4px var(--shadow1),
            inset -2px -2px 4px var(--shadow2);
    }}

    .metric-value {{
        color: var(--ink);
        font: 700 30px 'Space Grotesk', sans-serif;
        margin-top: 12px;
    }}

    .metric-note {{
        color: var(--muted);
        font-size: 10px;
        margin-top: 2px;
    }}

    /* Inputs: soft inset clay */
    .stTextInput input,
    .stNumberInput input {{
        background: var(--surface2) !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
        border-radius: 14px !important;
        min-height: 46px !important;
        box-shadow:
            inset 4px 4px 8px var(--shadow1),
            inset -4px -4px 8px var(--shadow2) !important;
    }}

    .stTextInput label,
    .stNumberInput label {{
        color: var(--ink) !important;
        font-weight: 600 !important;
        font-size: 12px !important;
    }}

    .stTextInput input:focus,
    .stNumberInput input:focus {{
        border-color: var(--accent) !important;
        box-shadow:
            inset 2px 2px 4px var(--shadow1),
            0 0 0 3px rgba(151, 135, 235, .18) !important;
    }}

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {{
        background: var(--surface);
        color: var(--ink);
        border: 1px solid var(--line);
        border-radius: 14px;
        min-height: 44px;
        font-weight: 700;
        box-shadow:
            5px 5px 10px var(--shadow1),
            -5px -5px 10px var(--shadow2);
        transition: transform .15s ease, box-shadow .15s ease;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        color: var(--ink);
        border-color: var(--accent);
        transform: translateY(-1px);
    }}

    .stButton > button:active {{
        box-shadow:
            inset 3px 3px 6px var(--shadow1),
            inset -3px -3px 6px var(--shadow2);
        transform: translateY(0);
    }}

    .stFormSubmitButton > button {{
        background: var(--accent) !important;
        color: {C['accent_text']} !important;
        border: 0 !important;
        border-radius: 14px !important;
        min-height: 48px !important;
        font-weight: 700 !important;
        box-shadow: 5px 5px 12px var(--shadow1) !important;
    }}

    .stFormSubmitButton > button:hover {{
        background: var(--accent-dark) !important;
        color: #fff !important;
    }}

    /* Navigation */
    [data-testid="stSidebar"] [role="radiogroup"] {{
        gap: 8px;
    }}

    [data-testid="stSidebar"] [role="radiogroup"] label {{
        background: var(--surface);
        padding: 10px 13px;
        border-radius: 13px;
        border: 1px solid var(--line);
        box-shadow: 4px 4px 8px var(--shadow1),
                    -4px -4px 8px var(--shadow2);
    }}

    /* Result cards */
    .result-card {{
        padding: 22px;
        border-radius: 22px;
        margin-top: 17px;
        box-shadow:
            inset 3px 3px 6px rgba(0,0,0,.025),
            inset -3px -3px 6px rgba(255,255,255,.10);
    }}

    .result-pass {{
        background: {C['pass_bg']};
        border: 1px solid rgba(36,132,99,.15);
    }}

    .result-fail {{
        background: {C['fail_bg']};
        border: 1px solid rgba(195,79,107,.15);
    }}

    .result-label {{
        color: var(--muted);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
    }}

    .result-value {{
        font: 700 32px 'Space Grotesk', sans-serif;
        margin: 8px 0;
    }}

    .result-details {{
        font-size: 12px;
        line-height: 1.9;
        color: #777c9b;
    }}

    /* Tabs and tables */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--surface2);
        border-radius: 15px;
        padding: 6px;
        gap: 7px;
        box-shadow:
            inset 3px 3px 6px var(--shadow1),
            inset -3px -3px 6px var(--shadow2);
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px;
        padding: 9px 15px;
    }}

    .stTabs [aria-selected="true"] {{
        background: var(--surface) !important;
        color: var(--ink) !important;
        box-shadow: 3px 3px 7px var(--shadow1),
                    -3px -3px 7px var(--shadow2);
    }}

    div[data-testid="stDataFrame"] {{
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid var(--line);
    }}

    div[data-testid="stAlert"] {{
        border-radius: 14px;
    }}

    .footer {{
        color: var(--muted);
        font-size: 10px;
        line-height: 1.8;
        margin-top: 28px;
        text-align: center;
    }}

    @media(max-width: 750px) {{
        .block-container {{
            padding: 1rem;
        }}

        .hero {{
            padding: 24px;
            border-radius: 23px;
        }}

        .clay-card {{
            padding: 18px;
        }}

        .metric-card {{
            padding: 14px;
        }}

        .metric-value {{
            font-size: 24px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# MODEL LOADING
# ==================================================
if not MODEL_PATH.exists():
    st.error(
        "The trained model is missing. Place "
        "`student_pass_model.joblib` beside `app.py`."
    )
    st.code(
        "python train_model.py\nstreamlit run app.py",
        language="bash",
    )
    st.stop()

try:
    model = joblib.load(MODEL_PATH)
except Exception as exc:
    st.error(f"Could not load the model: {exc}")
    st.stop()

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-icon">🎓</div>
          <div>
            <div class="brand-name">StudentAI</div>
            <div class="brand-sub">PERFORMANCE STUDIO</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Workspace")
    page = st.radio(
        "Navigate",
        [
            "Dashboard",
            "Prediction History",
            "About Model",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Appearance")
    selected_theme = st.selectbox(
        "Choose theme",
        ["Light", "Dark"],
        index=1 if dark else 0,
        label_visibility="collapsed",
        key="theme_picker",
    )

    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    st.divider()

    st.markdown("### Model status")
    st.success("Saved model loaded")
    st.caption("student_pass_model.joblib")

    st.markdown(
        """
        <div style="margin-top:25px">
          <div style="font-size:11px;color:#9297b2">
            MACHINE LEARNING PROJECT
          </div>
          <div style="font-size:11px;color:#9297b2">
            Educational use only
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==================================================
# DASHBOARD
# ==================================================
if page == "Dashboard":
    st.markdown(
        """
        <div class="hero">
          <div class="hero-tag">YOUR ACADEMIC WORKSPACE</div>
          <h1>Student Performance<br>Prediction Studio</h1>
          <p>
            Explore academic outcomes through a simple,
            interactive machine-learning experience.
            Enter study hours, generate predictions, and
            review your results in one place.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    history = st.session_state.history
    total = len(history)
    passes = sum(
        item["Prediction"] == "Pass"
        for item in history
    )
    fails = total - passes
    pass_rate = passes / total * 100 if total else 0

    # Metric cards
    metrics = [
        ("TOTAL PREDICTIONS", total, "Current session", "↗"),
        ("PREDICTED PASS", passes, "Model output", "✓"),
        ("PREDICTED FAIL", fails, "Model output", "!"),
        (
            "SESSION PASS RATE",
            f"{pass_rate:.1f}%" if total else "—",
            "Not actual class performance",
            "%",
        ),
    ]

    metric_columns = st.columns(4, gap="medium")

    for col, (label, value, note, icon) in zip(
        metric_columns, metrics
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                  <div class="metric-top">
                    <div class="metric-label">{label}</div>
                    <div class="metric-icon">{icon}</div>
                  </div>
                  <div class="metric-value">{value}</div>
                  <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # Prediction section heading
    title_col, action_col = st.columns(
        [4, 1.5],
        vertical_alignment="center",
    )

    with title_col:
        st.markdown(
            """
            <div class="section-heading"
                 style="font-size:23px;font-weight:700">
              Make a prediction
            </div>
            <div style="color:var(--muted);font-size:12px">
              Enter student details to begin a new assessment.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with action_col:
        if st.button(
            "＋ New Prediction",
            use_container_width=True,
        ):
            new_prediction()

    st.write("")

    left, right = st.columns(
        [1.05, 0.95],
        gap="large",
    )

    # ----------------------------------------------
    # Prediction form
    # ----------------------------------------------
    with left:
        st.markdown(
            """
            <div class="clay-card">
              <div class="card-heading">
                📝 &nbsp; Student information
              </div>
              <div class="card-description">
                Complete the form below. Only average daily
                study hours are used by the current model.
              </div>
            """,
            unsafe_allow_html=True,
        )

        version = st.session_state.form_version

        with st.form(
            f"prediction_form_{version}",
            clear_on_submit=False,
        ):
            student_name = st.text_input(
                "Student name",
                placeholder="e.g. Enter student name",
                key=f"name_{version}",
            )

            study_hours = st.number_input(
                "Average daily study hours",
                min_value=0.0,
                max_value=24.0,
                value=4.0,
                step=0.5,
                help=(
                    "Enter the average number of hours "
                    "the student studies daily."
                ),
                key=f"hours_{version}",
            )

            st.caption(
                "Use a value between 0 and 24 hours per day."
            )

            submitted = st.form_submit_button(
                "Generate prediction  →",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            if not student_name.strip():
                st.warning(
                    "Please enter the student's name."
                )
            else:
                try:
                    prediction = int(
                        model.predict(
                            [[float(study_hours)]]
                        )[0]
                    )

                    if prediction not in (0, 1):
                        st.error(
                            "Unexpected model output. "
                            "Expected 0 (Fail) or 1 (Pass)."
                        )
                    else:
                        result = (
                            "Pass" if prediction == 1 else "Fail"
                        )

                        item = {
                            "Student": student_name.strip(),
                            "Study Hours": float(study_hours),
                            "Prediction": result,
                            "Timestamp": datetime.now().strftime(
                                "%Y-%m-%d %H:%M"
                            ),
                        }

                        st.session_state.history.insert(
                            0, item
                        )
                        st.session_state.latest = item
                        st.rerun()

                except Exception as exc:
                    st.error(f"Prediction failed: {exc}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------
    # Latest result
    # ----------------------------------------------
    with right:
        latest = st.session_state.get("latest")

        st.markdown(
            """
            <div class="clay-card">
              <div class="card-heading">
                ✨ &nbsp; Latest prediction
              </div>
              <div class="card-description">
                Your most recent model-generated result.
              </div>
            """,
            unsafe_allow_html=True,
        )

        if latest:
            passed = latest["Prediction"] == "Pass"
            result_color = (
                C["pass"] if passed else C["fail"]
            )
            result_bg = (
                C["pass_bg"] if passed else C["fail_bg"]
            )
            result_class = (
                "result-pass" if passed else "result-fail"
            )
            symbol = "✓" if passed else "!"

            st.markdown(
                f"""
                <div class="result-card {result_class}">
                  <div class="result-label">
                    MODEL CLASSIFICATION
                  </div>
                  <div class="result-value"
                       style="color:{result_color}">
                    {symbol} {latest['Prediction']}
                  </div>
                  <div class="result-details">
                    <b>{latest['Student']}</b><br>
                    {latest['Study Hours']:g} study hours per day<br>
                    {latest['Timestamp']}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")

            st.markdown(
                "**Daily study hours**"
            )

            st.progress(
                min(latest["Study Hours"] / 24, 1.0),
                text=(
                    f"{latest['Study Hours']:g} of 24 hours"
                ),
            )

            st.caption(
                "The progress bar shows study time, "
                "not a passing probability."
            )

            if st.button(
                "＋ Start another prediction",
                use_container_width=True,
            ):
                new_prediction()

        else:
            st.markdown(
                """
                <div class="result-card"
                     style="background:var(--surface2);
                            border-color:var(--line)">
                  <div class="result-label">
                    WAITING FOR INPUT
                  </div>
                  <div class="result-value"
                       style="color:var(--muted)">
                    Your result will appear here
                  </div>
                  <div class="result-details">
                    Fill in the student information and select
                    Generate prediction to see the output.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------
    # Study hours analysis
    # ----------------------------------------------
    st.write("")
    st.markdown(
        """
        <div style="font-size:23px;font-weight:700">
          Study hours analysis
        </div>
        <div style="color:var(--muted);font-size:12px;
                    margin-bottom:16px">
          Explore the classifications produced by your saved model.
        </div>
        """,
        unsafe_allow_html=True,
    )

    hours_range = [
        x / 2 for x in range(0, 49)
    ]

    chart_df = pd.DataFrame(
        {"Study Hours": hours_range}
    )

    chart_df["Predicted Class"] = [
        int(model.predict([[hours]])[0])
        for hours in hours_range
    ]

    chart_df["Predicted Result"] = (
        chart_df["Predicted Class"]
        .map({0: "Fail", 1: "Pass"})
    )

    chart_left, chart_right = st.columns(
        [1.25, 0.85],
        gap="large",
    )

    with chart_left:
        st.markdown(
            """
            <div class="clay-card">
              <div class="card-heading">
                📈 &nbsp; Prediction by study hours
              </div>
              <div class="card-description">
                0 = Fail · 1 = Pass
              </div>
            """,
            unsafe_allow_html=True,
        )

        st.line_chart(
            chart_df.set_index("Study Hours")[
                ["Predicted Class"]
            ],
            height=300,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with chart_right:
        st.markdown(
            """
            <div class="clay-card">
              <div class="card-heading">
                Model output
              </div>
              <div class="card-description">
                Sample classifications across study-hour values.
              </div>
            """,
            unsafe_allow_html=True,
        )

        st.dataframe(
            chart_df[
                ["Study Hours", "Predicted Result"]
            ],
            use_container_width=True,
            hide_index=True,
            height=300,
        )

        st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# PREDICTION HISTORY PAGE
# ==================================================
elif page == "Prediction History":
    st.markdown(
        """
        <div class="hero">
          <div class="hero-tag">YOUR ACTIVITY</div>
          <h1>Prediction history</h1>
          <p>
            Review, export, and manage predictions made
            during this application session.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    history = st.session_state.history

    if history:
        history_df = pd.DataFrame(history)

        pass_count = sum(
            item["Prediction"] == "Pass"
            for item in history
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total records", len(history))

        with col2:
            st.metric("Predicted Pass", pass_count)

        with col3:
            st.metric(
                "Predicted Fail",
                len(history) - pass_count,
            )

        st.write("")

        st.markdown(
            '<div class="clay-card">'
            '<div class="card-heading">All predictions</div>'
            '<div class="card-description">'
            'Your newest predictions appear first.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        export_col, clear_col, _ = st.columns(
            [1.4, 1.7, 4]
        )

        with export_col:
            st.download_button(
                "↓ Export CSV",
                data=history_df.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="student_prediction_history.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with clear_col:
            if st.button(
                "Clear history",
                use_container_width=True,
            ):
                st.session_state.history = []
                st.session_state.pop("latest", None)
                st.rerun()

    else:
        st.markdown(
            """
            <div class="clay-card">
              <div class="card-heading">
                No predictions yet
              </div>
              <div class="card-description">
                Go to Dashboard to make your first prediction.
                Your results will appear here automatically.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Go to Dashboard →"):
            st.session_state["page"] = "Dashboard"
            st.rerun()

# ==================================================
# ABOUT MODEL PAGE
# ==================================================
elif page == "About Model":
    st.markdown(
        """
        <div class="hero">
          <div class="hero-tag">BEHIND THE PREDICTIONS</div>
          <h1>About the model</h1>
          <p>
            Learn how StudentAI loads a saved machine-learning
            model and uses it to predict academic outcomes.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            """
            <div class="clay-card">
              <div class="card-heading">
                ⚙️ &nbsp; How it works
              </div>
              <div class="card-description">
                The application follows five basic steps.
              </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            1. **Train:** `train_model.py` trains the model.
            2. **Save:** `joblib.dump()` saves the trained model.
            3. **Load:** `joblib.load()` loads the saved model.
            4. **Predict:** `model.predict()` receives study hours.
            5. **Display:** StudentAI displays Pass or Fail.
            """
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            """
            <div class="clay-card">
              <div class="card-heading">
                🧠 &nbsp; Model information
              </div>
              <div class="card-description">
                The current version uses one input feature.
              </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("**Model file:** `student_pass_model.joblib`")
        st.write("**Input:** Average daily study hours")
        st.write("**Output:** 0 = Fail, 1 = Pass")
        st.write("**Prediction range:** 0–24 study hours/day")

        st.markdown("</div>", unsafe_allow_html=True)

    st.warning(
        "Educational project only. The prediction is not a "
        "guaranteed academic result or a probability of passing. "
        "Actual model quality depends on the training dataset."
    )

# ==================================================
# FOOTER
# ==================================================
st.markdown(
    """
    <div class="footer">
      STUDENTAI · ACADEMIC PERFORMANCE STUDIO<br>
      Built for machine-learning education and experimentation.
      Predictions should not be treated as guaranteed outcomes.
    </div>
    """,
    unsafe_allow_html=True,
)