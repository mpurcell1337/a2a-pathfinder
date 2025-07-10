# Dense Vector Encoding and Snippitization

This document describes the enhanced dense vector encoding and snippitization capabilities for sub-agent outputs and orchestration outputs.

## Overview

The system now supports granular search and retrieval of individual sub-agent outputs and orchestration outputs through dense vector encoding. Each output is broken down into searchable snippets with their own embeddings, enabling precise semantic search and retrieval.

## Architecture

### Dual Index Structure

The system uses two Elasticsearch indices:

1. **`ai_agents`** - Stores complete plans with combined embeddings at the agent leve.
2. **`ai_subagents`** - Stores individual chunks of plans with their own embeddings at the subagent level.

### Snippet Types

- **`subagent_output`** - Individual sub-agent research results
- **`strategic_plan`** - Strategic planning content
- **`executive_summary`** - Executive summary content
- **`enhanced_strategic_plan`** - Advanced chunked strategic planning content

## Features

### 1. Granular Snippet Storage

Each sub-agent output and orchestration output is stored as individual snippets with:
- Unique snippet ID
- Plan ID reference
- Content vector embedding
- Snippet type classification
- Metadata (task description, subagent ID, etc.)

### 2. Semantic Search

Search across all snippet types with semantic similarity:
```python
# Search subagent outputs
results = es_client.search_snippets(
    query="market research findings",
    snippet_type="subagent_output",
    size=5
)

# Search strategic planning content
results = es_client.search_snippets(
    query="business strategy implementation",
    snippet_type="strategic_plan",
    size=3
)
```

### 3. Advanced Snippitization

The `AdvancedSnippitizer` class provides:
- Semantic boundary detection (headers, paragraphs)
- Overlapping chunk creation
- Metadata extraction (headers, key phrases, word count)
- Configurable chunk sizes and overlap

### 4. Filtered Search

Search with multiple filters:
```python
# Search with filters
results = es_client.search_snippets(
    query="technology implementation",
    snippet_type="subagent_output",
    plan_type="ai_art_company",
    size=5
)
```

## Usage Examples

### Basic Snippet Search

```python
from utils.elasticsearch_client import ElasticsearchClient

es_client = ElasticsearchClient()

# Search for specific subagent outputs
results = es_client.search_snippets(
    query="research findings analysis",
    snippet_type="subagent_output",
    size=3
)

for result in results:
    print(f"Subagent: {result['subagent_id']}")
    print(f"Task: {result['task_description']}")
    print(f"Content: {result['content'][:200]}...")
```

### Advanced Snippitization

```python
from scripts.advanced_snippitization import AdvancedSnippitizer

snippitizer = AdvancedSnippitizer(chunk_size=800, overlap=150)

# Create semantic chunks
chunks = snippitizer.split_by_semantic_boundaries(large_text)

# Create overlapping chunks
overlapping_chunks = snippitizer.create_overlapping_chunks(text)

# Extract metadata
metadata = snippitizer.extract_metadata(chunk)
```

### Get All Snippets for a Plan

```python
# Get all snippets for a specific plan
snippets = es_client.get_snippets_by_plan(plan_id)

for snippet in snippets:
    print(f"Type: {snippet['snippet_type']}")
    print(f"Content: {snippet['content'][:100]}...")
```

## Scripts

### 1. Snippet Search Demo (`scripts/snippet_search.py`)

Demonstrates basic snippet search functionality:
- Search subagent outputs
- Search strategic planning content
- Search executive summaries
- Cross-type search
- Plan-specific snippet retrieval

### 2. Advanced Snippitization (`scripts/advanced_snippitization.py`)

Demonstrates advanced snippitization features:
- Semantic boundary detection
- Overlapping chunk creation
- Metadata extraction
- Enhanced search capabilities
- Snippet analytics

## Running the Demos

1. Start Elasticsearch:
```bash
docker-compose up -d
```

2. Run the lead orchestrator to generate plans:
```bash
python lead_orchestrater.py
```

3. Run the snippet search demo:
```bash
python scripts/snippet_search.py
```

4. Run the advanced snippitization demo:
```bash
python scripts/advanced_snippitization.py
```

## Configuration

### Chunk Size and Overlap

Configure the `AdvancedSnippitizer`:
```python
snippitizer = AdvancedSnippitizer(
    chunk_size=1000,  # Target chunk size in characters
    overlap=200       # Overlap between chunks
)
```

### Embedding Model

The system uses `all-MiniLM-L6-v2` for embeddings (384 dimensions). To change:
```python
# In utils/elasticsearch_client.py
self.model = SentenceTransformer('your-model-name')
```

## Benefits

1. **Granular Search**: Search specific sub-agent outputs or orchestration outputs
2. **Semantic Retrieval**: Find relevant content using semantic similarity
3. **Context Preservation**: Overlapping chunks maintain context
4. **Metadata Enrichment**: Rich metadata for better organization
5. **Scalability**: Efficient storage and retrieval of large numbers of snippets

## Future Enhancements

1. **Hierarchical Snippets**: Parent-child relationships between snippets
2. **Temporal Snippets**: Time-based snippet organization
3. **Collaborative Snippets**: Multi-agent snippet relationships
4. **Dynamic Chunking**: Adaptive chunk sizes based on content
5. **Snippet Clustering**: Group similar snippets together

## Troubleshooting

### Common Issues

1. **Elasticsearch Connection**: Ensure Elasticsearch is running
2. **Index Creation**: Check that indices are created properly
3. **Embedding Generation**: Verify the sentence transformer model loads
4. **Memory Usage**: Large documents may require chunking

### Debug Commands

```python
# Check if indices exist
es_client.es.indices.exists(index="ai_subagents")

# List all snippets
snippets = es_client.search_snippets("", size=100)

# Get snippet count
count = es_client.es.count(index="ai_subagents")
print(f"Total snippets: {count['count']}")
``` 