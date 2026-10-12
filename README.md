# Darukaa.Earth — Biodiversity AI

A local AI prototype that turns a description of environmental conditions into recommendations backed by a curated knowledge base. It combines semantic retrieval, an Ollama language model, response validation, a heuristic health score, and an intervention plan.

## Start here

1. Describe a farm or landscape using information you actually know: soil carbon/pH, rainfall, temperature, crop, land use, or region.
2. Read the assessment, recommendations, evidence citations, missing information, and proposed time horizons.
3. Ask follow-up questions in the same session to build on the earlier context.

**Example:** "My soil organic carbon is 0.3%, rainfall is low, and I grow wheat in a semi-arid region. What should I consider first?"

The system is a decision-support prototype. Its score is heuristic, and evidence citations/validation do not establish that every generated recommendation is scientifically correct.

## Quick setup

Use a Python environment compatible with the dependencies in [requirements.txt](requirements.txt), plus Git and a running Ollama installation. From the repository root:

```sh
git clone https://github.com/parzival787/darukaa-biodiversity-ai.git
cd darukaa-biodiversity-ai
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
ollama pull llama3.2:3b
python knowledge/build_kb.py
python -m uvicorn api.main:app --reload --port 8000
```

In a second terminal with the same environment activated:

```sh
python -m streamlit run ui/app.py
```

Open the Streamlit URL printed by the terminal, normally http://localhost:8501. API documentation is at http://127.0.0.1:8000/docs. The first embedding-model download requires internet access.

The reasoner currently sets the Ollama URL and model in [core/reasoner.py](core/reasoner.py). The UI supports `DARUKAA_API_URL` when the API is hosted at a different address.

## Repository map

- [ui/app.py](ui/app.py): chat interface and API client.
- [api/main.py](api/main.py): `/health`, `/chat`, and `/analyze` endpoints.
- [core/retriever.py](core/retriever.py): environmental variable extraction and evidence retrieval.
- [core/reasoner.py](core/reasoner.py): local LLM calls and response processing.
- [core/validator.py](core/validator.py): output checks.
- [core/scoring.py](core/scoring.py): heuristic health score.
- [core/planner.py](core/planner.py): intervention roadmap.
- [knowledge/knowledge_base.py](knowledge/knowledge_base.py): curated evidence.
- [knowledge/build_kb.py](knowledge/build_kb.py): builds the persistent ChromaDB collection.

## API usage and storage

| Endpoint | Request |
| --- | --- |
| `GET /health` | Component readiness flags |
| `POST /chat` | JSON containing `message` and a `session_id` |
| `POST /analyze` | Structured environmental fields such as `soil_ph`, `soil_organic_carbon`, `rainfall`, `crop_type`, `region`, plus `session_id` |

Example body for `POST /chat`:

```json
{
  "message": "My soil organic carbon is 0.3% and rainfall is low. What information should I collect next?",
  "session_id": "farm-demo-1"
}
```

Reuse the session ID for follow-up questions; use a distinct ID for each independent conversation. Omitting it uses the shared `default-session`. Conversation memory is held in the API process, retains up to ten turns and is lost on restart; it is not a persistent account/history system.

The evidence collection persists in `data/chroma_db` using `all-MiniLM-L6-v2` embeddings. Running `knowledge/build_kb.py` rebuilds the named knowledge collection, so treat it as a rebuild operation rather than a conversation backup.

## Checking a local installation

1. Run Ollama with `llama3.2:3b` available, build the knowledge collection, and start the API.
2. Open `/health` and check that `components.retriever` and `components.reasoner` are both true. The top-level `status: healthy` alone is not sufficient.
3. Send the sample chat request through `/docs`, then provide another environmental fact with the same session ID.
4. Open Streamlit and confirm that the assessment, retrieved evidence and follow-up context appear.

If initialization failed, fix the missing collection/model or Ollama connection and restart the API; the components are initialized when the module loads. Change `DARUKAA_API_URL` for the UI's API destination; the Ollama URL/model are separate settings in `core/reasoner.py`.

The local-model architecture still needs downloads during setup. Generated confidence and health scores are heuristic indicators, not calibrated probabilities or field validation.

## Detailed design notes

### 1. Project Overview

Darukaa.Earth AI Biodiversity Intelligence Chatbot is a Retrieval-Augmented Generation (RAG) based system designed to analyze environmental conditions and provide evidence-backed biodiversity and land-management recommendations.

Instead of relying only on a general-purpose language model, the system retrieves relevant scientific knowledge from a curated biodiversity knowledge base and passes that evidence to a local LLM for reasoning.

The system can reason across multiple environmental dimensions such as:

Soil organic carbon

Soil pH

Rainfall and water availability

Temperature

Land use

Crop type

