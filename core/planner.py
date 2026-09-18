"""
Darukaa.Earth - Biodiversity Intervention Planner

Converts validated recommendations into a practical
implementation timeline.

This module does not generate new scientific claims.
It only organizes recommendations already produced
by the reasoning layer.
"""

from __future__ import annotations

from typing import Any


class InterventionPlanner:
    """Create an implementation roadmap from recommendations."""

    def __init__(self) -> None:
        self.horizon_order = {
            "short-term": 0,
            "medium-term": 1,
            "long-term": 2,
        }

    def create_plan(
        self,
        recommendations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Convert recommendations into a timeline.

        Recommendations are grouped according to the
        time_horizon already assigned by the reasoner.
        """

        timeline = {
            "short-term": [],
            "medium-term": [],
            "long-term": [],
        }

        if not recommendations:
            return {
                "plan_available": False,
                "timeline": self._build_timeline(timeline),
                "total_actions": 0,
            }

        horizon_aliases = {
            "short": "short-term",
            "short term": "short-term",
            "short-term": "short-term",
            "medium": "medium-term",
            "medium term": "medium-term",
            "medium-term": "medium-term",
            "long": "long-term",
            "long term": "long-term",
            "long-term": "long-term",
        }

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):
            action = str(
                recommendation.get(
                    "action",
                    "",
                )
            ).strip()

            if not action:
                continue

            raw_horizon = str(
                recommendation.get(
                    "time_horizon",
                    "",
                )
            ).strip().lower()

            horizon = horizon_aliases.get(raw_horizon)

            # Do not invent a timeline placement. The validator/reasoner
            # remains responsible for reporting an invalid horizon.
            if horizon is None:
                continue

            item = {
                "priority": index,
                "action": action,
                "time_horizon": horizon,
                "confidence": recommendation.get(
                    "confidence",
                    "medium",
                ),
                "impacted_metrics": recommendation.get(
                    "impacted_metrics",
                    [],
                ),
                "source_citation": recommendation.get(
                    "source_citation",
                    "",
                ),
                "improvement_estimate": recommendation.get(
                    "improvement_estimate",
                    "",
                ),
            }

            timeline[horizon].append(item)

        ordered_timeline = self._build_timeline(timeline)

        total_actions = sum(
            len(stage["actions"])
            for stage in ordered_timeline
        )

        return {
            "plan_available": total_actions > 0,
            "timeline": ordered_timeline,
            "total_actions": total_actions,
        }

    @staticmethod
    def _build_timeline(
        timeline: dict[str, list[dict[str, Any]]],
    ) -> list[dict[str, Any]]:
        """
        Always expose all three implementation stages.
        Empty stages contain no invented actions.
        """

        stage_details = {
            "short-term": {
                "label": "Immediate Actions",
                "period": "0-3 months",
                "purpose": (
                    "Start low-delay interventions and "
                    "reduce immediate environmental stress."
                ),
            },
            "medium-term": {
                "label": "Medium-Term Actions",
                "period": "3-12 months",
                "purpose": (
                    "Build measurable improvements in "
                    "soil, water and habitat conditions."
                ),
            },
            "long-term": {
                "label": "Long-Term Actions",
                "period": "1-3 years",
                "purpose": (
                    "Strengthen ecosystem resilience and "
                    "landscape-level biodiversity."
                ),
            },
        }

        ordered_timeline = []

        for horizon in (
            "short-term",
            "medium-term",
            "long-term",
        ):
            details = stage_details[horizon]

            ordered_timeline.append(
                {
                    "stage": horizon,
                    "label": details["label"],
                    "period": details["period"],
                    "purpose": details["purpose"],
                    "actions": timeline[horizon],
                }
            )

        return ordered_timeline


def create_intervention_plan(
    recommendations: list[dict[str, Any]],
) -> dict[str, Any]:
    """Convenience function for API integration."""

    planner = InterventionPlanner()

    return planner.create_plan(
        recommendations
    )


def _run_test() -> None:
    """Run a small standalone planner test."""

    recommendations = [
        {
            "action": (
                "Implement conservation tillage "
                "combined with cover cropping."
            ),
            "confidence": "medium",
            "impacted_metrics": [
                "soil organic carbon",
                "soil erosion",
            ],
            "source_citation": "EVIDENCE 5",
            "improvement_estimate": (
                "18% improvement in depth-weighted "
                "soil organic carbon."
            ),
            "time_horizon": "medium-term",
        },
        {
            "action": (
                "Consider drought-tolerant crop varieties "
                "to improve crop resilience to water stress."
            ),
            "confidence": "low",
            "impacted_metrics": [
                "species survival",
                "ecosystem resilience",
            ],
            "source_citation": "EVIDENCE 1",
            "improvement_estimate": (
                "Quantitative estimate unavailable "
                "from retrieved evidence"
            ),
            "time_horizon": "short-term",
        },
    ]

    planner = InterventionPlanner()

    result = planner.create_plan(
        recommendations
    )

    print("=" * 60)
    print("DARUKAA.EARTH - INTERVENTION PLANNER TEST")
    print("=" * 60)

    print()
    print(
        f"Plan available: "
        f"{result['plan_available']}"
    )

    print(
        f"Total actions: "
        f"{result['total_actions']}"
    )

    print()

    for stage in result["timeline"]:
        print(
            f"{stage['label']} "
            f"({stage['period']})"
        )

        print(
            f"Purpose: {stage['purpose']}"
        )

        if not stage["actions"]:
            print("  No grounded actions assigned.")

        for action in stage["actions"]:
            print(
                f"  {action['priority']}. "
                f"{action['action']}"
            )

        print()

    print("=" * 60)
    print("PLANNER TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    _run_test()
