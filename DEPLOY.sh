#!/bin/bash
# Quick deployment script for GitHub Pages

echo "🚀 Deploying Book Index Generator to GitHub"
echo ""

# Check if origin is set
if ! git remote get-url origin &> /dev/null; then
    echo "❌ No GitHub remote found!"
    echo ""
    echo "Please set up your GitHub repository first:"
    echo "  1. Create a new repo on GitHub"
    echo "  2. Run: git remote add origin https://github.com/YOUR_USERNAME/indexer.git"
    echo ""
    exit 1
fi

# Show current remote
echo "📍 Current remote:"
git remote get-url origin
echo ""

# Add all changes
echo "📦 Adding files..."
git add .

# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
    echo "✓ No changes to commit"
else
    # Commit changes
    echo "💾 Committing changes..."
    git commit -m "Update project"
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully deployed!"
    echo ""
    echo "🌐 Your site will be live at:"
    echo "   https://YOUR_USERNAME.github.io/indexer/"
    echo ""
    echo "⏱️  Wait 2-3 minutes for GitHub Pages to build"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Go to GitHub repository → Settings → Pages"
    echo "   2. Under Source: select 'main' branch and '/docs' folder"
    echo "   3. Save and wait for deployment"
else
    echo ""
    echo "❌ Push failed. Please check your GitHub credentials."
fi
