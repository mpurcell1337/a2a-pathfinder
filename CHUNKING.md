# Advanced Chunking Strategy

This document outlines the advanced chunking strategy used in the AI Agent Pathfinder system. Each output is broken down into searchable chunks with their own embeddings, enabling precise semantic search and retrieval.

## Index Structure

The system uses two main Elasticsearch indices:

1. **`ai_agents`** - Stores complete strategic plans and orchestration outputs
2. **`ai_subagents`** - Stores individual chunks of plans with their own embeddings at the subagent level.

## Chunk Types

The system supports various chunk types for different content categories:

- **`subagent_output`** - Individual subagent research and analysis results
- **`orchestration_output`** - Lead agent orchestration and synthesis
- **`strategic_plan`** - Strategic planning content
- **`executive_summary`** - Executive summaries and high-level insights
- **`enhanced_strategic_plan`** - Advanced chunked strategic planning content

## Core Features

### 1. Granular Chunk Storage

Each sub-agent output and orchestration output is stored as individual chunks with:
- Unique chunk ID
- Content vector embeddings
- Chunk type classification
- Metadata and context information

### 2. Semantic Search

Search across all chunk types with semantic similarity:

```python
# Search subagent outputs
results = es_client.search_chunks(
    query="market analysis competition",
    chunk_type="subagent_output",
    size=5
)

# Search strategic plans
results = es_client.search_chunks(
    query="business strategy implementation",
    chunk_type="strategic_plan",
    size=5
)
```

### 3. Advanced Filtering

Filter chunks by type, plan, and metadata:

```python
# Filter by specific plan type
results = es_client.search_chunks(
    query="AI art company",
    plan_type="ai_art_company",
    chunk_type="subagent_output"
)

# Search with multiple filters
results = es_client.search_chunks(
    query="revenue model pricing",
    chunk_type="subagent_output",
    plan_type="ai_art_company"
)
```

### 4. Plan-Specific Retrieval

Get all chunks for a specific plan:

```python
# Get all chunks for a specific plan
chunks = es_client.get_chunks_by_plan(plan_id)

for chunk in chunks:
    print(f"Type: {chunk['chunk_type']}")
    print(f"Content: {chunk['content'][:100]}...")
```

## Usage Examples

### 1. Chunk Search Demo (`scripts/chunk_search.py`)

Demonstrates basic chunk search functionality:

- Semantic similarity search
- Type-based filtering
- Plan-specific chunk retrieval
- Chunk analytics

### 2. Advanced Chunking (`scripts/semantic_chunking.py`)

Advanced chunking features including:

- Semantic boundary detection
- Overlapping chunk creation
- Configurable chunk sizes and overlap
- Enhanced metadata extraction

## Implementation Details

### Basic Chunk Search

```python
from utils.elasticsearch_client import ElasticsearchClient

es_client = ElasticsearchClient()
es_client.create_index()

# Search for relevant chunks
results = es_client.search_chunks(
    query="market research competition analysis",
    chunk_type="subagent_output",
    size=10
)

for result in results:
    print(f"Score: {result['score']}")
    print(f"Content: {result['content']}")
    print(f"Type: {result['chunk_type']}")
```

### Get All Chunks for a Plan

```python
# Get all chunks for a specific plan
chunks = es_client.get_chunks_by_plan(plan_id)

for chunk in chunks:
    print(f"Type: {chunk['chunk_type']}")
    print(f"Content: {chunk['content'][:100]}...")
```

### Chunk Analytics

```python
# List all chunks
chunks = es_client.search_chunks("", size=100)

# Get chunk count
count = es_client.es.count(index=es_client.chunks_index_name)
print(f"Total chunks: {count['count']}")
```

## Advanced Features

### 1. **Semantic Boundaries**: Intelligent chunk splitting at natural content boundaries
### 2. **Overlap Management**: Configurable overlap between chunks for context preservation
### 3. **Metadata Extraction**: Automatic extraction of headers, key phrases, and content features
### 4. **Type Classification**: Automatic categorization of chunk content types
### 5. **Scalability**: Efficient storage and retrieval of large numbers of chunks

## Future Enhancements

1. **Hierarchical Chunks**: Parent-child relationships between chunks
2. **Temporal Chunks**: Time-based chunk organization
3. **Collaborative Chunks**: Multi-agent chunk relationships
4. **Dynamic Chunking**: Adaptive chunk sizes based on content
5. **Chunk Clustering**: Group similar chunks together

## Performance Considerations

1. **Index Optimization**: Proper mapping and settings for efficient search
2. **Vector Dimensions**: Optimized embedding dimensions for balance of performance and accuracy
3. **Query Optimization**: Efficient query construction for large datasets
4. **Memory Usage**: Large documents may require chunking

## Usage Commands

1. Start Elasticsearch:
```bash
docker-compose up -d
```

2. Run the chunk search demo:
```bash
python scripts/chunk_search.py
```

3. Run advanced chunking:
```bash
python scripts/semantic_chunking.py
```

## Example Output

```
📊 Chunk Analytics
==============================
📈 Total chunks: 15

📋 Chunk types:
  - subagent_output: 8 chunks
  - strategic_plan: 3 chunks
  - executive_summary: 2 chunks
  - enhanced_strategic_plan: 2 chunks

📋 Plan types:
  - ai_art_company: 15 chunks

📏 Size distribution:
  - small: 5 chunks (33.3%)
  - medium: 7 chunks (46.7%)
  - large: 3 chunks (20.0%)
```

## Configuration

### Chunk Size and Overlap

```python
# Configure chunking parameters
chunk_size=1000,  # Target chunk size in characters
overlap=200       # Overlap between chunks
```

### Search Parameters

```python
# Configure search parameters
size=10,          # Number of results to return
min_score=0.5,    # Minimum similarity score
```

## Benefits

1. **Precision**: Granular search across specific content sections
2. **Context Preservation**: Overlapping chunks maintain context
3. **Flexibility**: Multiple chunk types for different use cases
4. **Scalability**: Efficient handling of large document collections
5. **Analytics**: Rich metadata for chunk analysis and optimization 