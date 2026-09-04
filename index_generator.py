"""
Book Index Generator
Automatically extracts person names from Word documents
and generates an alphabetical index with page numbers.
"""

import spacy
from docx import Document
from collections import defaultdict
import re
from typing import Dict, List, Tuple


class IndexGenerator:
    def __init__(self, words_per_page: int = 250, model_name: str = "en_core_web_sm"):
        """
        Initialize the index generator.
        
        Args:
            words_per_page: Approximate words per page for page number calculation
        """
        self.words_per_page = words_per_page
        self.model_name = model_name
        try:
            self.nlp = spacy.load(self.model_name)
        except OSError:
            print(f"SpaCy model '{self.model_name}' not found. Please install/download it.")
            raise
        
        # Track terms and their page numbers
        self.index_terms: Dict[str, set] = defaultdict(set)
        
    def extract_text_with_positions(self, docx_path: str) -> List[Tuple[str, int]]:
        """
        Extract text from DOCX file with approximate page numbers.
        
        Args:
            docx_path: Path to the Word document
            
        Returns:
            List of (text, page_number) tuples
        """
        doc = Document(docx_path)
        
        text_with_pages = []
        word_count = 0
        current_page = 1
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                # Count words in this paragraph
                words = len(text.split())
                word_count += words
                
                # Calculate current page
                current_page = (word_count // self.words_per_page) + 1
                
                text_with_pages.append((text, current_page))
        
        return text_with_pages

    def extract_text_with_positions_from_document(self, document: Document) -> List[Tuple[str, int]]:
        """
        Extract text from an already loaded python-docx Document with approximate page numbers.

        Args:
            document: Loaded python-docx document

        Returns:
            List of (text, page_number) tuples
        """
        text_with_pages = []
        word_count = 0

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()
            if not text:
                continue

            word_count += len(text.split())
            current_page = (word_count // self.words_per_page) + 1
            text_with_pages.append((text, current_page))

        return text_with_pages
    
    def is_likely_person_name(self, text: str, label: str) -> bool:
        """
        Check if text is likely a person name based on patterns.
        
        Args:
            text: The entity text
            label: The entity label from SpaCy
            
        Returns:
            True if likely a person name
        """
        # Words that indicate it's NOT a person name
        non_person_keywords = [
            'city', 'empire', 'kingdom', 'library', 'gardens', 'wall', 
            'temple', 'pyramid', 'road', 'dynasty', 'civilization',
            'itza', 'picchu', 'tikal', 'citadel', 'capital', 'river',
            'army', 'code', 'wonders', 'sea', 'ancient',
            'bce', 'ce', 'ad', 'bc'
        ]
        
        # Known place names to exclude
        known_places = [
            'alexandria', 'athens', 'sparta', 'rome', 'egypt', 'china', 
            'peru', 'mexico', 'india', 'europe', 'africa', 'gaul',
            'mesopotamia', 'chang\'an', 'xi\'an', 'cuzco', 'maya',
            'inca', 'north africa', 'south america', 'central america'
        ]
        
        text_lower = text.lower()
        
        # Skip if contains non-person keywords
        if any(keyword in text_lower for keyword in non_person_keywords):
            return False
        
        # Skip known place names
        if text_lower in known_places:
            return False
        
        # Skip very short or numeric
        if len(text) <= 2 or text.isdigit():
            return False
        
        # Pattern: Name + "the Great" or "the + Title" likely a person
        if 'the great' in text_lower or 'the elder' in text_lower:
            return True
        
        # Roman numerals at end (e.g., "Cleopatra VII") - likely a person
        if text.split()[-1] in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']:
            return True
        
        # If labeled as PERSON, accept it (after filters above)
        if label == 'PERSON':
            return True
        
        # Check if it looks like a person name from other entity types
        # ORG, GPE, PRODUCT, WORK_OF_ART sometimes misclassify historical figures
        if label in ['ORG', 'PRODUCT', 'WORK_OF_ART']:
            words = text.split()
            
            # Single capitalized words might be names (e.g., "Socrates", "Plato", "Aristotle")
            # But be more conservative - must not be a known place
            if len(words) == 1 and text[0].isupper() and text_lower not in known_places:
                return True
            
            # Two words where both start with capital (e.g., "Julius Caesar")
            # Must not contain place indicators
            if len(words) == 2 and all(w and w[0].isupper() for w in words):
                return True
        
        # Be very conservative with GPE (geo-political entities)
        # Only accept if it has strong person indicators
        if label == 'GPE':
            # Accept single names that are clearly people, not places
            # This is risky, so only do it for very strong signals
            if len(text.split()) == 1 and text[0].isupper():
                # Only accept if not in known places list
                if text_lower not in known_places:
                    # Accept names like "Romulus", "Pachacuti"
                    return True
        
        return False
    
    def extract_indexable_terms(self, text_with_pages: List[Tuple[str, int]]) -> None:
        """
        Extract person names using NLP.
        
        Args:
            text_with_pages: List of (text, page_number) tuples
        """
        for text, page_num in text_with_pages:
            # Process text with spaCy
            doc = self.nlp(text)
            
            # Check all entities for potential person names
            for ent in doc.ents:
                # Clean up the name
                name = ent.text.strip()
                
                # Check if this looks like a person name
                if self.is_likely_person_name(name, ent.label_):
                    self.index_terms[name].add(page_num)
    
    def generate_index(self) -> str:
        """
        Generate formatted index from extracted terms.
        
        Returns:
            Formatted index as string
        """
        if not self.index_terms:
            return "No index terms found."
        
        # Sort terms alphabetically (case-insensitive)
        sorted_terms = sorted(self.index_terms.items(), key=lambda x: x[0].lower())
        
        # Format the index
        index_lines = ["INDEX", "=" * 50, ""]
        
        current_letter = None
        for term, pages in sorted_terms:
            # Add letter headers
            first_letter = term[0].upper()
            if first_letter != current_letter:
                if current_letter is not None:
                    index_lines.append("")  # Blank line between letter groups
                index_lines.append(f"--- {first_letter} ---")
                current_letter = first_letter
            
            # Format page numbers
            page_list = sorted(list(pages))
            pages_str = ", ".join(map(str, page_list))
            
            index_lines.append(f"{term}: {pages_str}")
        
        return "\n".join(index_lines)
    
    def process_document(self, docx_path: str, output_path: str = None) -> str:
        """
        Process a Word document and generate an index.
        
        Args:
            docx_path: Path to input Word document
            output_path: Optional path to save index (defaults to docx_path with _index.txt)
            
        Returns:
            The generated index as string
        """
        print(f"Processing document: {docx_path}")
        
        # Extract text with page positions
        print("Extracting text...")
        text_with_pages = self.extract_text_with_positions(docx_path)
        print(f"Found {len(text_with_pages)} paragraphs")
        
        # Extract indexable terms
        print("Analyzing text and extracting index terms...")
        self.extract_indexable_terms(text_with_pages)
        print(f"Found {len(self.index_terms)} unique terms")
        
        # Generate the index
        print("Generating index...")
        index = self.generate_index()
        
        # Save to file
        if output_path is None:
            output_path = docx_path.rsplit(".", 1)[0] + "_index.txt"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(index)
        
        print(f"\nIndex saved to: {output_path}")
        print(f"\nPreview (first 20 lines):")
        print("\n".join(index.split("\n")[:20]))
        
        return index


def main():
    """Main function to run the index generator."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python index_generator.py <path_to_docx_file> [output_file]")
        print("\nExample:")
        print("  python index_generator.py my_book.docx")
        print("  python index_generator.py my_book.docx custom_index.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create generator and process document
    generator = IndexGenerator(words_per_page=250)
    generator.process_document(input_file, output_file)


if __name__ == "__main__":
    main()
