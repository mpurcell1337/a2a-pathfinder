#!/usr/bin/env python3
"""
Chunk Search Demo

This script demonstrates the chunk search functionality of the AI Agent Pathfinder system.
It shows how to search across different chunk types and retrieve relevant content.
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.elasticsearch_client import ElasticsearchClient

# Load environment variables
load_dotenv()

def demo_chunk_search():
    """Demonstrate chunk search functionality."""
    
    # Initialize Elasticsearch client
    es_client = ElasticsearchClient()
    
    # Get all plans
    plans = es_client.list_all_plans()
    if not plans:
        print("❌ No plans found. Please run the lead orchestrator first.")
        return
    
    # Use the most recent plan
    latest_plan = plans[0]
    plan_id = latest_plan['id']
    
    print("🔍 Chunk Search Demo")
    print("=" * 50)
    print(f"📋 Using plan: {latest_plan['title']}")
    print(f"🆔 Plan ID: {plan_id}")
    print(f"📅 Created: {latest_plan['created_at']}")
    print(f"🔍 Query: {latest_plan['user_query']}")
    
    # Get all chunks for this plan
    chunks = es_client.get_chunks_by_plan(plan_id)
    print(f"📝 Found {len(chunks)} chunks for this plan")
    
    # Display chunk types
    chunk_types = {}
    for chunk in chunks:
        chunk_type = chunk['chunk_type']
        chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
    
    print("\n📊 Chunk breakdown:")
    for chunk_type, count in chunk_types.items():
        print(f"  - {chunk_type}: {count} chunks")
    
    print("\n" + "=" * 50)
    
    # Demo 1: Search subagent outputs
    print("🔍 Demo 1: Searching subagent outputs")
    print("-" * 30)
    
    subagent_results = es_client.search_chunks(
        query="market research findings analysis",
        chunk_type="subagent_output",
        size=3
    )
    
    print(f"Found {len(subagent_results)} relevant subagent chunks:")
    for i, result in enumerate(subagent_results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Type: {result['chunk_type']}")
        if result['subagent_id']:
            print(f"   Subagent: {result['subagent_id']}")
        if result['task_description']:
            print(f"   Task: {result['task_description'][:100]}...")
        print(f"   Content: {result['content'][:150]}...")
    
    print("\n" + "=" * 50)
    
    # Demo 2: Search strategic planning content
    print("🔍 Demo 2: Searching strategic planning content")
    print("-" * 30)
    
    strategic_results = es_client.search_chunks(
        query="business strategy implementation plan",
        chunk_type="strategic_plan",
        size=3
    )
    
    print(f"Found {len(strategic_results)} relevant strategic planning chunks:")
    for i, result in enumerate(strategic_results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Type: {result['chunk_type']}")
        print(f"   Content: {result['content'][:150]}...")
    
    print("\n" + "=" * 50)
    
    # Demo 3: Search executive summaries
    print("🔍 Demo 3: Searching executive summaries")
    print("-" * 30)
    
    summary_results = es_client.search_chunks(
        query="executive summary key insights",
        chunk_type="executive_summary",
        size=3
    )
    
    print(f"Found {len(summary_results)} relevant executive summary chunks:")
    for i, result in enumerate(summary_results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Type: {result['chunk_type']}")
        print(f"   Content: {result['content'][:150]}...")
    
    print("\n" + "=" * 50)
    
    # Demo 4: Cross-type search
    print("🔍 Demo 4: Cross-type search (all chunk types)")
    print("-" * 30)
    
    cross_results = es_client.search_chunks(
        query="AI art company strategy market",
        size=5
    )
    
    print(f"Found {len(cross_results)} relevant chunks across all types:")
    for i, result in enumerate(cross_results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Type: {result['chunk_type']}")
        print(f"   Content: {result['content'][:150]}...")
    
    print("\n" + "=" * 50)
    
    # Demo 5: Show chunk retrieval by plan
    print("🔍 Demo 5: Retrieving all chunks for a specific plan")
    print("-" * 30)
    
    plan_chunks = es_client.get_chunks_by_plan(plan_id)
    print(f"All chunks for plan {plan_id}:")
    
    for i, chunk in enumerate(plan_chunks, 1):
        print(f"\n{i}. Type: {chunk['chunk_type']}")
        if chunk['subagent_id']:
            print(f"   Subagent: {chunk['subagent_id']}")
        if chunk['task_description']:
            print(f"   Task: {chunk['task_description'][:100]}...")
        print(f"   Content preview: {chunk['content'][:100]}...")
    
    print("\n" + "=" * 50)
    
    # Demo 6: Filtered search
    print("🔍 Demo 6: Filtered search by plan type")
    print("-" * 30)
    
    filtered_results = es_client.search_chunks(
        query="technology research findings",
        chunk_type="subagent_output",
        plan_type="ai_art_company",
        size=3
    )
    
    print(f"Found {len(filtered_results)} relevant chunks with filters:")
    for i, result in enumerate(filtered_results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Type: {result['chunk_type']}")
        print(f"   Plan Type: {result['plan_type']}")
        print(f"   Content: {result['content'][:150]}...")
    
    print("\n" + "=" * 50)
    
    # Demo 7: Search with different queries
    print("🔍 Demo 7: Different search queries")
    print("-" * 30)
    
    queries = [
        "revenue model pricing strategy",
        "technology stack infrastructure",
        "market competition analysis",
        "financial projections funding"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        subagent_results = es_client.search_chunks(
            query=query,
            chunk_type="subagent_output",
            size=2
        )
        
        if subagent_results:
            print(f"Found {len(subagent_results)} results:")
            for result in subagent_results:
                print(f"  - Score: {result['score']:.3f}")
                print(f"    Content: {result['content'][:100]}...")
        else:
            print("No results found.")

if __name__ == "__main__":
    try:
        demo_chunk_search()
        
        print("\n" + "=" * 50)
        print("✅ Chunk search demo completed!")
        print("=" * 50)
        
        print("\n📋 Available search features:")
        print("1. Search by chunk type (subagent_output, strategic_plan, etc.)")
        print("2. Search across all chunk types")
        print("3. Filter by plan type")
        print("4. Filter by chunk type and plan type")
        print("5. Retrieve all chunks for a specific plan")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("Make sure Elasticsearch is running with: docker-compose up -d") 