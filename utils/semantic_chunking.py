# #!/usr/bin/env python3
# """
# Advanced Chunking Utility

# This script provides advanced features for chunking large outputs into smaller,
# searchable chunks with overlapping context and semantic boundaries.
# """

# import os
# import sys
# import re
# from typing import List, Dict, Any, Tuple
# from dotenv import load_dotenv

# # Add the parent directory to the path to import utils
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from utils.elasticsearch_client import ElasticsearchClient

# # Load environment variables
# load_dotenv()

# class AdvancedChunkizer:
#     """Advanced chunking with semantic chunking and overlap."""
    
#     def __init__(self, chunk_size: int = 1000, overlap: int = 200):
#         """
#         Initialize the advanced chunkizer.
        
#         Args:
#             chunk_size: Target size for each chunk in characters
#             overlap: Number of characters to overlap between chunks
#         """
#         self.chunk_size = chunk_size
#         self.overlap = overlap
    
#     def split_by_semantic_boundaries(self, text: str) -> List[str]:
#         """
#         Split text by semantic boundaries (headers, paragraphs, etc.).
        
#         Args:
#             text: The text to split
            
#         Returns:
#             List of text chunks
#         """
#         # Split by headers (##, ###, etc.)
#         header_pattern = r'^#{2,}\s+.*$'
#         sections = re.split(header_pattern, text, flags=re.MULTILINE)
        
#         chunks = []
#         for section in sections:
#             if section.strip():
#                 # Further split by paragraphs
#                 paragraphs = section.split('\n\n')
#                 for paragraph in paragraphs:
#                     if paragraph.strip():
#                         chunks.append(paragraph.strip())
        
#         return chunks
    
#     def create_overlapping_chunks(self, text: str) -> List[str]:
#         """
#         Create overlapping chunks from text.
        
#         Args:
#             text: The text to chunk
            
#         Returns:
#             List of overlapping text chunks
#         """
#         if len(text) <= self.chunk_size:
#             return [text]
        
#         chunks = []
#         start = 0
        
#         while start < len(text):
#             end = start + self.chunk_size
            
#             # Try to break at sentence boundaries
#             if end < len(text):
#                 # Look for sentence endings
#                 for i in range(end, max(start + self.chunk_size // 2, end - 100), -1):
#                     if text[i] in '.!?':
#                         end = i + 1
#                         break
                
#                 # If no sentence boundary found, look for paragraph breaks
#                 if end == start + self.chunk_size:
#                     for i in range(end, max(start + self.chunk_size // 2, end - 100), -1):
#                         if text[i] == '\n':
#                             end = i + 1
#                             break
                
#                 # If still no good break point, look for word boundaries
#                 if end == start + self.chunk_size:
#                     for i in range(end, max(start + self.chunk_size // 2, end - 100), -1):
#                         if text[i] == ' ':
#                             end = i + 1
#                             break
            
#             chunk = text[start:end].strip()
#             if chunk:
#                 chunks.append(chunk)
            
#             # Move start position with overlap
#             start = end - self.overlap
#             if start >= len(text):
#                 break
        
#         return chunks
    
#     def extract_metadata(self, chunk: str) -> Dict[str, Any]:
#         """
#         Extract metadata from a chunk.
        
#         Args:
#             chunk: The text chunk
            
#         Returns:
#             Dictionary of metadata
#         """
#         words = chunk.split()
#         sentences = re.split(r'[.!?]+', chunk)
        
#         return {
#             "word_count": len(words),
#             "character_count": len(chunk),
#             "sentence_count": len([s for s in sentences if s.strip()]),
#             "has_headers": '##' in chunk,
#             "has_lists": any(line.strip().startswith('-') or line.strip().startswith('*') for line in chunk.split('\n')),
#             "has_code": '```' in chunk,
#             "avg_sentence_length": len(words) / max(len([s for s in sentences if s.strip()]), 1)
#         }

# def enhance_chunking():
#     """Demonstrate enhanced chunking features."""
    
#     # Initialize Elasticsearch client
#     es_client = ElasticsearchClient()
#     es_client.create_index()
    
#     # Initialize chunkizer
#     chunkizer = AdvancedChunkizer(chunk_size=800, overlap=150)
    
#     print("🔧 Advanced Chunking Demo")
#     print("=" * 50)
    
#     # Example strategic plan text
#     strategic_plan = """
# ## Strategic Overview

# Our AI art company will revolutionize the creative industry by leveraging cutting-edge artificial intelligence to democratize artistic expression. We will focus on three core pillars: accessibility, innovation, and community.

# ## Market Analysis

# The AI art market is experiencing explosive growth, with the global market expected to reach $2.5 billion by 2025. Key drivers include:

# - Increasing demand for personalized content
# - Growing adoption of AI tools by artists
# - Rising interest in digital art and NFTs

# ## Technology Stack

# Our platform will utilize state-of-the-art AI models including:

# 1. **Text-to-Image Models**: Stable Diffusion, DALL-E 2
# 2. **Image Enhancement**: Advanced upscaling and refinement
# 3. **Style Transfer**: Neural style transfer capabilities
# 4. **User Interface**: Intuitive web and mobile applications

# ## Revenue Model

# We will implement a freemium model with multiple revenue streams:

