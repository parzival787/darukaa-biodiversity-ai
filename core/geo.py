"""
Darukaa.Earth - Geographic Context Layer

Provides lightweight regional and climate context
from user-provided environmental variables.

This module does not call external APIs and does not
invent geographic coordinates or environmental data.
"""

from __future__ import annotations

from typing import Any


class GeographicContext:
    """Interpret user-provided geographic/environmental context."""

    def analyze(
        self,
        variables: dict[str, Any],
    ) -> dict[str, Any]:

        region = variables.get("region")
        rainfall = variables.get("rainfall")
        temperature = variables.get("temperature")
        soil_type = variables.get("soil_type")
        land_use = variables.get("land_use")

        context: list[str] = []
        signals: list[str] = []

        # Region
        if region:
            context.append(
                f"User-provided region: {region}."
            )

        # Rainfall
        rainfall_text = str(
            rainfall or ""
        ).lower()

        if "very low" in rainfall_text:
            signals.append(
                "Very low rainfall indicates strong "
                "water-availability pressure."
            )
        elif "low" in rainfall_text:
            signals.append(
                "Low rainfall indicates water limitation "
                "should be considered."
            )
        elif "moderate" in rainfall_text:
            signals.append(
                "Moderate rainfall provides an intermediate "
                "water-availability context."
            )
        elif "high" in rainfall_text:
            signals.append(
                "High rainfall should be considered when "
                "assessing water movement and habitat conditions."
            )

        # Temperature
        if isinstance(temperature, (int, float)):
            if temperature >= 35:
                signals.append(
                    "High temperature indicates potential "
                    "thermal and water-stress pressure."
                )
            elif temperature >= 30:
                signals.append(
                    "Elevated temperature should be considered "
                    "when assessing environmental stress."
                )

        # Soil
        if soil_type:
            context.append(
                f"User-provided soil type: {soil_type}."
            )

        # Land use
        if land_use:
            context.append(
                f"User-provided land use: {land_use}."
            )

        # Climate interpretation
        climate_context = "Not determined"

        if (
            "very low" in rainfall_text
            and isinstance(temperature, (int, float))
            and temperature >= 35
        ):
            climate_context = (
                "Hot and water-limited conditions"
            )
        elif "low" in rainfall_text:
            climate_context = (
                "Water-limited conditions"
            )
        elif (
            isinstance(temperature, (int, float))
            and temperature >= 35
        ):
            climate_context = (
                "High-temperature conditions"
            )
        elif rainfall:
            climate_context = (
                "Rainfall condition supplied by user"
            )

        return {
            "available": bool(
                context or signals
            ),
            "region": region,
            "climate_context": climate_context,
            "context": context,
            "environmental_signals": signals,
            "data_source": "user-provided inputs",
        }


def analyze_geographic_context(
    variables: dict[str, Any],
) -> dict[str, Any]:
    """Convenience function for API integration."""

    geo = GeographicContext()

    return geo.analyze(variables)


def _run_test() -> None:
    """Standalone geographic-context test."""

    variables = {
        "region": "semi-arid region",
        "rainfall": "very low",
        "temperature": 38,
        "soil_type": "sandy soil",
        "land_use": "monoculture",
    }

    result = analyze_geographic_context(
        variables
    )

    print("=" * 60)
    print("DARUKAA.EARTH - GEO CONTEXT TEST")
    print("=" * 60)

    print()
    print(
        f"Available: {result['available']}"
    )

    print(
        f"Region: {result['region']}"
    )

    print(
        f"Climate context: "
        f"{result['climate_context']}"
    )

    print()
    print("Context:")

    for item in result["context"]:
        print(f"  - {item}")

    print()
    print("Environmental signals:")

    for signal in result["environmental_signals"]:
        print(f"  - {signal}")

    print()
    print(
        f"Data source: "
        f"{result['data_source']}"
    )

    print()
    print("=" * 60)
    print("GEO CONTEXT TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    _run_test()