Region / climate zone

Biodiversity status

The final response contains structured recommendations, environmental variables used, impacted metrics, evidence citations, time horizon, confidence, validation information, and an intervention roadmap.

### 2. System Architecture

                         ┌───────────────────────────┐
                         │        USER / FARMER       │
                         │                           │
                         │ Natural Language Query    │
                         │ or Structured JSON Input  │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │       STREAMLIT UI         │
                         │       ui/app.py            │
                         │                           │
                         │ Chat Interface             │
                         │ Evidence Display           │
                         │ Recommendations            │
                         │ Health Score               │
                         │ Intervention Roadmap       │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │       FASTAPI API          │
                         │       api/main.py          │
                         │                           │
                         │ /chat                     │
                         │ /analyze                  │
                         │ /health                   │
                         └─────────────┬─────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    │                                     │
                    ▼                                     ▼
        ┌────────────────────────┐             ┌──────────────────────┐
        │  CONVERSATION MEMORY   │             │     RETRIEVER        │
        │ core/conversation.py   │             │ core/retriever.py    │
        │                        │             │                      │
        │ Session history        │             │ Variable extraction  │
        │ Previous context       │             │ Query embedding      │
        └────────────┬───────────┘             │ Semantic retrieval   │
                     │                         └──────────┬───────────┘
                     │                                    │
                     │                                    ▼
                     │                         ┌──────────────────────┐
                     │                         │       ChromaDB       │
                     │                         │                      │
                     │                         │ biodiversity_        │
                     │                         │ knowledge            │
                     │                         │                      │
                     │                         │ 70 knowledge chunks  │
                     │                         │ + scientific metadata│
                     │                         └──────────┬───────────┘
                     │                                    │
                     └────────────────┬───────────────────┘
                                      │
                                      ▼
                         ┌───────────────────────────┐
                         │     LOCAL REASONER        │
                         │     core/reasoner.py      │
                         │                           │
                         │ Prompt + User Variables   │
                         │ + Retrieved Evidence      │
                         │ + Conversation Context    │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │          OLLAMA           │
                         │                           │
                         │       llama3.2:3b         │
                         │       Local LLM           │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │     STRUCTURED JSON       │
                         │                           │
                         │ Assessment                │
                         │ Recommendations           │
                         │ Metrics                   │
                         │ Citation                  │
                         │ Confidence                │
                         │ Missing information       │
                         └─────────────┬─────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
        ┌────────────────────────┐             ┌──────────────────────┐
        │       VALIDATOR        │             │    HEALTH SCORER     │
        │                        │             │                      │
        │ Citation checks       │             │ Environmental score  │
        │ Required fields       │             │ Biodiversity factors │
        │ Variables / metrics   │             │ Constraint analysis  │
        └────────────┬───────────┘             └──────────┬───────────┘
                     │                                    │
                     └────────────────┬───────────────────┘
                                      │
                                      ▼
                         ┌───────────────────────────┐
                         │   INTERVENTION PLANNER    │
                         │                           │
                         │ Short-term: 0–3 months   │
                         │ Medium-term: 3–12 months │
                         │ Long-term: 1–3 years     │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │       FINAL RESPONSE      │
                         │                           │
                         │ Evidence-backed actions   │
                         │ Metrics + time horizon    │
                         │ Confidence + citations    │
                         │ Health score + roadmap    │
                         └───────────────────────────┘

### 3. How the System Works

Step 1 — User Input

The user provides environmental information in natural language.

Example:

Soil organic carbon is 0.3%, rainfall is very low, I grow monoculture wheat in a semi-arid region, and temperature is 38°C.

The API accepts natural-language chat input and also supports structured environmental information through the analysis interface.

Step 2 — Environmental Variable Extraction

core/retriever.py extracts measurable or explicitly stated environmental variables from the query.

For example:

{
  "soil_organic_carbon": 0.3,
  "rainfall": "very low",
  "land_use": "monoculture",
  "crop_type": "wheat",
  "region": "semi-arid",
  "temperature": 38
}

The system only treats information explicitly present in the user's input as an environmental variable. It does not invent missing measurements.

### 4. Knowledge Retrieval

The retriever converts the query into embeddings using:

Sentence Transformers
all-MiniLM-L6-v2
384-dimensional embeddings

The embeddings are compared against the persistent ChromaDB knowledge base.

Knowledge Base

Collection:

biodiversity_knowledge

The current knowledge base contains approximately 70 scientific knowledge chunks covering topics such as:

Soil organic carbon

Soil pH

Soil microbiology

Water availability

Temperature stress

Semi-arid restoration

Farm diversification

Agroforestry

Pollinators

Habitat fragmentation

Land use

Wetland biodiversity

Invasive species

Nitrogen cycle

Deforestation

