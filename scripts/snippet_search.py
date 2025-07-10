#!/usr/bin/env python3
"""
Snippet Search Demo

This script demonstrates the dense vector encoding and search capabilities
for individual sub-agent outputs and orchestration outputs.
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.elasticsearch_client import ElasticsearchClient

# Load environment variables
load_dotenv()

def demo_snippet_search():
    """Demonstrate snippet search functionality."""
    
    # Initialize Elasticsearch client
    es_client = ElasticsearchClient()
    
    print("🔍 Snippet Search Demo")
    print("=" * 50)
    
    # Check if we have any plans stored
    plans = es_client.list_all_plans()
    if not plans:
        print("❌ No plans found in Elasticsearch.")
        print("Please run the lead orchestrator first to generate some plans.")
        return
    
    print(f"✅ Found {len(plans)} plans in Elasticsearch")
    
    # Get the most recent plan
    latest_plan = plans[0]
    plan_id = latest_plan['id']
    print(f"📋 Using plan: {latest_plan['title']}")
    
    # Get all snippets for this plan
    snippets = es_client.get_snippets_by_plan(plan_id)
    print(f"📝 Found {len(snippets)} snippets for this plan")
    
    # Display snippet types
    snippet_types = {}
    for snippet in snippets:
        snippet_type = snippet['snippet_type']
        snippet_types[snippet_type] = snippet_types.get(snippet_type, 0) + 1
    
    print("\n📊 Snippet breakdown:")
    for snippet_type, count in snippet_types.items():
        print(f"  - {snippet_type}: {count} snippets")
    
    # Demo 1: Search for subagent outputs
    print("\n" + "=" * 50)
    print("🔍 Demo 1: Searching subagent outputs")
    print("=" * 50)
    
    subagent_results = es_client.search_snippets(
        query="research findings analysis",
        snippet_type="subagent_output",
        size=3
    )
    
    print(f"Found {len(subagent_results)} relevant subagent outputs:")
    for i, result in enumerate(subagent_results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Subagent: {result['subagent_id']}")
        print(f"   Task: {result['task_description'][:100]}...")
        print(f"   Content: {result['content'][:200]}...")
    
    # Demo 2: Search for strategic planning content
    print("\n" + "=" * 50)
    print("🔍 Demo 2: Searching strategic planning content")
    print("=" * 50)
    
    strategic_results = es_client.search_snippets(
        query="business strategy market analysis",
        snippet_type="strategic_plan",
        size=3
    )
    
    print(f"Found {len(strategic_results)} relevant strategic planning snippets:")
    for i, result in enumerate(strategic_results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Type: {result['snippet_type']}")
        print(f"   Content: {result['content'][:200]}...")
    
    # Demo 3: Search for executive summary content
    print("\n" + "=" * 50)
    print("🔍 Demo 3: Searching executive summary content")
    print("=" * 50)
    
    summary_results = es_client.search_snippets(
        query="recommendations action items",
        snippet_type="executive_summary",
        size=3
    )
    
    print(f"Found {len(summary_results)} relevant executive summary snippets:")
    for i, result in enumerate(summary_results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Type: {result['snippet_type']}")
        print(f"   Content: {result['content'][:200]}...")
    
    # Demo 4: Cross-type search
    print("\n" + "=" * 50)
    print("🔍 Demo 4: Cross-type search (all snippet types)")
    print("=" * 50)
    
    cross_results = es_client.search_snippets(
        query="AI art generation technology",
        size=5
    )
    
    print(f"Found {len(cross_results)} relevant snippets across all types:")
    for i, result in enumerate(cross_results, 1):
        print(f"\n{i}. Score: {result['score']:.3f}")
        print(f"   Type: {result['snippet_type']}")
        if result['subagent_id']:
            print(f"   Subagent: {result['subagent_id']}")
        print(f"   Content: {result['content'][:150]}...")
    
    # Demo 5: Show snippet retrieval by plan
    print("\n" + "=" * 50)
    print("🔍 Demo 5: Retrieving all snippets for a specific plan")
    print("=" * 50)
    
    plan_snippets = es_client.get_snippets_by_plan(plan_id)
    print(f"All snippets for plan {plan_id}:")
    
    for i, snippet in enumerate(plan_snippets, 1):
        print(f"\n{i}. Type: {snippet['snippet_type']}")
        if snippet['subagent_id']:
            print(f"   Subagent: {snippet['subagent_id']}")
        if snippet['task_description']:
            print(f"   Task: {snippet['task_description'][:100]}...")
        print(f"   Content preview: {snippet['content'][:100]}...")

def demo_advanced_search():
    """Demonstrate advanced search features."""
    
    es_client = ElasticsearchClient()
    
    print("\n" + "=" * 50)
    print("🔍 Advanced Search Features")
    print("=" * 50)
    
    # Search with filters
    print("\n1. Searching subagent outputs for AI art company plans:")
    filtered_results = es_client.search_snippets(
        query="market research competitive analysis",
        snippet_type="subagent_output",
        plan_type="ai_art_company",
        size=3
    )
    
    print(f"Found {len(filtered_results)} results:")
    for result in filtered_results:
        print(f"  - {result['subagent_id']}: {result['content'][:100]}...")
    
    # Search for specific subagent
    print("\n2. Searching for specific subagent outputs:")
    subagent_results = es_client.search_snippets(
        query="technology stack implementation",
        snippet_type="subagent_output",
        size=5
    )
    
    # Group by subagent
    subagent_groups = {}
    for result in subagent_results:
        subagent_id = result['subagent_id']
        if subagent_id not in subagent_groups:
            subagent_groups[subagent_id] = []
        subagent_groups[subagent_id].append(result)
    
    for subagent_id, results in subagent_groups.items():
        print(f"\n  {subagent_id}:")
        for result in results:
            print(f"    - Score {result['score']:.3f}: {result['content'][:80]}...")

if __name__ == "__main__":
    try:
        demo_snippet_search()
        demo_advanced_search()
        
        print("\n" + "=" * 50)
        print("✅ Snippet search demo completed!")
        print("=" * 50)
        print("\nYou can now:")
        print("1. Search for specific subagent outputs")
        print("2. Search for strategic planning content")
        print("3. Search for executive summaries")
        print("4. Filter by snippet type and plan type")
        print("5. Retrieve all snippets for a specific plan")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("Make sure Elasticsearch is running with: docker-compose up -d") 