"""
Build ChromaDB vector knowledge base for Darukaa.Earth.

Run from project root:

    python knowledge\build_kb.py
"""

import sys
from pathlib import Path

# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import chromadb
from sentence_transformers import SentenceTransformer

from knowledge.knowledge_base import (
    KNOWLEDGE_CHUNKS,
    validate_knowledge_base,
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

CHROMA_PATH = PROJECT_ROOT / "data" / "chroma_db"

COLLECTION_NAME = "biodiversity_knowledge"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# ---------------------------------------------------------
# Helper: convert metadata to Chroma-compatible values
# ---------------------------------------------------------

def normalize_metadata(chunk):
    """
    Convert the metadata fields in a knowledge chunk into
    values that ChromaDB can store safely.

    This supports both:
        "metrics_affected": ["soil", "biodiversity"]

    and:

        "metrics_affected": "soil, biodiversity"
    """

    topic = chunk.get("topic", "")
    source = chunk.get("source", "")
    source_year = chunk.get(
        "source_year",
        chunk.get("year", "")
    )

    metrics = chunk.get(
        "metrics_affected",
        []
    )

    climate_zones = chunk.get(
        "climate_zones",
        []
    )

    # Convert list → string
    if isinstance(metrics, list):
        metrics = ", ".join(
            str(item) for item in metrics
        )

    if isinstance(climate_zones, list):
        climate_zones = ", ".join(
            str(item) for item in climate_zones
        )

    return {
        "topic": str(topic),
        "source": str(source),
        "source_year": str(source_year),
        "metrics_affected": str(metrics),
        "climate_zones": str(climate_zones),
    }


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("DARUKAA.EARTH - KNOWLEDGE BASE BUILDER")
    print("=" * 60)

    # -----------------------------------------------------
    # 1. Validate knowledge base
    # -----------------------------------------------------

    print("\n[1/6] Validating knowledge base...")

    validate_knowledge_base()

    print(
        f"Knowledge chunks: {len(KNOWLEDGE_CHUNKS)}"
    )

    print("Knowledge base validation passed.")

    # -----------------------------------------------------
    # 2. Prepare ChromaDB directory
    # -----------------------------------------------------

    print("\n[2/6] Preparing ChromaDB...")

    CHROMA_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"ChromaDB path: {CHROMA_PATH}"
    )

    # -----------------------------------------------------
    # 3. Load embedding model
    # -----------------------------------------------------

    print("\n[3/6] Loading embedding model...")

    print(
        f"Model: {EMBEDDING_MODEL_NAME}"
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    embedding_dimension = (
        model.get_embedding_dimension()
    )

    print(
        f"Embedding dimension: {embedding_dimension}"
    )

    if embedding_dimension != 384:
        raise RuntimeError(
            "Unexpected embedding dimension. "
            f"Expected 384, got {embedding_dimension}."
        )

    print("Embedding model ready.")

    # -----------------------------------------------------
    # 4. Connect to ChromaDB
    # -----------------------------------------------------

    print("\n[4/6] Connecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    # Remove previous version so the database always
    # matches the current knowledge_base.py.
    try:

        client.delete_collection(
            name=COLLECTION_NAME
        )

        print(
            "Existing collection deleted."
        )

    except Exception:

        print(
            "No existing collection found."
        )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": (
                "Darukaa.Earth biodiversity and "
                "environmental intelligence knowledge base"
            ),
            "embedding_model": EMBEDDING_MODEL_NAME,
            "embedding_dimension": str(
                embedding_dimension
            ),
        },
    )

    print(
        f"Collection: {COLLECTION_NAME}"
    )

    # -----------------------------------------------------
    # 5. Generate embeddings and store documents
    # -----------------------------------------------------

    print(
        "\n[5/6] Generating embeddings..."
    )

    documents = []
    ids = []
    metadatas = []

    # IMPORTANT:
    # There is NO chunk["metadata"] here.
    # The existing knowledge_base.py stores the fields
    # directly inside each chunk.

    for chunk in KNOWLEDGE_CHUNKS:

        # Required fields
        chunk_id = chunk["id"]

        content = chunk["content"]

        # Normalize metadata
        chroma_metadata = normalize_metadata(
            chunk
        )

        ids.append(chunk_id)

        documents.append(content)

        metadatas.append(
            chroma_metadata
        )

    print(
        f"Generating {len(documents)} embeddings..."
    )

    embeddings = model.encode(
        documents,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    embeddings = embeddings.tolist()

    # -----------------------------------------------------
    # Validate embeddings
    # -----------------------------------------------------

    if len(embeddings) != len(documents):

        raise RuntimeError(
            "Embedding count does not match "
            "document count."
        )

    for index, vector in enumerate(
        embeddings
    ):

        if len(vector) != embedding_dimension:

            raise RuntimeError(
                f"Embedding {index} has dimension "
                f"{len(vector)} instead of "
                f"{embedding_dimension}."
            )

    # -----------------------------------------------------
    # Store in ChromaDB
    # -----------------------------------------------------

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        "Embeddings successfully stored."
    )

    # -----------------------------------------------------
    # 6. Verify ChromaDB
    # -----------------------------------------------------

    print(
        "\n[6/6] Verifying ChromaDB..."
    )

    stored_count = collection.count()

    print(
        f"Documents stored: {stored_count}"
    )

    expected_count = len(
        KNOWLEDGE_CHUNKS
    )

    if stored_count != expected_count:

        raise RuntimeError(
            f"Expected {expected_count} documents "
            f"but ChromaDB contains {stored_count}."
        )

    # -----------------------------------------------------
    # Semantic retrieval tests
    # -----------------------------------------------------

    print(
        "\nTesting semantic retrieval..."
    )

    test_queries = [
        "low soil organic carbon in dry farming",
        "how to improve pollinator biodiversity",
        "habitat fragmentation and wildlife",
        "water stress in semi-arid agriculture",
        "agroforestry and soil biodiversity",
    ]

    for query in test_queries:

        print("\n" + "-" * 60)

        print(
            f"QUERY: {query}"
        )

        query_embedding = model.encode(
            query,
            normalize_embeddings=True,
        ).tolist()

        results = collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=3,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        result_ids = results.get(
            "ids",
            [[]]
        )[0]

        result_documents = results.get(
            "documents",
            [[]]
        )[0]

        result_metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        result_distances = results.get(
            "distances",
            [[]]
        )[0]

        for i in range(
            len(result_ids)
        ):

            metadata = (
                result_metadatas[i]
            )

            topic = metadata.get(
                "topic",
                "unknown"
            )

            distance = (
                result_distances[i]
            )

            print(
                f"{i + 1}. "
                f"{result_ids[i]} | "
                f"topic={topic} | "
                f"distance={distance:.4f}"
            )

            preview = (
                result_documents[i]
                .replace("\n", " ")
                [:160]
            )

            print(
                f"   {preview}..."
            )

    # -----------------------------------------------------
    # Final status
    # -----------------------------------------------------

    print("\n" + "=" * 60)

    print(
        "KNOWLEDGE BASE BUILD COMPLETE"
    )

    print("=" * 60)

    print(
        f"Documents: {stored_count}"
    )

    print(
        f"Collection: {COLLECTION_NAME}"
    )

    print(
        f"Embedding model: "
        f"{EMBEDDING_MODEL_NAME}"
    )

    print(
        f"Embedding dimension: "
        f"{embedding_dimension}"
    )

    print(
        f"Database: {CHROMA_PATH}"
    )

    print(
        "\nSTATUS: READY FOR RETRIEVER"
    )

    print("=" * 60)


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()