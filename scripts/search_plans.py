#!/usr/bin/env python3
import sys
sys.path.append("./")

"""
Search utility for AI plans stored in Elasticsearch.
This script demonstrates how to search through stored plans using semantic similarity.
"""

import argparse
from utils.elasticsearch_client import ElasticsearchClient

def main():
    parser = argparse.ArgumentParser(description="Search AI plans in Elasticsearch")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Number of results to return")
    parser.add_argument("--list", action="store_true", help="List all plans instead of searching")
    parser.add_argument("--id", help="Get specific plan by ID")
    
    args = parser.parse_args()
    
    # Initialize Elasticsearch client
    es_client = ElasticsearchClient()
    
    try:
        if args.list:
            # List all plans
            print("📋 All stored plans:")
            print("=" * 80)
            plans = es_client.list_all_plans()
            for plan in plans:
                print(f"ID: {plan['id']}")
                print(f"Title: {plan['title']}")
                print(f"Type: {plan['plan_type']}")
                print(f"Created: {plan['created_at']}")
                print(f"Query: {plan['user_query']}")
                print("-" * 40)
        
        elif args.id:
            # Get specific plan by ID
            print(f"📄 Plan with ID: {args.id}")
            print("=" * 80)
            plan = es_client.get_plan_by_id(args.id)
            if plan:
                print(f"Title: {plan['title']}")
                print(f"Type: {plan['plan_type']}")
                print(f"Created: {plan['created_at']}")
                print(f"User Query: {plan['user_query']}")
                print("\n📊 Complete Plan Content:")
                print(plan['content'])
            else:
                print(f"❌ Plan with ID {args.id} not found")
        
        else:
            # Search plans
            print(f"🔍 Searching for: '{args.query}'")
            print("=" * 80)
            results = es_client.search_plans(args.query, args.limit)
            
            if not results:
                print("❌ No plans found matching your query")
                return
            
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']} (Score: {result['score']:.3f})")
                print(f"   Type: {result['plan_type']}")
                print(f"   Created: {result['created_at']}")
                print(f"   Original Query: {result['user_query']}")
                print(f"   ID: {result['id']}")
                print("\n   Content Preview:")
                print(f"   {result['content']}")
                print("-" * 60)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Elasticsearch is running with: docker-compose up -d")

if __name__ == "__main__":
    main() 

# Example usage:
# python3 ./scripts/search_plans.py --query "marketing" --limit 3
# python3 ./scripts/search_plans.py --list
# python3 ./scripts/search_plans.py --id 123