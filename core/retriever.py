"""
Darukaa.Earth Biodiversity Intelligence
Semantic Retriever

Responsibilities:
1. Load the ChromaDB knowledge base.
2. Convert user questions into embeddings.
3. Retrieve the most relevant scientific knowledge.
4. Extract environmental variables from the user's text.
5. Return clean evidence for the reasoning layer.
"""

import re
from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer


# =========================================================
# Configuration
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_PATH = PROJECT_ROOT / "data" / "chroma_db"

COLLECTION_NAME = "biodiversity_knowledge"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

DEFAULT_TOP_K = 8


# =========================================================
# Retriever
# =========================================================

class BiodiversityRetriever:

    def __init__(
        self,
        top_k: int = DEFAULT_TOP_K,
    ):
        self.top_k = top_k

        print(
            "Loading biodiversity retrieval model..."
        )

        self.model = SentenceTransformer(
            EMBEDDING_MODEL_NAME
        )

        print(
            "Connecting to ChromaDB..."
        )

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PATH)
        )

        try:
            self.collection = (
                self.client.get_collection(
                    name=COLLECTION_NAME
                )
            )
        except Exception as exc:
            raise RuntimeError(
                "Could not load ChromaDB collection "
                f"'{COLLECTION_NAME}'. "
                "Run 'python knowledge\\build_kb.py' first."
            ) from exc

        document_count = (
            self.collection.count()
        )

        if document_count == 0:
            raise RuntimeError(
                "The ChromaDB collection is empty."
            )

        print(
            f"Retriever ready. "
            f"Knowledge documents: {document_count}"
        )

    # -----------------------------------------------------
    # Extract environmental variables
    # -----------------------------------------------------

    def extract_environmental_variables(
        self,
        text: str,
    ) -> dict[str, Any]:

        variables: dict[str, Any] = {}

        text_lower = text.lower()

        # ---------------------------------------------
        # Soil pH
        # ---------------------------------------------

        ph_patterns = [
            r"ph\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)",
            r"soil\s+ph\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)",
        ]

        for pattern in ph_patterns:

            match = re.search(
                pattern,
                text_lower,
            )

            if match:
                variables["soil_ph"] = float(
                    match.group(1)
                )
                break

        # ---------------------------------------------
        # Soil organic carbon
        # ---------------------------------------------

        soc_patterns = [
            r"soil organic carbon\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)\s*(?:%|percent)",
            r"soc\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)\s*(?:%|percent)",
            r"organic carbon\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)\s*(?:%|percent)",
        ]

        for pattern in soc_patterns:

            match = re.search(
                pattern,
                text_lower,
            )

            if match:
                variables[
                    "soil_organic_carbon"
                ] = float(match.group(1))
                break

        # ---------------------------------------------
        # Rainfall
        # ---------------------------------------------

                # ---------------------------------------------
        # Rainfall
        # ---------------------------------------------

        # First handle qualitative rainfall descriptions.
        # Examples:
        #   rainfall is very low
        #   rainfall is low
        #   rainfall is moderate
        #   rainfall is high
        #   rainfall is very high

        rainfall_condition_patterns = [
            (
                r"(?:annual\s+)?rainfall\s*"
                r"(?:is|of|=|:)?\s*"
                r"(very\s+low|very\s+high|low|moderate|medium|high)"
            ),
            (
                r"precipitation\s*"
                r"(?:is|of|=|:)?\s*"
                r"(very\s+low|very\s+high|low|moderate|medium|high)"
            ),
        ]

        for pattern in rainfall_condition_patterns:

            match = re.search(
                pattern,
                text_lower,
            )

            if match:

                variables["rainfall"] = (
                    match.group(1).strip()
                )

                break

        # If a qualitative condition was not found,
        # check for numeric rainfall measurements.

        if "rainfall" not in variables:

            rainfall_patterns = [
                r"rainfall\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)\s*mm",
                r"annual rainfall\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)\s*mm",
                r"precipitation\s*(?:is|of|=|:)?\s*(\d+(?:\.\d+)?)\s*mm",
            ]

            for pattern in rainfall_patterns:

                match = re.search(
                    pattern,
                    text_lower,
                )

                if match:

                    variables["rainfall"] = float(
                        match.group(1)
                    )

                    break

        # ---------------------------------------------
        # Temperature
        # ---------------------------------------------

        temperature_patterns = [
            r"temperature\s*(?:is|of|=|:)?\s*(-?\d+(?:\.\d+)?)\s*°?\s*c",
            r"temp\s*(?:is|of|=|:)?\s*(-?\d+(?:\.\d+)?)\s*°?\s*c",
        ]

        for pattern in temperature_patterns:

            match = re.search(
                pattern,
                text_lower,
            )

            if match:
                variables["temperature"] = float(
                    match.group(1)
                )
                break

        # ---------------------------------------------
        # Land use
        # ---------------------------------------------

        land_use_keywords = {
            "monoculture": "monoculture",
            "cropland": "cropland",
            "agriculture": "agriculture",
            "agricultural": "agriculture",
            "forest": "forest",
            "forested": "forest",
            "grassland": "grassland",
            "wetland": "wetland",
            "pasture": "pasture",
            "agroforestry": "agroforestry",
        }

        for keyword, value in land_use_keywords.items():

            if keyword in text_lower:

                variables["land_use"] = value
                break

        # ---------------------------------------------
        # Crop type
        # ---------------------------------------------

        crop_keywords = [
            "wheat",
            "rice",
            "maize",
            "corn",
            "soybean",
            "soy",
            "cotton",
            "sugarcane",
            "millet",
            "sorghum",
            "barley",
            "pulses",
        ]

        for crop in crop_keywords:

            if crop in text_lower:

                variables["crop_type"] = (
                    "soybean"
                    if crop == "soy"
                    else (
                        "maize"
                        if crop == "corn"
                        else crop
                    )
                )

                break

        # ---------------------------------------------
        # Region
        # ---------------------------------------------

        region_keywords = [
            "semi-arid",
            "semi arid",
            "arid",
            "tropical",
            "temperate",
            "subtropical",
            "mediterranean",
            "dryland",
            "dry land",
        ]

        for region in region_keywords:

            if region in text_lower:

                variables["region"] = (
                    region.replace(
                        " ",
                        "-"
                    )
                )

                break

        # ---------------------------------------------
        # Biodiversity status
        # ---------------------------------------------

        biodiversity_keywords = [
            "low biodiversity",
            "poor biodiversity",
            "declining biodiversity",
            "biodiversity loss",
            "high biodiversity",
            "rich biodiversity",
            "pollinator decline",
            "pollinator loss",
        ]

        for status in biodiversity_keywords:

            if status in text_lower:

                if (
                    "low" in status
                    or "poor" in status
                    or "declining" in status
                    or "loss" in status
                ):
                    variables[
                        "biodiversity_status"
                    ] = "low_or_declining"

                else:
                    variables[
                        "biodiversity_status"
                    ] = "high"

                break

        return variables

    # -----------------------------------------------------
    # Semantic search
    # -----------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[dict[str, Any]]:

        if not query or not query.strip():
            return []

        if top_k is None:
            top_k = self.top_k

        top_k = max(
            1,
            min(
                top_k,
                self.collection.count(),
            ),
        )

        # -----------------------------------------------------
        # Build focused retrieval queries
        # -----------------------------------------------------
        #
        # A single semantic query can be dominated by one topic.
        # For example, a query containing "soil organic carbon"
        # may return five SOC documents even when rainfall,
        # land use and temperature are also important.
        #
        # We therefore combine:
        #   1. Original semantic query
        #   2. Focused environmental-topic queries
        #
        # Results are deduplicated and diversified by topic.
        # -----------------------------------------------------

        variables = self.extract_environmental_variables(query)

        retrieval_queries: list[str] = [query]

        if "soil_organic_carbon" in variables:
            retrieval_queries.append(
                "soil organic carbon soil health carbon storage"
            )

        if "soil_ph" in variables:
            retrieval_queries.append(
                "soil pH nutrient availability microbial biodiversity"
            )

        if "rainfall" in variables:
            retrieval_queries.append(
                "rainfall water availability drought water stress "
                "soil moisture biodiversity"
            )

        if "temperature" in variables:
            retrieval_queries.append(
                "high temperature heat stress crop stress "
                "soil biodiversity climate"
            )

        if "land_use" in variables:
            land_use = str(variables["land_use"])

            if land_use == "monoculture":
                retrieval_queries.append(
                    "monoculture crop diversification intercropping "
                    "agroforestry biodiversity"
                )
            elif land_use in {
                "agriculture",
                "cropland",
            }:
                retrieval_queries.append(
                    "agricultural land diversification agroforestry "
                    "pollinators biodiversity"
                )

        if "crop_type" in variables:
            retrieval_queries.append(
                f"{variables['crop_type']} crop diversification "
                "water soil biodiversity"
            )

        if "region" in variables:
            region = str(variables["region"])

            if region in {
                "semi-arid",
                "arid",
                "dryland",
            }:
                retrieval_queries.append(
                    "semi-arid dryland restoration drought "
                    "water conservation biodiversity"
                )
            elif region in {
                "tropical",
                "subtropical",
            }:
                retrieval_queries.append(
                    "tropical agriculture biodiversity "
                    "soil water ecosystem"
                )

        # Explicit biodiversity observations should trigger dedicated
        # pollinator / soil-fauna evidence retrieval.
        query_lower = query.lower()
        if any(term in query_lower for term in (
            "pollinator",
            "pollinators",
            "earthworm",
            "earthworms",
            "fewer pollinators",
            "declining pollinators",
        )):
            retrieval_queries.append(
                "pollinators earthworms farm biodiversity habitat "
                "crop diversification flowering vegetation"
            )

        # Monoculture plus low vegetation cover is a direct signal for
        # diversification / habitat evidence, even when biodiversity_status
        # was not explicitly extracted.
        if (
            "monoculture" in query_lower
            or "little vegetation cover" in query_lower
            or "low vegetation cover" in query_lower
        ):
            retrieval_queries.append(
                "farm diversification monoculture vegetation cover "
                "pollinator habitat biodiversity"
            )

        if "drainage" in query_lower or "wetland" in query_lower:
            retrieval_queries.append(
                "seasonal drainage wetland habitat biodiversity "
                "water retention habitat connectivity"
            )

        if "biodiversity_status" in variables:
            retrieval_queries.append(
                "biodiversity habitat pollinators ecosystem "
                "species conservation"
            )

        # Remove duplicate queries while preserving order.
        retrieval_queries = list(
            dict.fromkeys(retrieval_queries)
        )

        # -----------------------------------------------------
        # Retrieve candidate evidence
        # -----------------------------------------------------

        candidate_limit = max(
            top_k * 3,
            10,
        )

        candidates: dict[str, dict[str, Any]] = {}

        for retrieval_query in retrieval_queries:

            query_embedding = self.model.encode(
                retrieval_query,
                normalize_embeddings=True,
            ).tolist()

            results = self.collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=min(
                    candidate_limit,
                    self.collection.count(),
                ),
                include=[
                    "documents",
                    "metadatas",
                    "distances",
                ],
            )

            ids = results.get(
                "ids",
                [[]],
            )[0]

            documents = results.get(
                "documents",
                [[]],
            )[0]

            metadatas = results.get(
                "metadatas",
                [[]],
            )[0]

            distances = results.get(
                "distances",
                [[]],
            )[0]

            for index in range(len(ids)):

                metadata = (
                    metadatas[index]
                    if index < len(metadatas)
                    else {}
                )

                distance = (
                    distances[index]
                    if index < len(distances)
                    else None
                )

                similarity = (
                    1.0 - distance
                    if distance is not None
                    else None
                )

                item = {
                    "id": ids[index],
                    "content": documents[index],
                    "topic": metadata.get(
                        "topic",
                        "",
                    ),
                    "source": metadata.get(
                        "source",
                        "",
                    ),
                    "source_year": metadata.get(
                        "source_year",
                        "",
                    ),
                    "metrics_affected": metadata.get(
                        "metrics_affected",
                        "",
                    ),
                    "climate_zones": metadata.get(
                        "climate_zones",
                        "",
                    ),
                    "distance": distance,
                    "similarity": similarity,
                }

                # Keep the best similarity for each document.
                existing = candidates.get(ids[index])

                if (
                    existing is None
                    or (
                        similarity is not None
                        and (
                            existing["similarity"] is None
                            or similarity > existing["similarity"]
                        )
                    )
                ):
                    candidates[ids[index]] = item

        # -----------------------------------------------------
        # Rank candidates
        # -----------------------------------------------------

        ranked = sorted(
            candidates.values(),
            key=lambda item: (
                item["similarity"]
                if item["similarity"] is not None
                else -1.0
            ),
            reverse=True,
        )

        # -----------------------------------------------------
        # Topic-diverse selection
        # -----------------------------------------------------
        # Prefer one strong result from each distinct topic first, then
        # fill remaining slots by semantic similarity. This keeps evidence
        # coverage broad enough for multi-metric reasoning.

        selected: list[dict[str, Any]] = []
        selected_ids: set[str] = set()

        best_by_topic: dict[str, dict[str, Any]] = {}
        for item in ranked:
            topic = str(item.get("topic", "")).strip()
            if topic and topic not in best_by_topic:
                best_by_topic[topic] = item

        diverse_candidates = sorted(
            best_by_topic.values(),
            key=lambda item: (
                item["similarity"]
                if item["similarity"] is not None
                else -1.0
            ),
            reverse=True,
        )

        for item in diverse_candidates:
            if len(selected) >= top_k:
                break
            if item["id"] in selected_ids:
                continue
            selected.append(item)
            selected_ids.add(item["id"])

        for item in ranked:
            if len(selected) >= top_k:
                break
            if item["id"] in selected_ids:
                continue
            selected.append(item)
            selected_ids.add(item["id"])

        return selected[:top_k]
    # -----------------------------------------------------
    # Combined retrieval
    # -----------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
    ) -> dict[str, Any]:

        variables = (
            self.extract_environmental_variables(
                query
            )
        )

        evidence = self.search(
            query=query,
            top_k=top_k,
        )

        return {
            "query": query,
            "environmental_variables": variables,
            "evidence": evidence,
            "evidence_count": len(evidence),
        }


