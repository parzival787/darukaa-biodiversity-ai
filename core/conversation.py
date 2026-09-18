"""
DARUKAA.EARTH - CONVERSATION MEMORY

Maintains multi-turn environmental context for each chat session.

The memory stores:
1. Extracted environmental variables
2. Previous user messages
3. Previous assistant responses
4. Recent conversation history

This is intentionally in-memory for the hackathon prototype.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class ConversationTurn:
    """One user/assistant interaction."""

    user_message: str
    assistant_response: dict[str, Any] | None = None
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


@dataclass
class ConversationSession:
    """Stores the complete state of one conversation."""

    session_id: str

    # Accumulated environmental information
    environmental_variables: dict[str, Any] = field(
        default_factory=dict
    )

    # Conversation turns
    history: list[ConversationTurn] = field(
        default_factory=list
    )


# ============================================================
# CONVERSATION MANAGER
# ============================================================

class ConversationManager:
    """
    Manages multiple conversation sessions.

    Example:

        manager = ConversationManager()

        manager.update_environment(
            "demo",
            {
                "soil_type": "sandy"
            }
        )

        manager.update_environment(
            "demo",
            {
                "rainfall": "very low"
            }
        )

        context = manager.get_context("demo")
    """

    def __init__(
        self,
        max_history: int = 10,
    ):
        self.sessions: dict[str, ConversationSession] = {}

        # Keep only the most recent N turns.
        self.max_history = max_history

    # ========================================================
    # SESSION MANAGEMENT
    # ========================================================

    def get_or_create_session(
        self,
        session_id: str,
    ) -> ConversationSession:
        """
        Return an existing session or create a new one.
        """

        if session_id not in self.sessions:

            self.sessions[session_id] = ConversationSession(
                session_id=session_id
            )

        return self.sessions[session_id]

    def get_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """Return a session if it exists."""

        return self.sessions.get(session_id)

    def delete_session(
        self,
        session_id: str,
    ) -> bool:
        """
        Delete a conversation session.

        Returns True if a session was deleted.
        """

        if session_id in self.sessions:

            del self.sessions[session_id]

            return True

        return False

    # ========================================================
    # ENVIRONMENTAL VARIABLES
    # ========================================================

    def update_environment(
        self,
        session_id: str,
        variables: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Merge newly extracted environmental variables
        into the existing session.

        Existing information is preserved unless a new
        non-empty value is provided.
        """

        session = self.get_or_create_session(
            session_id
        )

        for key, value in variables.items():

            if value is None:
                continue

            # Ignore empty strings.
            if isinstance(value, str) and not value.strip():
                continue

            normalized_key = self._normalize_variable_name(
                key
            )

            session.environmental_variables[
                normalized_key
            ] = value

        return dict(
            session.environmental_variables
        )

    def get_environment(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """Return accumulated environmental variables."""

        session = self.get_or_create_session(
            session_id
        )

        return dict(
            session.environmental_variables
        )

    # ========================================================
    # CONVERSATION HISTORY
    # ========================================================

    def add_turn(
        self,
        session_id: str,
        user_message: str,
        assistant_response: dict[str, Any] | None = None,
    ) -> None:
        """
        Add a user/assistant interaction to the session.
        """

        session = self.get_or_create_session(
            session_id
        )

        turn = ConversationTurn(
            user_message=user_message,
            assistant_response=assistant_response,
        )

        session.history.append(turn)

        # Keep memory bounded.
        if len(session.history) > self.max_history:

            session.history = session.history[
                -self.max_history:
            ]

    def get_history(
        self,
        session_id: str,
    ) -> list[ConversationTurn]:
        """Return conversation history."""

        session = self.get_or_create_session(
            session_id
        )

        return list(session.history)

    # ========================================================
    # LLM-FRIENDLY HISTORY
    # ========================================================

    def get_history_for_llm(
        self,
        session_id: str,
    ) -> list[dict[str, str]]:
        """
        Convert conversation history into a format that
        can be passed directly to the reasoner.
        """

        session = self.get_or_create_session(
            session_id
        )

        messages: list[dict[str, str]] = []

        for turn in session.history:

            messages.append(
                {
                    "role": "user",
                    "content": turn.user_message,
                }
            )

            if turn.assistant_response is not None:

                assistant_text = self._response_to_text(
                    turn.assistant_response
                )

                messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_text,
                    }
                )

        return messages

    # ========================================================
    # COMPLETE CONTEXT
    # ========================================================

    def get_context(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """
        Return all useful information for reasoning.
        """

        session = self.get_or_create_session(
            session_id
        )

        return {
            "session_id": session.session_id,
            "environmental_variables": dict(
                session.environmental_variables
            ),
            "history": self.get_history_for_llm(
                session_id
            ),
            "turn_count": len(session.history),
        }

    # ========================================================
    # RESET ENVIRONMENT
    # ========================================================

    def clear_environment(
        self,
        session_id: str,
    ) -> None:
        """
        Clear only environmental variables while keeping
        conversation history.
        """

        session = self.get_or_create_session(
            session_id
        )

        session.environmental_variables.clear()

    # ========================================================
    # RESET EVERYTHING
    # ========================================================

    def clear_session(
        self,
        session_id: str,
    ) -> None:
        """
        Completely reset a session.
        """

        self.delete_session(session_id)

    # ========================================================
    # NORMALIZATION
    # ========================================================

    @staticmethod
    def _normalize_variable_name(
        key: str,
    ) -> str:
        """
        Normalize environmental variable names.

        Examples:

            soil organic carbon
            soil-organic-carbon
            soil_organic_carbon

        all become:

            soil_organic_carbon
        """

        if not isinstance(key, str):
            return str(key)

        normalized = key.lower().strip()

        normalized = normalized.replace(
            "-",
            "_",
        )

        normalized = normalized.replace(
            " ",
            "_",
        )

        aliases = {
            "soc": "soil_organic_carbon",
            "soil_carbon": "soil_organic_carbon",
            "organic_carbon": "soil_organic_carbon",
            "soil_ph_level": "soil_ph",
            "rainfall_condition": "rainfall",
            "rainfall_level": "rainfall",
            "landuse": "land_use",
            "crop": "crop_type",
            "temp": "temperature",
            "temperature_c": "temperature",
        }

        return aliases.get(
            normalized,
            normalized,
        )

    # ========================================================
    # RESPONSE CONVERSION
    # ========================================================

    @staticmethod
    def _response_to_text(
        response: dict[str, Any],
    ) -> str:
        """
        Convert a structured assistant response into a compact
        textual representation for conversation history.
        """

        if not isinstance(response, dict):
            return str(response)

        parts: list[str] = []

        assessment = response.get(
            "environmental_assessment"
        )

        if isinstance(assessment, dict):

            summary = assessment.get(
                "summary"
            )

            if summary:
                parts.append(
                    f"Assessment: {summary}"
                )

        recommendations = response.get(
            "recommendations",
            []
        )

        if isinstance(recommendations, list):

            for index, recommendation in enumerate(
                recommendations,
                start=1,
            ):

                if not isinstance(
                    recommendation,
                    dict,
                ):
                    continue

                action = recommendation.get(
                    "action"
                )

                reasoning = recommendation.get(
                    "scientific_reasoning"
                )

                if action:

                    parts.append(
                        f"Recommendation {index}: {action}"
                    )

                if reasoning:

                    parts.append(
                        f"Reasoning: {reasoning}"
                    )

        follow_up = response.get(
            "follow_up_question"
        )

        if follow_up:

            parts.append(
                f"Follow-up: {follow_up}"
            )

        return "\n".join(parts)


# ============================================================
# STANDALONE TEST
# ============================================================

def main():

    print("=" * 60)
    print("DARUKAA.EARTH - CONVERSATION MEMORY TEST")
    print("=" * 60)

    manager = ConversationManager(
        max_history=10
    )

    session_id = "demo-session"

    # --------------------------------------------------------
    # TURN 1
    # --------------------------------------------------------

    print("\nTURN 1")
    print("-" * 60)

    manager.update_environment(
        session_id,
        {
            "soil_type": "sandy",
        },
    )

    manager.add_turn(
        session_id,
        "My soil is sandy.",
        {
            "environmental_assessment": {
                "summary": "Sandy soil may have lower water retention."
            },
            "recommendations": [
                {
                    "action": "Increase organic matter inputs."
                }
            ],
            "follow_up_question": (
                "What is your rainfall level?"
            ),
        },
    )

    print(
        "Environment:",
        manager.get_environment(session_id)
    )

    # --------------------------------------------------------
    # TURN 2
    # --------------------------------------------------------

    print("\nTURN 2")
    print("-" * 60)

    manager.update_environment(
        session_id,
        {
            "rainfall": "very low",
        },
    )

    manager.add_turn(
        session_id,
        "Rainfall is very low.",
        {
            "environmental_assessment": {
                "summary": (
                    "Low rainfall combined with sandy soil "
                    "increases water stress."
                )
            },
            "recommendations": [
                {
                    "action": "Use water-conserving practices."
                }
            ],
            "follow_up_question": (
                "What crop are you growing?"
            ),
        },
    )

    print(
        "Environment:",
        manager.get_environment(session_id)
    )

    # --------------------------------------------------------
    # TURN 3
    # --------------------------------------------------------

    print("\nTURN 3")
    print("-" * 60)

    manager.update_environment(
        session_id,
        {
            "crop_type": "wheat",
            "temperature": 38,
        },
    )

    manager.add_turn(
        session_id,
        "I grow wheat and the temperature reaches 38°C.",
        None,
    )

    # --------------------------------------------------------
    # DISPLAY COMPLETE CONTEXT
    # --------------------------------------------------------

    print("\nACCUMULATED ENVIRONMENT")
    print("-" * 60)

    environment = manager.get_environment(
        session_id
    )

    for key, value in environment.items():

        print(
            f"  {key}: {value}"
        )

    print("\nCONVERSATION HISTORY")
    print("-" * 60)

    history = manager.get_history_for_llm(
        session_id
    )

    for message in history:

        print(
            f"  {message['role'].upper()}: "
            f"{message['content']}"
        )

    print("\nCOMPLETE CONTEXT")
    print("-" * 60)

    context = manager.get_context(
        session_id
    )

    print(
        f"Session ID: {context['session_id']}"
    )

    print(
        f"Turn count: {context['turn_count']}"
    )

    print(
        f"Stored variables: "
        f"{len(context['environmental_variables'])}"
    )

    # --------------------------------------------------------
    # TEST VARIABLE UPDATE
    # --------------------------------------------------------

    print("\nVARIABLE UPDATE TEST")
    print("-" * 60)

    manager.update_environment(
        session_id,
        {
            "rainfall": "moderate",
        },
    )

    updated = manager.get_environment(
        session_id
    )

    print(
        "Updated rainfall:",
        updated["rainfall"]
    )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CONVERSATION MEMORY TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()