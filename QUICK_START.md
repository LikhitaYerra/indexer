# Quick Start Guide

## ✨ What it does

This tool automatically extracts **person names** from Word documents and creates an alphabetical index with page numbers.

## 🚀 Usage

### Basic command:
```bash
python3 index_generator.py your_document.docx
```

This creates `your_document_index.txt` with all the names found.

### Specify output file:
```bash
python3 index_generator.py input.docx output_index.txt
```

## 📋 Example

```bash
# Try the sample document
python3 index_generator.py sample_document.docx

# Output: sample_document_index.txt
```

## 🔍 Debug Mode

Want to see what the AI is detecting?

```bash
python3 debug_entities.py your_document.docx
```

This shows all entities detected by SpaCy, including what might be misclassified.

## ⚙️ Configuration

Edit the `words_per_page` if your documents have different formatting:

```python
from index_generator import IndexGenerator

# For documents with more text per page
generator = IndexGenerator(words_per_page=350)

# For documents with less text per page (large margins, spacing)
generator = IndexGenerator(words_per_page=200)

generator.process_document("my_book.docx")
```

## 📝 Tips

1. **Names must be capitalized** in your document
2. **Full names work better** than single names (e.g., "Abraham Lincoln" vs "Lincoln")
3. **Consistent spelling** - use the same name format throughout
4. **Review the output** - AI isn't perfect, you may need to manually edit the index

## 🛠️ Files

- `index_generator.py` - Main program
- `debug_entities.py` - See what entities are detected
- `create_sample.py` - Generate a test document
- `sample_document.docx` - Example document to try
- `README.md` - Full documentation

## ❓ Troubleshooting

**Missing names?**
- Check if names are capitalized in your document
- Run `debug_entities.py` to see what SpaCy is detecting
- Some historical/uncommon names may not be recognized

**False positives (places showing up)?**
- The code filters most place names automatically
- You can manually edit the output file
- Report persistent issues so we can improve the filters

## 🎯 What it extracts

✅ Person names (historical figures, authors, characters, etc.)  
❌ Place names (cities, countries)  
❌ Organizations  
❌ Events  
❌ Other entities  

---

**Need help?** Check `README.md` for full documentation.
