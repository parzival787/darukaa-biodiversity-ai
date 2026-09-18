"""
DARUKAA.EARTH - RESPONSE VALIDATOR

Validates structured biodiversity recommendations produced by
the local Ollama reasoner.
"""

from __future__ import annotations

import re
from typing import Any


class BiodiversityValidator:

    REQUIRED_RECOMMENDATION_FIELDS = {
        "action",
        "scientific_reasoning",
        "environmental_variables_used",
        "impacted_metrics",
        "improvement_estimate",
        "source_citation",
        "time_horizon",
        "confidence",
    }

    VALID_CONFIDENCE = {
        "low",
        "medium",
        "high",
    }

    VALID_TIME_HORIZONS = {
        "short-term",
        "medium-term",
        "long-term",
    }

    # These are the ONLY fields that count as environmental
    # variables for the 3-variable reasoning requirement.
    VALID_ENVIRONMENTAL_VARIABLES = {
        "soil_organic_carbon",
        "soil_ph",
        "rainfall",
        "land_use",
        "crop_type",
        "region",
        "temperature",
        "biodiversity_status",
        "soil_type",
    }

    def __init__(
        self,
        retrieved_evidence: list[dict[str, Any]] | None = None,
        environmental_variables: dict[str, Any] | None = None,
    ):
        self.retrieved_evidence = (
            retrieved_evidence or []
        )

        self.environmental_variables = (
            environmental_variables or {}
        )

    # ========================================================
    # MAIN VALIDATION
    # ========================================================

    def validate(
        self,
        response: dict[str, Any],
    ) -> dict[str, Any]:

        errors: list[str] = []
        warnings: list[str] = []

        if not isinstance(response, dict):

            return {
                "valid": False,
                "quality_score": 0,
                "errors": [
                    "Reasoner output is not a JSON object."
                ],
                "warnings": [],
                "checks": {},
            }

        # ----------------------------------------------------
        # Top-level fields
        # ----------------------------------------------------

        required_top_level = {
            "environmental_assessment",
            "recommendations",
            "missing_information",
            "follow_up_question",
            "overall_confidence",
        }

        missing_top_level = (
            required_top_level
            - set(response.keys())
        )

        if missing_top_level:

            errors.append(
                "Missing top-level fields: "
                + ", ".join(
                    sorted(missing_top_level)
                )
            )

        # ----------------------------------------------------
        # Environmental assessment
        # ----------------------------------------------------

        assessment = response.get(
            "environmental_assessment"
        )

        assessment_valid = isinstance(
            assessment,
            dict,
        )

        if not assessment_valid:

            errors.append(
                "environmental_assessment must be a JSON object."
            )

        # ----------------------------------------------------
        # Recommendations
        # ----------------------------------------------------

        recommendations = response.get(
            "recommendations",
            [],
        )

        recommendations_valid = (
            isinstance(recommendations, list)
            and len(recommendations) >= 2
        )

        if not recommendations_valid:

            errors.append(
                "At least 2 recommendations are required."
            )

        recommendation_reports = []

        if isinstance(
            recommendations,
            list,
        ):

            for index, recommendation in enumerate(
                recommendations,
                start=1,
            ):

                report = self._validate_recommendation(
                    recommendation,
                    index,
                )

                recommendation_reports.append(
                    report
                )

                errors.extend(
                    report["errors"]
                )

                warnings.extend(
                    report["warnings"]
                )

        # ----------------------------------------------------
        # Missing information
        # ----------------------------------------------------

        missing_information = response.get(
            "missing_information",
            [],
        )

        missing_information_valid = isinstance(
            missing_information,
            list,
        )

        if not missing_information_valid:

            errors.append(
                "missing_information must be a JSON array."
            )

        # ----------------------------------------------------
        # Follow-up
        # ----------------------------------------------------

        follow_up = response.get(
            "follow_up_question"
        )

        follow_up_valid = (
            isinstance(follow_up, str)
            and bool(follow_up.strip())
        )

        if not follow_up_valid:

            warnings.append(
                "No useful follow-up question was provided."
            )

        # ----------------------------------------------------
        # Overall confidence
        # ----------------------------------------------------

        overall_confidence = response.get(
            "overall_confidence"
        )

        confidence_valid = (
            isinstance(
                overall_confidence,
                str,
            )
            and overall_confidence.lower()
            in self.VALID_CONFIDENCE
        )

        if not confidence_valid:

            warnings.append(
                "overall_confidence should be "
                "low, medium, or high."
            )

        # ----------------------------------------------------
        # Quality score
        # ----------------------------------------------------

        quality_score = self._calculate_quality_score(
            response=response,
            recommendation_reports=recommendation_reports,
            errors=errors,
            warnings=warnings,
        )

        return {
            "valid": len(errors) == 0,
            "quality_score": quality_score,
            "errors": errors,
            "warnings": warnings,
            "checks": {
                "top_level_structure": (
                    len(missing_top_level) == 0
                ),
                "environmental_assessment": (
                    assessment_valid
                ),
                "minimum_recommendations": (
                    recommendations_valid
                ),
                "missing_information": (
                    missing_information_valid
                ),
                "follow_up_question": (
                    follow_up_valid
                ),
                "overall_confidence": (
                    confidence_valid
                ),
            },
            "recommendations": recommendation_reports,
        }

    # ========================================================
    # RECOMMENDATION VALIDATION
    # ========================================================

    def _validate_recommendation(
        self,
        recommendation: Any,
        index: int,
    ) -> dict[str, Any]:

        errors: list[str] = []
        warnings: list[str] = []

        if not isinstance(
            recommendation,
            dict,
        ):

            return {
                "recommendation": index,
                "valid": False,
                "errors": [
                    f"Recommendation {index} "
                    "is not a JSON object."
                ],
                "warnings": [],
                "checks": {},
            }

        # ----------------------------------------------------
        # Required fields
        # ----------------------------------------------------

        missing_fields = (
            self.REQUIRED_RECOMMENDATION_FIELDS
            - set(recommendation.keys())
        )

        if missing_fields:

            errors.append(
                f"Recommendation {index} missing fields: "
                + ", ".join(
                    sorted(missing_fields)
                )
            )

        # ----------------------------------------------------
        # Action
        # ----------------------------------------------------

        action = recommendation.get(
            "action"
        )

        action_valid = (
            isinstance(action, str)
            and len(action.strip()) >= 10
        )

        if not action_valid:

            errors.append(
                f"Recommendation {index}: "
                "action is missing or too short."
            )

        # ----------------------------------------------------
        # Scientific reasoning
        # ----------------------------------------------------

        reasoning = recommendation.get(
            "scientific_reasoning"
        )

        reasoning_valid = (
            isinstance(reasoning, str)
            and len(reasoning.strip()) >= 20
        )

        if not reasoning_valid:

            errors.append(
                f"Recommendation {index}: "
                "scientific reasoning is missing or too short."
            )

        # ----------------------------------------------------
        # Environmental variables
        # ----------------------------------------------------

        variables = recommendation.get(
            "environmental_variables_used",
            [],
        )

        variables_valid = isinstance(
            variables,
            list,
        )

        if not variables_valid:

            errors.append(
                f"Recommendation {index}: "
                "environmental_variables_used "
                "must be an array."
            )

            variables = []

        normalized_variables = {
            self._normalize_variable(v)
            for v in variables
            if isinstance(v, str)
        }

        # Only genuine environmental inputs count.
        actual_environmental_variables = (
            normalized_variables
            & self.VALID_ENVIRONMENTAL_VARIABLES
        )

        non_environmental_variables = (
            normalized_variables
            - self.VALID_ENVIRONMENTAL_VARIABLES
        )

        # ----------------------------------------------------
        # Non-environmental entries
        # ----------------------------------------------------

        if non_environmental_variables:

            warnings.append(
                f"Recommendation {index}: "
                "these entries are not recognized as "
                "environmental input variables: "
                + ", ".join(
                    sorted(
                        non_environmental_variables
                    )
                )
            )

        # ----------------------------------------------------
        # Three-variable requirement
        # ----------------------------------------------------

        three_variable_requirement = (
            len(actual_environmental_variables)
            >= 3
        )

        if not three_variable_requirement:

            errors.append(
                f"Recommendation {index}: "
                "must combine at least 3 actual "
                "environmental variables."
            )

        # ----------------------------------------------------
        # Impacted metrics
        # ----------------------------------------------------

        metrics = recommendation.get(
            "impacted_metrics",
            [],
        )

        metrics_valid = (
            isinstance(metrics, list)
            and len(metrics) >= 1
        )

        if not metrics_valid:

            errors.append(
                f"Recommendation {index}: "
                "at least one impacted metric "
                "is required."
            )

        # ----------------------------------------------------
        # Citation
        # ----------------------------------------------------

        citation = recommendation.get(
            "source_citation",
            "",
        )

        citation_valid = (
            self._validate_citation(
                citation
            )
        )

        if not citation_valid:

            errors.append(
                f"Recommendation {index}: "
                "invalid or missing evidence citation."
            )

        # ----------------------------------------------------
        # Improvement estimate
        # ----------------------------------------------------

        estimate = recommendation.get(
            "improvement_estimate",
            "",
        )

        estimate_valid = (
            isinstance(estimate, str)
            and bool(estimate.strip())
        )

        if not estimate_valid:

            errors.append(
                f"Recommendation {index}: "
                "improvement_estimate is missing."
            )

        has_numeric_estimate = (
            self._contains_number(
                estimate
            )
        )

        if (
            estimate_valid
            and not has_numeric_estimate
        ):
            if (
                isinstance(estimate, str)
                and "quantitative estimate unavailable from retrieved evidence"
                in estimate.lower()
            ):
                warnings.append(
                    f"Recommendation {index}: "
                    "quantitative estimate is unavailable "
                    "from retrieved evidence."
                )
            else:
                warnings.append(
                    f"Recommendation {index}: "
                    "no numerical improvement estimate found."
                )

        # ----------------------------------------------------
        # Time horizon
        # ----------------------------------------------------

        time_horizon = recommendation.get(
            "time_horizon"
        )

        time_horizon_valid = (
            isinstance(
                time_horizon,
                str,
            )
            and time_horizon.lower()
            in self.VALID_TIME_HORIZONS
        )

        if not time_horizon_valid:

            warnings.append(
                f"Recommendation {index}: "
                "time_horizon should be short-term, "
                "medium-term, or long-term."
            )

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        confidence = recommendation.get(
            "confidence"
        )

        confidence_valid = (
            isinstance(
                confidence,
                str,
            )
            and confidence.lower()
            in self.VALID_CONFIDENCE
        )

        if not confidence_valid:

            warnings.append(
                f"Recommendation {index}: "
                "confidence should be low, medium, or high."
            )

        # ----------------------------------------------------
        # Compare variables with actual user variables
        # ----------------------------------------------------

        known_variables = {
            self._normalize_variable(k)
            for k in self.environmental_variables.keys()
        }

        known_variables &= (
            self.VALID_ENVIRONMENTAL_VARIABLES
        )

        unknown_variables = (
            actual_environmental_variables
            - known_variables
        )

        if unknown_variables:

            warnings.append(
                f"Recommendation {index}: "
                "some environmental variables were "
                "not present in the extracted "
                "user/environment data: "
                + ", ".join(
                    sorted(
                        unknown_variables
                    )
                )
            )

        # ----------------------------------------------------
        # Final recommendation report
        # ----------------------------------------------------

        return {
            "recommendation": index,
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "checks": {
                "required_fields": (
                    len(missing_fields) == 0
                ),
                "action": action_valid,
                "scientific_reasoning": (
                    reasoning_valid
                ),
                "three_environmental_variables": (
                    three_variable_requirement
                ),
                "impacted_metrics": (
                    metrics_valid
                ),
                "citation": citation_valid,
                "improvement_estimate": (
                    estimate_valid
                ),
                "numeric_estimate": (
                    has_numeric_estimate
                ),
                "time_horizon": (
                    time_horizon_valid
                ),
                "confidence": (
                    confidence_valid
                ),
            },
            "environmental_variables_used": sorted(
                actual_environmental_variables
            ),
            "non_environmental_entries": sorted(
                non_environmental_variables
            ),
        }

    # ========================================================
    # CITATION VALIDATION
    # ========================================================

    def _validate_citation(
        self,
        citation: Any,
    ) -> bool:
        """
        Accept either:

        EVIDENCE 1

        or a full citation matching one of the retrieved
        evidence sources.
        """

        if not isinstance(
            citation,
            str,
        ):
            return False

        citation = citation.strip()

        if not citation:
            return False

        # ----------------------------------------------------
        # If no evidence exists, only check that a citation
        # string was provided.
        # ----------------------------------------------------

        if not self.retrieved_evidence:

            return True

        # ----------------------------------------------------
        # EVIDENCE N format
        # ----------------------------------------------------

        match = re.search(
            r"EVIDENCE\s+(\d+)",
            citation,
            re.IGNORECASE,
        )

        if match:

            evidence_number = int(
                match.group(1)
            )

            return (
                1
                <= evidence_number
                <= len(
                    self.retrieved_evidence
                )
            )

        # ----------------------------------------------------
        # Full source citation format
        # ----------------------------------------------------

        citation_lower = citation.lower()

        for evidence in self.retrieved_evidence:

            if not isinstance(
                evidence,
                dict,
            ):
                continue

            source = str(
                evidence.get(
                    "source",
                    "",
                )
            ).strip()

            if not source:
                continue

            source_lower = source.lower()

            if citation_lower == source_lower:
                return True

            if source_lower in citation_lower:
                return True

            if citation_lower in source_lower:
                return True

        return False

    # ========================================================
    # NUMBER DETECTION
    # ========================================================

    @staticmethod
    def _contains_number(
        value: Any,
    ) -> bool:

        if not isinstance(
            value,
            str,
        ):
            return False

        return bool(
            re.search(
                r"[-+]?\d+(?:\.\d+)?\s*"
                r"(?:%|percent)?",
                value,
                re.IGNORECASE,
            )
        )

    # ========================================================
    # VARIABLE NORMALIZATION
    # ========================================================

    @staticmethod
    def _normalize_variable(
        variable: Any,
    ) -> str:

        if not isinstance(
            variable,
            str,
        ):
            return ""

        value = variable.lower().strip()

        value = value.replace(
            "-",
            "_",
        )

        value = value.replace(
            " ",
            "_",
        )

        aliases = {
            "soc": "soil_organic_carbon",
            "soil_carbon": "soil_organic_carbon",
            "organic_carbon": "soil_organic_carbon",
            "soil_organic_carbon": "soil_organic_carbon",
            "soil_ph_level": "soil_ph",
            "rainfall_condition": "rainfall",
            "rainfall_level": "rainfall",
            "landuse": "land_use",
            "crop": "crop_type",
            "temp": "temperature",
            "temperature_c": "temperature",
        }

        return aliases.get(
            value,
            value,
        )

    # ========================================================
    # QUALITY SCORE
    # ========================================================

    def _calculate_quality_score(
        self,
        response: dict[str, Any],
        recommendation_reports: list[
            dict[str, Any]
        ],
        errors: list[str],
        warnings: list[str],
    ) -> int:

        if not recommendation_reports:
            return 0

        total_checks = 0
        passed_checks = 0

        for report in recommendation_reports:

            checks = report.get(
                "checks",
                {},
            )

            for result in checks.values():

                total_checks += 1

                if result is True:

                    passed_checks += 1

        if total_checks == 0:
            return 0

        score = (
            passed_checks
            / total_checks
        ) * 100

        score -= min(
            len(errors) * 5,
            30,
        )

        score -= min(
            len(warnings),
            10,
        )

        score = max(
            0,
            min(
                100,
                score,
            ),
        )

        return round(score)


