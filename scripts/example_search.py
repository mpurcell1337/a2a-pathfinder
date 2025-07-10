#!/usr/bin/env python3
"""
Example script demonstrating Elasticsearch search functionality.
This shows how to programmatically search through stored AI plans.
"""

from utils.elasticsearch_client import ElasticsearchClient

def main():
    # Initialize the Elasticsearch client
    es_client = ElasticsearchClient()
    
    print("🔍 AI Plan Search Examples")
    print("=" * 50)
    
    # Example 1: List all plans
    print("\n1. Listing all stored plans:")
    print("-" * 30)
    try:
        plans = es_client.list_all_plans()
        if plans:
            for plan in plans[:3]:  # Show first 3
                print(f"  • {plan['title']} (ID: {plan['id']})")
        else:
            print("  No plans found. Run lead_orchestrater.py first to generate plans.")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 2: Search for marketing-related content
    print("\n2. Searching for marketing strategies:")
    print("-" * 30)
    try:
        results = es_client.search_plans("marketing strategy", 3)
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']} (Score: {result['score']:.3f})")
        else:
            print("  No marketing-related plans found.")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 3: Search for technical content
    print("\n3. Searching for technical infrastructure:")
    print("-" * 30)
    try:
        results = es_client.search_plans("technical infrastructure", 3)
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']} (Score: {result['score']:.3f})")
        else:
            print("  No technical infrastructure plans found.")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Example 4: Search for revenue models
    print("\n4. Searching for revenue models:")
    print("-" * 30)
    try:
        results = es_client.search_plans("revenue model", 3)
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']} (Score: {result['score']:.3f})")
        else:
            print("  No revenue model plans found.")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n💡 Tips:")
    print("  • Use semantic search with natural language queries")
    print("  • Try different keywords: 'scaling', 'competition', 'risks'")
    print("  • Access Kibana at http://localhost:5601 for advanced search")
    print("  • Use search_plans.py for command-line search")

if __name__ == "__main__":
    main() 