"""
Darukaa.Earth Biodiversity Intelligence
Local LLM Reasoning Engine  —  v2

Uses:
    Ollama
    llama3.2:3b  (or any installed model)

Pipeline:

    User Query
        ↓
    Environmental Variables  (from retriever)
        ↓
    ChromaDB Evidence  (from retriever)
        ↓
    PromptBuilder → Ollama LLM
        ↓
    ResponseParser → sanitized structured JSON
        ↓
    Caller (API / CLI)
"""

from __future__ import annotations

import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("darukaa.reasoner")


# =========================================================
# OLLAMA CONFIGURATION
# =========================================================

OLLAMA_URL            = "http://localhost:11434"
OLLAMA_CHAT_ENDPOINT  = f"{OLLAMA_URL}/api/chat"
OLLAMA_TAGS_ENDPOINT  = f"{OLLAMA_URL}/api/tags"
OLLAMA_MODEL          = "llama3.2:3b"

# Retry config
MAX_RETRIES           = 3
RETRY_BACKOFF_BASE    = 2.0      # seconds; doubles each attempt

# Per-attempt timeout (seconds)
REQUEST_TIMEOUT       = 180


# =========================================================
# PROMPT BUILDER
# =========================================================

class PromptBuilder:
    """
    Builds the full user-turn prompt from structured inputs.
    Keeping this separate makes unit-testing and prompt
    iteration straightforward without touching inference code.
    """

    # Maximum number of history turns to include
    HISTORY_WINDOW = 6

    # ── helpers ──────────────────────────────────────────

    @staticmethod
    def _format_variables(variables: dict[str, Any]) -> str:
        if not variables:
            return "No environmental variables were extracted."
        return "\n".join(f"- {k}: {v}" for k, v in variables.items())

    @staticmethod
    def _format_evidence(evidence: list[dict[str, Any]]) -> str:
        if not evidence:
            return "No scientific evidence was retrieved."

        blocks: list[str] = []

        for idx, item in enumerate(evidence, start=1):
            sim = item.get("similarity")
            sim_str = f"{sim:.4f}" if isinstance(sim, float) else "unknown"

            block = (
                f"EVIDENCE {idx}\n"
                f"ID:            {item.get('id', '')}\n"
                f"TOPIC:         {item.get('topic', '')}\n"
                f"SOURCE:        {item.get('source', '')}\n"
                f"YEAR:          {item.get('source_year', '')}\n"
                f"SIMILARITY:    {sim_str}\n"
                f"METRICS:       {item.get('metrics_affected', '')}\n"
                f"CLIMATE ZONES: {item.get('climate_zones', '')}\n"
                f"CONTENT:\n{item.get('content', '')}"
            )
            blocks.append(block)

        return "\n\n".join(blocks)

    @staticmethod
    def _format_history(history: list[dict[str, Any]] | None) -> str:
        if not history:
            return "No previous conversation."
        lines = [
            f"{msg.get('role','unknown').upper()}: {msg.get('content','')}"
            for msg in history[-PromptBuilder.HISTORY_WINDOW:]
        ]
        return "\n".join(lines)

    # ── public ───────────────────────────────────────────

    def build(
        self,
        query: str,
        variables: dict[str, Any],
        evidence: list[dict[str, Any]],
        history: list[dict[str, Any]] | None = None,
    ) -> str:
        """Return the complete prompt string."""

        n_evidence = len(evidence)
        valid_evidence_labels = ", ".join(
            f"EVIDENCE {i}" for i in range(1, n_evidence + 1)
        )
        valid_variable_names = ", ".join(variables.keys()) if variables else "none"

        prompt = f"""You are an environmental scientist for Darukaa.Earth.

Analyze the user's environmental situation using ONLY the variables and
retrieved scientific evidence provided below. Produce evidence-grounded,
practical biodiversity and environmental recommendations.

━━━ USER QUERY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{query}

━━━ ENVIRONMENTAL VARIABLES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Valid variable names (use these exactly in environmental_variables_used):
{valid_variable_names}

{self._format_variables(variables)}

━━━ CONVERSATION HISTORY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self._format_history(history)}

━━━ RETRIEVED SCIENTIFIC EVIDENCE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Valid citation labels: {valid_evidence_labels}

{self._format_evidence(evidence)}

━━━ STRICT RULES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDATION COUNT
• Produce EXACTLY 2 recommendations when the retrieved evidence supports
  two distinct interventions. One recommendation is acceptable only when
  the evidence genuinely covers only one actionable topic.
• Each recommendation MUST be grounded in a DIFFERENT evidence chunk.
  Do NOT cite the same EVIDENCE N label twice across the two recommendations.
• Do not fabricate a second recommendation if evidence does not support it.

CITATION RULES (non-negotiable)
• Every source_citation MUST be one of: {valid_evidence_labels}
• Cite only evidence that DIRECTLY supports the recommended action.
• Before selecting a citation, verify that the cited evidence supports the specific
  intervention being proposed.
• Do NOT use evidence merely because it contains a related environmental variable.
• Do NOT claim that evidence supports a specific outcome, species response,
  management practice, or intervention unless that evidence directly supports it.
• If no retrieved evidence directly supports an action, OMIT that action.
• NEVER invent studies, papers, statistics, or percentages.
• Each recommendation must cite a DIFFERENT evidence chunk.


VARIABLE RULES
• environmental_variables_used: only names from the valid variable list above.
• Metrics (biodiversity, soil health, water retention …) go in impacted_metrics.
• Each recommendation must reference ≥ 3 actual variables when at least
  3 relevant variables are available in the user's extracted inputs.
• The 3 variables must form a meaningful causal or environmental connection
  to the intervention. Do not add unrelated variables simply to reach 3.
• Use variables that are genuinely relevant to the recommended intervention.
• Do NOT add variables merely to reach the 3-variable requirement.
• environmental_variables_used must come only from the variables explicitly extracted
  from the user's query.
• Never treat an impacted metric as an environmental variable.
• Never invent a missing environmental variable. For example, if rainfall was not
  explicitly provided by the user, do not list rainfall as an environmental variable.

NUMERICAL EVIDENCE
• If retrieved evidence contains a quantitative result relevant to the
  recommendation, USE that number in improvement_estimate.
• Never transfer a number to an unrelated metric.
• If no relevant number exists write exactly:
  "Quantitative estimate unavailable from retrieved evidence"

REASONING QUALITY
• Analyze variable interactions, not each variable in isolation.
• Use hedged language: "may improve", "evidence suggests", "has been associated with".
• Give specific actions (e.g. "implement conservation tillage with cover cropping")
  not vague ones (e.g. "use sustainable farming").
• Link the proposed intervention explicitly to the environmental variables actually
  used in the recommendation.
• Identify at least 3 impacted metrics per recommendation where evidence supports it.
• Do not claim improvement in a metric unless the cited evidence supports that
  relationship.
• Do not infer species-specific benefits, such as increased pollinators or earthworms,
  unless the cited evidence directly supports those effects.


FOLLOW-UP QUESTION
• If missing_information is non-empty, follow_up_question MUST be a single,
  concrete question about the most important missing item.
• Do NOT ask users to explain the recommendation itself.

━━━ OUTPUT FORMAT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Return ONLY valid JSON — no markdown, no code fences, no preamble.

{{
  "environmental_assessment": {{
    "summary": "concise scientific assessment",
    "key_constraints": ["constraint 1", "constraint 2"],
    "interactions": ["interaction 1", "interaction 2"]
  }},
  "recommendations": [
    {{
      "action": "specific actionable intervention",
      "scientific_reasoning": "explanation linking intervention to user variables",
      "environmental_variables_used": ["var1", "var2", "var3"],
      "impacted_metrics": ["metric 1", "metric 2", "metric 3"],
      "improvement_estimate": "evidence-backed number or unavailability statement",
      "source_citation": "EVIDENCE N",
      "time_horizon": "short-term | medium-term | long-term",
      "confidence": "high | medium | low"
    }}
  ],
  "missing_information": ["missing variable"],
  "follow_up_question": "one concrete question or empty string",
  "overall_confidence": "high | medium | low"
}}

━━━ SELF-CHECK BEFORE RESPONDING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] recommendations array has 2 entries (or 1 only if evidence truly covers
    just one distinct intervention)
[ ] the two recommendations cite DIFFERENT evidence chunks
[ ] every source_citation is one of: {valid_evidence_labels}
[ ] each cited evidence chunk DIRECTLY supports the proposed intervention
[ ] no recommendation claims an outcome that is not supported by its cited evidence
[ ] environmental_variables_used contains only names from the valid list
[ ] environmental_variables_used contains only variables actually extracted
    from the user's query
[ ] each recommendation uses ≥ 3 relevant environmental variables when the
    query provides at least 3 relevant variables
[ ] no metric is incorrectly placed inside environmental_variables_used
[ ] numerical estimate comes from the cited evidence and applies to the correct metric
[ ] if no relevant numerical result exists, use exactly:
    "Quantitative estimate unavailable from retrieved evidence"
[ ] no invented citations, studies, statistics, or unsupported biological effects

Return ONLY the JSON object.

Return ONLY the JSON object."""

        return prompt


