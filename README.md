# A2A Pathfinder

## UV
- To enter the virtual environment associated with this project:
    - `source .venv/bin/activate`
- To exit the virtual environment:
    - `deactivate`
- To add a new dependency:
    - `uv add elasicsearch`
    - If no package satisfies the requirement:
        - `uv pip install sentence-transformers`

## Elasticsearch Integration

This project now includes Elasticsearch integration for storing and searching AI-generated plans using sentence transformer embeddings.

### Setup

1. **Start Elasticsearch and Kibana:**
   ```bash
   docker-compose up -d
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Run the lead orchestrator:**
   ```bash
   python lead_orchestrater.py
   ```

### Features

- **Automatic Storage**: Each generated plan is automatically stored in Elasticsearch with semantic embeddings
- **Semantic Search**: Search plans using natural language queries with cosine similarity
- **Full-Text Search**: Traditional keyword-based search capabilities
- **Plan Retrieval**: Get complete plans by ID or list all stored plans

### Search Usage

#### List all plans:
```bash
python search_plans.py --list
```

#### Search for specific content:
```bash
python search_plans.py --query "marketing strategy for AI art"
```

#### Get a specific plan by ID:
```bash
python search_plans.py --id "your_plan_id_here"
```

#### Search with custom limit:
```bash
python search_plans.py --query "revenue model" --limit 10
```

### Web Interface

- **Kibana**: http://localhost:5601 (for advanced search and visualization)
- **Elasticsearch API**: http://localhost:9200

### Technical Details

- **Embedding Model**: `all-MiniLM-L6-v2` (384 dimensions, lightweight)
- **Index Name**: `ai_plans`
- **Vector Search**: Uses cosine similarity for semantic matching
- **Storage**: Complete plans with strategic plans, subagent reports, and executive summaries

### Example Search Queries

- "marketing strategy"
- "revenue model"
- "technical infrastructure"
- "competitive analysis"
- "risk assessment"
- "scaling strategy"

## Citations / Source
### Anthropic
- `Prompt-Chaining / Parallelization / Routing`
- https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/README.md

## OpenAI
- https://www.forbes.com/sites/jodiecook/2024/07/16/openais-5-levels-of-super-ai-agi-to-outperform-human-capability/