Each evidence chunk contains metadata such as:

ID
Topic
Scientific source
Source year
Affected metrics
Climate zones
Content

This allows the reasoning layer to show where recommendations originate.

### 5. Multi-Topic Retrieval

A single semantic query can sometimes be dominated by one environmental topic.

For example, a query containing "soil organic carbon" may retrieve mostly soil-related documents even when temperature, water and land-use conditions are also important.

The retriever therefore creates focused retrieval queries for relevant environmental dimensions.

Examples:

soil organic carbon → soil health / carbon storage

soil pH → nutrient availability / microbial biodiversity

rainfall → water availability / drought / soil moisture

temperature → heat stress / climate / soil biodiversity

monoculture → crop diversification / agroforestry / biodiversity

semi-arid → dryland restoration / water conservation / biodiversity

Retrieved documents are then deduplicated and diversified by topic before being supplied to the reasoning layer.

### 6. Evidence-Grounded Reasoning

core/reasoner.py combines:

User Query
     +
Extracted Environmental Variables
     +
Retrieved Scientific Evidence
     +
Conversation History

and sends them to the local Ollama model.

The configured local model is:

llama3.2:3b

Ollama runs locally at:

http://localhost:11434

The reasoning prompt requires the model to:

Produce actionable recommendations.

Ground recommendations in retrieved evidence.

Cite the evidence chunk used.

Use only environmental variables actually extracted.

Avoid inventing missing environmental data.

Connect multiple environmental variables.

Identify impacted metrics.

Provide a time horizon.

Provide confidence.

Use quantitative estimates only when supported by retrieved evidence.

Explicitly state when a quantitative estimate is unavailable.

### 7. Scientific Evidence and Citations

Every recommendation contains a citation such as:

EVIDENCE 1
EVIDENCE 2
EVIDENCE 3

The citation refers directly to a retrieved knowledge chunk supplied to the reasoning layer.

The system is designed to prevent unsupported recommendations from being presented as evidence-backed conclusions.

For example, if retrieved evidence contains a quantitative finding relevant to soil organic carbon, that value may be used in the estimate.

If no relevant quantitative evidence exists, the system uses:

Quantitative estimate unavailable from retrieved evidence

This avoids fabricating numerical scientific claims.

### 8. Multi-Metric Reasoning

The chatbot is designed to reason about interactions between environmental factors rather than treating each variable independently.

Examples include:

Soil health
      ↕
Soil organic carbon
      ↕
Water retention / runoff
      ↕
Vegetation cover
      ↕
Biodiversity

and:

Low rainfall
      +
High temperature
      +
Limited irrigation
      ↓
Water stress
      ↓
Vegetation stress
      ↓
Habitat and biodiversity pressure

and:

Monoculture
      ↓
Low agricultural diversity
      ↓
Reduced habitat heterogeneity
      ↓
Potential biodiversity pressure

The exact relationship stated in the final answer is constrained by the retrieved scientific evidence.

### 9. Validation Layer

The structured response is passed through the biodiversity validator.

The validator checks:

Required recommendation fields

Recommendation count

Action quality

Scientific reasoning

Environmental variables

Minimum relevant variables

Impacted metrics

Evidence citation validity

Improvement estimate

Time horizon

Confidence

Consistency with extracted environmental variables

A recommendation should not pass validation when its citation does not support the proposed intervention or when required environmental information is incorrectly represented.

### 10. Biodiversity Health Score

The health-scoring component provides a structured assessment of the environmental situation.

It considers the available environmental constraints and produces a heuristic biodiversity/environmental score.

The score is intended as a decision-support indicator for the prototype rather than a replacement for field measurements or professional ecological assessment.

### 11. Intervention Planner

The intervention planner converts recommendations into a practical roadmap.

Short-Term

0–3 months

Immediate management actions.

Medium-Term

3–12 months

Actions that require a growing or management cycle to show results.

Long-Term

1–3 years

Landscape-scale or structural interventions.

The planner does not invent a new recommendation. It organizes the validated recommendations according to their supplied time horizons.

### 12. Conversation Memory

The system maintains session-level conversation context.

This allows follow-up questions to build on previously provided environmental information.

For example:

User:
My soil organic carbon is 0.3%.

Assistant:
...

User:
What should I do first?


The system can use the accumulated session context when processing the follow-up request.

### 13. API

The backend is implemented using FastAPI.

Health Check

GET /health

Returns the status of the main system components.

Chat

POST /chat

Used for natural-language biodiversity analysis and conversational interaction.

Structured Analysis

POST /analyze

Supports structured environmental input such as:

{
  "soil_organic_carbon": 0.3,
  "soil_ph": 8.1,
  "rainfall": "very low",
  "land_use": "monoculture",
  "crop_type": "wheat",
  "region": "semi-arid",
  "temperature": 38
}

