import json
import os
from typing import Dict, Any

class KnowledgeLoader:
    def __init__(self, knowledge_dir: str = "app/knowledge"):
        self.knowledge_dir = knowledge_dir
        self.data: Dict[str, Any] = {}

    def load_all(self):
        """
        Loads all JSON files from the knowledge directory into memory.
        """
        if not os.path.exists(self.knowledge_dir):
            print(f"Warning: Knowledge directory '{self.knowledge_dir}' does not exist.")
            return

        for filename in os.listdir(self.knowledge_dir):
            if filename.endswith(".json"):
                key_name = filename.replace(".json", "")
                filepath = os.path.join(self.knowledge_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.data[key_name] = json.load(f)
                    print(f"Loaded knowledge base: {filename}")
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")

    def get_section(self, section_name: str) -> Any:
        """
        Retrieve a specific section of the knowledge base (e.g., 'faq', 'products').
        """
        return self.data.get(section_name, None)

    def get_full_context(self) -> str:
        """
        Returns a massive string of the knowledge base for simple RAG injection.
        Note: For a real production app with huge data, this would blow up the token limit.
        Module 10 (RAG) will improve this by searching instead of dumping everything.
        """
        return json.dumps(self.data, indent=2)

# Singleton instance
knowledge_base = KnowledgeLoader()
# We will call knowledge_base.load_all() when the FastAPI app starts up