# =========================================================
# Simple standalone test
# =========================================================

def main():

    print("=" * 60)
    print("DARUKAA.EARTH - RETRIEVER TEST")
    print("=" * 60)

    retriever = BiodiversityRetriever(
        top_k=5
    )

    query = (
        "Soil organic carbon is 0.3%, "
        "rainfall is very low, "
        "I grow monoculture wheat "
        "in a semi-arid region, "
        "temperature is 38°C."
    )

    print("\nQUERY:")
    print(query)

    # -----------------------------------------------------
    # Extract variables
    # -----------------------------------------------------

    result = retriever.retrieve(
        query
    )

    print(
        "\nENVIRONMENTAL VARIABLES:"
    )

    if result["environmental_variables"]:

        for key, value in (
            result[
                "environmental_variables"
            ].items()
        ):

            print(
                f"  {key}: {value}"
            )

    else:

        print("  No variables detected.")

    # -----------------------------------------------------
    # Retrieved evidence
    # -----------------------------------------------------

    print(
        "\nRETRIEVED EVIDENCE:"
    )

    for index, item in enumerate(
        result["evidence"],
        start=1,
    ):

        similarity = item[
            "similarity"
        ]

        similarity_text = (
            f"{similarity:.4f}"
            if similarity is not None
            else "N/A"
        )

        print(
            f"\n{index}. "
            f"{item['id']}"
        )

        print(
            f"   Topic: {item['topic']}"
        )

        print(
            f"   Similarity: "
            f"{similarity_text}"
        )

        print(
            f"   Source: "
            f"{item['source']}"
        )

        print(
            f"   Content: "
            f"{item['content'][:250]}..."
        )

    print("\n" + "=" * 60)
    print("RETRIEVER TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()