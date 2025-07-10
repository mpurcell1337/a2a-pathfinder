import os
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
import uuid

class ElasticsearchClient:
    def __init__(self, host: str = "localhost", port: int = 9200):
        """Initialize Elasticsearch client with sentence transformer model."""
        self.es = Elasticsearch(f"http://{host}:{port}")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model for embeddings
        self.index_name = "ai_plans"
        self.snippets_index_name = "ai_snippets"
        
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
        
        snippets_mapping = {
            "mappings": {
                "properties": {
                    "snippet_id": {"type": "keyword"},
                    "plan_id": {"type": "keyword"},
                    "content": {"type": "text"},
                    "content_vector": {
                        "type": "dense_vector",
                        "dims": 384
                    },
                    "snippet_type": {"type": "keyword"},  # "subagent_output", "orchestration_output", "strategic_plan", "executive_summary"
                    "subagent_id": {"type": "keyword"},  # For subagent outputs
                    "task_description": {"type": "text"},  # Original task for subagent
                    "metadata": {"type": "object"},  # Additional metadata
                    "created_at": {"type": "date"},
                    "user_query": {"type": "text"},
                    "plan_type": {"type": "keyword"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        # Create main plans index
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, mappings=mapping["mappings"], settings=mapping["settings"])
            print(f"Created index: {self.index_name}")
        else:
            print(f"Index {self.index_name} already exists")
            
        # Create snippets index
        if not self.es.indices.exists(index=self.snippets_index_name):
            self.es.indices.create(index=self.snippets_index_name, mappings=snippets_mapping["mappings"], settings=snippets_mapping["settings"])
            print(f"Created index: {self.snippets_index_name}")
        else:
            print(f"Index {self.snippets_index_name} already exists")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text."""
        return self.model.encode(text).tolist()
    
    def store_snippet(self, 
                     plan_id: str,
                     content: str,
                     snippet_type: str,
                     user_query: str,
                     plan_type: str,
                     subagent_id: Optional[str] = None,
                     task_description: Optional[str] = None,
                     metadata: Optional[Dict] = None) -> str:
        """Store an individual snippet with its embedding."""
        
        # Generate embedding for the snippet
        embedding = self.generate_embedding(content)
        
        # Create snippet document
        doc = {
            "snippet_id": str(uuid.uuid4()),
            "plan_id": plan_id,
            "content": content,
            "content_vector": embedding,
            "snippet_type": snippet_type,
            "subagent_id": subagent_id,
            "task_description": task_description,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "user_query": user_query,
            "plan_type": plan_type
        }
        
        # Store in Elasticsearch
        response = self.es.index(index=self.snippets_index_name, document=doc)
        snippet_id = response['_id']
        print(f"Stored snippet with ID: {snippet_id}")
        return snippet_id
    
    def store_plan_with_chunking(self, 
                                user_query: str,
                                strategic_plan: str,
                                subagent_reports: str,
                                executive_summary: str,
                                plan_type: str = "ai_art_company") -> str:
        """Store a complete plan with individual chunking embeddings."""
        
        # First, store the main plan
        combined_content = f"{strategic_plan}\n\n{subagent_reports}\n\n{executive_summary}"
        embedding = self.generate_embedding(combined_content)
        
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
        
        # Store main plan
        response = self.es.index(index=self.index_name, document=doc)
        plan_id = response['_id']
        print(f"Stored main plan with ID: {plan_id}")
        
        # Store strategic plan as chunk
        self.store_snippet(
            plan_id=plan_id,
            content=strategic_plan,
            snippet_type="strategic_plan",
            user_query=user_query,
            plan_type=plan_type,
            metadata={"section": "strategic_planning"}
        )
        print(f"  - Stored strategic plan chunk")
        
        # Parse and store individual subagent outputs
        # This is a simplified parser - you might want more sophisticated parsing
        subagent_sections = subagent_reports.split("## Subagent")
        for i, section in enumerate(subagent_sections[1:], 1):  # Skip first empty section
            lines = section.strip().split('\n')
            if lines:
                # Extract task and content
                task_line = next((line for line in lines if line.startswith('**Task:**')), '')
                task = task_line.replace('**Task:**', '').strip()
                
                # Get content (everything after the task)
                content_start = section.find('\n\n') + 2 if '\n\n' in section else 0
                content = section[content_start:].strip()
                
                if content:
                    self.store_snippet(
                        plan_id=plan_id,
                        content=content,
                        snippet_type="subagent_output",
                        user_query=user_query,
                        plan_type=plan_type,
                        subagent_id=f"subagent_{i}",
                        task_description=task,
                        metadata={"subagent_number": i, "section": "research"}
                    )
                    print(f"  - Stored subagent {i} chunk")
        
        # Store executive summary as chunk
        self.store_snippet(
            plan_id=plan_id,
            content=executive_summary,
            snippet_type="executive_summary",
            user_query=user_query,
            plan_type=plan_type,
            metadata={"section": "synthesis"}
        )
        print(f"  - Stored executive summary chunk")
        
        return plan_id
    
    def search_snippets(self, query: str, snippet_type: Optional[str] = None, 
                       plan_type: Optional[str] = None, size: int = 10) -> List[Dict[str, Any]]:
        """Search snippets using semantic similarity with optional filters."""
        
        # Generate embedding for search query
        query_embedding = self.generate_embedding(query)
        
        # Build query
        must_clauses = [
            {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
        ]
        
        # Add filters if specified
        filter_clauses = []
        if snippet_type:
            filter_clauses.append({"term": {"snippet_type": snippet_type}})
        if plan_type:
            filter_clauses.append({"term": {"plan_type": plan_type}})
        
        if filter_clauses:
            search_body = {
                "query": {
                    "bool": {
                        "must": must_clauses,
                        "filter": filter_clauses
                    }
                },
                "size": size
            }
        else:
            search_body = {
                "query": must_clauses[0],
                "size": size
            }
        
        response = self.es.search(index=self.snippets_index_name, body=search_body)
        
        results = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            results.append({
                'id': hit['_id'],
                'snippet_id': source['snippet_id'],
                'plan_id': source['plan_id'],
                'score': hit['_score'],
                'content': source['content'][:500] + "..." if len(source['content']) > 500 else source['content'],
                'snippet_type': source['snippet_type'],
                'subagent_id': source.get('subagent_id'),
                'task_description': source.get('task_description'),
                'user_query': source['user_query'],
                'plan_type': source['plan_type'],
                'created_at': source['created_at']
            })
        
        return results
    
    def get_snippets_by_plan(self, plan_id: str) -> List[Dict[str, Any]]:
        """Get all snippets for a specific plan."""
        search_body = {
            "query": {"term": {"plan_id": plan_id}},
            "sort": [{"created_at": {"order": "desc"}}]
        }
        
        response = self.es.search(index=self.snippets_index_name, body=search_body)
        
        results = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            results.append({
                'snippet_id': source['snippet_id'],
                'content': source['content'],
                'snippet_type': source['snippet_type'],
                'subagent_id': source.get('subagent_id'),
                'task_description': source.get('task_description'),
                'metadata': source.get('metadata', {})
            })
        
        return results
    
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