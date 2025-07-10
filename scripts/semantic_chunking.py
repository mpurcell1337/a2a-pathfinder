#!/usr/bin/env python3
"""
Advanced Chunking Utility

This script provides advanced features for chunking large outputs into smaller,
searchable snippets with overlapping context and semantic boundaries.
"""

import os
import sys
import re
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.elasticsearch_client import ElasticsearchClient

# Load environment variables
load_dotenv()

class AdvancedSnippitizer:
    """Advanced chunking with semantic chunking and overlap."""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize the snippitizer.
        
        Args:
            chunk_size: Target size for each chunk in characters
            overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def split_by_semantic_boundaries(self, text: str) -> List[str]:
        """
        Split text by semantic boundaries (paragraphs, sections, etc.).
        
        Args:
            text: The text to split
            
        Returns:
            List of text chunks
        """
        # Split by markdown headers first
        header_pattern = r'^#{1,6}\s+.+$'
        sections = re.split(header_pattern, text, flags=re.MULTILINE)
        
        chunks = []
        for section in sections:
            if section.strip():
                # Further split by paragraphs
                paragraphs = section.split('\n\n')
                for paragraph in paragraphs:
                    if paragraph.strip():
                        chunks.append(paragraph.strip())
        
        return chunks
    
    def create_overlapping_chunks(self, text: str) -> List[str]:
        """
        Create overlapping chunks from text.
        
        Args:
            text: The text to chunk
            
        Returns:
            List of overlapping text chunks
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to find a good break point
            if end < len(text):
                # Look for sentence boundaries
                for i in range(end, max(start + self.chunk_size // 2, end - 100), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
                # If no sentence boundary, look for paragraph breaks
                else:
                    for i in range(end, max(start + self.chunk_size // 2, end - 100), -1):
                        if text[i] == '\n':
                            end = i
                            break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.overlap
            if start >= len(text):
                break
        
        return chunks
    
    def extract_metadata(self, text: str) -> Dict[str, Any]:
        """
        Extract metadata from text (headers, key phrases, etc.).
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary of metadata
        """
        metadata = {
            'headers': [],
            'key_phrases': [],
            'word_count': len(text.split()),
            'has_numbers': bool(re.search(r'\d+', text)),
            'has_urls': bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
        }
        
        # Extract headers
        headers = re.findall(r'^#{1,6}\s+(.+)$', text, re.MULTILINE)
        metadata['headers'] = headers
        
        # Extract potential key phrases (simplified)
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences[:5]:  # First 5 sentences
            words = sentence.split()
            if len(words) >= 3:
                # Simple key phrase extraction (words starting with capital letters)
                key_words = [word for word in words if word[0].isupper() and len(word) > 3]
                metadata['key_phrases'].extend(key_words[:3])  # Top 3 per sentence
        
        return metadata

    def enhance_chunking():
        """Demonstrate enhanced chunking features."""
        
        es_client = ElasticsearchClient()
        snippitizer = AdvancedSnippitizer(chunk_size=800, overlap=150)
        
        print("🔧 Advanced Chunking Demo")
        print("=" * 50)
        
        # Get existing plans
        plans = es_client.list_all_plans()
        if not plans:
            print("❌ No plans found. Please run the lead orchestrator first.")
            return
        
        # Get the most recent plan
        latest_plan = plans[0]
        plan_id = latest_plan['id']
        
        # Get the full plan content
        plan_data = es_client.get_plan_by_id(plan_id)
        if not plan_data:
            print("❌ Could not retrieve plan data.")
            return
        
        print(f"📋 Processing plan: {latest_plan['title']}")
        
        # Process strategic plan with advanced chunking
        strategic_plan = plan_data['strategic_plan']
        print(f"\n📝 Strategic Plan ({len(strategic_plan)} characters)")
        
        # Create semantic chunks
        semantic_chunks = snippitizer.split_by_semantic_boundaries(strategic_plan)
        print(f"  - Created {len(semantic_chunks)} semantic chunks")
        
        # Create overlapping chunks for longer sections
        overlapping_chunks = []
        for chunk in semantic_chunks:
            if len(chunk) > snippitizer.chunk_size:
                sub_chunks = snippitizer.create_overlapping_chunks(chunk)
                overlapping_chunks.extend(sub_chunks)
            else:
                overlapping_chunks.append(chunk)
        
        print(f"  - Total chunks after overlap processing: {len(overlapping_chunks)}")
        
        # Store enhanced chunks as snippets
        print("\n💾 Storing enhanced chunks as snippets...")
        
        for i, chunk in enumerate(overlapping_chunks):
            if len(chunk.strip()) < 50:  # Skip very short chunks
                continue
                
            metadata = snippitizer.extract_metadata(chunk)
            
            # Store as enhanced snippet
            snippet_id = es_client.store_snippet(
                plan_id=plan_id,
                content=chunk,
                snippet_type="enhanced_strategic_plan",
                user_query=plan_data['user_query'],
                plan_type=plan_data['plan_type'],
                metadata={
                    "chunk_index": i,
                    "chunk_size": len(chunk),
                    "headers": metadata['headers'],
                    "key_phrases": metadata['key_phrases'][:5],  # Top 5
                    "word_count": metadata['word_count'],
                    "enhanced": True
                }
            )
            
            print(f"  - Stored chunk {i+1}: {len(chunk)} chars, {metadata['word_count']} words")
        
        print(f"\n✅ Enhanced chunking completed!")
        print(f"📊 Created {len(overlapping_chunks)} searchable chunks")
        
        # Demonstrate search on enhanced chunks
        print("\n🔍 Testing search on enhanced chunks...")
        
        enhanced_results = es_client.search_snippets(
            query="business strategy implementation",
            snippet_type="enhanced_strategic_plan",
            size=3
        )
        
        print(f"Found {len(enhanced_results)} relevant enhanced chunks:")
        for i, result in enumerate(enhanced_results, 1):
            print(f"\n{i}. Score: {result['score']:.3f}")
            print(f"   Chunk size: {result['metadata'].get('chunk_size', 'N/A')} chars")
            print(f"   Headers: {result['metadata'].get('headers', [])}")
            print(f"   Content: {result['content'][:150]}...")

    def create_snippet_analytics():
        """Create analytics about snippet usage and effectiveness."""
        
        es_client = ElasticsearchClient()
        
        print("\n📊 Snippet Analytics")
        print("=" * 50)
        
        # Get all snippets
        all_snippets = es_client.search_snippets("", size=100)  # Get all snippets
        
        if not all_snippets:
            print("❌ No snippets found.")
            return
        
        # Analyze snippet types
        type_counts = {}
        plan_type_counts = {}
        content_lengths = []
        
        for snippet in all_snippets:
            snippet_type = snippet['snippet_type']
            plan_type = snippet['plan_type']
            content_length = len(snippet['content'])
            
            type_counts[snippet_type] = type_counts.get(snippet_type, 0) + 1
            plan_type_counts[plan_type] = plan_type_counts.get(plan_type, 0) + 1
            content_lengths.append(content_length)
        
        print(f"📈 Total snippets: {len(all_snippets)}")
        print(f"📊 Average content length: {sum(content_lengths) / len(content_lengths):.0f} characters")
        
        print("\n📋 Snippet types:")
        for snippet_type, count in sorted(type_counts.items()):
            print(f"  - {snippet_type}: {count} snippets")
        
        print("\n🏢 Plan types:")
        for plan_type, count in sorted(plan_type_counts.items()):
            print(f"  - {plan_type}: {count} snippets")
        
        # Show content length distribution
        print("\n📏 Content length distribution:")
        length_ranges = [
            (0, 500, "Short (0-500 chars)"),
            (500, 1000, "Medium (500-1000 chars)"),
            (1000, 2000, "Long (1000-2000 chars)"),
            (2000, float('inf'), "Very Long (2000+ chars)")
        ]
        
        for min_len, max_len, label in length_ranges:
            count = sum(1 for length in content_lengths if min_len <= length < max_len)
            percentage = (count / len(content_lengths)) * 100
            print(f"  - {label}: {count} snippets ({percentage:.1f}%)")

    if __name__ == "__main__":
        try:
            enhance_chunking()
            create_snippet_analytics()
            
            print("\n" + "=" * 50)
            print("✅ Advanced chunking demo completed!")
            print("=" * 50)
            print("\nEnhanced features:")
            print("1. Semantic boundary detection")
            print("2. Overlapping chunk creation")
            print("3. Metadata extraction")
            print("4. Enhanced search capabilities")
            print("5. Snippet analytics")
            
        except Exception as e:
            print(f"❌ Error during demo: {e}")
            print("Make sure Elasticsearch is running with: docker-compose up -d") 