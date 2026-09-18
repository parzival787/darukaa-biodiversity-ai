"""
DARUKAA.EARTH - BIODIVERSITY INTELLIGENCE API

FastAPI integration layer.

Pipeline:

User Query
    ↓
Conversation Memory
    ↓
Retriever
    ↓
Ollama Reasoner
    ↓
Validator
    ↓
Biodiversity Health Score
    ↓
Structured API Response
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from core.retriever import BiodiversityRetriever
from core.reasoner import BiodiversityReasoner
from core.validator import BiodiversityValidator
from core.conversation import ConversationManager
from core.scoring import BiodiversityHealthScorer
from core.planner import create_intervention_plan
from core.geo import analyze_geographic_context


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Darukaa.Earth Biodiversity Intelligence API",
    description=(
        "AI-powered biodiversity and environmental "
        "intelligence system."
    ),
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# GLOBAL COMPONENTS
# ============================================================

print("=" * 60)
print("DARUKAA.EARTH - INITIALIZING API")
print("=" * 60)

try:

    retriever = BiodiversityRetriever()

    reasoner = BiodiversityReasoner()

    conversation_manager = ConversationManager(
        max_history=10
    )

    scorer = BiodiversityHealthScorer()

    print("Retriever: READY")
    print("Reasoner: READY")
    print("Conversation Manager: READY")
    print("Health Scorer: READY")

except Exception as exc:

    print(
        f"WARNING: Component initialization failed: {exc}"
    )

    retriever = None
    reasoner = None
    conversation_manager = ConversationManager(
        max_history=10
    )
    scorer = BiodiversityHealthScorer()


# ============================================================
# REQUEST MODELS
# ============================================================


class ChatRequest(BaseModel):
    """
    Natural-language chat request.
    """

    message: str = Field(
        ...,
        min_length=1,
        description="User's environmental question.",
    )

    session_id: str = Field(
        default="default-session",
        description="Conversation session identifier.",
    )


class AnalyzeRequest(BaseModel):
    """
    Structured environmental analysis request.
    """

    soil_organic_carbon: float | None = None

    soil_ph: float | None = None

    rainfall: str | float | None = None

    land_use: str | None = None

    crop_type: str | None = None

    region: str | None = None

    temperature: float | None = None

    biodiversity_status: str | None = None

    soil_type: str | None = None

    session_id: str = "default-session"

    message: str = (
        "Analyze the environmental conditions "
        "and provide biodiversity recommendations."
    )


# ============================================================
# RESPONSE HELPERS
# ============================================================


def build_environment(
    request: AnalyzeRequest,
) -> dict[str, Any]:
    """
    Convert structured request fields into the common
    environmental-variable dictionary.
    """

    environment: dict[str, Any] = {}

    fields = {
        "soil_organic_carbon": request.soil_organic_carbon,
        "soil_ph": request.soil_ph,
        "rainfall": request.rainfall,
        "land_use": request.land_use,
        "crop_type": request.crop_type,
        "region": request.region,
        "temperature": request.temperature,
        "biodiversity_status": request.biodiversity_status,
        "soil_type": request.soil_type,
    }

    for key, value in fields.items():

        if value is not None:

            if isinstance(value, str) and not value.strip():
                continue

            environment[key] = value

    return environment


def merge_environment(
    extracted: dict[str, Any],
    existing: dict[str, Any],
) -> dict[str, Any]:
    """
    Merge newly extracted information with accumulated
    conversation information.

    New non-empty values take precedence.
    """

    merged = dict(existing)

    for key, value in extracted.items():

        if value is None:
            continue

        if isinstance(value, str) and not value.strip():
            continue

        merged[key] = value

    return merged


def safe_reasoner_call(
    query: str,
    environmental_variables: dict[str, Any],
    evidence: list[dict[str, Any]],
    history: list[dict[str, str]],
) -> dict[str, Any]:
    """
    Call the existing local Ollama reasoner using its
    actual interface.
    """

    if reasoner is None:
        raise RuntimeError(
            "Reasoner is not initialized."
        )

    return reasoner.reason(
        query=query,
        variables=environmental_variables,
        evidence=evidence,
        history=history,
    )

    # --------------------------------------------------------
    # Primary interface
    # --------------------------------------------------------

    if hasattr(reasoner, "reason"):

        try:

            return reasoner.reason(
                query=query,
                environmental_variables=environmental_variables,
                retrieved_evidence=evidence,
                conversation_history=history,
            )

        except TypeError:
            pass

    # --------------------------------------------------------
    # Alternative interface
    # --------------------------------------------------------

    if hasattr(reasoner, "generate"):

        try:

            return reasoner.generate(
                query=query,
                environmental_variables=environmental_variables,
                retrieved_evidence=evidence,
                conversation_history=history,
            )

        except TypeError:
            pass

    # --------------------------------------------------------
    # Fail clearly
    # --------------------------------------------------------

    raise RuntimeError(
        "Could not find a compatible reasoning method "
        "in BiodiversityReasoner."
    )


# ============================================================
# HEALTH ENDPOINT
# ============================================================


@app.get("/health")
def health() -> dict[str, Any]:
    """
    Basic API health check.
    """

    return {
        "status": "healthy",
        "service": (
            "Darukaa.Earth Biodiversity "
            "Intelligence API"
        ),
        "version": "1.0.0",
        "components": {
            "retriever": retriever is not None,
            "reasoner": reasoner is not None,
            "conversation_memory": True,
            "health_scorer": scorer is not None,
            "intervention_planner": True,
            "geographic_context": True,
        },
    }


# ============================================================
# ROOT ENDPOINT
# ============================================================


@app.get("/")
def root() -> dict[str, Any]:
    """
    API information.
    """

    return {
        "message": (
            "Darukaa.Earth Biodiversity "
            "Intelligence API"
        ),
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "/health",
            "/chat",
            "/analyze",
        ],
    }


# ============================================================
# CHAT ENDPOINT
# ============================================================


@app.post("/chat")
def chat(
    request: ChatRequest,
) -> dict[str, Any]:

    if retriever is None or reasoner is None:

        raise HTTPException(
            status_code=503,
            detail="AI components are not initialized.",
        )

    session_id = request.session_id.strip()

    if not session_id:

        session_id = "default-session"

    # --------------------------------------------------------
    # Get previous memory
    # --------------------------------------------------------

    existing_environment = (
        conversation_manager.get_environment(
            session_id
        )
    )

    history = (
        conversation_manager.get_history_for_llm(
            session_id
        )
    )

    # --------------------------------------------------------
    # Retrieve evidence + extract variables
    # --------------------------------------------------------

    try:

        retrieval_result = retriever.retrieve(
            request.message
        )

    except TypeError:

        # Some retriever implementations use query=.
        retrieval_result = retriever.retrieve(
            query=request.message
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Retrieval failed: {exc}",
        )

    # --------------------------------------------------------
    # Normalize retrieval result
    # --------------------------------------------------------

    if isinstance(retrieval_result, dict):

        extracted_variables = (
            retrieval_result.get(
                "environmental_variables",
                {},
            )
        )

        evidence = (
            retrieval_result.get(
                "evidence",
                retrieval_result.get(
                    "retrieved_evidence",
                    retrieval_result.get(
                        "results",
                        [],
                    ),
                ),
            )
        )

    else:

        extracted_variables = {}

        evidence = retrieval_result

    if not isinstance(
        extracted_variables,
        dict,
    ):

        extracted_variables = {}

    if not isinstance(
        evidence,
        list,
    ):

        evidence = []

    # --------------------------------------------------------
    # Combine current + previous environment
    # --------------------------------------------------------

    environment = merge_environment(
        extracted_variables,
        existing_environment,
    )

    # --------------------------------------------------------
    # Save current environmental state
    # --------------------------------------------------------

    conversation_manager.update_environment(
        session_id,
        environment,
    )

    # Get the final accumulated state.
    environment = (
        conversation_manager.get_environment(
            session_id
        )
    )

    # --------------------------------------------------------
    # Generate reasoning
    # --------------------------------------------------------

    try:

        reasoning = safe_reasoner_call(
            query=request.message,
            environmental_variables=environment,
            evidence=evidence,
            history=history,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Reasoning failed: {exc}",
        )

    # --------------------------------------------------------
    # Geographic context
    # --------------------------------------------------------

    geo_context = analyze_geographic_context(
        environment
    )

    # --------------------------------------------------------
    # Intervention planning
    # --------------------------------------------------------

    recommendations = reasoning.get(
        "recommendations",
        [],
    )

    intervention_plan = create_intervention_plan(
        recommendations
    )

    # --------------------------------------------------------
    # Validate reasoning
    # --------------------------------------------------------

    validator = BiodiversityValidator(
        retrieved_evidence=evidence,
        environmental_variables=environment,
    )

    validation = validator.validate(
        reasoning
    )

    # --------------------------------------------------------
    # Calculate biodiversity health
    # --------------------------------------------------------

    health_score = scorer.calculate(
        environment
    )

    # --------------------------------------------------------
    # Save conversation turn
    # --------------------------------------------------------

    conversation_manager.add_turn(
        session_id=session_id,
        user_message=request.message,
        assistant_response=reasoning,
    )

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {
        "success": True,
        "session_id": session_id,
        "query": request.message,
        "environmental_variables": environment,
        "retrieved_evidence": evidence,
        "reasoning": reasoning,
        "validation": validation,
        "biodiversity_health": health_score,
        "geographic_context": geo_context,
        "intervention_plan": intervention_plan,
        "conversation": {
            "turn_count": (
                conversation_manager
                .get_context(session_id)
                .get("turn_count", 0)
            ),
        },
    }


# ============================================================
# STRUCTURED ANALYZE ENDPOINT
# ============================================================


@app.post("/analyze")
def analyze(
    request: AnalyzeRequest,
) -> dict[str, Any]:

    if retriever is None or reasoner is None:

        raise HTTPException(
            status_code=503,
            detail="AI components are not initialized.",
        )

    session_id = request.session_id.strip()

    if not session_id:

        session_id = "default-session"

    # --------------------------------------------------------
    # Structured environment
    # --------------------------------------------------------

    provided_environment = build_environment(
        request
    )

    # --------------------------------------------------------
    # Previous memory
    # --------------------------------------------------------

    previous_environment = (
        conversation_manager.get_environment(
            session_id
        )
    )

    history = (
        conversation_manager.get_history_for_llm(
            session_id
        )
    )

    # --------------------------------------------------------
    # Merge structured values into memory
    # --------------------------------------------------------

    environment = merge_environment(
        provided_environment,
        previous_environment,
    )

    conversation_manager.update_environment(
        session_id,
        environment,
    )

    environment = (
        conversation_manager.get_environment(
            session_id
        )
    )

    # --------------------------------------------------------
    # Retrieve scientific evidence
    # --------------------------------------------------------

    try:

        retrieval_result = retriever.retrieve(
            request.message
        )

    except TypeError:

        retrieval_result = retriever.retrieve(
            query=request.message
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Retrieval failed: {exc}",
        )

    # --------------------------------------------------------
    # Normalize retrieval result
    # --------------------------------------------------------

    if isinstance(retrieval_result, dict):

        evidence = retrieval_result.get(
            "evidence",
            retrieval_result.get(
                "retrieved_evidence",
                retrieval_result.get(
                    "results",
                    [],
                ),
            ),
        )

    else:

        evidence = retrieval_result

    if not isinstance(
        evidence,
        list,
    ):

        evidence = []

    # --------------------------------------------------------
    # Reasoning
    # --------------------------------------------------------

    try:

        reasoning = safe_reasoner_call(
            query=request.message,
            environmental_variables=environment,
            evidence=evidence,
            history=history,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Reasoning failed: {exc}",
        )

    # --------------------------------------------------------
    # Geographic context
    # --------------------------------------------------------

    geo_context = analyze_geographic_context(
        environment
    )

    # --------------------------------------------------------
    # Intervention planning
    # --------------------------------------------------------

    recommendations = reasoning.get(
        "recommendations",
        [],
    )

    intervention_plan = create_intervention_plan(
        recommendations
    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    validator = BiodiversityValidator(
        retrieved_evidence=evidence,
        environmental_variables=environment,
    )

    validation = validator.validate(
        reasoning
    )

    # --------------------------------------------------------
    # Biodiversity score
    # --------------------------------------------------------

    health_score = scorer.calculate(
        environment
    )

    # --------------------------------------------------------
    # Store conversation
    # --------------------------------------------------------

    conversation_manager.add_turn(
        session_id=session_id,
        user_message=request.message,
        assistant_response=reasoning,
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "success": True,
        "session_id": session_id,
        "environmental_variables": environment,
        "retrieved_evidence": evidence,
        "reasoning": reasoning,
        "validation": validation,
        "biodiversity_health": health_score,
        "geographic_context": geo_context,
        "intervention_plan": intervention_plan,
    }


# ============================================================
# STARTUP MESSAGE
# ============================================================


@app.on_event("startup")
async def startup_event():

    print("=" * 60)
    print("DARUKAA.EARTH API STARTED")
    print("=" * 60)

    print("Swagger UI:")
    print("http://127.0.0.1:8000/docs")

    print("\nHealth:")
    print("http://127.0.0.1:8000/health")

    print("=" * 60)