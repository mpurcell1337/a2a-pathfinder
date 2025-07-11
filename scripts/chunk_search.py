#!/usr/bin/env python3
"""
Chunk Search

Search chunks in Elasticsearch using semantic similarity.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.elasticsearch_client import ElasticsearchClient

# Load environment variables
load_dotenv()

def search_chunks(query, chunk_type=None, plan_type=None, size=5):
    """Search chunks with a specific query."""
    
    # Initialize Elasticsearch client
    es_client = ElasticsearchClient()
    
    print(f"🔍 Searching for: '{query}'")
    print("=" * 50)
    
    # Perform the search
    results = es_client.search_chunks(
        query=query,
        chunk_type=chunk_type,
        plan_type=plan_type,
        size=size
    )
    
    if not results:
        print("❌ No chunks found matching your query")
        return
    
    print(f"Found {len(results)} relevant chunks:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Type: {result['chunk_type']}")
        if result['plan_type']:
            print(f"   Plan Type: {result['plan_type']}")
        if result['subagent_id']:
            print(f"   Subagent: {result['subagent_id']}")
        if result['task_description']:
            print(f"   Task: {result['task_description']}")
        print(f"   Content: {result['content']}")
    
    print("\n" + "=" * 50)

def main():
    parser = argparse.ArgumentParser(description="Search chunks in Elasticsearch")
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--chunk-type", "-t", help="Filter by chunk type (e.g., subagent_output, strategic_plan, executive_summary)")
    parser.add_argument("--plan-type", "-p", help="Filter by plan type")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of results to return")
    
    args = parser.parse_args()
    
    try:
        search_chunks(
            query=args.query,
            chunk_type=args.chunk_type,
            plan_type=args.plan_type,
            size=args.limit
        )
    
    except Exception as e:
        print(f"❌ Error during search: {e}")
        print("Make sure Elasticsearch is running with: docker-compose up -d")

if __name__ == "__main__":
    main()

# Basic search
# python3 ./scripts/chunk_search.py --query "market research"

# Search with chunk type filter
# python3 ./scripts/chunk_search.py --query "strategy" --chunk-type strategic_plan

# Search with plan type filter
# python3 ./scripts/chunk_search.py --query "AI art" --plan-type ai_art_company

# Search with custom limit
# python3 ./scripts/chunk_search.py --query "technology" --limit 10 --plan-type ai_art_company