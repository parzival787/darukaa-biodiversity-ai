"""
DARUKAA.EARTH - BIODIVERSITY HEALTH SCORE

Provides a transparent heuristic biodiversity/environmental
health score from 0-100.

IMPORTANT:
This is a prototype heuristic score for the hackathon UI.
It is NOT a scientifically validated biodiversity index.
"""

from __future__ import annotations

from typing import Any


class BiodiversityHealthScorer:
    """
    Calculates a transparent environmental health score.

    The score is divided into:
        - Soil Health
        - Water Availability
        - Land/Crop Diversity
        - Climate Stress

    Missing information is handled explicitly instead of
    silently assuming a value.
    """

    def __init__(self):
        self.component_weights = {
            "soil_health": 0.30,
            "water_availability": 0.25,
            "land_diversity": 0.25,
            "climate_stress": 0.20,
        }

    # ========================================================
    # MAIN SCORE
    # ========================================================

    def calculate(
        self,
        environmental_variables: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Calculate the overall biodiversity health score.
        """

        soil = self._score_soil_health(
            environmental_variables
        )

        water = self._score_water_availability(
            environmental_variables
        )

        land = self._score_land_diversity(
            environmental_variables
        )

        climate = self._score_climate_stress(
            environmental_variables
        )

        components = {
            "soil_health": soil,
            "water_availability": water,
            "land_diversity": land,
            "climate_stress": climate,
        }

        # ----------------------------------------------------
        # Weighted score
        # ----------------------------------------------------

        weighted_scores = []
        available_weights = []

        for name, result in components.items():

            if result["available"]:

                weight = self.component_weights[name]

                weighted_scores.append(
                    result["score"] * weight
                )

                available_weights.append(
                    weight
                )

        if available_weights:

            # Normalize when some components are unavailable.
            score = (
                sum(weighted_scores)
                / sum(available_weights)
            )

            overall_score = round(score)

        else:

            overall_score = None

        # ----------------------------------------------------
        # Interpretation
        # ----------------------------------------------------

        interpretation = self._interpret_score(
            overall_score
        )

        # ----------------------------------------------------
        # Missing information
        # ----------------------------------------------------

        missing_information = []

        for name, result in components.items():

            if not result["available"]:
                missing_information.append(
                    result["missing_reason"]
                )

        # ----------------------------------------------------
        # Return
        # ----------------------------------------------------

        return {
            "score": overall_score,
            "scale": "0-100",
            "type": "heuristic_prototype",
            "scientific_validation": False,
            "interpretation": interpretation,
            "components": components,
            "missing_information": missing_information,
        }

    # ========================================================
    # SOIL HEALTH
    # ========================================================

    def _score_soil_health(
        self,
        env: dict[str, Any],
    ) -> dict[str, Any]:

        soc = self._get_numeric(
            env,
            "soil_organic_carbon",
        )

        ph = self._get_numeric(
            env,
            "soil_ph",
        )

        scores = []
        factors = []

        # ----------------------------------------------------
        # Soil Organic Carbon
        # ----------------------------------------------------

        if soc is not None:

            # Simple prototype scale.
            #
            # < 0.5%  -> poor
            # 0.5-1%  -> moderate
            # 1-2%    -> good
            # > 2%     -> very good

            if soc < 0.5:
                soc_score = 25
                factors.append(
                    "Very low soil organic carbon"
                )

            elif soc < 1.0:
                soc_score = 45
                factors.append(
                    "Low soil organic carbon"
                )

            elif soc < 2.0:
                soc_score = 70
                factors.append(
                    "Moderate soil organic carbon"
                )

            else:
                soc_score = 90
                factors.append(
                    "Relatively high soil organic carbon"
                )

            scores.append(soc_score)

        # ----------------------------------------------------
        # Soil pH
        # ----------------------------------------------------

        if ph is not None:

            # Broad prototype range.
            # This is intentionally not presented as a
            # crop-specific optimum.

            if 6.0 <= ph <= 7.5:

                ph_score = 85

            elif 5.5 <= ph < 6.0 or 7.5 < ph <= 8.0:

                ph_score = 65

            elif 5.0 <= ph < 5.5 or 8.0 < ph <= 8.5:

                ph_score = 45

            else:

                ph_score = 25

            scores.append(ph_score)

        # ----------------------------------------------------
        # No soil data
        # ----------------------------------------------------

        if not scores:

            return {
                "score": None,
                "available": False,
                "factors": [],
                "missing_reason": (
                    "Soil organic carbon or soil pH "
                    "was not provided."
                ),
            }

        return {
            "score": round(
                sum(scores) / len(scores)
            ),
            "available": True,
            "factors": factors,
            "missing_reason": None,
        }

    # ========================================================
    # WATER AVAILABILITY
    # ========================================================

    def _score_water_availability(
        self,
        env: dict[str, Any],
    ) -> dict[str, Any]:

        rainfall = env.get("rainfall")

        if rainfall is None:

            rainfall = env.get(
                "rainfall_condition"
            )

        if rainfall is None:

            return {
                "score": None,
                "available": False,
                "factors": [],
                "missing_reason": (
                    "Rainfall or water availability "
                    "information was not provided."
                ),
            }

        value = str(rainfall).lower().strip()

        if any(
            word in value
            for word in [
                "very low",
                "severe",
                "extreme drought",
                "drought",
            ]
        ):

            score = 25

            factor = "Severe water limitation"

        elif any(
            word in value
            for word in [
                "low",
                "limited",
                "dry",
            ]
        ):

            score = 45

            factor = "Low water availability"

        elif any(
            word in value
            for word in [
                "moderate",
                "medium",
                "normal",
            ]
        ):

            score = 70

            factor = "Moderate water availability"

        elif any(
            word in value
            for word in [
                "high",
                "good",
                "abundant",
            ]
        ):

            score = 85

            factor = "Good water availability"

        else:

            numeric_rainfall = self._get_numeric_value(
                rainfall
            )

            if numeric_rainfall is None:

                return {
                    "score": None,
                    "available": False,
                    "factors": [],
                    "missing_reason": (
                        "Rainfall was provided but its "
                        "condition could not be interpreted."
                    ),
                }

            # Broad prototype interpretation.
            if numeric_rainfall < 300:
                score = 30
            elif numeric_rainfall < 600:
                score = 50
            elif numeric_rainfall < 1000:
                score = 70
            else:
                score = 85

            factor = (
                f"Annual rainfall interpreted as "
                f"{numeric_rainfall}"
            )

        return {
            "score": score,
            "available": True,
            "factors": [factor],
            "missing_reason": None,
        }

    # ========================================================
    # LAND / CROP DIVERSITY
    # ========================================================

    def _score_land_diversity(
        self,
        env: dict[str, Any],
    ) -> dict[str, Any]:

        land_use = str(
            env.get("land_use", "")
        ).lower()

        crop_type = str(
            env.get("crop_type", "")
        ).lower()

        if not land_use and not crop_type:

            return {
                "score": None,
                "available": False,
                "factors": [],
                "missing_reason": (
                    "Land-use or crop information "
                    "was not provided."
                ),
            }

        factors = []

        # ----------------------------------------------------
        # Monoculture
        # ----------------------------------------------------

        if any(
            word in land_use
            for word in [
                "monoculture",
                "single crop",
                "single-crop",
            ]
        ):

            score = 30

            factors.append(
                "Monoculture land use reduces crop diversity"
            )

        # ----------------------------------------------------
        # Agroforestry
        # ----------------------------------------------------

        elif "agroforestry" in land_use:

            score = 85

            factors.append(
                "Agroforestry provides greater structural diversity"
            )

        # ----------------------------------------------------
        # Mixed / diversified systems
        # ----------------------------------------------------

        elif any(
            word in land_use
            for word in [
                "mixed",
                "diverse",
                "diversified",
                "intercrop",
                "intercropping",
            ]
        ):

            score = 80

            factors.append(
                "Diversified land use"
            )

        # ----------------------------------------------------
        # Forest / natural habitat
        # ----------------------------------------------------

        elif any(
            word in land_use
            for word in [
                "forest",
                "natural",
                "native",
                "wetland",
            ]
        ):

            score = 90

            factors.append(
                "Natural or habitat-oriented land use"
            )

        # ----------------------------------------------------
        # Generic agricultural land
        # ----------------------------------------------------

        elif any(
            word in land_use
            for word in [
                "agriculture",
                "cropland",
                "farm",
                "farmland",
            ]
        ):

            score = 55

            factors.append(
                "Agricultural land with unspecified diversity"
            )

        else:

            score = 50

            factors.append(
                "Land-use diversity could not be determined precisely"
            )

        if crop_type:

            factors.append(
                f"Crop type: {crop_type}"
            )

        return {
            "score": score,
            "available": True,
            "factors": factors,
            "missing_reason": None,
        }

    # ========================================================
    # CLIMATE STRESS
    # ========================================================

    def _score_climate_stress(
        self,
        env: dict[str, Any],
    ) -> dict[str, Any]:

        temperature = self._get_numeric(
            env,
            "temperature",
        )

        if temperature is None:

            return {
                "score": None,
                "available": False,
                "factors": [],
                "missing_reason": (
                    "Temperature information "
                    "was not provided."
                ),
            }

        factors = []

        # ----------------------------------------------------
        # Temperature stress
        # ----------------------------------------------------

        if temperature >= 40:

            score = 20

            factors.append(
                "Very high temperature stress"
            )

        elif temperature >= 35:

            score = 40

            factors.append(
                "High temperature stress"
            )

        elif temperature >= 30:

            score = 60

            factors.append(
                "Moderate temperature stress"
            )

        elif temperature >= 20:

            score = 80

            factors.append(
                "Lower temperature stress"
            )

        else:

            score = 70

            factors.append(
                "Low temperature stress based on prototype scale"
            )

        return {
            "score": score,
            "available": True,
            "factors": factors,
            "missing_reason": None,
        }

    # ========================================================
    # SCORE INTERPRETATION
    # ========================================================

    @staticmethod
    def _interpret_score(
        score: int | None,
    ) -> str:

        if score is None:
            return "Insufficient environmental data"

        if score >= 80:
            return "Relatively healthy"

        if score >= 60:
            return "Moderate"

        if score >= 40:
            return "Stressed"

        return "Highly stressed"

    # ========================================================
    # HELPERS
    # ========================================================

    @staticmethod
    def _get_numeric(
        env: dict[str, Any],
        key: str,
    ) -> float | None:

        value = env.get(key)

        return BiodiversityHealthScorer._get_numeric_value(
            value
        )

    @staticmethod
    def _get_numeric_value(
        value: Any,
    ) -> float | None:

        if value is None:
            return None

        if isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):

            cleaned = (
                value
                .replace("%", "")
                .replace("°C", "")
                .replace("°", "")
                .strip()
            )

            try:
                return float(cleaned)

            except ValueError:
                return None

        return None


# ============================================================
# STANDALONE TEST
# ============================================================

def main():

    print("=" * 60)
    print("DARUKAA.EARTH - BIODIVERSITY HEALTH SCORE TEST")
    print("=" * 60)

    scorer = BiodiversityHealthScorer()

    # --------------------------------------------------------
    # Test scenario from the hackathon specification
    # --------------------------------------------------------

    environmental_variables = {
        "soil_organic_carbon": 0.3,
        "rainfall": "very low",
        "land_use": "monoculture",
        "crop_type": "wheat",
        "region": "semi-arid",
        "temperature": 38,
    }

    result = scorer.calculate(
        environmental_variables
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print("\nBIODIVERSITY HEALTH")
    print("-" * 60)

    print(
        f"Score: {result['score']}/100"
    )

    print(
        f"Interpretation: "
        f"{result['interpretation']}"
    )

    print(
        f"Type: {result['type']}"
    )

    print(
        f"Scientific validation: "
        f"{result['scientific_validation']}"
    )

    print("\nCOMPONENTS")
    print("-" * 60)

    for name, component in result[
        "components"
    ].items():

        if component["available"]:

            print(
                f"\n{name}: "
                f"{component['score']}/100"
            )

            for factor in component["factors"]:

                print(
                    f"  - {factor}"
                )

        else:

            print(
                f"\n{name}: unavailable"
            )

            print(
                f"  - {component['missing_reason']}"
            )

    print("\nMISSING INFORMATION")
    print("-" * 60)

    if result["missing_information"]:

        for item in result[
            "missing_information"
        ]:

            print(
                f"  - {item}"
            )

    else:

        print("  None")

    print("\n" + "=" * 60)
    print("BIODIVERSITY HEALTH SCORE TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()