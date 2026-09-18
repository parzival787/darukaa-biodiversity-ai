"""
Darukaa.Earth — AI Biodiversity Intelligence
Streamlit demonstration interface.

Connects to the existing FastAPI backend:
    GET  /health
    POST /chat
    POST /analyze

The UI intentionally contains no scientific reasoning logic.
All recommendations, evidence, validation, health scoring, geo context,
and planning come from the existing backend.
"""

from __future__ import annotations

import json
import os
import uuid
from typing import Any

import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_API_URL = "http://127.0.0.1:8000"
API_URL = os.getenv("DARUKAA_API_URL", DEFAULT_API_URL).rstrip("/")
REQUEST_TIMEOUT = 180


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Darukaa.Earth | Biodiversity Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lora:wght@400;600&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0e1a12;
    }

    .main .block-container {
        padding-top: 0;
        padding-bottom: 3rem;
        max-width: 1300px;
    }

    /* ── Hero ── */
    .hero-wrap {
        background: linear-gradient(160deg, #112018 0%, #0e1a12 60%, #091510 100%);
        border-bottom: 1px solid #1f3328;
        padding: 2.5rem 2rem 2rem;
        margin-bottom: 2rem;
    }

    .hero-eyebrow {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        color: #4caf7d;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .hero-title {
        font-family: 'Lora', Georgia, serif;
        font-size: 2.4rem;
        font-weight: 600;
        color: #e8f5ec;
        line-height: 1.2;
        margin: 0 0 0.6rem;
    }

    .hero-sub {
        font-size: 0.95rem;
        color: #6b9a7a;
        max-width: 560px;
        line-height: 1.6;
        margin: 0;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: #111f17;
        border: 1px solid #1e3328;
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        min-height: 100px;
    }

    .metric-title {
        font-size: 0.73rem;
        font-weight: 500;
        color: #5a8a6a !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #d4eed9 !important;
        line-height: 1.1;
    }

    .metric-sub {
        font-size: 0.82rem;
        color: #7aab8a !important;
        margin-top: 0.3rem;
    }

    /* ── Rec cards ── */
    .rec-card {
        background: #111f17;
        border: 1px solid #1e3328;
        border-radius: 14px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1.2rem;
    }

    .rec-index {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        color: #4caf7d;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .rec-action {
        font-size: 1.05rem;
        font-weight: 600;
        color: #e8f5ec;
        line-height: 1.4;
        margin-bottom: 0.9rem;
    }

    .rec-body {
        font-size: 0.9rem;
        color: #8fb89a;
        line-height: 1.65;
    }

    /* ── Tag pills ── */
    .tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        margin: 0.15rem 0.2rem 0.15rem 0;
        border-radius: 999px;
        background: #162a1e;
        border: 1px solid #2a4a35;
        color: #7fc99a !important;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* ── Source box ── */
    .source-box {
        background: #0d1a11;
        border-left: 3px solid #2e7d4f;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        font-size: 0.85rem;
        color: #7aab8a !important;
        margin-top: 0.9rem;
    }

    /* ── Stat grid ── */
    .stat-row {
        display: flex;
        gap: 0.6rem;
        margin-top: 0.9rem;
    }

    .stat-item {
        flex: 1;
        background: #0d1a11;
        border: 1px solid #1a2e21;
        border-radius: 9px;
        padding: 0.7rem 0.9rem;
    }

    .stat-label {
        font-size: 0.7rem;
        color: #4e7a5e !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.2rem;
    }

    .stat-value {
        font-size: 0.88rem;
        font-weight: 600;
        color: #c8e6cc !important;
    }

    /* ── Health score ring ── */
    .health-wrap {
        background: #111f17;
        border: 1px solid #1e3328;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
    }

    .health-score {
        font-size: 3rem;
        font-weight: 700;
        color: #4caf7d !important;
        line-height: 1;
    }

    .health-label {
        font-size: 0.73rem;
        font-weight: 600;
        color: #5a8a6a !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.3rem;
    }

    .health-interp {
        font-size: 0.88rem;
        color: #7aab8a !important;
        margin-top: 0.4rem;
    }

    /* ── Geo card ── */
    .geo-card {
        background: #111f17;
        border: 1px solid #1e3328;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        height: 100%;
    }

    /* ── Section titles ── */
    .section-title {
        font-family: 'Lora', Georgia, serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: #c8e6cc;
        margin-bottom: 1rem;
    }

    .section-eyebrow {
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        color: #4caf7d;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    /* ── Chat styles ── */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
    }

    [data-testid="stChatMessageContent"] {
        background: #111f17 !important;
        border: 1px solid #1e3328 !important;
        border-radius: 12px !important;
        color: #c8e6cc !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #090f0c !important;
        border-right: 1px solid #172218 !important;
    }

    [data-testid="stSidebar"] * {
        color: #9fc8ab !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #d4eed9 !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: #1a3325 !important;
        border: 1px solid #2a4a35 !important;
        color: #a8d5b5 !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #2e7d4f !important;
        border-color: #3d9e64 !important;
        color: #e8f5ec !important;
    }

    /* ── Input ── */
    .stChatInputContainer textarea {
        background: #111f17 !important;
        border: 1px solid #2a4035 !important;
        border-radius: 12px !important;
        color: #e8f5ec !important;
    }

    /* ── Divider ── */
    hr {
        border-color: #1a2e21 !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Plan stage ── */
    .plan-stage {
        background: #111f17;
        border: 1px solid #1e3328;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    .plan-stage-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: #c8e6cc;
        margin-bottom: 0.2rem;
    }

    .plan-stage-period {
        font-size: 0.78rem;
        color: #5a8a6a;
        margin-bottom: 0.7rem;
    }

    .plan-action-row {
        display: flex;
        align-items: flex-start;
        gap: 0.7rem;
        padding: 0.6rem 0;
        border-top: 1px solid #152219;
    }

    .plan-priority {
        background: #162a1e;
        border: 1px solid #2a4035;
        color: #4caf7d !important;
        font-size: 0.7rem;
        font-weight: 700;
        border-radius: 6px;
        padding: 0.15rem 0.45rem;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }

    /* ── Signals ── */
    .signal-item {
        background: #0d1a11;
        border-left: 2px solid #2e7d4f;
        padding: 0.4rem 0.75rem;
        margin-bottom: 0.35rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.85rem;
        color: #8fb89a !important;
    }

    /* ── Info empty state ── */
    .empty-state {
        background: #0d1a11;
        border: 1px dashed #1e3328;
        border-radius: 14px;
        padding: 2.5rem;
        text-align: center;
        color: #4e7a5e !important;
    }

    .empty-icon {
        font-size: 2.5rem;
        margin-bottom: 0.7rem;
    }

    .empty-text {
        font-size: 0.9rem;
        color: #5a8a6a !important;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "api_url" not in st.session_state:
    st.session_state.api_url = API_URL


# ============================================================
# HELPERS
# ============================================================

def api_request(
    method: str,
    endpoint: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Call the existing FastAPI backend."""
    url = f"{st.session_state.api_url}{endpoint}"

    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=20)
        else:
            response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            raise RuntimeError("API returned an unexpected response format.")

        return data

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Could not connect to the FastAPI backend. "
            "Start it with: python -m uvicorn api.main:app --reload"
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "The backend request timed out while generating the analysis."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        detail = ""
        try:
            detail = response.json().get("detail", "")
        except Exception:
            pass
        raise RuntimeError(
            f"API request failed ({response.status_code}). {detail}"
        ) from exc

    except ValueError as exc:
        raise RuntimeError("The backend returned invalid JSON.") from exc


def send_chat(message: str) -> dict[str, Any]:
    return api_request(
        "POST",
        "/chat",
        {
            "message": message,
            "session_id": st.session_state.session_id,
        },
    )


def send_structured_analysis(
    soil_organic_carbon: float | None,
    soil_ph: float | None,
    rainfall: str | None,
    land_use: str | None,
    crop_type: str | None,
    region: str | None,
    temperature: float | None,
) -> dict[str, Any]:
    return api_request(
        "POST",
        "/analyze",
        {
            "soil_organic_carbon": soil_organic_carbon,
            "soil_ph": soil_ph,
            "rainfall": rainfall,
            "land_use": land_use,
            "crop_type": crop_type,
            "region": region,
            "temperature": temperature,
            "session_id": st.session_state.session_id,
        },
    )


def get_nested(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
    return default if current is None else current


def render_health_score(health: dict[str, Any]) -> None:
    score = health.get("score")
    interpretation = health.get("interpretation", "Unknown")

    if isinstance(score, (int, float)):
        score_text = f"{score:.0f}"
        score_color = (
            "#4caf7d" if score >= 70
            else "#e6a817" if score >= 40
            else "#e05252"
        )
    else:
        score_text = "—"
        score_color = "#4caf7d"

    st.markdown(
        f"""
        <div class="health-wrap">
            <div class="health-label">Biodiversity Health</div>
            <div class="health-score" style="color:{score_color} !important">{score_text}<span style="font-size:1.2rem;color:#4e7a5e;font-weight:400">/100</span></div>
            <div class="health-interp">{interpretation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if health.get("scientific_validation") is False:
        st.caption("Heuristic prototype score — not scientifically validated.")


def render_environment(environment: dict[str, Any]) -> None:
    if not environment:
        st.info("No environmental variables were extracted yet.")
        return

    items = list(environment.items())
    cols = st.columns(min(max(len(items), 1), 4))

    for i, (key, value) in enumerate(items):
        col = cols[i % len(cols)]
        label = key.replace("_", " ").title()
        col.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_recommendations(reasoning: dict[str, Any]) -> None:
    recommendations = reasoning.get("recommendations", [])

    if not recommendations:
        st.warning("No evidence-grounded recommendations were returned.")
        return

    st.markdown('<div class="section-eyebrow">Evidence-grounded</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)

    for index, rec in enumerate(recommendations, start=1):
        action = rec.get("action", "")
        scientific_reasoning = rec.get("scientific_reasoning", "")
        variables = rec.get("environmental_variables_used", [])
        metrics = rec.get("impacted_metrics", [])
        estimate = rec.get("improvement_estimate", "")
        citation = rec.get("source_citation", "")
        horizon = rec.get("time_horizon", "")
        confidence = rec.get("confidence", "")

        tags_html = ""
        for v in variables:
            tags_html += f'<span class="tag">{v}</span>'
        for m in metrics:
            tags_html += f'<span class="tag">↑ {m}</span>'

        st.markdown(
            f"""
            <div class="rec-card">
                <div class="rec-index">Recommendation {index}</div>
                <div class="rec-action">{action}</div>
                <div class="rec-body">{scientific_reasoning}</div>
                {f'<div style="margin-top:0.85rem">{tags_html}</div>' if tags_html else ""}
                <div class="stat-row">
                    <div class="stat-item">
                        <div class="stat-label">Time horizon</div>
                        <div class="stat-value">{horizon or "Not specified"}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Confidence</div>
                        <div class="stat-value">{confidence or "Not specified"}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Est. improvement</div>
                        <div class="stat-value">{estimate or "Not specified"}</div>
                    </div>
                </div>
                {f'<div class="source-box"><strong>Retrieved evidence:</strong> {citation}</div>' if citation else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_evidence(evidence: list[dict[str, Any]]) -> None:
    st.markdown('<div class="section-eyebrow">Knowledge base</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Retrieved Scientific Evidence</div>', unsafe_allow_html=True)

    if not evidence:
        st.info("No evidence chunks were retrieved.")
        return

    with st.expander(f"Show {len(evidence)} retrieved knowledge chunks", expanded=False):
        for index, item in enumerate(evidence, start=1):
            source = item.get("source", "Unknown source")
            year = item.get("source_year", "")
            topic = item.get("topic", "Unknown topic")
            similarity = item.get("similarity")

            sim_text = f"{similarity:.3f}" if isinstance(similarity, (int, float)) else "N/A"

            st.markdown(f"**{index}. {topic}**")
            st.caption(f"Source: {source} · {year} · Similarity: {sim_text}")
            st.write(item.get("content", ""))

            metrics = item.get("metrics_affected", "")
            if metrics:
                st.caption(f"Metrics: {metrics}")

            if index < len(evidence):
                st.divider()


def render_geo(geo: dict[str, Any]) -> None:
    if not geo or not geo.get("available"):
        return

    region = geo.get("region", "Not specified")
    climate = geo.get("climate_context", "Not specified")
    signals = geo.get("environmental_signals", [])

    signals_html = ""
    for s in signals:
        signals_html += f'<div class="signal-item">{s}</div>'

    st.markdown(
        f"""
        <div class="geo-card">
            <div class="section-eyebrow">Geographic context</div>
            <div style="margin-top:0.8rem">
                <div class="stat-row">
                    <div class="stat-item">
                        <div class="stat-label">Region</div>
                        <div class="stat-value">{region}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Climate</div>
                        <div class="stat-value">{climate}</div>
                    </div>
                </div>
                {f'<div style="margin-top:0.85rem">{signals_html}</div>' if signals_html else ""}
            </div>
            <div style="font-size:0.72rem;color:#4e7a5e;margin-top:0.9rem">
                Data source: {geo.get("data_source", "N/A")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_plan(plan: dict[str, Any]) -> None:
    if not plan or not plan.get("plan_available"):
        return

    st.markdown('<div class="section-eyebrow">Roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Intervention Plan</div>', unsafe_allow_html=True)

    timeline = plan.get("timeline", [])

    for stage in timeline:
        label = stage.get("label", stage.get("stage", "Actions"))
        period = stage.get("period", "")
        purpose = stage.get("purpose", "")
        actions = stage.get("actions", [])

        actions_html = ""
        for action in actions:
            priority = action.get("priority", "")
            action_text = action.get("action", "")
            confidence = action.get("confidence", "")
            citation = action.get("source_citation", "")
            estimate = action.get("improvement_estimate", "")

            meta = " · ".join(filter(None, [
                f"Confidence: {confidence}" if confidence else "",
                f"Est: {estimate}" if estimate else "",
                f"Ref: {citation}" if citation else "",
            ]))

            actions_html += f"""
            <div class="plan-action-row">
                <span class="plan-priority">{priority}</span>
                <div>
                    <div style="font-size:0.88rem;color:#c8e6cc;font-weight:500">{action_text}</div>
                    {f'<div style="font-size:0.75rem;color:#5a8a6a;margin-top:0.15rem">{meta}</div>' if meta else ""}
                </div>
            </div>
            """

        st.markdown(
            f"""
            <div class="plan-stage">
                <div class="plan-stage-title">{label}</div>
                {f'<div class="plan-stage-period">{period}</div>' if period else ""}
                {f'<div style="font-size:0.85rem;color:#7aab8a;margin-bottom:0.6rem">{purpose}</div>' if purpose else ""}
                {actions_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_follow_up(reasoning: dict[str, Any]) -> None:
    missing = reasoning.get("missing_information", [])
    question = reasoning.get("follow_up_question", "")

    if missing:
        st.warning(
            "Additional information that could improve the analysis: "
            + ", ".join(missing)
        )

    if question:
        st.info(f"💬 {question}")


def render_validation(validation: dict[str, Any]) -> None:
    valid = validation.get("valid")
    score = validation.get("quality_score")

    if valid:
        st.success(f"Validation passed · Quality score: {score}/100")
    else:
        st.error(f"Validation requires attention · Quality score: {score}/100")

    warnings = validation.get("warnings", [])
    errors = validation.get("errors", [])

    if errors:
        with st.expander("Validation errors"):
            for error in errors:
                st.write(f"• {error}")

    if warnings:
        with st.expander("Validation warnings"):
            for warning in warnings:
                st.write(f"• {warning}")


def render_response(data: dict[str, Any]) -> None:
    st.session_state.last_response = data

    environment = data.get("environmental_variables", {})
    reasoning = data.get("reasoning", {})
    evidence = data.get("retrieved_evidence", [])
    health = data.get("biodiversity_health", {})
    validation = data.get("validation", {})
    geo = data.get("geographic_context", {})
    plan = data.get("intervention_plan", {})

    # ── Assessment ──
    assessment = reasoning.get("environmental_assessment", {})

    st.markdown('<div class="section-eyebrow">Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Environmental Overview</div>', unsafe_allow_html=True)

    if assessment.get("summary"):
        st.markdown(
            f'<div style="font-size:0.95rem;color:#8fb89a;line-height:1.65">{assessment["summary"]}</div>',
            unsafe_allow_html=True,
        )

    constraints = assessment.get("key_constraints", [])
    interactions = assessment.get("interactions", [])

    if constraints or interactions:
        col1, col2 = st.columns(2)
        with col1:
            if constraints:
                st.markdown("**Key constraints**")
                for c in constraints:
                    st.markdown(f'<div class="signal-item">{c}</div>', unsafe_allow_html=True)
        with col2:
            if interactions:
                st.markdown("**Variable interactions**")
                for i in interactions:
                    st.markdown(f'<div class="signal-item">{i}</div>', unsafe_allow_html=True)

    st.divider()

    # ── Env variables ──
    st.markdown('<div class="section-eyebrow">Inputs extracted</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Environmental Variables</div>', unsafe_allow_html=True)
    render_environment(environment)

    st.divider()

    # ── Health + Geo ──
    col1, col2 = st.columns([1, 2])
    with col1:
        render_health_score(health)
    with col2:
        render_geo(geo)

    st.divider()

    # ── Recommendations ──
    render_recommendations(reasoning)
    render_follow_up(reasoning)

    st.divider()

    # ── Plan ──
    render_plan(plan)

    if plan and plan.get("plan_available"):
        st.divider()

    # ── Validation ──
    render_validation(validation)

    st.divider()

    # ── Evidence ──
    render_evidence(evidence)

    st.divider()

    with st.expander("Raw API response (JSON)"):
        st.json(data)


def assistant_text(data: dict[str, Any]) -> str:
    reasoning = data.get("reasoning", {})
    assessment = reasoning.get("environmental_assessment", {})
    recommendations = reasoning.get("recommendations", [])
    summary = assessment.get("summary", "")

    if recommendations:
        actions = "\n".join(
            f"{i}. {item.get('action', '')}"
            for i, item in enumerate(recommendations, start=1)
        )
        return f"{summary}\n\nEvidence-grounded actions:\n{actions}"

    return summary or "Analysis completed."


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding:0.5rem 0 1.2rem">
            <div style="font-size:1.3rem;font-weight:700;color:#d4eed9">🌿 Darukaa.Earth</div>
            <div style="font-size:0.78rem;color:#4e7a5e;margin-top:0.15rem">AI Biodiversity Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Backend**")

    api_url_input = st.text_input("FastAPI URL", value=st.session_state.api_url)
    st.session_state.api_url = api_url_input.rstrip("/")

    if st.button("Check backend health", use_container_width=True):
        try:
            health_response = api_request("GET", "/health")
            st.success(f"Backend: {health_response.get('status', 'unknown')}")

            components = health_response.get("components", {})
            for component, available in components.items():
                icon = "✅" if available else "❌"
                st.write(f"{icon} {component.replace('_', ' ').title()}")

        except RuntimeError as exc:
            st.error(str(exc))

    st.markdown("---")
    st.markdown("**Structured Analysis**")
    st.caption("Optional structured inputs sent to the /analyze endpoint.")

    use_soc = st.checkbox("Provide soil organic carbon", value=True)
    soc = (
        st.number_input("Soil organic carbon (%)", min_value=0.0, max_value=20.0, value=0.3, step=0.1)
        if use_soc else None
    )

    use_ph = st.checkbox("Provide soil pH", value=False)
    soil_ph = (
        st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
        if use_ph else None
    )

    rainfall = st.selectbox(
        "Rainfall",
        ["very low", "low", "moderate", "high", "very high"],
        index=0,
    )

    land_use = st.selectbox(
        "Land use",
        ["monoculture", "mixed cropping", "agroforestry", "forest", "grassland", "wetland", "restored land"],
        index=0,
    )

    crop_type = st.text_input("Crop type", value="wheat")
    region = st.text_input("Region", value="semi-arid")

    use_temperature = st.checkbox("Provide temperature", value=True)
    temperature = (
        st.number_input("Temperature (°C)", min_value=-20.0, max_value=60.0, value=38.0, step=1.0)
        if use_temperature else None
    )

    analyze_button = st.button("Run analysis", type="primary", use_container_width=True)

    if analyze_button:
        structured_message = "Analyze this environmental profile using the provided structured variables."

        with st.spinner("Running biodiversity analysis..."):
            try:
                data = send_structured_analysis(
                    soil_organic_carbon=soc,
                    soil_ph=soil_ph,
                    rainfall=rainfall,
                    land_use=land_use,
                    crop_type=crop_type or None,
                    region=region or None,
                    temperature=temperature,
                )

                st.session_state.messages.append({"role": "user", "content": structured_message})
                st.session_state.messages.append({"role": "assistant", "content": assistant_text(data)})
                st.session_state.last_response = data
                st.rerun()

            except RuntimeError as exc:
                st.error(str(exc))

    st.markdown("---")

    if st.button("New conversation", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.last_response = None
        st.rerun()

    st.caption(f"Session: {st.session_state.session_id[:8]}…")


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-eyebrow">Biodiversity Intelligence Platform</div>
        <h1 class="hero-title">Darukaa.Earth</h1>
        <p class="hero-sub">
            Evidence-grounded AI for land health assessment, biodiversity
            recovery planning, and environmental decision support.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input("Describe your environmental situation or ask a biodiversity question…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving evidence and generating reasoning…"):
            try:
                data = send_chat(prompt)
                response_text = assistant_text(data)

                st.markdown(response_text)

                st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.session_state.last_response = data

            except RuntimeError as exc:
                error_text = f"⚠️ {exc}"
                st.error(error_text)
                st.session_state.messages.append({"role": "assistant", "content": error_text})


# ============================================================
# FULL ANALYSIS PANEL
# ============================================================

if st.session_state.last_response:
    st.markdown("---")
    render_response(st.session_state.last_response)
else:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">🌱</div>
            <div class="empty-text">
                Describe your land, soil, or ecosystem situation above,<br>
                or use Structured Analysis in the sidebar to run a parameterised assessment.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )