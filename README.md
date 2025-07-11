# AI Agent Pathfinder

A sophisticated multi-agent system for strategic planning and research using AI agents with advanced chunking and semantic search capabilities.

## Overview

The AI Agent Pathfinder orchestrates multiple AI agents to conduct comprehensive research and create strategic plans. The system features advanced chunking strategies that break down large outputs into searchable chunks with individual embeddings, enabling precise semantic search and retrieval.

## Features

### 🤖 Multi-Agent Orchestration
- **Lead Agent**: Orchestrates research and planning processes
- **Sub-Agents**: Specialized agents for market research, technology analysis, financial planning, and more
- **Coordinated Workflow**: Seamless coordination between agents

### 🔍 Advanced Search & Retrieval
- **Semantic Search**: Vector-based similarity search across all content
- **Elasticsearch Integration**: Robust search infrastructure
- **Dual Index Structure**: Separate indices for plans and chunks
- **Index Names**: `ai_agents` (complete plans), `ai_subagents` (individual chunks)

### 📊 Advanced Chunking Strategy
- **Granular Storage**: Individual sub-agent outputs and orchestration outputs stored as searchable chunks
- **Semantic Boundaries**: Intelligent chunk splitting at natural content boundaries
- **Overlap Management**: Configurable overlap between chunks for context preservation

### 🔧 Chunk Search Features
- **Semantic Similarity**: Find relevant content using vector embeddings
- **Type Filtering**: Filter by chunk type (subagent_output, strategic_plan, etc.)
- **Filtered Search**: Filter by chunk type, plan type, and other metadata
- **Plan-Specific Retrieval**: Get all chunks for a specific plan

### 📋 Chunk Types
- **`subagent_output`** - Individual subagent research and analysis results
- **`orchestration_output`** - Lead agent orchestration and synthesis
- **`strategic_plan`** - Strategic planning content
- **`executive_summary`** - Executive summaries and high-level insights
- **`enhanced_strategic_plan`** - Advanced chunked strategic planning content

### 🔍 Chunk Search Usage
```bash
# Search for relevant chunks
python scripts/chunk_search.py

# Advanced chunking features
python scripts/semantic_chunking.py
```

## Quick Start

### 1. Prerequisites
- Python 3.8+
- Docker and Docker Compose
- OpenAI API key

### 2. Setup
```bash
# Clone the repository
git clone <repository-url>
cd a2a-pathfinder

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 3. Start Services
```bash
# Start Elasticsearch and Kibana
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 4. Run the System
```bash
# Run the lead orchestrator
python lead_orchestrater.py

# Search chunks
python scripts/chunk_search.py
```

## Architecture

### Agent Structure
```
Lead Agent (Orchestrator)
├── Market Research Sub-Agent
├── Technology Research Sub-Agent
├── Financial Analysis Sub-Agent
├── Legal Research Sub-Agent
└── Marketing Research Sub-Agent
```

### Data Flow
1. **User Query** → Lead Agent receives strategic planning request
2. **Task Decomposition** → Lead Agent breaks down into specialized tasks
3. **Sub-Agent Execution** → Each sub-agent conducts focused research
4. **Chunk Storage** → Individual outputs stored as searchable chunks
5. **Synthesis** → Lead Agent combines findings into strategic plan
6. **Search & Retrieval** → Users can search across all chunks

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
```

### Chunking Parameters
```python
# Configure chunking in semantic_chunking.py
chunk_size=1000,  # Target chunk size in characters
overlap=200       # Overlap between chunks
```

## Usage Examples

### Basic Chunk Search
```python
from utils.elasticsearch_client import ElasticsearchClient

es_client = ElasticsearchClient()

# Search for market research chunks
results = es_client.search_chunks(
    query="market analysis competition",
    chunk_type="subagent_output",
    size=5
)

for result in results:
    print(f"Score: {result['score']}")
    print(f"Content: {result['content'][:200]}...")
```

### Advanced Filtering
```python
# Filter by plan type and chunk type
results = es_client.search_chunks(
    query="AI art company strategy",
    plan_type="ai_art_company",
    chunk_type="strategic_plan"
)
```

### Plan-Specific Retrieval
```python
# Get all chunks for a specific plan
chunks = es_client.get_chunks_by_plan(plan_id)

for chunk in chunks:
    print(f"Type: {chunk['chunk_type']}")
    print(f"Content: {chunk['content'][:100]}...")
```

## Scripts

### Core Scripts
- **`lead_orchestrater.py`** - Main orchestrator for multi-agent planning
- **`scripts/chunk_search.py`** - Chunk search and retrieval demo
- **`scripts/semantic_chunking.py`** - Advanced chunking features

### Utility Scripts
- **`scripts/example_search.py`** - Example search queries
- **`scripts/search_plans.py`** - Plan search functionality

## Monitoring & Analytics

### Kibana Dashboard
Access Kibana at `http://localhost:5601` to:
- View Elasticsearch indices
- Create custom dashboards
- Analyze chunk distributions
- Monitor search performance

### Chunk Analytics
```python
# Get chunk statistics
chunks = es_client.search_chunks("", size=100)
print(f"Total chunks: {len(chunks)}")

# Analyze by type
type_counts = {}
for chunk in chunks:
    chunk_type = chunk['chunk_type']
    type_counts[chunk_type] = type_counts.get(chunk_type, 0) + 1
```

## Development

### Adding New Chunk Types
1. Update the chunk type mapping in `elasticsearch_client.py`
2. Add new chunk type to the documentation
3. Update search examples

### Customizing Chunking Strategy
1. Modify `AdvancedChunkizer` in `semantic_chunking.py`
2. Adjust chunk size and overlap parameters
3. Add custom metadata extraction

## Troubleshooting

### Common Issues
1. **Elasticsearch Connection**: Ensure Docker containers are running
2. **API Key**: Verify OpenAI API key is set correctly
3. **Index Creation**: Check that indices are created properly
4. **Memory Usage**: Large documents may require chunking

### Debug Commands
```bash
# Check Elasticsearch status
curl http://localhost:9200/_cluster/health

# List indices
curl http://localhost:9200/_cat/indices

# Check chunk count
python -c "from utils.elasticsearch_client import ElasticsearchClient; es=ElasticsearchClient(); print(es.es.count(index='ai_subagents'))"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.