# - **Free Tier**: Basic AI art generation with watermarks
# - **Premium Tier**: High-resolution, watermark-free art
# - **Enterprise Tier**: Custom AI model training and API access
# - **Marketplace**: Commission-based sales of AI-generated art

# ## Competitive Advantage

# Our unique positioning includes:

# - **Advanced AI Models**: Proprietary fine-tuned models
# - **Community Features**: Artist collaboration and sharing
# - **Educational Content**: AI art tutorials and workshops
# - **Ethical AI**: Transparent and responsible AI practices
# """
    
#     print("📝 Processing strategic plan with advanced chunking...")
    
#     # Create semantic chunks
#     semantic_chunks = chunkizer.split_by_semantic_boundaries(strategic_plan)
#     print(f"  - Created {len(semantic_chunks)} semantic chunks")
    
#     # Create overlapping chunks for longer sections
#     overlapping_chunks = []
#     for chunk in semantic_chunks:
#         if len(chunk) > chunkizer.chunk_size:
#             sub_chunks = chunkizer.create_overlapping_chunks(chunk)
#             overlapping_chunks.extend(sub_chunks)
#         else:
#             overlapping_chunks.append(chunk)
    
#     print(f"  - Total chunks after overlap processing: {len(overlapping_chunks)}")
    
#     # Store enhanced chunks as chunks
#     print("\n💾 Storing enhanced chunks as chunks...")
    
#     for i, chunk in enumerate(overlapping_chunks):
#         if len(chunk.strip()) < 50:  # Skip very short chunks
#             continue
            
#         metadata = chunkizer.extract_metadata(chunk)
        
#         # Store as enhanced chunk
#         chunk_id = es_client.store_chunk(
#             plan_id="demo_plan",
#             content=chunk,
#             chunk_type="enhanced_strategic_plan",
#             user_query="Create a strategic plan for an AI art company",
#             plan_type="ai_art_company",
#             metadata={
#                 "chunk_index": i,
#                 "chunk_size": len(chunk),
#                 "processing_method": "semantic_boundaries",
#                 "overlap_used": chunkizer.overlap,
#                 **metadata
#             }
#         )
#         print(f"  - Stored chunk {i+1}: {len(chunk)} chars, {metadata['word_count']} words")
    
#     print(f"\n✅ Enhanced chunking completed!")
#     print(f"📊 Created {len(overlapping_chunks)} searchable chunks")
    
#     # Demonstrate search on enhanced chunks
#     print("\n🔍 Testing search on enhanced chunks...")
    
#     enhanced_results = es_client.search_chunks(
#         query="AI art market growth revenue",
#         chunk_type="enhanced_strategic_plan",
#         size=5
#     )
    
#     print(f"Found {len(enhanced_results)} relevant enhanced chunks:")
#     for result in enhanced_results:
#         print(f"   Score: {result['score']:.3f}")
#         print(f"   Content: {result['content'][:100]}...")
#         print(f"   Chunk size: {result['metadata'].get('chunk_size', 'N/A')} chars")
#         print()

# def create_chunk_analytics():
#     """Create analytics about chunk usage and effectiveness."""
    
#     es_client = ElasticsearchClient()
    
#     print("\n📊 Chunk Analytics")
#     print("=" * 30)
    
#     # Get all chunks
#     all_chunks = es_client.search_chunks("", size=100)  # Get all chunks
    
#     if not all_chunks:
#         print("❌ No chunks found.")
#         return
    
#     # Analyze chunk types
#     type_counts = {}
#     plan_type_counts = {}
#     size_distribution = {"small": 0, "medium": 0, "large": 0}
    
#     for chunk in all_chunks:
#         chunk_type = chunk['chunk_type']
#         plan_type = chunk['plan_type']
#         content_length = len(chunk['content'])
        
#         # Count by type
#         type_counts[chunk_type] = type_counts.get(chunk_type, 0) + 1
#         plan_type_counts[plan_type] = plan_type_counts.get(plan_type, 0) + 1
        
#         # Size distribution
#         if content_length < 500:
#             size_distribution["small"] += 1
#         elif content_length < 1000:
#             size_distribution["medium"] += 1
#         else:
#             size_distribution["large"] += 1
    
#     print(f"📈 Total chunks: {len(all_chunks)}")
    
#     print("\n📋 Chunk types:")
#     for chunk_type, count in sorted(type_counts.items()):
#         print(f"  - {chunk_type}: {count} chunks")
    
#     print("\n📋 Plan types:")
#     for plan_type, count in sorted(plan_type_counts.items()):
#         print(f"  - {plan_type}: {count} chunks")
    
#     print("\n📏 Size distribution:")
#     total = len(all_chunks)
#     for label, count in size_distribution.items():
#         percentage = (count / total) * 100 if total > 0 else 0
#         print(f"  - {label}: {count} chunks ({percentage:.1f}%)")

# if __name__ == "__main__":
#     print("🚀 Advanced Chunking Demo")
#     print("=" * 50)
    
#     enhance_chunking()
#     create_chunk_analytics()
    
#     print("\n✅ Advanced chunking demo completed!")
#     print("\n📋 Available features:")
#     print("1. Semantic boundary detection")
#     print("2. Overlapping chunk creation")
#     print("3. Metadata extraction")
#     print("4. Enhanced search capabilities")
#     print("5. Chunk analytics") 