import re
from typing import List, Dict, Any
from app.knowledge.loader import knowledge_base

class SimpleRetriever:
    """
    A lightweight, keyword-based search engine to simulate RAG (Retrieval-Augmented Generation).
    In a true production environment with millions of rows, this would be replaced by 
    a Vector Database (like Pinecone, Milvus, or ChromaDB) using Embeddings.
    """
    
    def __init__(self):
        # Stop words to ignore during keyword matching
        self.stop_words = {"a", "an", "the", "is", "are", "how", "what", "do", "i", "to", "for", "with", "my", "in", "of"}

    def _tokenize(self, text: str) -> set:
        """Convert text into a set of lowercase keywords, ignoring stop words."""
        if not isinstance(text, str):
            text = str(text)
        words = re.findall(r'\b\w+\b', text.lower())
        return set(words) - self.stop_words

    def search(self, query: str, top_k: int = 3) -> str:
        """
        Searches the entire JSON knowledge base and returns the top_k most relevant records 
        as a formatted string for the LLM context.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return "No specific keywords found. Use general company context."

        results = []

        # Iterate over all loaded JSON sections (faq, products, troubleshooting, etc.)
        for section_name, section_data in knowledge_base.data.items():
            
            # Ensure we are dealing with a list of dictionaries (like our FAQs and Products)
            if isinstance(section_data, list):
                for item in section_data:
                    # Convert the entire JSON object to a string to easily search all its fields
                    item_str = str(item)
                    item_tokens = self._tokenize(item_str)
                    
                    # Calculate relevance score: how many query keywords appear in this item?
                    score = len(query_tokens.intersection(item_tokens))
                    
                    # Boost score if the query mentions the section name (handles plurals like 'policies' vs 'policy')
                    section_root = section_name.rstrip('s')
                    section_y = section_name.replace('ies', 'y') if section_name.endswith('ies') else section_name
                    
                    for q in query_tokens:
                        if q == section_name or q == section_root or q == section_y or q.replace('ies', 'y') == section_root or q.rstrip('s') == section_name:
                            score += 5
                    
                    if score > 0:
                        results.append({
                            "score": score,
                            "section": section_name,
                            "content": item
                        })
            
            # Handle single dictionary (like company.json)
            elif isinstance(section_data, dict):
                item_str = str(section_data)
                item_tokens = self._tokenize(item_str)
                score = len(query_tokens.intersection(item_tokens))
                
                # Boost score if the query mentions the section name (handles plurals like 'policies' vs 'policy')
                section_root = section_name.rstrip('s')
                section_y = section_name.replace('ies', 'y') if section_name.endswith('ies') else section_name
                
                for q in query_tokens:
                    if q == section_name or q == section_root or q == section_y or q.replace('ies', 'y') == section_root or q.rstrip('s') == section_name:
                        score += 5
                        
                if score > 0:
                    results.append({
                        "score": score,
                        "section": section_name,
                        "content": section_data
                    })

        # Sort by highest score first
        results.sort(key=lambda x: x["score"], reverse=True)

        # Take only the top_k results
        top_results = results[:top_k]

        # Format them beautifully for the LLM
        context_string = ""
        for idx, res in enumerate(top_results):
            context_string += f"--- Result {idx + 1} (From {res['section'].upper()}) ---\n"
            context_string += f"{res['content']}\n\n"

        # If nothing matched, fallback to company basics
        if not context_string:
            return str(knowledge_base.get_section("company"))

        return context_string

# Singleton instance
retriever = SimpleRetriever()
