import os
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from datetime import datetime
from typing import Dict, Any, List
import json

class ElasticsearchClient:
    def __init__(self, host: str = "localhost", port: int = 9200):
        """Initialize Elasticsearch client with sentence transformer model."""
        self.es = Elasticsearch([{'host': host, 'port': port}])
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model for embeddings
        self.index_name = "ai_plans"
        
    def create_index(self):
        """Create the index with proper mapping for embeddings."""
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "content_vector": {
                        "type": "dense_vector",
                        "dims": 384  # Dimension for all-MiniLM-L6-v2
                    },
                    "plan_type": {"type": "keyword"},
                    "user_query": {"type": "text"},
                    "created_at": {"type": "date"},
                    "strategic_plan": {"type": "text"},
                    "subagent_reports": {"type": "text"},
                    "executive_summary": {"type": "text"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=mapping)
            print(f"Created index: {self.index_name}")
        else:
            print(f"Index {self.index_name} already exists")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text."""
        return self.model.encode(text).tolist()
    
    def store_plan(self, 
                   user_query: str,
                   strategic_plan: str,
                   subagent_reports: str,
                   executive_summary: str,
                   plan_type: str = "ai_art_company") -> str:
        """Store a complete plan with embeddings in Elasticsearch."""
        
        # Combine all content for embedding
        combined_content = f"{strategic_plan}\n\n{subagent_reports}\n\n{executive_summary}"
        
        # Generate embedding
        embedding = self.generate_embedding(combined_content)
        
        # Create document
        doc = {
            "title": f"AI Art Company Plan - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "content": combined_content,
            "content_vector": embedding,
            "plan_type": plan_type,
            "user_query": user_query,
            "created_at": datetime.now().isoformat(),
            "strategic_plan": strategic_plan,
            "subagent_reports": subagent_reports,
            "executive_summary": executive_summary
        }
        
        # Store in Elasticsearch
        response = self.es.index(index=self.index_name, body=doc)
        doc_id = response['_id']
        print(f"Stored plan with ID: {doc_id}")
        return doc_id
    
    def search_plans(self, query: str, size: int = 10) -> List[Dict[str, Any]]:
        """Search plans using semantic similarity."""
        
        # Generate embedding for search query
        query_embedding = self.generate_embedding(query)
        
        # Perform vector search
        search_body = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            },
            "size": size
        }
        
        response = self.es.search(index=self.index_name, body=search_body)
        
        results = []
        for hit in response['hits']['hits']:
            results.append({
                'id': hit['_id'],
                'score': hit['_score'],
                'title': hit['_source']['title'],
                'plan_type': hit['_source']['plan_type'],
                'created_at': hit['_source']['created_at'],
                'user_query': hit['_source']['user_query'],
                'strategic_plan': hit['_source']['strategic_plan'][:500] + "..." if len(hit['_source']['strategic_plan']) > 500 else hit['_source']['strategic_plan'],
                'executive_summary': hit['_source']['executive_summary'][:500] + "..." if len(hit['_source']['executive_summary']) > 500 else hit['_source']['executive_summary']
            })
        
        return results
    
    def get_plan_by_id(self, plan_id: str) -> Dict[str, Any]:
        """Retrieve a specific plan by ID."""
        try:
            response = self.es.get(index=self.index_name, id=plan_id)
            return response['_source']
        except Exception as e:
            print(f"Error retrieving plan {plan_id}: {e}")
            return None
    
    def list_all_plans(self, size: int = 50) -> List[Dict[str, Any]]:
        """List all stored plans."""
        search_body = {
            "query": {"match_all": {}},
            "sort": [{"created_at": {"order": "desc"}}],
            "size": size
        }
        
        response = self.es.search(index=self.index_name, body=search_body)
        
        results = []
        for hit in response['hits']['hits']:
            results.append({
                'id': hit['_id'],
                'title': hit['_source']['title'],
                'plan_type': hit['_source']['plan_type'],
                'created_at': hit['_source']['created_at'],
                'user_query': hit['_source']['user_query']
            })
        
        return results 