#!/bin/bash
# Setup script for Book Index Generator

echo "📚 Setting up Book Index Generator..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🤖 Downloading SpaCy language model..."
python3 -m spacy download en_core_web_sm

if [ $? -ne 0 ]; then
    echo "❌ Failed to download SpaCy model"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage:"
echo "  python3 index_generator.py your_document.docx"
echo ""
echo "Example:"
echo "  python3 index_generator.py sample_book.docx"