### 14. Project Structure

darukaa-biodiversity-ai/
│
├── api/
│   └── main.py
│
├── core/
│   ├── retriever.py
│   ├── reasoner.py
│   └── conversation.py
│
├── knowledge/
│   ├── knowledge_base.py
│   └── build_kb.py
│
├── data/
│   └── chroma_db/
│
├── ui/
│   └── app.py
│
├── core/validator.py
├── core/planner.py
├── core/scoring.py
├── requirements.txt
├── README.md
└── .env

### 15. Technology Stack

Layer

Technology

Frontend

Streamlit

Backend

FastAPI

Programming Language

Python

Vector Database

ChromaDB

Embeddings

Sentence Transformers

Embedding Model

all-MiniLM-L6-v2

LLM Runtime

Ollama

LLM

llama3.2:3b

Knowledge Storage

ChromaDB persistent collection

API Format

JSON / REST

Environment

Local Python virtual environment

### 16. Local Setup

Prerequisites

Install:

A Python environment compatible with requirements.txt

Ollama

Git

Ensure Ollama is running.

Check:

ollama --version

Check installed models:

ollama list

Make sure the required model is available:

ollama pull llama3.2:3b

Create Virtual Environment

Windows PowerShell:

python -m venv .venv
.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Build Knowledge Base

If the ChromaDB database needs to be created or rebuilt:

python knowledge\build_kb.py

Start FastAPI

python -m uvicorn api.main:app --reload

The API will normally be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

Start Streamlit

Open another terminal:

.venv\Scripts\Activate.ps1
streamlit run ui\app.py

### 17. Environment Configuration

The current reasoner uses constants in `core/reasoner.py` for `http://localhost:11434` and `llama3.2:3b`; setting `OLLAMA_BASE_URL` or `OLLAMA_MODEL` in a `.env` file does not override those constants. The Streamlit client reads `DARUKAA_API_URL` from its process environment.

### 18. Example End-to-End Flow

Input:

I have a semi-arid farm with soil organic carbon of 0.3%.
The soil pH is 8.1. Most of the land is monoculture wheat.
Temperature regularly goes above 40 C and irrigation is limited.

Processing:

### 1. Extract environmental variables
          ↓
### 2. Generate semantic retrieval queries
          ↓
### 3. Retrieve relevant scientific evidence
          ↓
### 4. Build evidence-grounded reasoning prompt
          ↓
### 5. Generate structured JSON using Ollama
          ↓
### 6. Validate recommendations and citations
          ↓
### 7. Calculate environmental/biodiversity score
          ↓
### 8. Build intervention roadmap
          ↓
### 9. Display final response in Streamlit

### 19. Design Principles

The project follows several important principles.

Evidence First

Recommendations should be based on retrieved scientific knowledge rather than unsupported LLM-generated claims.

No Invented Measurements

If the user does not provide a measurement, the system should not manufacture one.

Traceability

Each recommendation identifies the evidence chunk used to support it.

Multi-Dimensional Reasoning

Environmental variables are considered together where the retrieved evidence supports their interaction.

Structured Output

The final response follows a predictable JSON structure so that it can be consumed by the API and UI.

Local AI

The reasoning layer uses Ollama locally, reducing dependence on external LLM APIs during demonstration.

### 20. Limitations

This project is a prototype decision-support system.

It does not replace:

Field sampling

Soil laboratory testing

Professional ecological surveys

Local agronomic advice

Biodiversity monitoring programs

Recommendations depend on the quality and coverage of the retrieved knowledge base and the information supplied by the user.

When the available evidence does not provide a quantitative effect size, the system explicitly reports that a quantitative estimate is unavailable rather than generating an unsupported number.

### 21. Testing

Basic component checks can be performed with:

python -m py_compile core\retriever.py
python -m py_compile core\reasoner.py
python -m py_compile api\main.py
python -m py_compile core/validator.py
python -m py_compile core/planner.py

Check the API:

GET /health

Then test the end-to-end flow through:

POST /chat

and the Streamlit UI.

### 22. Submission Notes

For the hackathon/job submission, provide:

GitHub repository URL

Live demo URL, if deployed

This README overview

Any required reviewer credentials or access instructions

If the GitHub repository is private, grant access to the intended reviewers through GitHub permissions.

If the repository is public, only the repository URL is required.

### 23. Project Summary

Darukaa.Earth combines:

Environmental Data
        +
Semantic Search
        +
Scientific Knowledge
        +
Local LLM Reasoning
        +
Validation
        +
Environmental Scoring
        +
Intervention Planning

to create an evidence-grounded biodiversity intelligence system capable of turning environmental conditions into structured, traceable and actionable recommendations.