# ============================================================
# STANDALONE TEST
# ============================================================

def main():

    print("=" * 60)
    print("DARUKAA.EARTH - VALIDATOR TEST")
    print("=" * 60)

    environmental_variables = {
        "soil_organic_carbon": 0.3,
        "rainfall": "very low",
        "land_use": "monoculture",
        "crop_type": "wheat",
        "region": "semi-arid",
        "temperature": 38,
    }

    retrieved_evidence = [
        {
            "content": (
                "Evidence about soil organic carbon."
            ),
            "source": "Scientific source",
            "topic": "soil_organic_carbon",
        },
        {
            "content": (
                "Evidence about cover crops."
            ),
            "source": "Scientific source",
            "topic": "soil_organic_carbon",
        },
        {
            "content": (
                "Evidence about water availability."
            ),
            "source": "Scientific source",
            "topic": "water_availability",
        },
        {
            "content": (
                "Evidence about conservation practices."
            ),
            "source": "Scientific source",
            "topic": "soil_health",
        },
    ]

    response = {
        "environmental_assessment": {
            "summary": (
                "Low SOC and low rainfall create "
                "environmental stress."
            ),
            "key_constraints": [
                "low soil organic carbon",
                "low rainfall",
            ],
            "interactions": [
                "soil carbon + rainfall + land use"
            ],
        },
        "recommendations": [
            {
                "action": (
                    "Implement conservation tillage "
                    "to reduce soil disturbance."
                ),
                "scientific_reasoning": (
                    "Reducing soil disturbance can help "
                    "retain organic matter."
                ),
                "environmental_variables_used": [
                    "soil_organic_carbon",
                    "rainfall",
                    "land_use",
                ],
                "impacted_metrics": [
                    "soil_organic_carbon",
                    "water_retention",
                    "erosion",
                ],
                "improvement_estimate": (
                    "12% increase in total soil organic "
                    "carbon under cover crops."
                ),
                "source_citation": "EVIDENCE 2",
                "time_horizon": "medium-term",
                "confidence": "medium",
            },
            {
                "action": (
                    "Use cover crops to increase "
                    "soil organic carbon."
                ),
                "scientific_reasoning": (
                    "Cover crops can increase soil "
                    "organic carbon and microbial biomass."
                ),
                "environmental_variables_used": [
                    "soil_organic_carbon",
                    "temperature",
                    "crop_type",
                ],
                "impacted_metrics": [
                    "soil_organic_carbon",
                    "microbial_biomass",
                ],
                "improvement_estimate": (
                    "33% increase in microbial biomass."
                ),
                "source_citation": "EVIDENCE 2",
                "time_horizon": "long-term",
                "confidence": "high",
            },
        ],
        "missing_information": [
            "rainfall frequency",
        ],
        "follow_up_question": (
            "What is the average annual rainfall?"
        ),
        "overall_confidence": "medium",
    }

    validator = BiodiversityValidator(
        retrieved_evidence=retrieved_evidence,
        environmental_variables=environmental_variables,
    )

    result = validator.validate(
        response
    )

    print("\nVALIDATION RESULT")
    print("=" * 60)

    print(
        f"Valid: {result['valid']}"
    )

    print(
        f"Quality Score: "
        f"{result['quality_score']}/100"
    )

    print("\nCHECKS:")

    for check, passed in result[
        "checks"
    ].items():

        status = (
            "PASS"
            if passed
            else "FAIL"
        )

        print(
            f"  {status:<5} {check}"
        )

    if result["errors"]:

        print("\nERRORS:")

        for error in result[
            "errors"
        ]:

            print(
                f"  - {error}"
            )

    if result["warnings"]:

        print("\nWARNINGS:")

        for warning in result[
            "warnings"
        ]:

            print(
                f"  - {warning}"
            )

    print("\nRECOMMENDATION CHECKS:")

    for report in result[
        "recommendations"
    ]:

        print(
            f"\nRecommendation "
            f"{report['recommendation']}: "
            f"{'VALID' if report['valid'] else 'INVALID'}"
        )

        for check, passed in report[
            "checks"
        ].items():

            status = (
                "PASS"
                if passed
                else "FAIL"
            )

            print(
                f"    {status:<5} {check}"
            )

    print("\n" + "=" * 60)
    print("VALIDATOR TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()