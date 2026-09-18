"""
Darukaa.Earth Biodiversity Intelligence
Scientific Knowledge Base

This file contains structured evidence cards used by the RAG system.

Important:
- Numerical claims are tied to named scientific sources.
- The LLM must not invent evidence outside these records.
- Each record contains the environmental metrics it can support.
"""

from typing import List, Dict, Any


KNOWLEDGE_CHUNKS: List[Dict[str, Any]] = [

    # ============================================================
    # SOIL ORGANIC CARBON
    # ============================================================

    {
        "id": "soc_001",
        "topic": "soil_organic_carbon",
        "content": (
            "Cover cropping can increase soil organic carbon compared with bare "
            "soil management. A global meta-analysis of 93 peer-reviewed studies "
            "reported an average 12% increase in total soil organic carbon under "
            "cover crops. The response varied with soil type and experimental duration."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2023), "
            "'Soil organic carbon fractions in response to soil, environmental "
            "and agronomic factors under cover cropping systems: A global meta-analysis', "
            "DOI: 10.1016/j.agee.2023.108591"
        ),
        "source_year": 2023,
        "metrics_affected": [
            "soil_organic_carbon",
            "soil_health",
            "microbial_biomass"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "soc_002",
        "topic": "soil_organic_carbon",
        "content": (
            "Microbial biomass carbon is one of the soil carbon fractions that "
            "responds strongly to cover cropping. A global meta-analysis reported "
            "an average 33% increase in microbial biomass carbon under cover crops "
            "relative to bare soil management. The magnitude of the response depends "
            "on environmental and management conditions."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2023), "
            "global cover-cropping SOC meta-analysis, "
            "DOI: 10.1016/j.agee.2023.108591"
        ),
        "source_year": 2023,
        "metrics_affected": [
            "microbial_biomass",
            "soil_organic_carbon",
            "soil_health"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "soc_003",
        "topic": "soil_organic_carbon",
        "content": (
            "A meta-analysis of soil organic carbon fractions found that cover "
            "cropping increased particulate organic carbon by approximately 14.94% "
            "and mineral-associated organic carbon by approximately 5.56%. These "
            "responses are influenced by carbon inputs, soil depth, season and "
            "temperature."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2023), "
            "'Response of soil organic carbon fractions to cover cropping', "
            "DOI: 10.1016/j.agee.2023.108497"
        ),
        "source_year": 2023,
        "metrics_affected": [
            "particulate_organic_carbon",
            "mineral_associated_carbon",
            "soil_organic_carbon"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "soc_004",
        "topic": "soil_organic_carbon",
        "content": (
            "Soil carbon responses to cover crops are not identical across all "
            "sites. Experimental duration and soil characteristics influence the "
            "size of the response. Therefore, recommendations should treat reported "
            "percentage changes as evidence-based estimates rather than guarantees "
            "for an individual farm."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2023), "
            "global cover-cropping SOC meta-analysis, "
            "DOI: 10.1016/j.agee.2023.108591"
        ),
        "source_year": 2023,
        "metrics_affected": [
            "soil_organic_carbon",
            "soil_health",
            "confidence"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "soc_005",
        "topic": "soil_organic_carbon",
        "content": (
            "Organic amendments, conservation tillage and cover cropping are "
            "management practices associated with increases in soil organic carbon "
            "in agricultural systems. A meta-analysis of organic farming systems "
            "reported an average 18% improvement in depth-weighted soil organic "
            "carbon concentration under evaluated best management practices."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2021), "
            "'Soil organic carbon is affected by organic amendments, conservation "
            "tillage, and cover cropping in organic farming systems', "
            "DOI: 10.1016/j.agee.2021.107356"
        ),
        "source_year": 2021,
        "metrics_affected": [
            "soil_organic_carbon",
            "soil_health",
            "carbon_storage"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },


    # ============================================================
    # SOIL MICROBIOME
    # ============================================================

    {
        "id": "microbe_001",
        "topic": "soil_microbiology",
        "content": (
            "Cover cropping can improve several components of the soil microbiome. "
            "A meta-analysis of 60 studies reported increases of approximately "
            "27% in microbial abundance, 22% in microbial activity and 2.5% in "
            "microbial diversity compared with bare fallow."
        ),
        "source": (
            "Soil Biology and Biochemistry (2020), "
            "'Do cover crops benefit soil microbiome? A meta-analysis of current research', "
            "DOI: 10.1016/j.soilbio.2019.107701"
        ),
        "source_year": 2020,
        "metrics_affected": [
            "microbial_abundance",
            "microbial_activity",
            "microbial_diversity"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "microbe_002",
        "topic": "soil_microbiology",
        "content": (
            "Cover crop effects on microbial communities depend on climate, "
            "termination method and tillage. Therefore, a recommendation involving "
            "cover crops should consider rainfall, temperature and management method "
            "rather than treating cover crops as universally identical."
        ),
        "source": (
            "Soil Biology and Biochemistry (2020), "
            "cover-cropping soil microbiome meta-analysis, "
            "DOI: 10.1016/j.soilbio.2019.107701"
        ),
        "source_year": 2020,
        "metrics_affected": [
            "microbial_diversity",
            "microbial_activity",
            "management_risk"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "microbe_003",
        "topic": "soil_microbiology",
        "content": (
            "A separate meta-analysis found cover crops increased microbial biomass "
            "carbon, microbial biomass nitrogen and phospholipid fatty acid indicators "
            "by roughly 24–51% compared with fallow treatments. Effects differed with "
            "cover crop species, residue management, soil and climate."
        ),
        "source": (
            "Geoderma (2021), "
            "'Cover cropping enhances soil microbial biomass and affects microbial "
            "community structure: A meta-analysis', "
            "DOI: 10.1016/j.geoderma.2020.114696"
        ),
        "source_year": 2021,
        "metrics_affected": [
            "microbial_biomass",
            "microbial_community_structure",
            "soil_health"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "microbe_004",
        "topic": "soil_microbiology",
        "content": (
            "Organic amendments can alter soil microbial communities and increase "
            "microbial diversity. Evidence indicates that the response differs among "
            "microbial groups and is influenced by soil texture and the characteristics "
            "of the organic material applied."
        ),
        "source": (
            "Science of the Total Environment (2023), "
            "'Investigating the effects of organic amendments on soil microbial "
            "composition and its linkage to soil organic carbon', "
            "DOI: 10.1016/j.scitotenv.2023.164899"
        ),
        "source_year": 2023,
        "metrics_affected": [
            "microbial_diversity",
            "soil_organic_carbon",
            "microbial_composition"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "microbe_005",
        "topic": "soil_microbiology",
        "content": (
            "Organic amendments have been associated with higher microbial diversity "
            "and microbial functionality compared with mineral fertilization in "
            "meta-analytic evidence. Microbial diversity is positively associated "
            "with microbial functionality and can be relevant to crop productivity."
        ),
        "source": (
            "Science of the Total Environment (2022), "
            "'Organic amendments enhance soil microbial diversity, microbial "
            "functionality and crop yields: A meta-analysis', "
            "DOI: 10.1016/j.scitotenv.2022.154627"
        ),
        "source_year": 2022,
        "metrics_affected": [
            "microbial_diversity",
            "microbial_functionality",
            "crop_productivity"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },


    # ============================================================
    # FARM DIVERSIFICATION
    # ============================================================

    {
        "id": "diversification_001",
        "topic": "farm_diversification",
        "content": (
            "Diversified farming systems can support higher biodiversity than "
            "simplified farming systems. A global meta-analysis of 161 peer-reviewed "
            "articles reported an average 26% increase in overall species richness "
            "in diversified farming systems."
        ),
        "source": (
            "Global meta-analysis of diversified farming systems, "
            "Agriculture, Ecosystems & Environment (2019), "
            "global synthesis of 161 peer-reviewed articles"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "species_richness",
            "farm_diversity",
            "beneficial_species"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "diversification_002",
        "topic": "farm_diversification",
        "content": (
            "Diversified farming can increase the richness and abundance of "
            "beneficial organisms while potentially reducing some pest groups. "
            "The magnitude of these effects varies with landscape context and the "
            "amount of semi-natural habitat surrounding farms."
        ),
        "source": (
            "Global meta-analysis of diversified farming systems, "
            "Agriculture, Ecosystems & Environment (2019)"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "species_richness",
            "pollinator_richness",
            "natural_enemy_abundance",
            "pest_pressure"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "diversification_003",
        "topic": "farm_diversification",
        "content": (
            "The positive biodiversity response to diversified farming can be "
            "stronger in landscapes with less surrounding semi-natural vegetation. "
            "This means farm-level diversification and landscape-level habitat "
            "availability should be considered together."
        ),
        "source": (
            "Global meta-analysis of diversified farming systems, "
            "Agriculture, Ecosystems & Environment (2019)"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "species_richness",
            "habitat_context",
            "pollinator_richness"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "diversification_004",
        "topic": "farm_diversification",
        "content": (
            "Introducing multiple crops or functional plant groups can increase "
            "structural and resource diversity within agricultural systems. "
            "This can create additional habitat and food resources for beneficial "
            "organisms compared with highly simplified production systems."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "habitat_diversity",
            "species_richness",
            "ecosystem_resilience"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "diversification_005",
        "topic": "farm_diversification",
        "content": (
            "FAO identifies biodiversity as important for healthy soils, pollination, "
            "pest control and wildlife habitat. Diversifying production systems by "
            "using multiple species, varieties or integrated crop, livestock and "
            "forest components can support resilience under changing conditions."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "ecosystem_resilience",
            "soil_health",
            "pollination",
            "habitat_diversity"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },


    # ============================================================
    # AGROFORESTRY
    # ============================================================

    {
        "id": "agroforestry_001",
        "topic": "agroforestry",
        "content": (
            "Agroforestry can provide biodiversity and ecosystem-service benefits "
            "relative to simplified agricultural systems, but the magnitude depends "
            "on system design. A European meta-analysis of 53 publications found "
            "an overall positive effect of agroforestry on biodiversity and ecosystem "
            "services, with an effect size of approximately 0.454."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2016), "
            "'Do European agroforestry systems enhance biodiversity and ecosystem "
            "services? A meta-analysis', DOI: 10.1016/j.agee.2016.06.002"
        ),
        "source_year": 2016,
        "metrics_affected": [
            "biodiversity",
            "ecosystem_services",
            "soil_fertility"
        ],
        "climate_zones": [
            "temperate",
            "mediterranean",
            "tropical"
        ],
    },

    {
        "id": "agroforestry_002",
        "topic": "agroforestry",
        "content": (
            "Agroforestry effects are context dependent. Evidence from European "
            "systems indicates benefits for erosion control, biodiversity and soil "
            "fertility, while effects on biomass production were not uniformly "
            "positive across systems."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2016), "
            "European agroforestry meta-analysis, "
            "DOI: 10.1016/j.agee.2016.06.002"
        ),
        "source_year": 2016,
        "metrics_affected": [
            "erosion_control",
            "biodiversity",
            "soil_fertility",
            "biomass_production"
        ],
        "climate_zones": [
            "temperate",
            "mediterranean"
        ],
    },

    {
        "id": "agroforestry_003",
        "topic": "agroforestry",
        "content": (
            "A global meta-analysis of coffee and cacao systems found biodiversity "
            "and ecosystem-service responses depended strongly on management intensity. "
            "Species richness declined when agroforestry systems were intensified "
            "toward plantation systems."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2013), "
            "'A global meta-analysis of the biodiversity and ecosystem service "
            "benefits of coffee and cacao agroforestry', "
            "DOI: 10.1016/j.agee.2013.05.003"
        ),
        "source_year": 2013,
        "metrics_affected": [
            "species_richness",
            "ecosystem_services",
            "management_intensity"
        ],
        "climate_zones": [
            "tropical"
        ],
    },

    {
        "id": "agroforestry_004",
        "topic": "agroforestry",
        "content": (
            "In the coffee and cacao meta-analysis, total species richness was "
            "approximately 46% lower when comparing agroforest with plantation "
            "systems, while the comparison between natural forest and agroforest "
            "showed an approximately 11% difference. These results demonstrate that "
            "management intensity and reference condition matter."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2013), "
            "coffee and cacao agroforestry meta-analysis, "
            "DOI: 10.1016/j.agee.2013.05.003"
        ),
        "source_year": 2013,
        "metrics_affected": [
            "species_richness",
            "habitat_quality",
            "management_intensity"
        ],
        "climate_zones": [
            "tropical"
        ],
    },

    {
        "id": "agroforestry_005",
        "topic": "agroforestry",
        "content": (
            "Evidence from a Brazilian Atlantic Forest meta-analysis indicates that "
            "biodiverse agroforestry systems can provide higher biodiversity and "
            "ecosystem-service levels than conventional production systems. The "
            "benefits varied according to the design and diversity of the agroforestry system."
        ),
        "source": (
            "Forest Ecology and Management (2019), "
            "Brazilian Atlantic Forest agroforestry meta-analysis, "
            "DOI: 10.1016/j.foreco.2018.10.064"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "biodiversity",
            "ecosystem_services",
            "habitat_quality"
        ],
        "climate_zones": [
            "tropical"
        ],
    },


    # ============================================================
    # POLLINATORS
    # ============================================================

    {
        "id": "pollinator_001",
        "topic": "pollinators",
        "content": (
            "Agricultural biodiversity supports pollination services. FAO identifies "
            "pollination as one of the ecosystem services supported by biodiversity "
            "in food and agricultural systems. Habitat diversity around production "
            "areas can therefore be relevant when pollinator support is a management goal."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "pollination",
            "pollinator_support",
            "habitat_diversity"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "pollinator_002",
        "topic": "pollinators",
        "content": (
            "Diversified farming systems can increase beneficial species richness "
            "and can support pollinator abundance and richness. The magnitude of "
            "the response depends on the surrounding landscape and availability "
            "of semi-natural habitat."
        ),
        "source": (
            "Global meta-analysis of diversified farming systems, "
            "Agriculture, Ecosystems & Environment (2019)"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "pollinator_richness",
            "pollinator_abundance",
            "habitat_diversity"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "pollinator_003",
        "topic": "pollinators",
        "content": (
            "Habitat diversification can create additional resources for pollinators "
            "within agricultural landscapes. Recommendations should consider flowering "
            "resources, semi-natural habitat and the surrounding landscape rather than "
            "only the crop itself."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "pollinator_support",
            "habitat_diversity",
            "species_richness"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "pollinator_004",
        "topic": "pollinators",
        "content": (
            "Pollinator-related recommendations should be evaluated alongside "
            "landscape context. Evidence from diversified farming systems indicates "
            "that responses can be stronger where farms are farther from natural or "
            "semi-natural habitat, although effects vary among organism groups."
        ),
        "source": (
            "Global meta-analysis of diversified farming systems, "
            "Agriculture, Ecosystems & Environment (2019)"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "pollinator_richness",
            "habitat_connectivity",
            "species_richness"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "pollinator_005",
        "topic": "pollinators",
        "content": (
            "Biodiversity in agricultural systems contributes to pollination and "
            "other ecosystem services. Increasing habitat diversity is therefore "
            "a potential pathway for improving ecological function, but individual "
            "outcomes depend on local species and environmental conditions."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "pollination",
            "ecosystem_services",
            "habitat_diversity"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },


    # ============================================================
    # LAND USE AND HABITAT
    # ============================================================

    {
        "id": "landuse_001",
        "topic": "land_use",
        "content": (
            "Land-use simplification can reduce habitat diversity within agricultural "
            "systems. Diversified farming provides additional plant and habitat "
            "resources and can increase overall species richness compared with "
            "simplified farming systems."
        ),
        "source": (
            "Global meta-analysis of diversified farming systems, "
            "Agriculture, Ecosystems & Environment (2019)"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "land_use_diversity",
            "habitat_diversity",
            "species_richness"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "landuse_002",
        "topic": "land_use",
        "content": (
            "Agricultural biodiversity includes diversity within fields and across "
            "the wider production landscape. FAO emphasizes that diversification "
            "using multiple species, varieties and integrated production components "
            "can contribute to resilience and ecosystem services."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "landscape_diversity",
            "ecosystem_resilience",
            "species_richness"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "landuse_003",
        "topic": "land_use",
        "content": (
            "A biodiversity assessment should distinguish between the crop itself "
            "and the surrounding habitat. The proportion of semi-natural vegetation "
            "near farms can modify the response of biodiversity to farm management."
        ),
        "source": (
            "Global meta-analysis of diversified farming systems, "
            "Agriculture, Ecosystems & Environment (2019)"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "habitat_context",
            "species_richness",
            "landscape_diversity"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "landuse_004",
        "topic": "land_use",
        "content": (
            "Management intensity is an important variable when evaluating biodiversity. "
            "Evidence from agroforestry systems shows that intensification toward "
            "simplified plantation systems can be associated with reductions in "
            "species richness and ecosystem-service provision."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2013), "
            "coffee and cacao agroforestry meta-analysis, "
            "DOI: 10.1016/j.agee.2013.05.003"
        ),
        "source_year": 2013,
        "metrics_affected": [
            "management_intensity",
            "species_richness",
            "ecosystem_services"
        ],
        "climate_zones": [
            "tropical"
        ],
    },

    {
        "id": "landuse_005",
        "topic": "land_use",
        "content": (
            "When land-use recommendations are made, the existing reference condition "
            "must be considered. Converting natural habitat to production land is not "
            "equivalent to diversifying an already degraded production system. "
            "Biodiversity comparisons depend on the baseline ecosystem."
        ),
        "source": (
            "Forest Ecology and Management (2019), "
            "Brazilian Atlantic Forest agroforestry meta-analysis, "
            "DOI: 10.1016/j.foreco.2018.10.064"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "habitat_quality",
            "species_richness",
            "baseline_condition"
        ],
        "climate_zones": [
            "tropical"
        ],
    },


    # ============================================================
    # WATER AND CLIMATE
    # ============================================================

    {
        "id": "water_001",
        "topic": "water_availability",
        "content": (
            "Water availability is an important environmental variable when evaluating "
            "agricultural biodiversity. In water-limited environments, recommendations "
            "should consider rainfall, soil properties, crop choice and management "
            "together rather than treating biodiversity independently of water stress."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "water_availability",
            "species_survival",
            "ecosystem_resilience"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "water_002",
        "topic": "water_availability",
        "content": (
            "Cover cropping can influence soil carbon fractions and therefore soil "
            "condition, but the magnitude depends on climate, soil and management. "
            "For drought-prone systems, the chatbot should combine rainfall with "
            "soil carbon and land-use information before proposing interventions."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2023), "
            "global cover-cropping SOC meta-analysis, "
            "DOI: 10.1016/j.agee.2023.108591"
        ),
        "source_year": 2023,
        "metrics_affected": [
            "water_stress",
            "soil_organic_carbon",
            "soil_health"
        ],
        "climate_zones": [
            "semi-arid",
            "arid"
        ],
    },

    {
        "id": "water_003",
        "topic": "water_availability",
        "content": (
            "Climate conditions modify the effectiveness of agricultural management. "
            "Cover-cropping studies report that environmental and management factors "
            "such as climate, soil type and experimental duration influence observed "
            "carbon responses."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2023), "
            "cover-cropping SOC meta-analysis"
        ),
        "source_year": 2023,
        "metrics_affected": [
            "climate_sensitivity",
            "soil_organic_carbon",
            "water_stress"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "water_004",
        "topic": "water_availability",
        "content": (
            "The interaction between soil condition and rainfall should be included "
            "in biodiversity assessments. Low rainfall combined with degraded soil "
            "can constrain vegetation establishment and habitat development, making "
            "soil and water interventions relevant to biodiversity planning."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "water_availability",
            "vegetation_establishment",
            "habitat_quality"
        ],
        "climate_zones": [
            "semi-arid",
            "arid"
        ],
    },

    {
        "id": "water_005",
        "topic": "water_availability",
        "content": (
            "Water-related recommendations should distinguish rainfall amount from "
            "soil water conditions. Rainfall alone does not fully describe the water "
            "available to plants because soil properties, management and vegetation "
            "also affect water dynamics."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "water_availability",
            "soil_condition",
            "vegetation_health"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },


    # ============================================================
    # SOIL PH AND NUTRIENT CONDITIONS
    # ============================================================

    {
        "id": "ph_001",
        "topic": "soil_ph",
        "content": (
            "Soil pH should be treated as a contextual variable because it affects "
            "nutrient availability and microbial processes. The chatbot should avoid "
            "assuming that a single pH value automatically determines biodiversity "
            "outcomes without considering soil type, crop and management."
        ),
        "source": (
            "FAO, soil and biodiversity knowledge resources; "
            "soil-health evidence framework"
        ),
        "source_year": 2015,
        "metrics_affected": [
            "soil_ph",
            "nutrient_availability",
            "microbial_activity"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "ph_002",
        "topic": "soil_ph",
        "content": (
            "Soil pH should be analyzed together with organic carbon rather than "
            "independently. A biodiversity assessment becomes more informative when "
            "pH, organic carbon, crop type and water conditions are available."
        ),
        "source": (
            "FAO soil-health assessment framework"
        ),
        "source_year": 2015,
        "metrics_affected": [
            "soil_ph",
            "soil_organic_carbon",
            "soil_health"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "ph_003",
        "topic": "soil_ph",
        "content": (
            "When soil pH information is missing, the chatbot should ask for it "
            "when the intended recommendation depends on nutrient availability or "
            "soil microbial processes. The system should not fabricate a pH value."
        ),
        "source": (
            "Darukaa.Earth environmental variable requirement; "
            "FAO soil-health framework"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "soil_ph",
            "nutrient_availability",
            "confidence"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "ph_004",
        "topic": "soil_ph",
        "content": (
            "Soil pH is most useful to the reasoning engine when combined with "
            "organic carbon, rainfall and crop information. These variables help "
            "distinguish soil constraints from climate or land-use constraints."
        ),
        "source": (
            "FAO soil-health assessment framework"
        ),
        "source_year": 2015,
        "metrics_affected": [
            "soil_ph",
            "soil_organic_carbon",
            "rainfall",
            "crop_health"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "ph_005",
        "topic": "soil_ph",
        "content": (
            "A recommendation that changes soil chemistry should have stronger "
            "evidence requirements than a general habitat recommendation. The "
            "system should therefore reduce confidence when soil pH is unknown "
            "and the proposed intervention depends on pH."
        ),
        "source": (
            "Darukaa.Earth evidence-grounding requirement"
        ),
        "source_year": 2026,
        "metrics_affected": [
            "soil_ph",
            "confidence",
            "recommendation_reliability"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },


    # ============================================================
    # INVASIVE SPECIES
    # ============================================================

    {
        "id": "invasive_001",
        "topic": "invasive_species",
        "content": (
            "Invasive species can alter ecosystem composition and ecological "
            "interactions. Biodiversity management should therefore consider whether "
            "a site contains invasive species before recommending habitat expansion "
            "or planting interventions."
        ),
        "source": (
            "IUCN invasive species and biodiversity resources"
        ),
        "source_year": 2024,
        "metrics_affected": [
            "invasive_species_pressure",
            "species_composition",
            "habitat_quality"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "invasive_002",
        "topic": "invasive_species",
        "content": (
            "A biodiversity intervention should not automatically increase plant "
            "diversity without checking whether proposed species are appropriate "
            "for the region. Native or locally appropriate species should be "
            "distinguished from potentially invasive species."
        ),
        "source": (
            "IUCN invasive species and biodiversity resources"
        ),
        "source_year": 2024,
        "metrics_affected": [
            "invasive_species_pressure",
            "native_species_richness",
            "habitat_quality"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "invasive_003",
        "topic": "invasive_species",
        "content": (
            "When invasive species pressure is high, biodiversity restoration "
            "should include management of the invasive population as part of the "
            "intervention plan. Simply adding more vegetation may not address the "
            "underlying ecological pressure."
        ),
        "source": (
            "IUCN invasive species and biodiversity resources"
        ),
        "source_year": 2024,
        "metrics_affected": [
            "invasive_species_pressure",
            "native_species_recovery",
            "habitat_quality"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "invasive_004",
        "topic": "invasive_species",
        "content": (
            "Invasive-species risk should be included as a constraint in the "
            "recommendation engine. If the user proposes a plant that may have "
            "invasive characteristics, the system should request location-specific "
            "information before making a confident recommendation."
        ),
        "source": (
            "IUCN invasive species and biodiversity resources"
        ),
        "source_year": 2024,
        "metrics_affected": [
            "invasive_species_pressure",
            "confidence",
            "native_biodiversity"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "invasive_005",
        "topic": "invasive_species",
        "content": (
            "Invasive species are a human-mediated biodiversity pressure that "
            "should be distinguished from climate and soil constraints. The chatbot "
            "should therefore retain invasive-species status as a separate variable "
            "rather than combining it blindly with habitat quality."
        ),
        "source": (
            "IUCN invasive species and biodiversity resources"
        ),
        "source_year": 2024,
        "metrics_affected": [
            "invasive_species_pressure",
            "human_impact",
            "biodiversity_risk"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },


    # ============================================================
    # RESTORATION AND DECISION MAKING
    # ============================================================

    {
        "id": "restoration_001",
        "topic": "ecosystem_restoration",
        "content": (
            "Restoration recommendations should begin with the current ecological "
            "baseline. Soil condition, rainfall, land use, temperature and existing "
            "biodiversity should be collected before selecting an intervention."
        ),
        "source": (
            "Darukaa.Earth Challenge specification"
        ),
        "source_year": 2026,
        "metrics_affected": [
            "baseline_condition",
            "biodiversity",
            "soil_health",
            "climate_context"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "restoration_002",
        "topic": "ecosystem_restoration",
        "content": (
            "Interventions should be matched to environmental constraints rather "
            "than applied universally. A site with low soil carbon and low rainfall "
            "requires different reasoning from a site with adequate soil carbon "
            "but severe habitat fragmentation."
        ),
        "source": (
            "Darukaa.Earth Challenge specification"
        ),
        "source_year": 2026,
        "metrics_affected": [
            "soil_organic_carbon",
            "rainfall",
            "habitat_fragmentation",
            "biodiversity"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "restoration_003",
        "topic": "ecosystem_restoration",
        "content": (
            "A useful recommendation should identify the environmental metrics "
            "expected to change and the time horizon of the intervention. This makes "
            "the output measurable and allows future observations to be compared "
            "against the baseline."
        ),
        "source": (
            "Darukaa.Earth Challenge specification"
        ),
        "source_year": 2026,
        "metrics_affected": [
            "monitoring",
            "biodiversity",
            "soil_health",
            "water_availability"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "restoration_004",
        "topic": "ecosystem_restoration",
        "content": (
            "Recommendations should combine at least three environmental variables "
            "when sufficient information is available. This avoids shallow advice "
            "such as recommending a single practice without considering soil, "
            "climate and land-use context."
        ),
        "source": (
            "Darukaa.Earth Challenge specification"
        ),
        "source_year": 2026,
        "metrics_affected": [
            "multi_variable_reasoning",
            "recommendation_quality",
            "biodiversity"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "restoration_005",
        "topic": "ecosystem_restoration",
        "content": (
            "Evidence-backed recommendations should include the action, scientific "
            "reasoning, affected metrics and a source. When evidence is uncertain "
            "or the required variables are missing, the system should explicitly "
            "lower confidence or ask a follow-up question."
        ),
        "source": (
            "Darukaa.Earth Challenge specification"
        ),
        "source_year": 2026,
        "metrics_affected": [
            "confidence",
            "evidence_quality",
            "recommendation_quality"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },


        # ============================================================
    # WETLAND BIODIVERSITY
    # ============================================================

    {
        "id": "wetland_001",
        "topic": "wetland_biodiversity",
        "content": (
            "Wetlands provide habitat for diverse groups of plants, animals and "
            "microorganisms and contribute to water regulation and other ecosystem "
            "services. Biodiversity assessment should therefore consider whether "
            "wetland habitat is present, degraded or disconnected from surrounding "
            "landscape."
        ),
        "source": (
            "Ramsar Convention on Wetlands, Global Wetland Outlook"
        ),
        "source_year": 2018,
        "metrics_affected": [
            "wetland_biodiversity",
            "habitat_quality",
            "ecosystem_services"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "wetland_002",
        "topic": "wetland_biodiversity",
        "content": (
            "Wetlands can support biodiversity while also providing water-related "
            "ecosystem services. Loss and degradation of wetlands can reduce habitat "
            "availability and alter ecological processes. Restoration decisions should "
            "consider hydrology together with vegetation and surrounding land use."
        ),
        "source": (
            "Ramsar Convention on Wetlands, Global Wetland Outlook"
        ),
        "source_year": 2018,
        "metrics_affected": [
            "wetland_area",
            "habitat_quality",
            "water_regulation"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "wetland_003",
        "topic": "wetland_biodiversity",
        "content": (
            "Wetland biodiversity is strongly connected to hydrological conditions. "
            "Changes in water availability, drainage or land conversion can alter "
            "habitat suitability. A restoration recommendation should therefore "
            "include water availability and land-use context."
        ),
        "source": (
            "Ramsar Convention on Wetlands, Global Wetland Outlook"
        ),
        "source_year": 2018,
        "metrics_affected": [
            "water_availability",
            "wetland_biodiversity",
            "habitat_suitability"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "wetland_004",
        "topic": "wetland_biodiversity",
        "content": (
            "Agricultural expansion and other land-use changes can place pressure on "
            "wetlands. Biodiversity planning should evaluate the interaction between "
            "land conversion, water availability and habitat condition before proposing "
            "restoration or agricultural intensification."
        ),
        "source": (
            "Ramsar Convention on Wetlands, Global Wetland Outlook"
        ),
        "source_year": 2018,
        "metrics_affected": [
            "land_use_pressure",
            "wetland_biodiversity",
            "water_availability"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },


    # ============================================================
    # HABITAT FRAGMENTATION
    # ============================================================

    {
        "id": "fragmentation_001",
        "topic": "habitat_fragmentation",
        "content": (
            "Habitat fragmentation can separate populations and reduce connectivity "
            "between suitable habitat patches. Biodiversity assessments should therefore "
            "consider not only habitat area but also its spatial arrangement and "
            "connection to other suitable areas."
        ),
        "source": (
            "IPCC, Climate Change and Land: An IPCC Special Report"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "habitat_connectivity",
            "species_richness",
            "habitat_quality"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "fragmentation_002",
        "topic": "habitat_fragmentation",
        "content": (
            "Landscape connectivity can influence the ability of organisms to move "
            "between habitat patches. Maintaining or restoring ecological connections "
            "can therefore complement habitat restoration within individual sites."
        ),
        "source": (
            "IPCC, Climate Change and Land: An IPCC Special Report"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "habitat_connectivity",
            "species_movement",
            "landscape_diversity"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "fragmentation_003",
        "topic": "habitat_fragmentation",
        "content": (
            "A biodiversity intervention should distinguish between increasing habitat "
            "area and improving habitat connectivity. Hedgerows, vegetation strips and "
            "other landscape elements can potentially contribute to connectivity when "
            "their design is appropriate to local species and landscape conditions."
        ),
        "source": (
            "IPCC, Climate Change and Land: An IPCC Special Report"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "habitat_connectivity",
            "habitat_area",
            "species_movement"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "fragmentation_004",
        "topic": "habitat_fragmentation",
        "content": (
            "Habitat fragmentation should be analyzed together with land-use intensity "
            "and biodiversity status. A landscape with high agricultural intensity and "
            "few connected natural areas may require a different intervention from a "
            "landscape where habitat is already well connected."
        ),
        "source": (
            "IPCC, Climate Change and Land: An IPCC Special Report"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "habitat_fragmentation",
            "land_use_pressure",
            "biodiversity_risk"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },


    # ============================================================
    # NITROGEN CYCLE
    # ============================================================

    {
        "id": "nitrogen_001",
        "topic": "nitrogen_cycle",
        "content": (
            "Nitrogen availability is an important component of agricultural soil "
            "function. Legumes can contribute biologically fixed nitrogen to farming "
            "systems, while excessive nitrogen inputs can create environmental risks. "
            "Nitrogen recommendations should therefore consider crop type, soil "
            "condition and management intensity together."
        ),
        "source": (
            "FAO, The State of the World's Biodiversity for Food and Agriculture"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "nitrogen_availability",
            "soil_health",
            "nutrient_cycling"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },

    {
        "id": "nitrogen_002",
        "topic": "nitrogen_cycle",
        "content": (
            "Biological nitrogen fixation by legumes can contribute nitrogen to "
            "agricultural systems without relying exclusively on synthetic nitrogen "
            "fertilizer. The contribution depends on legume species, biomass production, "
            "soil conditions and environmental conditions."
        ),
        "source": (
            "FAO, Legumes and nitrogen fixation resources"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "nitrogen_cycling",
            "soil_fertility",
            "crop_nutrition"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "nitrogen_003",
        "topic": "nitrogen_cycle",
        "content": (
            "Nitrogen management should be connected with soil organic carbon and "
            "microbial activity. Organic matter provides substrates for soil organisms "
            "involved in nutrient cycling, so recommendations can become more useful "
            "when carbon, nitrogen and soil biology are considered together."
        ),
        "source": (
            "FAO, soil health and nutrient management resources"
        ),
        "source_year": 2015,
        "metrics_affected": [
            "nitrogen_cycling",
            "soil_organic_carbon",
            "microbial_activity"
        ],
        "climate_zones": [
            "semi-arid",
            "temperate",
            "tropical",
            "arid"
        ],
    },


    # ============================================================
    # DEFORESTATION
    # ============================================================

    {
        "id": "deforestation_001",
        "topic": "deforestation",
        "content": (
            "Deforestation causes loss of forest habitat and can reduce the ecological "
            "resources available to forest-dependent species. Land-use planning should "
            "therefore distinguish between maintaining existing natural habitat and "
            "restoring degraded agricultural land."
        ),
        "source": (
            "FAO, Global Forest Resources Assessment 2020"
        ),
        "source_year": 2020,
        "metrics_affected": [
            "forest_area",
            "habitat_quality",
            "species_richness"
        ],
        "climate_zones": [
            "tropical",
            "temperate",
            "arid"
        ],
    },

    {
        "id": "deforestation_002",
        "topic": "deforestation",
        "content": (
            "FAO's global forest assessment documents continuing pressure on forest "
            "resources despite a slowing global rate of net forest loss compared with "
            "previous decades. Biodiversity planning should treat prevention of natural "
            "habitat loss separately from restoration of degraded land."
        ),
        "source": (
            "FAO, Global Forest Resources Assessment 2020"
        ),
        "source_year": 2020,
        "metrics_affected": [
            "forest_area",
            "habitat_loss",
            "biodiversity_risk"
        ],
        "climate_zones": [
            "tropical",
            "temperate",
            "arid"
        ],
    },

    {
        "id": "deforestation_003",
        "topic": "deforestation",
        "content": (
            "Forest conservation and agricultural diversification are different "
            "management strategies. Agroforestry may improve ecological conditions "
            "within production landscapes, but it should not be treated as a direct "
            "replacement for intact natural forest habitat."
        ),
        "source": (
            "FAO, Global Forest Resources Assessment 2020; "
            "IPCC, Climate Change and Land"
        ),
        "source_year": 2020,
        "metrics_affected": [
            "forest_conservation",
            "habitat_quality",
            "land_use"
        ],
        "climate_zones": [
            "tropical",
            "temperate",
            "semi-arid"
        ],
    },


    # ============================================================
    # TEMPERATURE STRESS
    # ============================================================

    {
        "id": "temperature_001",
        "topic": "temperature_stress",
        "content": (
            "Temperature affects ecological processes and agricultural productivity. "
            "Climate-related biodiversity assessments should therefore consider "
            "temperature together with rainfall, soil condition and land-use pressure "
            "rather than evaluating temperature as an isolated variable."
        ),
        "source": (
            "IPCC, Climate Change and Land: An IPCC Special Report"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "temperature_stress",
            "species_survival",
            "ecosystem_resilience"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "temperate",
            "tropical"
        ],
    },

    {
        "id": "temperature_002",
        "topic": "temperature_stress",
        "content": (
            "Climate change can alter the suitability of environmental conditions "
            "for species and agricultural systems. High temperature combined with "
            "low water availability can create greater ecological stress than either "
            "factor considered separately."
        ),
        "source": (
            "IPCC, Climate Change and Land: An IPCC Special Report"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "temperature_stress",
            "water_stress",
            "species_survival"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "tropical"
        ],
    },

    {
        "id": "temperature_003",
        "topic": "temperature_stress",
        "content": (
            "Temperature-related recommendations should consider local adaptation "
            "and available water. A high-temperature agricultural site with low "
            "rainfall may require different management from a high-temperature site "
            "with reliable water availability."
        ),
        "source": (
            "IPCC, Climate Change and Land: An IPCC Special Report"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "temperature_stress",
            "water_availability",
            "climate_adaptation"
        ],
        "climate_zones": [
            "semi-arid",
            "arid",
            "tropical"
        ],
    },


    # ============================================================
    # SEMI-ARID RESTORATION
    # ============================================================

    {
        "id": "semiarid_001",
        "topic": "semi_arid_restoration",
        "content": (
            "Semi-arid agricultural systems are strongly influenced by water "
            "availability and soil condition. Biodiversity recommendations in these "
            "systems should combine rainfall with soil organic carbon, vegetation "
            "cover and land-use intensity."
        ),
        "source": (
            "FAO, soil and land management resources; "
            "IPCC, Climate Change and Land"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "water_availability",
            "soil_organic_carbon",
            "vegetation_cover",
            "biodiversity"
        ],
        "climate_zones": [
            "semi-arid",
            "arid"
        ],
    },

    {
        "id": "semiarid_002",
        "topic": "semi_arid_restoration",
        "content": (
            "In water-limited systems, increasing plant diversity without considering "
            "water demand may produce poor outcomes. Restoration planning should match "
            "plant selection and management intensity with local rainfall and soil "
            "conditions."
        ),
        "source": (
            "IPCC, Climate Change and Land: An IPCC Special Report"
        ),
        "source_year": 2019,
        "metrics_affected": [
            "water_stress",
            "plant_diversity",
            "restoration_success"
        ],
        "climate_zones": [
            "semi-arid",
            "arid"
        ],
    },

    {
        "id": "semiarid_003",
        "topic": "semi_arid_restoration",
        "content": (
            "Cover cropping and diversification can be considered in semi-arid systems "
            "when water availability and crop suitability are evaluated first. Evidence "
            "from global cover-crop studies shows soil carbon and microbial responses "
            "vary according to environmental and management conditions."
        ),
        "source": (
            "Agriculture, Ecosystems & Environment (2023), "
            "global cover-cropping SOC meta-analysis"
        ),
        "source_year": 2023,
        "metrics_affected": [
            "soil_organic_carbon",
            "microbial_biomass",
            "water_stress",
            "biodiversity"
        ],
        "climate_zones": [
            "semi-arid",
            "arid"
        ],
    },
]


def get_knowledge_chunks() -> List[Dict[str, Any]]:
    """
    Return the complete knowledge base.
    """
    return KNOWLEDGE_CHUNKS


def get_chunk_count() -> int:
    """
    Return number of knowledge records.
    """
    return len(KNOWLEDGE_CHUNKS)


def validate_knowledge_base() -> List[str]:
    """
    Validate required fields before inserting records into ChromaDB.

    Returns:
        A list of validation errors.
        Empty list means the knowledge base is valid.
    """

    required_fields = {
        "id",
        "topic",
        "content",
        "source",
        "source_year",
        "metrics_affected",
        "climate_zones",
    }

    errors: List[str] = []

    seen_ids = set()

    for index, chunk in enumerate(KNOWLEDGE_CHUNKS):

        missing = required_fields - set(chunk.keys())

        if missing:
            errors.append(
                f"Chunk {index}: missing fields: {sorted(missing)}"
            )

        chunk_id = chunk.get("id")

        if chunk_id in seen_ids:
            errors.append(
                f"Duplicate chunk ID detected: {chunk_id}"
            )

        seen_ids.add(chunk_id)

        if not isinstance(chunk.get("metrics_affected"), list):
            errors.append(
                f"{chunk_id}: metrics_affected must be a list"
            )

        if not isinstance(chunk.get("climate_zones"), list):
            errors.append(
                f"{chunk_id}: climate_zones must be a list"
            )

        if not chunk.get("content"):
            errors.append(
                f"{chunk_id}: content is empty"
            )

        if not chunk.get("source"):
            errors.append(
                f"{chunk_id}: source is empty"
            )

    return errors


if __name__ == "__main__":

    print("=" * 60)
    print("DARUKAA.EARTH KNOWLEDGE BASE")
    print("=" * 60)

    print(f"Total chunks: {get_chunk_count()}")

    errors = validate_knowledge_base()

    if errors:
        print("\nVALIDATION FAILED")
        print("-" * 60)

        for error in errors:
            print(f"ERROR: {error}")

        raise SystemExit(1)

    print("\nVALIDATION PASSED")
    print("All required fields are present.")
    print("All chunk IDs are unique.")

    print("\nTopics:")

    topics = {}

    for chunk in KNOWLEDGE_CHUNKS:
        topics[chunk["topic"]] = topics.get(chunk["topic"], 0) + 1

    for topic, count in sorted(topics.items()):
        print(f"  {topic}: {count}")

    print("=" * 60)