"""
Debug tool to see what entities SpaCy detects in a document.
Useful for understanding what the index generator is finding.
"""

import spacy
from docx import Document
from collections import defaultdict


def debug_document(docx_path: str):
    """Show all entities detected by SpaCy in a document."""
    
    # Load SpaCy model
    nlp = spacy.load("en_core_web_sm")
    
    # Read document
    doc = Document(docx_path)
    
    # Collect all entities by type
    entities_by_type = defaultdict(set)
    
    print(f"\n{'='*60}")
    print(f"DEBUG: Analyzing {docx_path}")
    print(f"{'='*60}\n")
    
    for para in doc.paragraphs:
        if para.text.strip():
            # Process with SpaCy
            spacy_doc = nlp(para.text)
            
            # Collect entities
            for ent in spacy_doc.ents:
                entities_by_type[ent.label_].add(ent.text)
    
    # Display results
    if not entities_by_type:
        print("❌ No entities found\n")
        return
    
    # Show PERSON entities first (most relevant)
    if 'PERSON' in entities_by_type:
        print("👤 PERSON entities (names):")
        for name in sorted(entities_by_type['PERSON']):
            print(f"   • {name}")
        print()
    
    # Show other entity types
    other_types = sorted(set(entities_by_type.keys()) - {'PERSON'})
    
    if other_types:
        print("📍 Other entities found:")
        for entity_type in other_types:
            print(f"\n   {entity_type}:")
            for entity in sorted(entities_by_type[entity_type]):
                print(f"      • {entity}")
        print()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"   Total PERSON entities: {len(entities_by_type.get('PERSON', set()))}")
    print(f"   Total entity types: {len(entities_by_type)}")
    print(f"   Total unique entities: {sum(len(v) for v in entities_by_type.values())}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 debug_entities.py <path_to_docx_file>")
        print("\nExample:")
        print("   python3 debug_entities.py sample_document.docx")
        sys.exit(1)
    
    debug_document(sys.argv[1])
