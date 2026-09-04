# Book Index Generator

Automatically generates a book index from Word documents by extracting **person names** and tracking their page numbers.

## Features

- 📄 Reads `.docx` (Word) files
- 🧠 Uses NLP (spaCy) to automatically identify **person names**
- 📖 Calculates approximate page numbers
- 📝 Generates alphabetically sorted index with page references
- 💾 Exports index to text file

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download the SpaCy language model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Command Line

Basic usage:
```bash
python index_generator.py your_document.docx
```

This will create `your_document_index.txt` in the same directory.

Specify custom output file:
```bash
python index_generator.py your_document.docx my_custom_index.txt
```

### Python API

```python
from index_generator import IndexGenerator

# Create generator
generator = IndexGenerator(words_per_page=250)

# Process document
index = generator.process_document("my_book.docx", "output_index.txt")

# The index string is also returned
print(index)
```

## Configuration

You can adjust the `words_per_page` parameter to match your document's formatting:

```python
# For documents with more text per page
generator = IndexGenerator(words_per_page=350)

# For documents with less text per page (large margins, spacing)
generator = IndexGenerator(words_per_page=200)
```

## Example Output

```
INDEX
==================================================

--- A ---
Abraham Lincoln: 12, 15, 23
Ancient Rome: 45, 47, 51

--- B ---
Boston: 8, 34, 67
British Empire: 23, 29, 30

--- N ---
New York City: 5, 12, 18, 45
Napoleon Bonaparte: 67, 69, 72

--- W ---
World War II: 89, 92, 95, 103
```

## How It Works

1. **Text Extraction**: Reads the Word document and extracts text from all paragraphs
2. **Page Calculation**: Estimates page numbers based on word count (default: 250 words/page)
3. **NLP Analysis**: Uses SpaCy to identify named entities and proper nouns
4. **Index Generation**: Creates alphabetically sorted index with page references
5. **Export**: Saves formatted index to a text file

## Limitations

- Page numbers are **approximate** (based on word count, not actual document pages)
- Works best with well-written text where proper nouns are capitalized
- Requires English language documents (uses `en_core_web_sm` model)

## Tips for Better Results

- Ensure person names are capitalized in your document
- Use consistent spelling for names (e.g., always "John Smith" not "J. Smith" or "Smith")
- The more context around names, the better the NLP can identify them
- Review and edit the generated index - automatic systems aren't perfect!
- Full names work better than single names (e.g., "Abraham Lincoln" vs just "Lincoln")

## Future Enhancements

Potential improvements:
- Support for subentries (e.g., "Dogs: breeds, 12; training, 45")
- Manual term list support
- Cross-references ("See also...")
- Better page number detection using actual page breaks
- Support for other document formats (PDF, plain text)

## High-Accuracy Web Deployment

To run the highest-accuracy pipeline (`en_core_web_trf`) behind your GitHub Pages site, deploy the FastAPI backend on Render.

See `RENDER_DEPLOYMENT.md` for full setup steps.
