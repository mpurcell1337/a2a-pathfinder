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
- **Index Names**: `ai_plans` (complete plans), `ai_snippets` (individual snippets)
- **Vector Search**: Uses cosine similarity for semantic matching
- **Storage**: Complete plans with strategic plans, subagent reports, and executive summaries
- **Snippitization**: Individual sub-agent outputs and orchestration outputs stored as searchable snippets

## Dense Vector Encoding and Snippitization

The system now supports granular search and retrieval of individual sub-agent outputs and orchestration outputs through dense vector encoding.

### Snippet Search Features

- **Granular Search**: Search specific sub-agent outputs or orchestration outputs
- **Semantic Retrieval**: Find relevant content using semantic similarity
- **Filtered Search**: Filter by snippet type, plan type, and other metadata
- **Advanced Chunking**: Semantic boundary detection with overlapping chunks

### Snippet Types

- **`subagent_output`** - Individual sub-agent research results
- **`strategic_plan`** - Strategic planning content
- **`executive_summary`** - Executive summary content
- **`enhanced_strategic_plan`** - Advanced chunked strategic planning content

### Snippet Search Usage

```bash
# Search subagent outputs
python scripts/snippet_search.py

# Advanced snippitization demo
python scripts/advanced_snippitization.py
```

For detailed documentation, see [SNIPPITIZATION.md](SNIPPITIZATION.md).

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