# =========================================================
# RESPONSE PARSER
# =========================================================

class ResponseParser:
    """
    Extracts and validates the structured JSON from raw LLM output.
    Handles markdown fences, leading prose, and partial JSON.
    """

    def parse(self, raw: str) -> dict[str, Any]:
        """Return parsed dict or raise ValueError."""

        text = raw.strip()

        # 1. Direct parse
        try:
            result = json.loads(text)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass

        # 2. Strip markdown fences
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text).strip()

        try:
            result = json.loads(text)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass

        # 3. Extract first {...} block
        start = text.find("{")
        end   = text.rfind("}")

        if start != -1 and end > start:
            try:
                result = json.loads(text[start : end + 1])
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError:
                pass

        raise ValueError(
            f"Ollama returned non-JSON output. "
            f"First 300 chars: {raw[:300]!r}"
        )


# =========================================================
# OUTPUT SANITIZER
# =========================================================

class OutputSanitizer:
    """
    Enforces output contracts without inventing scientific claims.

    Citation handling — three strict tiers:

      TIER 1 — Valid citation
        The LLM produced a correct EVIDENCE N label.
        → Accept as-is.

      TIER 2 — Topic-match repair
        The citation is missing or wrong, BUT the recommendation's
        action text contains a significant keyword from the evidence
        chunk's curated `topic` field.
        We use the topic field rather than full content overlap because
        `topic` is a short, curated label that names the intervention
        the chunk actually supports.  A content overlap match risks
        assigning evidence that merely mentions the same variables
        without supporting the specific action.
        → Repair: assign that chunk's label, downgrade confidence to
          "low", set citation_repaired=True so the UI can distinguish
          LLM-generated from system-repaired citations.

      TIER 3 — No defensible match
        No evidence chunk's topic meaningfully appears in the
        recommendation action text.
        → Drop the recommendation.  Scientific grounding cannot be
          established without a direct topic match.

    Variable handling:
      Remove names not present in the retrieved variable dict.
      After filtering, keep the recommendation but record a
      validation_flag so the caller/UI can surface the gap.
      This avoids silently fabricating variables to pad the count.

    validation_flags:
      Every issue that does not cause a drop is recorded in a
      top-level "validation_flags" list on the result dict.
      Each flag is a plain-English string.  The UI renders this
      as a warning panel; the validator can check the list
      programmatically.
    """

    # Minimum fraction of topic keywords that must appear in the
    # recommendation action to accept a topic-match repair.
    # Example: topic = "conservation tillage carbon sequestration"
    #          → keywords = {"conservation", "tillage", "carbon", "sequestration"}
    #          → rec action must contain ≥ 50% of those 4 words (≥ 2).
    _TOPIC_MATCH_THRESHOLD: float = 0.75

    # Deterministic fallback follow-up questions keyed by missing item
    _FOLLOW_UP_MAP: dict[str, str] = {
        "vegetation cover":
            "What percentage of the field currently has vegetation cover?",
        "irrigation availability":
            "Do you have access to irrigation during the dry season?",
        "field size":
            "What is the approximate size of the field in hectares?",
        "existing crop rotation":
            "Are you currently using crop rotation, or only growing one crop?",
        "pesticide use":
            "Which pesticides are currently being applied, and at what frequency?",
        "soil depth":
            "What is the approximate depth of the topsoil layer?",
        "distance to natural habitat":
            "How far is the field from the nearest natural habitat or protected area?",
        "slope or topography":
            "What is the approximate slope of the land?",
        "water table depth":
            "How deep is the water table in this area?",
    }

    # ── Topic-match repair ────────────────────────────────

    @staticmethod
    def _topic_keywords(topic: str) -> set[str]:
        """
        Extract meaningful keywords from a curated evidence topic.

        Topic labels may use underscores, so they are normalized to spaces.
        Generic environmental words are ignored because they do not identify
        a specific intervention or evidence area.
        """
        generic = {
            "soil", "water", "land", "use", "availability", "stress",
            "health", "environmental", "biodiversity", "system", "systems",
            "management", "region", "regions", "cycle", "impact", "impacts",
        }

        words = re.findall(r"[a-zA-Z]+", str(topic).replace("_", " "))
        return {
            w.lower()
            for w in words
            if len(w) > 3 and w.lower() not in generic
        }

    @staticmethod
    def _action_tokens(action: str) -> set[str]:
        """Return normalized action tokens without substring matching."""
        return {
            w.lower()
            for w in re.findall(r"[a-zA-Z]+", str(action))
            if len(w) > 3
        }

    def _topic_match_repair(
        self,
        rec: dict[str, Any],
        evidence: list[dict[str, Any]],
    ) -> tuple[str, float] | None:
        """
        Attempt a conservative citation repair using the curated topic only.

        At least 75% of the meaningful topic keywords must appear in the
        recommendation's action. The reasoning text is intentionally excluded
        because it can echo evidence language without the action itself being
        supported.

        Repaired citations are always marked by the caller and confidence is
        downgraded to low.
        """
        action_tokens = self._action_tokens(rec.get("action", ""))

        if not action_tokens:
            return None

        best_label: str | None = None
        best_score: float = 0.0

        for idx, ev in enumerate(evidence, start=1):
            keywords = self._topic_keywords(ev.get("topic", ""))

            if not keywords:
                continue

            matched = sum(1 for kw in keywords if kw in action_tokens)
            score = matched / len(keywords)

            if score > best_score:
                best_score = score
                best_label = f"EVIDENCE {idx}"

        if best_label and best_score >= self._TOPIC_MATCH_THRESHOLD:
            return best_label, best_score

        return None

    @staticmethod
    def _validate_single_grounded_citation(
        citation: str,
        evidence: list[dict[str, Any]],
    ) -> bool:
        """Validate that a recommendation cites exactly one retrieved evidence chunk."""
        citation = str(citation).strip()

        if not re.fullmatch(r"EVIDENCE \d+", citation):
            return False

        match = re.fullmatch(r"EVIDENCE (\d+)", citation)
        if not match:
            return False

        index = int(match.group(1))
        return 1 <= index <= len(evidence)

    # ── Public ────────────────────────────────────────────

    def sanitize(
        self,
        result: dict[str, Any],
        variables: dict[str, Any],
        evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:

        valid_variables = set(variables.keys())
        valid_citations = {f"EVIDENCE {i}" for i in range(1, len(evidence) + 1)}

        # Accumulate non-fatal issues here so callers and the UI
        # can surface them without parsing log lines.
        validation_flags: list[str] = []

        # ── Recommendations ──────────────────────────────
        raw_recs = result.get("recommendations", [])
        if not isinstance(raw_recs, list):
            raw_recs = []

        clean_recs: list[dict[str, Any]] = []

        for rec_idx, rec in enumerate(raw_recs, start=1):
            if not isinstance(rec, dict):
                continue

            # 1. Restrict variables to known retrieved inputs
            used = rec.get("environmental_variables_used", [])
            if not isinstance(used, list):
                used = []

            filtered_vars = [v for v in used if v in valid_variables]
            removed       = set(used) - set(filtered_vars)

            if removed:
                msg = (
                    f"Recommendation {rec_idx}: removed out-of-scope "
                    f"variable(s) {sorted(removed)} — these are metrics, "
                    f"not environmental inputs."
                )
                logger.warning(msg)
                validation_flags.append(msg)

            rec["environmental_variables_used"] = filtered_vars

            # Record (don't drop) if fewer than 3 valid variables remain
            if len(filtered_vars) < 3:
                msg = (
                    f"Recommendation {rec_idx}: only {len(filtered_vars)} "
                    f"valid environmental variable(s) after filtering "
                    f"(expected ≥ 3). Evidence coverage may be narrow."
                )
                logger.warning(msg)
                validation_flags.append(msg)

            # 2. Citation validation
            # Each recommendation must have exactly ONE valid evidence label.
            citation = str(rec.get("source_citation", "")).strip()

            if self._validate_single_grounded_citation(
                citation=citation,
                evidence=evidence,
            ):
                rec["source_citation"] = citation
                rec["citation_repaired"] = False
                clean_recs.append(rec)
                continue

            msg = (
                f"Recommendation {rec_idx}: invalid citation {citation!r}. "
                "Each recommendation must cite exactly one retrieved evidence chunk."
            )
            logger.warning(msg)
            validation_flags.append(msg)

            rec["source_citation"] = citation
            rec["citation_repaired"] = False
            clean_recs.append(rec)

        result["recommendations"]  = clean_recs
        result["validation_flags"] = validation_flags

        # ── Scalar fields ─────────────────────────────────
        if not isinstance(result.get("missing_information"), list):
            result["missing_information"] = []

        if not isinstance(result.get("follow_up_question"), str):
            result["follow_up_question"] = ""

        if not isinstance(result.get("overall_confidence"), str):
            result["overall_confidence"] = "low"

        # ── Fallback follow-up question ───────────────────
        missing  = result["missing_information"]
        question = result["follow_up_question"].strip()

        if missing and not question:
            first = str(missing[0]).strip().lower()
            result["follow_up_question"] = self._FOLLOW_UP_MAP.get(
                first,
                f"Can you provide information about {first}?",
            )

        return result


# =========================================================
# BIODIVERSITY REASONER
# =========================================================

class BiodiversityReasoner:
    """
    Orchestrates prompt building, Ollama inference (with retry),
    response parsing, and output sanitization.
    """

    def __init__(
        self,
        model: str = OLLAMA_MODEL,
        max_retries: int = MAX_RETRIES,
        request_timeout: int = REQUEST_TIMEOUT,
    ) -> None:

        self.model           = model
        self.max_retries     = max_retries
        self.request_timeout = request_timeout

        self._prompt_builder = PromptBuilder()
        self._parser         = ResponseParser()
        self._sanitizer      = OutputSanitizer()

        self._verify_ollama()

        logger.info("Reasoner ready — model: %s", self.model)

    # ── Startup checks ────────────────────────────────────

    def _verify_ollama(self) -> None:
        """Confirm Ollama is running and the model is installed."""

        try:
            requests.get(OLLAMA_URL, timeout=5).raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(
                "Ollama is not reachable at "
                f"{OLLAMA_URL}. Start it and retry."
            ) from exc

        try:
            data            = requests.get(OLLAMA_TAGS_ENDPOINT, timeout=10).json()
            installed       = [m.get("name", "") for m in data.get("models", [])]
            # Ollama sometimes strips ":latest" — compare without tag too
            model_base      = self.model.split(":")[0]
            available       = any(
                m == self.model or m.split(":")[0] == model_base
                for m in installed
            )
        except requests.RequestException as exc:
            raise RuntimeError("Could not query Ollama model list.") from exc

        if not available:
            raise RuntimeError(
                f"Model '{self.model}' is not installed.\n"
                f"Installed: {installed}\n"
                f"Run:  ollama pull {self.model}"
            )

    # ── Inference with retry ──────────────────────────────

    def _call_ollama(self, prompt: str) -> str:
        """
        POST to Ollama with exponential-backoff retry.
        Returns the raw response text.
        """

        payload = {
            "model":    self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream":   False,
            "format":   "json",
            "options":  {"temperature": 0},
        }

        last_exc: Exception | None = None

        for attempt in range(1, self.max_retries + 1):

            try:
                logger.info(
                    "Ollama call — attempt %d/%d", attempt, self.max_retries
                )

                t0       = time.monotonic()
                response = requests.post(
                    OLLAMA_CHAT_ENDPOINT,
                    json=payload,
                    timeout=self.request_timeout,
                )
                response.raise_for_status()
                elapsed  = time.monotonic() - t0

                data         = response.json()
                content      = data.get("message", {}).get("content", "")
                eval_count   = data.get("eval_count", "?")
                prompt_tokens = data.get("prompt_eval_count", "?")

                logger.info(
                    "Ollama response received — "
                    "%.1fs | prompt_tokens=%s | completion_tokens=%s",
                    elapsed, prompt_tokens, eval_count,
                )

                if not content.strip():
                    raise RuntimeError("Ollama returned an empty response.")

                return content

            except (requests.Timeout, requests.ConnectionError) as exc:
                last_exc = exc
                wait     = RETRY_BACKOFF_BASE ** (attempt - 1)
                logger.warning(
                    "Attempt %d failed (%s). Retrying in %.1fs…",
                    attempt, type(exc).__name__, wait,
                )
                time.sleep(wait)

            except requests.HTTPError as exc:
                # Non-retryable
                raise RuntimeError(
                    f"Ollama HTTP error: {exc}"
                ) from exc

        raise RuntimeError(
            f"Ollama unreachable after {self.max_retries} attempts. "
            f"Last error: {last_exc}"
        )

    # ── Public API ────────────────────────────────────────

    def reason(
        self,
        query: str,
        variables: dict[str, Any],
        evidence: list[dict[str, Any]],
        history: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Full reasoning pipeline:
          1. Build prompt
          2. Call Ollama (with retry)
          3. Parse JSON
          4. Normalize missing fields
          5. Sanitize (citation / variable enforcement)
        Returns the sanitized reasoning dict.
        """

        logger.info(
            "Reasoning — variables=%d  evidence=%d  history=%d",
            len(variables),
            len(evidence),
            len(history) if history else 0,
        )

        # 1. Build prompt
        prompt = self._prompt_builder.build(
            query=query,
            variables=variables,
            evidence=evidence,
            history=history,
        )

        logger.debug("Prompt length: %d chars", len(prompt))

        # 2. Call Ollama
        raw_text = self._call_ollama(prompt)

        # 3. Parse JSON
        try:
            result = self._parser.parse(raw_text)
        except ValueError as exc:
            raise RuntimeError(str(exc)) from exc

        # 4. Normalize missing top-level fields
        result.setdefault(
            "environmental_assessment",
            {"summary": "", "key_constraints": [], "interactions": []},
        )
        result.setdefault("recommendations",    [])
        result.setdefault("missing_information", [])
        result.setdefault("follow_up_question",  "")
        result.setdefault("overall_confidence",  "low")

        # 5. Sanitize
        result = self._sanitizer.sanitize(
            result=result,
            variables=variables,
            evidence=evidence,
        )

        recs   = result.get("recommendations", [])
        n_recs = len(recs)
        flags = result.get("validation_flags", [])
        if not isinstance(flags, list):
            flags = []

        # Warn if fewer than 2 recommendations survived sanitization
        if n_recs < 2:
            msg = (
                f"Only {n_recs} recommendation(s) after sanitization. "
                "Check validation_flags for dropped recommendation details."
            )
            logger.warning(msg)
            flags.append(msg)

        # Validate the requirement that recommendations use distinct
        # evidence chunks. Keep the recommendations, but expose the issue.
        if n_recs >= 2:
            citations: list[str] = [r.get("source_citation", "") for r in recs]
            seen: set[str] = set()
            for c in citations:
                if c in seen:
                    msg = (
                        f"Duplicate citation {c!r} used across multiple "
                        "recommendations. Recommendations should use distinct "
                        "evidence chunks."
                    )
                    logger.warning(msg)
                    flags.append(msg)
                seen.add(c)

        result["validation_flags"] = flags

        repaired = sum(1 for r in recs if r.get("citation_repaired"))

        logger.info(
            "Reasoning complete — recs=%d  repaired=%d  flags=%d  confidence=%s",
            n_recs,
            repaired,
            len(flags),
            result.get("overall_confidence", "?"),
        )

        return result


# =========================================================
# CLI TEST HARNESS
# =========================================================

def _color(code: int, text: str) -> str:
    """ANSI color wrapper. Falls back gracefully on Windows."""
    try:
        return f"\033[{code}m{text}\033[0m"
    except Exception:
        return text

GREEN  = lambda t: _color(32, t)
CYAN   = lambda t: _color(36, t)
YELLOW = lambda t: _color(33, t)
BOLD   = lambda t: _color(1,  t)
DIM    = lambda t: _color(2,  t)


def _print_section(title: str) -> None:
    width = 62
    print()
    print(CYAN("━" * width))
    print(BOLD(f"  {title}"))
    print(CYAN("━" * width))


def _print_recommendations(recs: list[dict[str, Any]]) -> None:
    for i, rec in enumerate(recs, start=1):
        print()
        print(BOLD(f"  [{i}]  {rec.get('action', '')}"))
        print()
        print(DIM("  Reasoning:"))
        reasoning = rec.get("scientific_reasoning", "")
        # Wrap at ~70 chars
        words, line = reasoning.split(), ""
        for word in words:
            if len(line) + len(word) + 1 > 70:
                print(f"      {line}")
                line = word
            else:
                line = f"{line} {word}".strip()
        if line:
            print(f"      {line}")

        print()
        vars_used = ", ".join(rec.get("environmental_variables_used", []))
        metrics   = ", ".join(rec.get("impacted_metrics", []))
        print(DIM("  Variables:  ") + vars_used)
        print(DIM("  Metrics:    ") + metrics)
        print(DIM("  Estimate:   ") + rec.get("improvement_estimate", ""))
        print(DIM("  Citation:   ") + GREEN(rec.get("source_citation", "")))
        print(DIM("  Horizon:    ") + rec.get("time_horizon", ""))
        print(DIM("  Confidence: ") + YELLOW(rec.get("confidence", "")))
        print()
        print(DIM("  " + "─" * 58))


def main() -> None:

    _print_section("DARUKAA.EARTH — LOCAL REASONER TEST")

    # ── Imports ───────────────────────────────────────────
    try:
        from core.retriever import BiodiversityRetriever
    except ImportError as exc:
        logger.error("Could not import retriever: %s", exc)
        sys.exit(1)

    # ── Init ──────────────────────────────────────────────
    logger.info("Initializing retriever …")
    retriever = BiodiversityRetriever(top_k=8)

    logger.info("Initializing reasoner …")
    reasoner = BiodiversityReasoner()

    # ── Query ─────────────────────────────────────────────
    query = (
        "Soil organic carbon is 0.3%, "
        "rainfall is very low, "
        "I grow monoculture wheat "
        "in a semi-arid region, "
        "temperature is 38°C."
    )

    _print_section("QUERY")
    print(f"  {query}")

    # ── Retrieve ──────────────────────────────────────────
    logger.info("Retrieving evidence …")
    t0        = time.monotonic()
    retrieved = retriever.retrieve(query)
    variables = retrieved["environmental_variables"]
    evidence  = retrieved["evidence"]
    retrieval_time = time.monotonic() - t0

    _print_section("RETRIEVED EVIDENCE")
    print(f"  {len(evidence)} chunk(s) in {retrieval_time:.2f}s")
    for i, ev in enumerate(evidence, start=1):
        sim = ev.get("similarity")
        sim_str = f"{sim:.3f}" if isinstance(sim, float) else "?"
        print(f"  [{i}] {DIM(ev.get('topic',''))} — sim={GREEN(sim_str)}")

    # ── Reason ────────────────────────────────────────────
    logger.info("Generating reasoning …")
    t0     = time.monotonic()
    result = reasoner.reason(
        query=query,
        variables=variables,
        evidence=evidence,
        history=[],
    )
    reason_time = time.monotonic() - t0

    # ── Assessment ────────────────────────────────────────
    assessment = result.get("environmental_assessment", {})

    _print_section("ENVIRONMENTAL ASSESSMENT")
    print(f"  {assessment.get('summary', '')}")

    constraints = assessment.get("key_constraints", [])
    if constraints:
        print()
        print(DIM("  Constraints:"))
        for c in constraints:
            print(f"    • {c}")

    interactions = assessment.get("interactions", [])
    if interactions:
        print()
        print(DIM("  Interactions:"))
        for ix in interactions:
            print(f"    • {ix}")

    # ── Recommendations ───────────────────────────────────
    _print_section("RECOMMENDATIONS")
    _print_recommendations(result.get("recommendations", []))

    # ── Validation flags ──────────────────────────────────
    flags = result.get("validation_flags", [])
    if flags:
        _print_section("VALIDATION FLAGS")
        for flag in flags:
            print(YELLOW(f"  ⚠  {flag}"))

    # ── Missing info ──────────────────────────────────────
    missing  = result.get("missing_information", [])
    question = result.get("follow_up_question", "")

    if missing or question:
        _print_section("MISSING INFORMATION")
        for m in missing:
            print(f"  • {m}")
        if question:
            print()
            print(YELLOW(f"  Follow-up: {question}"))

    # ── Summary ───────────────────────────────────────────
    _print_section("RUN SUMMARY")
    recs_out  = result.get("recommendations", [])
    n_recs    = len(recs_out)
    n_repaired = sum(1 for r in recs_out if r.get("citation_repaired"))
    n_flags   = len(result.get("validation_flags", []))
    print(f"  Retrieval time    : {retrieval_time:.2f}s")
    print(f"  Reasoning time    : {reason_time:.2f}s")
    print(f"  Recommendations   : {n_recs}")
    print(f"  Citations repaired: {n_repaired}")
    print(f"  Validation flags  : {n_flags}")
    print(f"  Overall confidence: {YELLOW(result.get('overall_confidence', '?'))}")
    print()

    # ── Raw JSON dump ─────────────────────────────────────
    _print_section("RAW JSON OUTPUT")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    _print_section("TEST COMPLETE")


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()